# Copyright (c) Anuj More
# See LICENSE.md for details

"""
Provides Robindro version information
"""

# Version is a human-readable version number. Use http://semver.org/ to decide
# a proper version while editing the version number

def version_string(info):
    product_version = '.'.join(info[0:3])
    if len(info) == 4:
        return product_version + "-" + info[3]
    return product_version

__version_info__ = ('0', '1', '0', 'alpha.1')
__version__ = version_string(__version_info__)
