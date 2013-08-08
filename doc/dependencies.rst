.. _dependencies:

Dependencies
============

The windML framework is based on Python 2.7.x, since some depencencies are not
yet fit for Python 3.x.  In the following section the dependenices for Ubuntu
LTS 12.04 are listed. For other operating systems, the dependencies will be
specified in the future. Feel free to contribute other dependency notes. 

Ubuntu LTS 12.04
----------------

.. highlight:: none

System Packages
+++++++++++++++

    * Git
    * Python 2.7.3
    * Python-PIP 1.0-1
    * Python-Setuptools 0.6.24
    * G++ Toolchain 4.6
    * GCC 4.6 Toolchain
    * Python-Dev (Libpython 2.7)
    * Libblas-Dev 1.2.20
    * Liblapack-Dev 3.3.1-1
    * GFortran-4.6
    * Libfreetype6-dev-2.4.8-1
    * Libpng12-dev 1.2.46

In order to install these packages run the following command as root user on your system: ::

  # apt-get install git python2.7 python-dev python-pip g++-4.6 gcc-4.6 \
    gfortran-4.6 libblas-dev liblapack-dev  libfreetype6-dev libping12-dev

Python Packages
+++++++++++++++

    * NumPy 1.7.1
    * SciPy 0.12.0
    * SciKit-Learn 0.13.1
    * Distribute 0.7.3
    * Matplotlib 1.3.0 

    In order to install these packages run the following command as root user on your system: ::

  # pip install numpy scipy scikit-learn distribute matplotlib

Note: For the "distribute" python package the "--upgrade" option may be necessary.

.. highlight:: python

