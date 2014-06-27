try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

from pip.req import parse_requirements

import os
import sys

# disables creation of .DS_Store files inside tarballs on Mac OS X
os.environ['COPY_EXTENDED_ATTRIBUTES_DISABLE'] = 'true'
os.environ['COPYFILE_DISABLE'] = 'true'

import windml

def extract_package_name(requirement):
    return str(requirement.req).replace('-', '_').split('==')[0]

def find_requirements(req_file='requirements.txt'):
    return [extract_package_name(r) for r in parse_requirements(req_file)]

DESCRIPTION = 'The windML framework provides an easy-to-use access to wind data '\
    'sources within the Python world, building upon numpy, scipy, sklearn, and '\
    'matplotlib. As a machine learning module, it provides versatile tools for '\
    'various learning tasks like time-series prediction, classification, clustering, '\
    'dimensionality reduction, and related tasks.'

setup(
    author=windml.__author__,
    author_email=windml.__author_email__,
classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Environment :: X11 Applications',
    'Environment :: X11 Applications :: GTK',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: MacOS',
    'Operating System :: POSIX',
    'Operating System :: POSIX :: Linux',
    'Operating System :: Unix',
    'Programming Language :: Python',
    'Topic :: Education',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Scientific/Engineering :: Atmospheric Science',
],
    data_files=[],
    description=DESCRIPTION,
    ext_modules=[],
    install_requires=find_requirements('requirements.txt'),
    license=windml.__license__,
    long_description=DESCRIPTION,
    name='windml',
    packages=find_packages(),
    package_data={},
    setup_requires=[],
    url=windml.__url__,
    use_2to3=(sys.version_info >= (3,)),
    version=windml.__version__,
)

