from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pycello",
    version = "0.0.1",
    author = "Timothy Jones",
    author_email = "tjones01@gmail.com",
    description = "A Python module for processing Cello2 inputs and outputs, namely the netlist and UCF.",
    license = "GPLv3",
    keywords = "cello cellular-logic synthetic-biology",
    url = "https://github.com/tim-tx/pycello",
    packages = find_packages(),
    install_requires = [
        "sympy>=1.5",
        "numpy>=1.17"
    ],
    long_description = read('README.org'),
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ]
)
