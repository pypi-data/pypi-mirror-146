
!include "mod_dqag_dqags.f90"

!%%%%%%%%%%%%%%%%%%%%%%%% module myquad %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
!************************               ******************************
! module myquad, estimates a double definite integral.
! Author: Zunli Yuan
! !!!! version 2019_11_16_16_01

!   main subroutine : myquad2d
!
!   Parameters:
!
!      a      - real ( kind = 8 )
!               lower limit of integration
!
!      b      - real ( kind = 8 )
!               upper limit of integration
!
!      g1     - real ( kind = 8 )
!               function subprogram defining the lower limit 
!               function g1(x). the actual name for g1 needs to be
!               declared 'external' in the driver program.
!      g2     - real ( kind = 8 )
!               function subprogram defining the upper limit
!               function g2(x). the actual name for g2 needs to be
!               declared 'external' in the driver program.

!      f2d    - real ( kind = 8 )
!               function subprogram defining the integrand
!               function f2d(x,y). the actual name for f2d needs to be
!               declared 'external' in the driver program.
module myquad  
  use dqag_and_dqags
  implicit none
  procedure(f1),pointer :: p1
  procedure(f2),pointer :: p2
  procedure(f3),pointer :: p3  
  
  interface    
    function f1(x)
      implicit none
      real(8),intent(in) :: x
      real(8) f1
    end function
    
    function f2(x)
      implicit none
      real(8),intent(in) :: x
      real(8) f2
    end function

    function f3(x,y)
      implicit none
      real(8),intent(in) :: x,y
      real(8) f3
    end function
  end interface  
 
  contains
  
  subroutine myquad2d(a,b,g1,g2,f2d,ans)
    implicit none
    !real (8), external :: g1,g2,f2d  !Declaring variables in this way is not supported here by f2py
    real(8) temp
    real(8) g1,g2,f2d
    external g1,g2,f2d  !should be this for running f2py    
    real(8),intent(in) :: a,b
    real(8),intent(out) :: ans
    integer ( kind = 4 ), parameter :: limit = 500
    real ( kind = 8 ) abserr
    real ( kind = 8 ), parameter :: epsabs = 0.0D+00
    real ( kind = 8 ), parameter :: epsrel = 0.001D+00
    integer ( kind = 4 ) ier
    integer ( kind = 4 ) last
    integer ( kind = 4 ) neval
    !%%%%%%%%%%%%%%  same  
    integer ( kind = 4 ), parameter :: lenw = 4 * limit
    integer ( kind = 4 ) iwork(limit)   
    real ( kind = 8 ) work(lenw)
    integer ( kind = 4 ), parameter :: key = 6
    !%%%%%%%%%%%%%%  different
    
    if(temp==1.0) then  ! for using f2py
      temp=g1(a)        ! redundant code, but it seems to be necessary for using f2py 
      temp=g2(a)
      temp=f2d(a,b)
    end if              ! for using f2py
    
    p1 => g1
    p2 => g2
    p3 => f2d 
    
    call dqag ( H, a, b, epsabs, epsrel, key, ans, abserr, neval, ier, &
      limit, lenw, last, iwork, work )  
  
  end subroutine myquad2d 
  
  real(8) function H(x)
    implicit none
    !real ( kind = 8 ), external :: f
    real(8) a,b,ans
    integer ( kind = 4 ), parameter :: limit = 500
    real ( kind = 8 ) abserr
    real ( kind = 8 ), parameter :: epsabs = 0.0D+00
    real ( kind = 8 ), parameter :: epsrel = 0.001D+00
    integer ( kind = 4 ) ier
    integer ( kind = 4 ) last
    integer ( kind = 4 ) neval
    !%%%%%%%%%%%%%%  same  
    integer ( kind = 4 ), parameter :: lenw = 4 * limit
    integer ( kind = 4 ) iwork(limit)   
    real ( kind = 8 ) work(lenw)
    integer ( kind = 4 ), parameter :: key = 6
    !%%%%%%%%%%%%%%  different
    real(8) x,xx
    common /groupx/ xx
    
    xx=x
    a=p1(x)
    b=p2(x)
    call dqag ( f, a, b, epsabs, epsrel, key, ans, abserr, neval, ier, &
      limit, lenw, last, iwork, work )
    H=ans
  end function
  
  real(8) function f(y)
    implicit none
    real(8),external :: p
    real(8) x,y
    common /groupx/ x 
    
    f=p3(x,y)  
  end function

end module myquad
!***********************                 ***********************************
!                       end module myquad
!%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  
  
  
  
  
  
  
  
  
  

























