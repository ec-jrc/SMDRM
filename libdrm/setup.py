"""
SMDRM LIBDRM setup module.
"""


import setuptools
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")


setuptools.setup(
    name="libdrm",
    version='0.1.3',
    description="Common helper modules shared by the pipeline services",
    long_description=long_description,
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
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6, <3.9",
    install_requires=[
        "marshmallow",
        "pydantic",
        "pytz",
        "requests",
    ],
    project_urls={
        "Bug Reports": "https://github.com/panc86/smdrm/issues",
        "Kanban": "https://github.com/panc86/smdrm/projects/1",
        "Source": "https://github.com/panc86/smdrm/",
    },
)
