import pathlib

from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
# This call to setup() does all the work

setup(
    name="ftpc",
    version='0.0.1',
    author="Baxromov",
    description="Develop ftpc",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "file_to_pdf_converter"},
    packages=find_packages(where="file_to_pdf_converter"),
    python_requires=">=3.6",
    include_package_data=True,
    long_description_content_type="text/markdown",
    long_description="You should install -> sudo apt-get install default-jre libreoffice-java-common to Ubuntu",
)
