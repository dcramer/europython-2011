#!/usr/bin/env python
# setup.py
from setuptools import setup, find_packages

setup(
    name='eurotwitter',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Django==1.3',
        'nydus',
    ],
    package_data={
        'eurotwitter': [
            'static/*.*',
            'templates/*.*'
        ]
    },
)