#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='drf-negotiate',
    version='0.1',
    description='Negotiate (GSSAPI) authentication support for django-rest-framework',
    author='Alexander Dutton',
    author_email='code@alexdutton.co.uk',
    url='https://github.com/alexsdutton/drf-negotiate',
    packages=find_packages(),
    install_requires=['django', 'gssapi', 'djangorestframework']
)
