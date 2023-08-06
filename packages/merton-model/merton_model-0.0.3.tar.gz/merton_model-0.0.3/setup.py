# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 13:24:07 2022

@author: charlesr
"""
from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name = 'merton_model',
    version = '0.0.3',
    author = 'Charles Rambo',
    author_email = 'charlesr@ssi-invest.com',
    description = 'Merton model distance to default',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
        ]
)

