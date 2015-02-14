#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os.path
import warnings
import sys

try:
    from setuptools import setup
    setuptools_available = True
except ImportError:
    from distutils.core import setup
    setuptools_available = False

"""
try:
    # This will create an exe that needs Microsoft Visual C++ 2008
    # Redistributable Package
    import py2exe
except ImportError:
    if len(sys.argv) >= 2 and sys.argv[1] == 'py2exe':
        print("Cannot import py2exe", file=sys.stderr)
        exit(1)

py2exe_options = {
    "bundle_files": 1,
    "compressed": 1,
    "optimize": 2,
    "dist_dir": '.',
    "dll_excludes": ['w9xpopen.exe'],
}

py2exe_console = [{
    "script": "./robindro/__main__.py",
    "dest_base": "robindro",
}]

py2exe_params = {
    'console': py2exe_console,
    'options': {"py2exe": py2exe_options},
    'zipfile': None
}
"""

if len(sys.argv) >= 2 and sys.argv[1] == 'py2exe':
    params = py2exe_params
else:
    """
    files_spec = [
        ('etc/bash_completion.d', ['robindro.bash-completion']),
        ('etc/fish/completions', ['robindro.fish']),
        ('share/doc/robindro', ['README.md']),
        ('share/man/man1', ['robindro.1'])
    ]
    """
    files_spec = []
    root = os.path.dirname(os.path.abspath(__file__))
    data_files = []

    for dirname, files in files_spec:
        resfiles = []
        for fn in files:
            if not os.path.exists(fn):
                warnings.warn('Skipping file %s since it is not present. Type  make  to build all automatically generated files.' % fn)
            else:
                resfiles.append(fn)
        data_files.append((dirname, resfiles))

    params = {
        'data_files': data_files,
    }

    if setuptools_available:
        params['entry_points'] = {'console_scripts': ['robindro = robindro:main']}
    else:
        params['scripts'] = ['bin/robindro']

# Get the version from youtube_dl/version.py without importing the package
exec(compile(open('robindro/version.py').read(),
             'robindro/version.py', 'exec'))

setup(
    name='robindro',
    version=__version__,
    description='Rabindranath Tagore info organizer',
    long_description='Small command-line program to download transations and '
    ' song metadata for Rabindranath Tagore\'s works from various websites.',
    url='https://github.com/execat/robindro',
    author='Anuj More',
    author_email='anujmorex+robindro@gmail.com',
    maintainer='Anuj More',
    maintainer_email='anujmorex+robindro@gmail.com',
    packages=[
        'robindro',
        'robindro.extractor', 'robindro.downloader',
        'robindro.postprocessor'],

    # Provokes warning on most systems (why?!)
    # test_suite = 'nose.collector',
    # test_requires = ['nosetest'],

    # From https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],

    **params
)
