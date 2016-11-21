#!/bin/env python
"""
Setuptools file for pyrtorrent
"""
from setuptools import (
    setup,
    find_packages,
)

setup(
    name='pyrtorrent',
    author='marhag87',
    author_email='marhag87@gmail.com',
    url='https://github.com/marhag87/pyrtorrent',
    version='0.1.0',
    packages=find_packages(),
    license='WTFPL',
    description='rTorrent xmlrpc wrapper',
    long_description='rTorrent xmlrpc wrapper',
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
)
