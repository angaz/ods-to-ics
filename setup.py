#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="eth-berlin-ics",
    version="0.0.1",
    # Modules to import from other scripts:
    packages=find_packages(),
    # Executables
    scripts=["main.py"],
)
