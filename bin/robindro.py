#!/usr/bin/env python
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

import os, sys

try:
    import _preamble
except ImportError:
    sys.exc_clear()

sys.path.insert(0, os.path.abspath(os.getcwd()))

def run():
    print("To be implemented")
