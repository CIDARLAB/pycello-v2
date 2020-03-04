from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pycello",
    version = "2.0.0",
    author = "Timothy Jones",
    author_email = "jonests@bu.edu",
    description = "A Python module for processing Cello v2 inputs and outputs, namely the netlist and UCF.",
    license = "GPLv3",
    keywords = "cello cellular-logic synthetic-biology",
    url = "https://github.com/CIDARLAB/pycello-v2",
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
