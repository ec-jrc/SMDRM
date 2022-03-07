"""SMDRM LIBDRM setup module."""

import os
from setuptools import setup

here = os.path.dirname(os.path.abspath(__file__))

about = {}
with open(os.path.join(here, 'libdrm', '__version__.py')) as f:
    exec(f.read(), about)

packages = ["libdrm"]

install_requires = ["pydantic~=1.8", "pytest>=7"]

setup(
    name="libdrm",
    version=about["__version__"],
    description="Common helper modules shared by the pipeline services",
    long_description_content_type="text/markdown",
    url="https://github.com/ec-jrc/SMDRM",
    author="Emanuele Panizio",
    author_email="Emanuele.PANIZIO@ext.ec.europa.eu",
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
    package_dir={"libdrm": "libdrm"},
    packages=packages,
    python_requires=">=3.7, <3.9",
    install_requires=install_requires,
    project_urls={
        "Bug Reports": "https://github.com/ec-jrc/SMDRM/issues",
        "Source": "https://github.com/ec-jrc/SMDRM",
    },
)
