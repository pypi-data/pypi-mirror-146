import pathlib

from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
# This call to setup() does all the work

setup(
    name='ftpc',
    version='0.0.5',
    license='MIT',
    author="Baxromov Shahzodbek",
    packages=find_packages('ftpc'),
    package_dir={'': 'ftpc'},
    keywords='example project',
    description='You should install -> sudo apt-get install default-jre libreoffice-java-common to Ubuntu',
)