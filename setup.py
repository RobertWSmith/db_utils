# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 19:40:41 2015

@author: Robert Smith
"""

import setuptools as st
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

st.setup(
    name = "db_utils",
    version = "0.0.1",
    packages = st.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests", "*.egg-info"]),
    author = "Robert Smith",
    author_email = "rob_smith@goodyear.com",
    description = "utilities for simplifying database operations",
    install_requires = ["pyodbc>=3.0.7", "pywin32>=219"],
    test_suite = 'tests'
)
