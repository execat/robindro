#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import setuptools
import sys

if os.path.exists('robindro'):
    sys.path.insert(0, '.')

version_file_path = os.path.join(
    os.path.dirname(__file__),
    'robindro',
    '_version.py'
    )

with open(version_file_path, 'r') as file_pointer:
    file_contents_string = file_pointer.read()
local_dict = {}
exec(file_contents_string, None, local_dict)
__version__ = local_dict['__version__']


description = 'Robindro is a crawler/scraper for Rabindranath Tagore\'s works'

long_description = '1'
long_description += ' 2'
long_description += ' 3.'

author = ['Anuj More']
author = ', '.join(author)

author_email = ['anujmorex+robindro@gmail.com']
author_email = ', '.join(author_email)

keywords = ['scraper', 'crawler', 'translation', 'literature']
keywords = ', '.join(keywords)

install_requires = ['pytest', 'nose', 'beautifulsoup4', 'requests']

setuptools.setup(
    author=author,
    author_email=author_email,
    description=description,
    entry_points={
        'console_scripts': [
            'robindro = bin.robindro:run_robindro',
        ]
    },
    include_package_data=True,
    install_requires=install_requires,
    keywords=keywords,
    license='GPL',
    long_description=long_description,
    name='Robindro',
    packages=('robindro', 'robindro.scripts', 'robindro.scraper'),
    platforms='Any',
    url='http://github.com/execat/robindro',
    version=__version__,
)
