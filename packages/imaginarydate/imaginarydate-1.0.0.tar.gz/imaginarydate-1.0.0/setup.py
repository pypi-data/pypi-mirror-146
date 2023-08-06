#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# import lib
import imaginarydate

# description
long_description = open('README.md').read()
# long_description += "\n\n"
# long_description += open('CHANGELOG').read()

# setup
setup(
    name='imaginarydate',
    version=imaginarydate.__version__,

    packages=find_packages(),

    author="MickBad",
    author_email="prog@mickbad.com",
    description="Fast imaginary calendar for RPG or other",

    long_description=long_description,
    long_description_content_type='text/markdown',

    install_requires=[],

    # activate MANIFEST.in
    include_package_data=True,

    # github source
    url='https://github.com/mickbad/pyImaginaryDate',

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],

    license="MIT",

    keywords="development tools calendar RPG",
)
