"""
``pycello`` is a module that reads a netlist in the Cello v2 JSON format
into a Python class structure.
"""

import sys

__version__ = '2.0.0'

if not (sys.version_info.major == 3):
    raise ImportError("pycello requires Python 3")

del sys
