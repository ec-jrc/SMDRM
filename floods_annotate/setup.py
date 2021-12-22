"""Floods Annotate SMDRM ETL pipeline task."""

import os
from setuptools import setup, find_packages

def get_version():
    root = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(root, "VERSION.txt")) as v:
        version = v.read()
        return version

setup(
    name='src',
    version=get_version(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click~=8.0',
        'pandas~=1.3',
        'requests~=2.26',
    ],
    entry_points={
        'console_scripts': [
            'floods_annotate = src.floods_annotate:cli',
        ],
    },
)
