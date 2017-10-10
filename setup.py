from setuptools import setup, find_packages


from pip.req import parse_requirements
import uuid
import os
import sys
import windml

# disables creation of .DS_Store files inside tarballs on Mac OS X
os.environ['COPY_EXTENDED_ATTRIBUTES_DISABLE'] = 'true'
os.environ['COPYFILE_DISABLE'] = 'true'


rand_uuid = uuid.uuid1()


def extract_package_name(requirement):
    return str(requirement.req)
    # return str(requirement.req).replace('-', '_').split('==')[0]


def find_requirements(req_file='requirements.txt'):
    reqs = [extract_package_name(r) for r in parse_requirements(
        req_file, session=rand_uuid)]
    np = [pkg for pkg in reqs if pkg.startswith('numpy')]
    reqs.remove(np[0])
    return reqs


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


DESCRIPTION = """The windML framework provides an easy-to-use access to wind data
    sources within the Python world, building upon numpy, scipy, sklearn, and
    matplotlib. As a machine learning module, it provides versatile tools for
    various learning tasks like time-series prediction, classification, clustering,
    dimensionality reduction, and related tasks."""

setup(
    author=windml.__author__,
    author_email=windml.__author_email__,
    classifiers=[
        'Development Status :: 4 - Beta',
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
    dependency_links=['https://github.com/matplotlib/basemap/archive/v1.0.7rel.tar.gz'],
    license=windml.__license__,
    long_description=read('README.md'),
    name='windml',
    packages=find_packages(),
    package_data={},
    setup_requires=['numpy'],
    url=windml.__url__,
    use_2to3=(sys.version_info >= (3,)),
    version=windml.__version__,
)
