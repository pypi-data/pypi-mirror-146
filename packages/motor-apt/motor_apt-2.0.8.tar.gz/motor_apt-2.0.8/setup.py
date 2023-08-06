#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on April 17, 2015

Copyright Alpes Lasers SA, Neuchatel, Switzerland, 2015

@author: juraj
"""

from setuptools import setup

setup(
    setup_requires=['pbr'],
    pbr=True,
    test_suite = "motor_apt.tests"
)