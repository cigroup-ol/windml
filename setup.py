from setuptools import setup, find_packages

setup(name='windml',
      packages=find_packages(exclude=['examples', 'tests']),
      include_package_data=True)
