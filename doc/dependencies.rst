.. _dependencies:

Dependencies
============

The windML framework has been updated to support both Python 2.7.x and Python >=3.5.  In the following section the dependenices for Ubuntu are listed. For other operating systems,the dependencies will be specified in the future. Feel free to contribute other dependency notes. 

Ubuntu/Debian 
-------------

For Ubuntu/Debian, the following system packages and Python packages are required.

.. highlight:: none

System Packages
+++++++++++++++

    * Git
    * Python 2.7.x
    * pip 9.0-1
    * setuptools >=
    * G++ Toolchain >= 4.6
    * GCC 4.6 Toolchain
    * python-dev (libpython2.7)
    * libblas-dev 1.2.20
    * liblapack-dev 3.3.1-1
    * gfortran-4.6
    * libfreetype6-dev
    * libpng16-dev 

In order to install these packages run the following command as root user on your system: ::

  # apt-get install git python2.7 python-dev python-pip g++-4.6 gcc-4.6 \
    gfortran-4.6 libblas-dev liblapack-dev  libfreetype6-dev libpng16-dev

where python2.7 can (should ?) be swapped with python3 as needed.

MacOS 
-----

brew install pkg-config
brew install freetype
brew install libpng

Python Packages
+++++++++++++++

    * numpy >= 1.13.0
    * scipy >= 0.19.0
    * scikit-learn 0.19.0    
    * matplotlib >= 2.0.2 
    * basemap == 1.0.7
    * Pillow >= 4.2.1
    * six >=1.10.0
    * future

In order to install these packages run the following command as root user on your system: ::

  # pip install numpy scipy scikit-learn matplotlib six Pillow future.

  # pip install https://github.com/matplotlib/basemap/archive/v1.0.7rel.tar.gz

You may also use conda (recommended) in a separate environment if necessary.

  # conda install basemap=1.0.7 numpy scipy scikit-learn matplotlib six Pillow future


.. highlight:: python

