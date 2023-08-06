"""
A sample setup.py file for Python packages

https://docs.python.org/3/distutils/setupscript.html
"""

import os

from setuptools import setup

PROJECT_NAME = "vagueify"


def read(fname):
    """
    Helper to read README
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read().strip()


setup(
    name=PROJECT_NAME,
    version="0.0.1", 
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="",
    author="Danny McDonald",
    include_package_data=True,
    zip_safe=True,
    packages=[PROJECT_NAME],
    scripts=["bin/vague_all.sh"],
    extras_require={"sci": ["pandas"]},
    author_email="daniel.mcdonald@uzh.ch",
    license="MIT",
    keywords=["corpus", "linguistics", "nlp"],
    install_requires=[
        "nltk==3.5",
        "wheel==0.37.0"
    ],
)
