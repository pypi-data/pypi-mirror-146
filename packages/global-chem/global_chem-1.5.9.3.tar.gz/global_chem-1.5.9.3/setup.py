#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# package setup
#
# ------------------------------------------------

# imports
# -------
import os

# config
# ------
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

TEST_REQUIREMENTS = [
    'pytest',
    'pytest-runner'
]

if os.path.exists('README.md'):
    long_description = open('README.md').read()
else:
    long_description = 'GlobalChem - Your Own Graph Network for Chemistry'

# exec
# ----
setup(
    name="global_chem",
    version="1.5.9.3",
    packages=find_packages(),
    license='MPL 2.0',
    author="Suliman Sharif",
    author_email="sharifsuliman1@gmail.com",
    url="https://www.github.com/Sulstice/global-chem",
    install_requires=[],
    long_description=long_description,
    long_description_content_type='text/markdown',
    extras_require={
        'extensions': ['global-chem-extensions'],
        'web_server': ['global-chem-extensions[web_server]'],
        'validation': ['global-chem-extensions[validation]'],
        'bioinformatics': ['global-chem-extensions[bioinformatics]'],
        'machine_learning': ['global-chem-extensions[machine_learning]'],
        'pdf': ['global-chem-extensions[pdf]'],

    },
    zip_safe=False,
    keywords='smiles molecules chemistry',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=TEST_REQUIREMENTS,
)
