# Copyright (c) Anuj More
# See LICENSE for details

"""
Robindro: the Robindronath scraper
"""

def _check_requirements():
    # Don't allow the user to run a version of Python we don't support
    import sys

    version = getattr(sys, "version_info", (0,))
    if version < (3, 0):
        required = "3.0"

_check_requirements()

# Setup version
# FIX
from robindro._version import version
__version__ = version.short()
