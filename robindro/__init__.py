#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
import robindro.splash


def _real_main(argv=None):
    robindro.splash.show()


def main(argv=None):
    try:
        _real_main(argv)
    except Exception:
        sys.exit('ERROR: fixed output name but more than one file to download')
    except KeyboardInterrupt:
        sys.exit('\nERROR: Interrupted by user')


__all__ = ['main']


# PRIVATE
def print_splash():
    string = """
88888888888888888888888888888888888888888888888888888888888888888888888888888
88888888888888888888888888888888888888888888888888888888888888888888888888888

                    .o8        o8o                    .o8
                   "888        `"'                   "888
oooo d8b  .ooooo.   888oooo.  oooo  ooo. .oo.    .oooo888  oooo d8b  .ooooo.
`888""8P d88' `88b  d88' `88b `888  `888P"Y88b  d88' `888  `888""8P d88' `88b
 888     888   888  888   888  888   888   888  888   888   888     888   888
 888     888   888  888   888  888   888   888  888   888   888     888   888
d888b    `Y8bod8P'  `Y8bod8P' o888o o888o o888o `Y8bod88P" d888b    `Y8bod8P'

88888888888888888888888888888888888888888888888888888888888888888888888888888
88888888888888888888888888888888888888888888888888888888888888888888888888888
"""
    print(string)
