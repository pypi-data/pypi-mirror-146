!
!  f2py3 --fcompiler=intelem --f90flags=-openmp -liomp5 -c -m kde kdeLF.f90 --quiet
!
!  last modification: 2022_04_10_17_20
!


module params
 implicit none
  real(8),parameter :: pi=3.141592653589793
  real(8), allocatable, dimension(:) :: xz,red,ylum,hi,f_pilot,weight,ni 
  real(8),save :: H0,matter,lambda
  real(8),save :: z1,z2,Lmin,Lmax
  real(8),save :: L1,L2
  integer,save :: ndata,process
  real(8),save :: h1,h2
  real(8),save :: h10,h20,beta 
  logical,save :: set_beta_fixed,small_sample,adaptive,weighting,absolute_magnitude,bounded_lum
  logical, allocatable :: xdif(:,:),ydif(:,:)
  real(8), allocatable :: limx(:),limy(:)
  real(8),save :: nw
  !$OMP THREADPRIVATE(L1,L2)
end module

!***********************************************************************************************************
!include "quad2d.f90"
!***********************************************************************************************************

MODULE prob_functions
  implicit none
  CONTAINS  
!*****************************************
real(8) function p2d(z,L)
  use params
  implicit none
  real(8) x,y,z,L,bandwidth
  real(8),external :: f_lim,f_ref

  x=log( (z-z1)/(z2-z) )
  y=L-f_lim(z)
  p2d=f_ref(x,y) * ( 1/(z-z1) + 1/(z2-z) )
  return 
end function
!*****************************************
real(8) function p2da(z,L)
  use params
  implicit none
  real(8) x,y,z,L
  real(8),external :: f_lim,f_ada

  x=log( (z-z1)/(z2-z) )
  y=L-f_lim(z)
  p2da=f_ada(x,y) * ( 1/(z-z1) + 1/(z2-z) )
  return
end function
!*****************************************
real(8) function p1d(z,L)
  use params
  implicit none
  real(8) y,z,L
  real(8),external :: f_lim,f1d

  y=L-f_lim(z)
  p1d=f1d(y)/(z2-z1)
end function
!*****************************************
real(8) function p1da(z,L)
  use params
  implicit none
  real(8) y,z,L
  real(8),external :: f_lim,f1da
  
  y=L-f_lim(z)
  p1da=f1da(y)/(z2-z1)
  return   
end function
!*****************************************
real(8) function pw2d(z,L)
  use params
  implicit none
  real(8) x,y,z,L
  real(8),external :: f_lim,fw_ref

  x=log( (z-z1)/(z2-z))
  y=L-f_lim(z)
  pw2d=fw_ref(x,y) * ( 1/(z-z1) + 1/(z2-z) )
  return 
end function
!*****************************************
real(8) function pw2da(z,L)
  use params
  implicit none
  real(8) x,y,z,L
  real(8),external :: f_lim,fw_ada

  x=log( (z-z1)/(z2-z) )
  y=L-f_lim(z)
  pw2da=fw_ada(x,y) * ( 1/(z-z1) + 1/(z2-z) )
  if ( (pw2da>10000.0) .or. (pw2da<0.0) ) then
    write(110,"(f20.16,2X,3f9.4,2X,f12.3,2X,2f8.4)") z,L,x,y,pw2da,h10,h20    
  end if  
  return
end function

END MODULE prob_functions

!################################################################################################

MODULE fhi_functions           ! module for leave-more-out functions  
  implicit none
  CONTAINS
 !***************************************** 
real(8) function fhi(i,xi,yi)
  use params
  implicit none
  real(8) xi,yi
  real(8) x_m,y_m,y_p,xj,yj,temp
  real(8),external :: K
  integer i,j
  
  fhi=0.0
  do j=1,ndata
    xj=xz(j)
    yj=ylum(j)            	    
    x_m=(xi-xj)/h1            
    y_m=(yi-yj)/h2
    y_p=(yi+yj)/h2

    if ( xdif(j,i) ) then
      if ( ydif(j,i) ) then  
        temp=( K(x_m,y_m) + K(x_m,y_p) ) 
      else
        temp=K(x_m,y_p)
      end if        
      fhi=fhi + temp
    end if 
  end do
  fhi=fhi/(h1*h2) 
end function
!*****************************************

real(8) function fhi_ada(i,xi,yi)
  use params
  implicit none
  real(8) xi,yi,ha1,ha2
  real(8) x_m,y_m,y_p,xj,yj,temp
  real(8),external :: K
  integer i,j  
  
  fhi_ada=0.0
  do j=1,ndata
    xj=xz(j)
    yj=ylum(j)            	    
    ha1=h10*hi(j)
    ha2=h20*hi(j)
    x_m=(xi-xj)/ha1            
    y_m=(yi-yj)/ha2
    y_p=(yi+yj)/ha2

    if ( xdif(j,i) ) then
      if ( ydif(j,i) ) then  
        temp=( K(x_m,y_m) + K(x_m,y_p) ) / (ha1*ha2)  
      else
        temp=K(x_m,y_p) / (ha1*ha2)
      end if        
      fhi_ada=fhi_ada + temp
    end if
    
  end do   
  return
end function
!*****************************************
real(8) function fwhi(i,xi,yi)
  use params
  implicit none
  real(8) xi,yi
  real(8) x_m,y_m,y_p,xj,yj,temp
  real(8),external :: K
  integer i,j
  
  fwhi=0.0
  do j=1,ndata
    xj=xz(j)
    yj=ylum(j)            	    
    x_m=(xi-xj)/h1            
    y_m=(yi-yj)/h2
    y_p=(yi+yj)/h2
    if ( xdif(j,i) ) then
      if ( ydif(j,i) ) then  
        temp=( K(x_m,y_m) + K(x_m,y_p) ) 
      else
        temp=K(x_m,y_p)
      end if        
      fwhi=fwhi + temp*weight(j)
    end if          
  end do
  fwhi=fwhi/(h1*h2) 
end function
!*****************************************

real(8) function fwhi_ada(i,xi,yi)
  use params
  implicit none
  real(8) xi,yi,ha1,ha2
  real(8) x_m,y_m,y_p,xj,yj,temp
  real(8),external :: K
  integer i,j  
  
  fwhi_ada=0.0
  do j=1,ndata
    xj=xz(j)
    yj=ylum(j)            	    
    ha1=h10*hi(j)
    ha2=h20*hi(j)
    x_m=(xi-xj)/ha1            
    y_m=(yi-yj)/ha2
    y_p=(yi+yj)/ha2

    if ( xdif(j,i) ) then
      if ( ydif(j,i) ) then  
        temp=( K(x_m,y_m) + K(x_m,y_p) ) / (ha1*ha2)  
      else
        temp=K(x_m,y_p) / (ha1*ha2)
      end if        
      fwhi_ada=fwhi_ada + temp*weight(j)
    end if
  end do   
  return
end function

END MODULE fhi_functions

!################################################################################################
!               
!************************************************************************************************


subroutine f2py_value(nd,input_python,md,process_python)
  use params
  implicit none
  integer :: nd,md,process_python
  real(8) :: input_python(md)
!f2py intent(in) :: nd,input_python,process_python 
!integer intent(hide),depend(input_python) :: md=shape(input_python)   
  ndata=nd 
  process=process_python
  H0=input_python(1)
  matter=input_python(2)
  lambda=1-matter
  z1=input_python(3)
  z2=input_python(4)
  Lmin=input_python(5)
  Lmax=input_python(6)     
  return
end subroutine f2py_value

!*****************************************

subroutine initialize(epson,ans)
  use params
  implicit none
  integer i,j,num
  real(8) epson,ans,dif
  !f2py intent(in) :: epson
  !f2py intent(out) :: ans 
  !real(8),parameter :: epson=1e-9
  
  if (allocated(ni)) deallocate(ni)   
  if (allocated(xdif)) deallocate(xdif)
  if (allocated(ydif)) deallocate(ydif)  
  
  allocate(xdif(ndata,ndata))
  allocate(ydif(ndata,ndata))  
  !open(unit=101,file="temp1.txt")
  !open(unit=102,file="temp2.txt")  
  !open(unit=103,file="temp3.txt")
  num=0
  do i=1,ndata
    do j=1,ndata
      if ( abs(xz(i)-xz(j))<epson ) then
        xdif(j,i)=.false.
!        if ( (i /= j) .and.  ( abs(xz(i)-xz(j))>1e-9 ) ) then
!          write(101,*) 'x,j,i',j,i, xz(i),xz(j)
!        end if        
      else
        xdif(j,i)=.true.
      end if  
      if ( abs(ylum(i)-ylum(j))<epson ) then
        ydif(j,i)=.false.
!        if ( (i /= j) .and. ( abs(ylum(i)-ylum(j))>1e-9 ) )then
!          write(102,*) 'y,j,i',j,i, ylum(i),ylum(j)
!        end if        
      else
        ydif(j,i)=.true.
      end if                
      
      dif=abs(ylum(i)-ylum(j))
      if ( dif > 1e-30 .and. dif < epson ) then
        num=num+1
      end if      
      !write(101,*) 'j,i',j,i,xdif(j,i),ydif(j,i)
    end do 
  end do 
   
  ans=num*1.0/ndata/ndata 
  !print*,num,ans 
   
  allocate(ni(ndata))
  if (weighting) then    
    do i=1,ndata
      ni(i)=0.0
      do j=1,ndata
        if ( xdif(j,i)==.false. ) then
          ni(i)=ni(i) + 2*weight(j)
        end if      
        if ( xdif(j,i) .and. ydif(j,i)==.false. )  then
          ni(i)= ni(i) + weight(j)     
        end if  
      end do
      !write(103,*) 'i',i,ni(i)
    end do 
  end if 
  
  if (.not. weighting) then    
    do i=1,ndata
      ni(i)=0.0
      do j=1,ndata
        if ( xdif(j,i)==.false. ) then
          ni(i)=ni(i) + 2.0
        end if      
        if ( xdif(j,i) .and. ydif(j,i)==.false. )  then
          ni(i)= ni(i) + 1.0     
        end if  
      end do
      !write(103,*) 'i',i,ni(i)
    end do 
  end if 
  
  
  !print*,ni(1)
  !print*,'nw',nw

  return    
end subroutine initialize


subroutine check()
  use params

  if (allocated(xz)) deallocate(xz)  
  if (allocated(red)) deallocate(red)
  if (allocated(ylum)) deallocate(ylum)  
  if (allocated(hi)) deallocate(hi)
  if (allocated(f_pilot)) deallocate(f_pilot)
  if (allocated(weight)) deallocate(weight) 
  if (allocated(ni)) deallocate(ni)   
  if (allocated(xdif)) deallocate(xdif)
  if (allocated(ydif)) deallocate(ydif)
  if (allocated(limx)) deallocate(limx)  
  if (allocated(limy)) deallocate(limy)    
  return    
end subroutine check

!################################################################################################
!************************************************************************************************
subroutine lnlike(h1_py,h2_py,ans)
  use params
  use myquad
  use prob_functions
  use fhi_functions
  implicit none
  real(8) :: h1_py,h2_py,ans
!f2py intent(in) :: h1_py,h2_py
!f2py intent(out) :: ans 
  real(8) :: f_hi(ndata)
  real(8) temp,x_m,y_m,y_p
  real(8) xi,yi,ftemp,xj,yj
  real(8) int2d,log_lik
  integer i,j
  !real(8),external :: fhi,fwhi
  real(8),external :: X1,X2   !p,pw    
  procedure(p2d), pointer :: p
  procedure(fhi), pointer :: fi
    
  h1=h1_py
  h2=h2_py 
  ftemp=0.0
  log_lik=0.0

  if (weighting) then
    p => pw2d
    fi => fwhi
  else
    p => p2d
    fi => fhi
    nw=ndata*1.0
  end if

  !$omp parallel NUM_THREADS(process) private(i,xi,yi,ftemp) shared(log_lik)  	
  !$omp do  
  do i=1,ndata
    f_hi(i)=0.0
    xi=xz(i)           
    yi=ylum(i)           	
    f_hi(i)=fi(i,xi,yi)    
    f_hi(i)=f_hi(i)*2/(2*nw-ni(i)) * ( 1/(red(i)-z1) + 1/(z2-red(i)) ) 
    ftemp = ftemp + log( f_hi(i) )
    !print*,'here',i,f_hi(i)    	
  end do    
  !$omp end do
  !$OMP ATOMIC
  log_lik=log_lik + ftemp
  !$omp end parallel  

  !***********************************************************************************************

  if(bounded_lum == .false.) then
    ans = log_lik
  else
    if (absolute_magnitude) then
      L2=Lmin
      call myquad2d(z1,z2,X2,X1,p,int2d)
    else
      L2=Lmax
      call myquad2d(z1,z2,X1,X2,p,int2d)    
    end if 
    !print*,'here3',int2d
    ans = log_lik - nw*int2d
  end if    
  return
end subroutine lnlike

!################################################################################################
!                Calculate expected cumulative distribution functions (CDFs)  
!************************************************************************************************
!subroutine czf(z,nd,ans)
!  use params
!  use myquad
!  implicit none
!  integer :: nd,i
!  real(8) :: ans(nd),z(nd),area
!!f2py intent(in) :: z 
!!integer intent(hide),depend(z) :: nd=shape(z) 
!!f2py intent(out) :: ans
!  real(8),external :: p,p_ada,p1da,X1,X2,pp

!  L1=Lmin
!  L2=Lmax  
!  do i=1,ndata
!    if (small_sample_approximation) then
!      call myquad2d(z1,z(i),X1,X2,p1da,area)
!    else
!      if (adaptive) then        
!        call myquad2d(z1,z(i),X1,X2,p_ada,area)
!      else             
!        call myquad2d(z1,z(i),X1,X2,p,area)
!      end if
!    end if  
!    ans(i)=area
!    !write(*,'(5f10.6)'),z,area
!  end do
!  return

!end subroutine czf


!subroutine clf1d(lum,nd,ans)
!  use params
!  use dqag_and_dqags
!  implicit none
!  integer :: nd,i
!  real(8) :: lum(nd),ans(nd),area
!!f2py intent(in) :: lum,z 
!!integer intent(hide),depend(lum) :: nd=shape(lum) 
!!f2py intent(out) :: ans
!  real(8),external :: f1d,f1da
!  integer ( kind = 4 ), parameter :: limit = 500
!  integer ( kind = 4 ), parameter :: lenw = limit * 4
!  real ( kind = 8 ) a
!  real ( kind = 8 ) abserr
!  real ( kind = 8 ) b
!  real ( kind = 8 ), parameter :: epsabs = 0.0D+00
!  real ( kind = 8 ), parameter :: epsrel = 0.001D+00
!  integer ( kind = 4 ) ier
!  integer ( kind = 4 ) iwork(limit)
!  integer ( kind = 4 ) last
!  integer ( kind = 4 ) neval
!  real ( kind = 8 ) work(lenw)
!  
!  do i=1,ndata
!    a=0
!    b=lum(i)
!    if (adaptive) then     
!      call dqags ( f1da, a, b, epsabs, epsrel, area, abserr, neval, ier, limit, lenw, last, iwork, work )        
!    else
!      call dqags ( f1d, a, b, epsabs, epsrel, area, abserr, neval, ier, limit, lenw, last, iwork, work )
!    end if
!    ans(i)=area
!    !write(*,'(5f10.6)'),L2,area
!  end do
!  return
!end subroutine clf1d


!subroutine clf(lum,nd,z2s,ans)
!  use params
!  use myquad
!  implicit none
!  integer :: nd,i
!  real(8) :: lum(nd),ans(nd),z2s(nd),area
!!f2py intent(in) :: lum,z 
!!integer intent(hide),depend(lum) :: nd=shape(lum) 
!!f2py intent(out) :: ans
!  real(8),external :: p,p_ada,p1d,p1da,X1,X2,pp,pw

!  do i=1,ndata
!    L1=Lmin
!    L2=lum(i)
!    if (small_sample_approximation) then
!      if (adaptive) then     
!        call myquad2d(z1,z2s(i),X1,X2,p1da,area)        
!      else
!        call myquad2d(z1,z2s(i),X1,X2,p1d,area)
!      end if    
!    else
!      if (adaptive) then        
!        call myquad2d(z1,z2s(i),X1,X2,p_ada,area)
!      else        
!        if (absolute_magnitude) then
!          call myquad2d(z1,z2s(i),X2,X1,pw,area)      
!        else
!          call myquad2d(z1,z2s(i),X1,X2,p,area)
!        end if
!      end if
!    end if  
!    ans(i)=area
!    write(133,'(I4,2f10.6)'),i,L2,area
!  end do
!  return

!end subroutine clf



subroutine clf_new(lum,nd,z2s,ans)
  use params
  use myquad
  use prob_functions
  implicit none
  integer :: nd
  real(8) :: lum(nd),ans(nd),z2s(nd),ai
!f2py intent(in) :: lum,z 
!integer intent(hide),depend(lum) :: nd=shape(lum) 
!f2py intent(out) :: ans
  !real(8),external :: p,pw
  real(8),external :: X1,X2,g_lim,f_lim
  real(8), allocatable :: st(:)
  real(8),parameter :: dl=0.0002
  real(8),parameter :: dz=0.0002
  real(8) dlj,lc,z,zc,zt,gj,gjj,dli,f_lim_z2
  integer i,j,n
  procedure(p2d), pointer :: p

  if (weighting) then
    p => pw2d
  else
    p => p2d
  end if

  f_lim_z2=f_lim(z2)
  DO i=1,nd    
    IF (i==1) then
      L2=lum(i)
      if (absolute_magnitude) then
        call myquad2d(z1,z2s(i),X2,X1,p,ai)
      else
        call myquad2d(z1,z2s(i),X1,X2,p,ai)
      end if  
      ans(i)=ai      
    ELSE
      dli=abs(lum(i)-lum(i-1))
      if ( dli>dl ) then
        n= max( floor(dli/dl),2 )
      else
        n=1
      end if        
      
      write(121,*) i,dli,n
      
      allocate(st(n+1))
      dlj=dli/n
      if (absolute_magnitude) then   !*******absolute_magnitude is .true.
          st(1)=lum(i-1)
          do j=2,n+1
            st(j)=st(j-1)-dlj
          end do      
          gj=0.0
          do j=1,n
            lc=st(j)-dlj/2      
            if (lc>f_lim_z2) then       
              zt=g_lim(lc)
            else
              zt=z2
            end if    
            z=z1+dz
            gjj=0.0
            do while(z<=zt)
              zc=z-dz/2
              gjj=gjj+p(zc,lc)*dz*dlj         
              z=z+dz
            end do
            gj=gj+gjj
          end do                       
      
      else                         !*******absolute_magnitude is .false.             
          st(1)=lum(i-1)
          do j=2,n+1
            st(j)=st(j-1)+dlj
          end do       
          gj=0.0
          do j=1,n
            lc=st(j)+dlj/2      
            if (lc<=f_lim_z2) then       
              zt=g_lim(lc)
            else
              zt=z2
            end if    
            z=z1+dz
            gjj=0.0
            do while(z<=zt)
              zc=z-dz/2
              gjj=gjj+p(zc,lc)*dz*dlj    
              z=z+dz
            end do
            gj=gj+gjj
          end do
      end if                      !*******absolute_magnitude judgement end if   
      deallocate(st)
      ans(i)=ans(i-1)+gj    
    END IF
    write(113,'(I4,2f10.6)') i,lum(i),ans(i)
  END DO  
  return
end subroutine clf_new


!subroutine clf1(lum,nd,z2s,ans)
!  use params
!  use myquad
!  implicit none
!  integer :: nd,i,n
!  real(8) :: lum(nd),ans(nd),z2s(nd),area
!!f2py intent(in) :: lum,z 
!!integer intent(hide),depend(lum) :: nd=shape(lum) 
!!f2py intent(out) :: ans
!  real(8),external :: p,p_ada,p1da,X1,X2,pp

!  process=10
!  n=3
!  !$omp parallel NUM_THREADS(n) private(i,area)  	
!  !$omp do
!  do i=1,ndata
!    L1=Lmin
!    L2=lum(i)
!    if (small_sample_approximation) then
!      call myquad2d(z1,z2s(i),X1,X2,p1da,area)
!    else
!      if (adaptive) then        
!        call myquad2d(z1,z2s(i),X1,X2,p_ada,area)
!      else        
!        !call myquad2d(z1,z2,X1,X2,pp,area)      
!        call myquad2d(z1,z2s(i),X1,X2,p,area)
!      end if
!    end if  
!    ans(i)=area
!    !write(*,'(I5,5f10.6)'),i,L2,area
!  end do
!  !$omp end do
!  !$omp end parallel
!  return

!end subroutine clf1

!subroutine clf2(lum,nd,z2s,ans)
!  use params
!  use myquad
!  implicit none
!  integer :: nd,i,n
!  real(8) :: lum(nd),ans(nd),z2s(nd),area
!!f2py intent(in) :: lum,z 
!!integer intent(hide),depend(lum) :: nd=shape(lum) 
!!f2py intent(out) :: ans
!  real(8),external :: p,p_ada,p1da,X1,X2,pp
!  
!  n=10
!  do i=1,ndata
!    if((i-n)<=0) then
!      L1=Lmin
!    else
!      L1=lum(i-n)
!    end if
!    L2=lum(i)     

!    if (small_sample_approximation) then
!      call myquad2d(z1,z2s(i),X1,X2,p1da,area)
!    else
!      if (adaptive) then        
!        call myquad2d(z1,z2s(i),X1,X2,p_ada,area)
!      else
!        !call myquad2d(z1,z2,X1,X2,pp,area)      
!        call myquad2d(z1,z2s(i),X1,X2,p,area)
!      end if
!    end if    
!    
!    if((i-n)<=0) then
!      ans(i)=area
!    else
!      ans(i)=ans(i-n)+area
!    end if    
!    
!    !write(*,'(5f10.6)'),L2,area
!  end do
!  return

!end subroutine clf2



!subroutine clf2d(lum,nd,z,ans)
!  use params
!  use myquad
!  implicit none
!  integer :: nd,i
!  real(8) :: lum(nd),ans(nd),z(nd),area
!!f2py intent(in) :: lum,z 
!!integer intent(hide),depend(lum) :: nd=shape(lum) 
!!f2py intent(out) :: ans
!  real(8),external :: p,p_ada,p1da,X1,X2,pp
!    
!  !l2lim=f_lim(z2)
!  do i=1,ndata
!    !if(lum(i)<l2lim) then
!    !  L1=lum(i)
!    !end if     
!    L1=Lmin
!    L2=lum(i)    
!    if (small_sample_approximation) then
!      call myquad2d(z1,z(i),X1,X2,p1da,area)
!    else
!      if (adaptive) then        
!        call myquad2d(z1,z(i),X1,X2,p_ada,area)
!      else        
!        !call myquad2d(z1,z2,X1,X2,pp,area)      
!        call myquad2d(z1,z(i),X1,X2,p,area)
!      end if
!    end if  
!    ans(i)=area
!    !write(*,'(3f10.6)'),lum(i),z(i),area
!  end do
!  return

!end subroutine clf2d


!************************************************************************************************
!################################################################################################
real(8) function K(x,y)
  implicit none
  real(8),parameter :: pi=3.141592653589793  
  real(8) x,y
  
  K=1/(2*pi)*exp(-0.5*(x*x+y*y))
end function

!***************************************
subroutine prob(z,L,ans)
  use params
  use prob_functions
  implicit none
  real(8) z,L,ans
!f2py intent(in) :: z,L
!f2py intent(out) :: ans
  procedure(p2d), pointer :: p
  
  if (adaptive) then
    hi=f_pilot**(-beta)    
    !hi=(1+f_pilot)**(-beta)
    !hi=exp(-beta*f_pilot)  
    if (weighting) then
      p => pw2da
    else
      p => p2da
    end if     
  
  else  
    if (weighting) then
      p => pw2d
    else
      p => p2d
    end if  
  end if  

  ans=p(z,L)
  return
end subroutine prob


subroutine prob1d(z,L,ans)
  use params
  use prob_functions
  implicit none
  real(8) z,L,ans
!f2py intent(in) :: z,L
!f2py intent(out) :: ans
  procedure(p2d), pointer :: p
  
  if (adaptive) then
    hi=f_pilot**(-beta)
    p => p1da 
  else
    p => p1d
  end if  

  ans=p(z,L)
  return
end subroutine prob1d


subroutine f_ref_f2py(x,y,ans)
  use params
  implicit none
  real(8) x,y,ans,x_minus,y_minus,y_plus,temp,ftemp
  real(8),external :: K
  integer i,num  
  real(8) xi,yi
!f2py intent(in) :: x,y
!f2py intent(out) :: ans

  num=ndata
  ans=0.0
  ftemp=0.0
  !$omp parallel NUM_THREADS(process) private(i,xi,yi,x_minus,y_minus,y_plus,temp,ftemp) shared(ans)  	
  !$omp do
  do i=1,num
    xi=xz(i)                 
    yi=ylum(i)                 
    x_minus=(x-xi)/h1
    y_minus=(y-yi)/h2
    y_plus=(y+yi)/h2
    temp= K(x_minus,y_minus)+K(x_minus,y_plus)
    ftemp=ftemp + temp
  end do
  !$omp end do
  !$OMP ATOMIC
  ans=ans + ftemp
  !$omp end parallel
  ans=ans/(h1*h2*num)
  return 
end subroutine f_ref_f2py

!***************************************
real(8) function f_ref(x,y)
  use params
  implicit none
  real(8) x,y,x_minus,y_minus,y_plus,temp,ftemp
  real(8),external :: K
  integer i,num  
  real(8) xi,yi

  num=ndata
  f_ref=0.0
  ftemp=0.0
  !$omp parallel NUM_THREADS(process) private(i,xi,yi,x_minus,y_minus,y_plus,temp,ftemp) shared(f_ref)  	
  !$omp do
  do i=1,num
    xi=xz(i)                 
    yi=ylum(i)                
    x_minus=(x-xi)/h1
    y_minus=(y-yi)/h2
    y_plus=(y+yi)/h2
    temp= K(x_minus,y_minus)+K(x_minus,y_plus)
    ftemp=ftemp + temp
  end do
  !$omp end do
  !$OMP ATOMIC
  f_ref=f_ref + ftemp
  !$omp end parallel
  f_ref=f_ref/(h1*h2*num)
  return  
end function

!***************************************
real(8) function pp(z,L)
  use params
  implicit none
  real(8) x,y,z,L,bandwidth
  real(8),external :: f_lim,f_ref

  x=log( (z-z1)/(z2-z) )
  y=L-f_lim(z)
  if (z>z1 .and. z<z2 .and. L>f_lim(z)) then 
    pp=f_ref(x,y) * ( 1/(z-z1) + 1/(z2-z) )
  else
    pp=0.0
  end if    
end function


!#############################################################################

real(kind=8) function X1(z)
  use params
  implicit none
  real(kind=8) z
  real(8),external :: f_lim 

  X1=f_lim(z)
  return
end function

real(kind=8) function X2(z)
  use params
  implicit none
  real(kind=8) z
  
  X2 = L2
  return
end function 
!************************************************************************************************
!################################################################################################
real(8) function f_ada(x,y)
  use params
  implicit none
  real(8) x,y,ha1,ha2
  real(8) xi,yi,x_m,y_m,y_p,ftemp
  real(8),external :: K
  integer i

  f_ada=0.0
  ftemp=0.0
  !$omp parallel NUM_THREADS(process) private(i,xi,yi,ha1,ha2,x_m,y_m,y_p,ftemp) shared(f_ada)  	
  !$omp do
  do i=1,ndata
    xi=xz(i)                   
    yi=ylum(i)            
    ha1=h10*hi(i)
    ha2=h20*hi(i)
    x_m=(x-xi)/ha1
    y_m=(y-yi)/ha2
    y_p=(y+yi)/ha2
    ftemp=ftemp + ( K(x_m,y_m)+K(x_m,y_p) )/(ha1*ha2)
  end do  	
  !$omp end do
  !$OMP ATOMIC
  f_ada=f_ada + ftemp
  !$omp end parallel
  f_ada=f_ada/ndata
end function

!################################################################################################
!************************************************
subroutine lnlike_ada(h1_py,h2_py,beta_py,ans)
  use params
  use myquad
  use prob_functions
  use fhi_functions
  implicit none
  real(8) :: h1_py,h2_py,beta_py,ans
!f2py intent(in) :: h1_py,h2_py,beta_py
!f2py intent(out) :: ans 
  real(8) :: f_hi(ndata)
  real(8) temp,x_m,y_m,y_p
  real(8) log_lik,int2d
  real(8) xi,yi,ftemp,xj,yj
  integer i,j
  !real(8),external :: fhi_ada,fwhi_ada
  real(8),external :: X1,X2   !,p_ada,pw_ada
  procedure(p2d), pointer :: p
  procedure(fhi), pointer :: fi

  if (weighting) then
    p => pw2da
    fi => fwhi_ada 
  else
    p => p2da
    fi => fhi_ada
    nw=ndata*1.0
  end if
    
  h10=h1_py
  h20=h2_py  
  beta=beta_py
  if (.not. set_beta_fixed) then  
    hi=f_pilot**(-beta)
    !hi=(1+f_pilot)**(-beta)
    !hi=exp(-beta*f_pilot) 
  end if  
  
  ftemp=0.0
  log_lik=0.0

  !******************************************************************************
  !$omp parallel NUM_THREADS(process) private(i,xi,yi,ftemp) shared(log_lik)  	
  !$omp do  
  do i=1,ndata
    f_hi(i)=0.0
    xi=xz(i)           
    yi=ylum(i)           	
    f_hi(i)=fi(i,xi,yi) 
    f_hi(i)=f_hi(i)*2/(2*nw-ni(i)) * ( 1/(red(i)-z1) + 1/(z2-red(i)) )
    ftemp = ftemp + log( f_hi(i) )   	
  end do    
  !$omp end do
  !$OMP ATOMIC
  log_lik=log_lik + ftemp
  !$omp end parallel  
  
  if(bounded_lum == .false.) then
    ans = log_lik
  else
    if (absolute_magnitude) then
      L2=Lmin
      call myquad2d(z1,z2,X2,X1,p,int2d)
    else
      L2=Lmax
      call myquad2d(z1,z2,X1,X2,p,int2d)    
    end if 
    !print*,'here3',int2d
    ans = log_lik - nw*int2d
  end if 

  return
end subroutine lnlike_ada


!#######################################################################################################################

subroutine lnlike_1d(h2_py,ans)
  use params
  use myquad
  implicit none
  real(8) :: h2_py,ans
!f2py intent(in) :: h2_py
!f2py intent(out) :: ans 
  real(8) :: f_hi(ndata)
  real(8) temp
  real(8) yi,ftemp,yj
  real(8) int2d,log_lik
  integer i,j
  real(8),external :: fhi_1d
  real(8),external :: p1d,X1,X2    

  h2=h2_py  
  ftemp=0.0
  log_lik=0.0
  !$omp parallel NUM_THREADS(process) private(i,yi,ftemp) shared(log_lik)  	
  !$omp do
  do i=1,ndata
    f_hi(i)=0.0          
    yi=ylum(i)           	
    f_hi(i)=fhi_1d(i,yi)    
    f_hi(i)=f_hi(i)*2/(2*ndata-1)/(z2-z1)
    ftemp = ftemp + log( f_hi(i) )    	
  end do    
  !$omp end do
  !$OMP ATOMIC
  log_lik=log_lik + ftemp
  !$omp end parallel
  
  L1=Lmin
  L2=Lmax
  call myquad2d(z1,z2,X1,X2,p1d,int2d)  
  ans = log_lik - ndata*int2d  
  return
end subroutine lnlike_1d


real(8) function fhi_1d(i,yi)
  use params
  implicit none
  real(8) yi,y_m,y_p,yj,temp
  integer i,j
  
  fhi_1d=0.0
  do j=1,ndata
    yj=ylum(j)           
    y_m=(yi-yj)/h2
    y_p=(yi+yj)/h2
    if(j /= i) then
    	temp= ( exp(-y_m**2/2) + exp(-y_p**2/2) )    
    else
    	temp=exp(-y_p**2/2)	  
    end if
    fhi_1d=fhi_1d + temp
  end do
  fhi_1d=fhi_1d/(h2*sqrt(2*pi))
end function


!***************************************
real(8) function f1d(y)
  use params
  implicit none
  real(8) y,y_minus,y_plus,temp,ftemp,f_ref
  integer i,num  
  real(8) xi,yi

  num=ndata
  f_ref=0.0
  ftemp=0.0
  !$omp parallel NUM_THREADS(process) private(i,yi,y_minus,y_plus,temp,ftemp) shared(f_ref)  	
  !$omp do
  do i=1,num                     
    yi=ylum(i)    
    y_minus=(y-yi)/h2
    y_plus=(y+yi)/h2
    temp=( exp(-y_minus**2/2) + exp(-y_plus**2/2) )/sqrt(2*pi)    
    ftemp=ftemp + temp
  end do
  !$omp end do
  !$OMP ATOMIC
  f_ref=f_ref + ftemp
  !$omp end parallel
  f1d=f_ref/(h2*num)
  return  
end function

!***************************************
real(8) function p1d(z,L)
  use params
  implicit none
  real(8) y,z,L
  real(8),external :: f_lim,f1d

  y=L-f_lim(z)
  p1d=f1d(y)/(z2-z1)
end function

!#############################################################################
subroutine lnlike_1da(h2_py,beta_py,ans)
  use params
  use myquad
  implicit none
  real(8) :: h2_py,beta_py,ans
!f2py intent(in) :: h2_py,beta_py
!f2py intent(out) :: ans 
  real(8) :: f_hi(ndata)
  real(8) temp
  real(8) yi,ftemp,yj
  real(8) int2d,log_lik
  integer i,j
  real(8),external :: fhi_1da
  real(8),external :: p1da,X1,X2    

  h20=h2_py
  beta=beta_py  
  hi=f_pilot**(-beta)
  
  ftemp=0.0
  log_lik=0.0
  !$omp parallel NUM_THREADS(process) private(i,yi,ftemp) shared(log_lik)  	
  !$omp do
  do i=1,ndata              
    yi=ylum(i)           	
    f_hi(i)=fhi_1da(i,yi)    
    f_hi(i)=f_hi(i)*2/(2*ndata-1)/(z2-z1)
    ftemp = ftemp + log( f_hi(i) )    	
  end do    
  !$omp end do
  !$OMP ATOMIC
  log_lik=log_lik + ftemp
  !$omp end parallel
  
  L1=Lmin
  L2=Lmax
  call myquad2d(z1,z2,X1,X2,p1da,int2d)  
  ans = log_lik - ndata*int2d  
  return
end subroutine lnlike_1da


!*****************************************************
real(8) function f1da(y)
  use params
  implicit none
  real(8) y,h
  real(8) yi,y_m,y_p,ftemp
  !real(8),external :: K
  integer i
  
  f1da=0.0
  ftemp=0.0
  !$omp parallel NUM_THREADS(process) private(i,yi,h,y_m,y_p,ftemp) shared(f1da)  	
  !$omp do
  do i=1,ndata
    yi=ylum(i) 	            
    h=h20*hi(i)
    y_m=(y-yi)/h
    y_p=(y+yi)/h
    ftemp=ftemp + ( exp(-y_m**2/2) + exp(-y_p**2/2) )/sqrt(2*pi) /h       
  end do  	
  !$omp end do
  !$OMP ATOMIC
  f1da=f1da + ftemp
  !$omp end parallel
  f1da=f1da/ndata
end function

real(8) function fhi_1da(i,yi)
  use params
  implicit none
  real(8) yi,yj,h
  real(8) y_m,y_p,temp
  integer i,j
  
  fhi_1da=0.0
  do j=1,ndata
    yj=ylum(j)           	    
    h=h20*hi(j)
    y_m=(yi-yj)/h
    y_p=(yi+yj)/h
    if(j /= i) then
    	temp=( exp(-y_m**2/2) + exp(-y_p**2/2) )/sqrt(2*pi) /h        !( K(y_m) + K(y_p) ) / h      
    else
    	temp= exp(-y_p**2/2) /sqrt(2*pi) /h  	  
    end if
    fhi_1da=fhi_1da + temp
  end do
end function

real(8) function p1da(z,L)
  use params
  implicit none
  real(8) y,z,L
  real(8),external :: f_lim,f1da
  
  y=L-f_lim(z)
  p1da=f1da(y)/(z2-z1)
  return   
end function

!################################################################################################
!             The KDE Method Considering the Weighting Due to the Selection Function  
!************************************************************************************************
real(8) function fw_ref(x,y)
  use params
  implicit none
  real(8) x,y,x_minus,y_minus,y_plus,temp,ftemp
  real(8),external :: K
  integer i,num  
  real(8) xi,yi

  fw_ref=0.0
  ftemp=0.0
  !$omp parallel NUM_THREADS(process) private(i,xi,yi,x_minus,y_minus,y_plus,temp,ftemp) shared(fw_ref)  	
  !$omp do
  do i=1,ndata
    xi=xz(i)                 
    yi=ylum(i)                
    x_minus=(x-xi)/h1
    y_minus=(y-yi)/h2
    y_plus=(y+yi)/h2
    temp= K(x_minus,y_minus)+K(x_minus,y_plus)
    ftemp=ftemp + temp*weight(i)
  end do
  !$omp end do
  !$OMP ATOMIC
  fw_ref=fw_ref + ftemp
  !$omp end parallel
  fw_ref=fw_ref/(h1*h2*nw)
  return  
end function

!#############################################################################

real(8) function fw_ada(x,y)
  use params
  implicit none
  real(8) x,y,ha1,ha2
  real(8) xi,yi,x_m,y_m,y_p,ftemp
  real(8),external :: K
  integer i,num

  fw_ada=0.0
  ftemp=0.0
  !$omp parallel NUM_THREADS(process) private(i,xi,yi,ha1,ha2,x_m,y_m,y_p,ftemp) shared(fw_ada)  	
  !$omp do
  do i=1,ndata
    xi=xz(i)                   
    yi=ylum(i)            
    ha1=h10*hi(i)
    ha2=h20*hi(i)
    x_m=(x-xi)/ha1
    y_m=(y-yi)/ha2
    y_p=(y+yi)/ha2
    ftemp=ftemp + ( K(x_m,y_m)+K(x_m,y_p) )*weight(i)/(ha1*ha2)
  end do  	
  !$omp end do
  !$OMP ATOMIC
  fw_ada=fw_ada + ftemp
  !$omp end parallel
  fw_ada=fw_ada/nw
end function

!################################################################################################
!         !!! lscv method, not used in current version  
!************************************************************************************************

subroutine lscv(h,ans)
  use params
  !use myquad
  implicit none
  real(8) :: h,ans
!f2py intent(in) :: h
!f2py intent(out) :: ans 
  real(8) xi,xj,x_m,x_p
  real(8) K2hi_m,K2hi_p,Khi_m,Khi_p
  real(8) lscv1,lscv2
  real(8) f_hi(ndata),f_2hi(ndata)   
  real(8) xm2,xp2
  integer i,j 

  do i=1,ndata
    f_hi(i)=0.0
    f_2hi(i)=0.0
    xi=ylum(i)
    do j=1,ndata               
      xj=ylum(j)  	    
      x_m=(xi-xj)/h
      x_p=(xi+xj)/h
      xm2=-(x_m**2)/2
      xp2=-(x_p**2)/2      
      Khi_m=exp(xm2)               
      Khi_p=exp(xp2)            
      K2hi_m=exp(xm2/2)         
      K2hi_p=exp(xp2/2)         
      f_2hi(i) = f_2hi(i) + (K2hi_m + K2hi_p) 
      f_hi(i) =f_hi(i) + (Khi_m + Khi_p)
    end do  
    f_hi(i)=f_hi(i)-1.0
  end do 
  lscv1=sum(f_2hi)/(2*sqrt(pi))/(2*ndata*ndata*h)
  lscv2=sum(f_hi)/(sqrt(2*pi)) /(ndata*(2*ndata-1)*h) 
  !print*,'lscv1,lscv2',lscv1,lscv2
  ans=lscv1 - 2*lscv2
  return
end subroutine lscv

subroutine lscv2d(h1_py,h2_py,ans)
  use params
  !use myquad
  implicit none
  real(8) :: h1_py,h2_py,ans
!f2py intent(in) :: h1_py,h2_py
!f2py intent(out) :: ans 
  real(8) xi,yi,xj,yj,x_m,y_m,y_p
  real(8) K2hi_m,K2hi_p,Khi_m,Khi_p
  real(8) lscv1,lscv2
  real(8) f_hi(ndata),f_2hi(ndata)   
  real(8) temp1,temp2,xmym,xmyp
  integer i,j  
    
  h1=h1_py
  h2=h2_py

  do i=1,ndata
    f_hi(i)=0.0
    f_2hi(i)=0.0
    xi=xz(i)                 
    yi=ylum(i)
    do j=1,ndata
      xj=xz(j)                 
      yj=ylum(j)  	    
      x_m=(xi-xj)/h1  
      y_m=(yi-yj)/h2
      y_p=(yi+yj)/h2
      xmym=-(x_m**2 + y_m**2)/2
      xmyp=-(x_m**2 + y_p**2)/2        
      Khi_m=exp(xmym)                 !Khi_m=exp(-(x_m**2 + y_m**2)/2)
      Khi_p=exp(xmyp)                 !Khi_p=exp(-(x_m**2 + y_p**2)/2)
      K2hi_m=exp(xmym/2)              !K2hi_m=exp(-(x_m**2 + y_m**2)/4)
      K2hi_p=exp(xmyp/2)              !K2hi_p=exp(-(x_m**2 + y_p**2)/4)
      f_2hi(i) = f_2hi(i) + (K2hi_m + K2hi_p) 
      f_hi(i) =f_hi(i) + (Khi_m + Khi_p)
    end do  
    f_hi(i)=f_hi(i)-1.0
  end do 
  lscv1=sum(f_2hi)/(4*h1*h2*pi)/(2*ndata*ndata)
  lscv2=sum(f_hi)/(2*h1*h2*pi) *2/(ndata*(2*ndata-1)) 
  !print*,'3:lscv1,lscv2',lscv1,lscv2
  ans=lscv1 - lscv2
  return
end subroutine lscv2d  


!################################################################################################
!         !!! interpolation to calculate the f_lim function  
!************************************************************************************************
real(8) function f_lim(z)
  use params
  implicit none
  integer,external :: locate
  real(8) z
  integer n,nlim
  
  nlim=size(limx)
  n=locate(limx,z,nlim)
  f_lim=(z-limx(n))*(limy(n+1)-limy(n)) / (limx(n+1)-limx(n)) + limy(n)    

  !print*,z,n
end function


real(8) function g_lim(L)   ! g_lim is the inverse function of f_lim
  use params
  implicit none
  integer,external :: locate
  real(8) L
  integer n,nlim
  
  nlim=size(limy)
  n=locate(limy,L,nlim)
  g_lim=(L-limy(n))*(limx(n+1)-limx(n)) / (limy(n+1)-limy(n)) + limx(n)    

  !print*,z,n
end function

	FUNCTION locate(xx,x,nn)	
	IMPLICIT NONE
	integer nn
	real(8) xx(nn)
	!REAL(8), DIMENSION(:), INTENT(IN) :: xx
	
	REAL(8), INTENT(IN) :: x
	INTEGER :: locate
	INTEGER :: n,jl,jm,ju
	LOGICAL :: ascnd
	n=size(xx)
	ascnd = (xx(n) >= xx(1))
	jl=0
	ju=n+1
	do
		if (ju-jl <= 1) exit
		jm=(ju+jl)/2
		if (ascnd .eqv. (x >= xx(jm))) then
			jl=jm
		else
			ju=jm
		end if
	end do
	if (x == xx(1)) then
		locate=1
	else if (x == xx(n)) then
		locate=n-1
	else
		locate=jl
	end if
	END FUNCTION locate



!subroutine time_lim()
!  use params
!  real(8),external :: f_lim1,f_lim2,f_lim
!  real(8) t1,t2,t3,t4,y
!  integer i,j
!  
!  call cpu_time(t1)
!  do j=1,100
!    do i=1,ndata
!      y=f_lim1(red(i))
!    end do
!  end do  
!  call cpu_time(t2)
!  
!  do j=1,100
!    do i=1,ndata
!      y=f_lim2(red(i))
!    end do
!  end do      
!  call cpu_time(t3)
!  do j=1,100
!    do i=1,ndata
!      y=f_lim(red(i))
!    end do    
!  end do
!  call cpu_time(t4)  
!  print*,'f_lim1,','f_lim2,','f_lim'
!  print*,t2-t1,t3-t2,t4-t3
!  return    
!end subroutine time_lim


real(8) function f_lim1(z)
  use params
  implicit none
  integer :: locate
  integer :: n,jl,jm,ju
  LOGICAL :: ascnd
  integer :: nlim
  real(8) z
  
  nlim=size(limx)
  ascnd = (limx(nlim) >= limx(1))
  jl=0
  ju=n+1
  do while(.true.)
      if (ju-jl <= 1) exit
      jm=(ju+jl)/2
      if (ascnd .eqv. (z >= limx(jm))) then
        jl=jm
      else
        ju=jm
      end if
  end do
  if (z == limx(1)) then
	  locate=1
  else if (z == limx(nlim)) then
	  locate=n-1
  else
	  locate=jl
  end if

  n=locate
  f_lim1=(z-limx(n))*(limy(n+1)-limy(n)) / (limx(n+1)-limx(n)) + limy(n) 
  !print*,z,n
end function

subroutine trap2d(pun,ans)
  use params
  implicit none
  real(8) dz,ans,a,z0,zc,lc,Ai,Le,h,s,vj
  integer i,j,nlim
  real(8),external :: pun 
  
  nlim=size(limx)
  z0=limx(1)
  dz=(z2-z0)/(nlim-1)   
  ans=0.0
  do i=1,nlim-1
    if (i==1) then
      a=dz+z0-z1
      zc=z0+dz/2
    else
      a=dz
      zc=limx(i)+dz/2
    end if
    j=1
    Ai=0.0
    Le=0.0
    
    IF (absolute_magnitude) then    
      do while (Le>=L2)      
        if (j==1) then
          h=limy(i)-limy(i+1)
          s=a*h/2       
          lc=limy(i)-0.7*h
          Le=limy(i+1)
          j=2
        else
          h=0.005
          s=a*h
          lc=Le-h/2   
          Le=Le-h
        end if  
        vj=s*pun(zc,lc)
        Ai=Ai+vj
      end do   
  
    ELSE  
      do while (Le<=L2)      
        if (j==1) then
          h=limy(i+1)-limy(i)
          s=a*h/2       
          lc=limy(i)+0.7*h
          Le=limy(i+1)
          j=2
        else
          h=0.005
          s=a*h
          lc=Le+h/2   
          Le=Le+h
        end if  
        vj=s*pun(zc,lc)
        Ai=Ai+vj
      end do
    END IF  
      ans=ans+Ai 
  end do  
  return
end subroutine trap2d  
 
