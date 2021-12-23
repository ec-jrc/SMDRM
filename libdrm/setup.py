"""SMDRM LIBDRM setup module."""

import os
from setuptools import find_packages, setup


def get_version():
    root = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(root, "VERSION.txt")) as v:
        version = v.read()
        return version


setup(
    name="libdrm",
    version=get_version(),
    description="Common helper modules shared by the pipeline services",
    long_description_content_type="text/markdown",
    url="https://github.com/panc86/smdrm",
    author="Emanuele Panizio",
    author_email="emanuele.panizio@ext.ec.europa.eu",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">3.7, <3.10",
    install_requires=[
        "pydantic~=1.8",
    ],
    project_urls={
        "Bug Reports": "https://github.com/panc86/smdrm/issues",
        "Kanban": "https://github.com/panc86/smdrm/projects/1",
        "Source": "https://github.com/panc86/smdrm",
    },
)
