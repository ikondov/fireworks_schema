#!/usr/bin/env python
import os
import sys
from setuptools import setup, find_packages

# module_dir = os.path.dirname(os.path.abspath(__file__))

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='fireworks_schema',
    version='2020.1',
    description='JSON Schema for FireWorks',
    long_description=long_description,
    author='Ivan Kondov',
    author_email='ivan.kondov@kit.edu',
    url='https://github.com/ikondov/fireworks_schema',
    keywords=['workflow system', 'json schema', 'fireworks'],
    license='BSD-3-Clause License',
    packages=find_packages(),
    package_data={},
    install_requires=['jsonschema>=3.2.0', 'fireworks>=1.9.6'],
    extras_require={},
    classifiers=['Programming Language :: Python',
                 'Development Status :: 4 - Beta',
                 'Intended Audience :: Science/Research',
                 'Intended Audience :: System Administrators',
                 'Intended Audience :: Information Technology',
                 'Operating System :: OS Independent',
                 'Topic :: Other/Nonlisted Topic',
                 'Topic :: Scientific/Engineering'],
    test_suite='tests',
    tests_require=['nose'],
    python_requires='>=3.6',
)
