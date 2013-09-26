#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import clime

setup(

    name = 'clime',
    version = clime.__version__,
    description = 'Convert functions into multi-command program breezily.',
    long_description = open('README.rst').read(),

    author = 'Mosky',
    url = 'http://clime.mosky.tw/',
    author_email = 'mosky.tw@gmail.com',
    license = 'MIT',
    platforms = 'any',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    packages = find_packages(),

    entry_points = {
        'console_scripts': [
            'clime = clime.__main__:run'
        ]
    }

)
