#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
from setuptools import setup, find_packages


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()


with open("README.md") as f:
    readme = f.read()

# Convert markdown to rst
try:
    from pypandoc import convert

    long_description = convert("README.md", "rst")
except:  # NOQA
    long_description = ""

version = ""
with open("wagtail_text_to_speech/__init__.py", "r") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)

setup(
    name="wagtail_text_to_speech",
    version=version,
    description=(
        "Create speech version of Wagtail article"
    ),  # NOQA
    long_description=long_description,
    author="mattlinares",
    author_email="matthew.linares@opendemocracy.net",
    url="https://github.com/marteinn/wagtail-alt-generator",
    packages=find_packages(
        exclude=("*.tests", "*.tests.*", "tests.*", "tests", "example*")
    ),
    include_package_data=True,
    install_requires=["requests", "wagtail>=1.12"],
    license="MIT",
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: Speech Synthesis",
        "Framework :: Django",
        "Topic :: Utilities",
    ],
)
