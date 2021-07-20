#!/usr/bin/env python

__author__ = 'Ivan Kondov'
__copyright__ = 'Copyright 2020-2021, Karlsruhe Institute of Technology'
__email__ = 'ivan.kondov@kit.edu'
__maintainer__ = 'Ivan Kondov'

import os
import sys
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='fireworks_schema',
    version='1.0.1',
    description='JSON Schema for FireWorks',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ivan Kondov',
    author_email='ivan.kondov@kit.edu',
    url='https://github.com/ikondov/fireworks_schema',
    keywords=['workflow system', 'json schema', 'fireworks'],
    license='BSD-3-Clause License',
    packages=find_packages(),
    package_data={'fireworks_schema': ['schema/*.json'],
                  'fireworks_schema.tests': ['*.yaml', 'samples/*/*.json']},
    install_requires=['jsonschema>=3.2.0', 'fireworks>=1.9.7'],
    extras_require={},
    classifiers=['Programming Language :: Python',
                 'Development Status :: 4 - Beta',
                 'Intended Audience :: Science/Research',
                 'Intended Audience :: System Administrators',
                 'Intended Audience :: Information Technology',
                 'Operating System :: OS Independent',
                 'Topic :: Other/Nonlisted Topic',
                 'Topic :: Scientific/Engineering'],
    test_suite='nose.collector',
    tests_require=['nose'],
    python_requires='>=3.6',
)
