#!/usr/bin/env python

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='KeywordListener',
    version='0.1.0',
    packages=find_packages(),
    install_requires=required,
    author='yuitest',
    license='BSD',
)
