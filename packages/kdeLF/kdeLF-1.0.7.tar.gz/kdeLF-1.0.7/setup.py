#!/usr/bin/env python3


try:
    import setuptools
except ImportError:
    pass

description = 'A flexible method for estimating luminosity functions via Kernel Density Estimation'

with open("README.md", "r") as fh:
    """ load package description from readme file """
    long_description = fh.read()


def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('kdeLF',parent_package,top_path)

    # Fortran extension
    config.add_extension(name = 'kde_fortran',
                         sources = ['kdeLF/mod_dqag_dqags.f90', 'kdeLF/quad2d.f90', 'kdeLF/kdeLF.f90'],
                         extra_compile_args=['-fopenmp'],
                         extra_link_args=['-liomp5'],
                         )
    return config

if __name__ == "__main__":
    from numpy.distutils.core import setup
    setup(configuration=configuration,
            packages=['kdeLF'],
            version="1.0.7",
            description=description, 
            long_description=long_description,    
            long_description_content_type="text/markdown",
            author = 'Zunli Yuan',
            author_email = 'yzl@hunnu.edu.cn',
            maintainer="Wenjie Wang",
            maintainer_email="wangwenjie327@foxmail.com",
            url = 'https://github.com/yunzunli/kdeLF',
            include_package_data=True,
            package_data={'kdeLF': ['examples/data/*.dat']},
            license='MIT',
            install_requires=[
      			'numpy >= 1.13',
      			'scipy',
      			'astropy',
      			'emcee',
      			'matplotlib',
      			'h5py',
      			'corner',
      			'tqdm',
      			],
            python_requires=">=3.6")





