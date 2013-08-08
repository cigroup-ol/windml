.. _dependencies:

Dependencies
============

We currently use Python 2.7.X, since some depencencies are not yet fit for Python 3.

For Ubuntu LTS 12.04
--------------------

System-Packages
+++++++++++++++

Git 1.7.9.5-1 (version is not so important)
Python 2.7.3 
Python-PIP 1.0-1 
Python-Setuptools 0.6.24 
G++ Toolchain 4.6 
GCC 4.6 Toolchain 
Python-Dev (Libpython 2.7) 
Libblas-Dev 1.2.20 
Liblapack-Dev 3.3.1-1 
GFortran-4.6 
Libfreetype6-dev-2.4.8-1 
Libpng12-dev 1.2.46 

::
  apt-get install git python2.7 python-dev python-pip g++-4.6 gcc-4.6 gfortran-4.6 libblas-dev liblapack-dev  libfreetype6-dev libping12-dev


Python Packages
+++++++++++++++

NumPy 1.7.1 (over numpy) 
SciPy 0.12.0 
SciKit-Learn 0.13.1 
Distribute 0.7.3 
Matplotlib 1.3.0 

::
  pip install numpy scipy scikit-learn distribute matplotlib

Maybe you want to do add the "--upgrade" option e.g. to the package "distribute". Or you want to install system wide via "sudo pip" instead of "pip".


Ubuntu 11.04 (natty)
------------

not yet fully documented.
We have some version issues, which maybe can be solved by re-installing new versions of some packages via pip.

To Build the documentation on natty
+++++++++++++++++++++++++++++++++++

 * Sphinx v1.2b1
 * playdoh
 * sklearn - which version? (when doing "make html" I get error with using module "sklearn"...)

  * "skilearn" 
  * "scikits.learn" 0.4 - 0.81? 
  *"scikit-learn"

::
  pip install --upgrade  sphinx playdoh

