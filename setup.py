#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/12/16 15:04
# @Author  : Cl0udG0d
# @File    : setup.py
# @Github: https://github.com/Cl0udG0d
import setuptools
from tookit.config import VERSION_NUM

with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fofa_hack",
    version=VERSION_NUM,
    author="Cl0udG0d",
    author_email="",
    description="fofa hack",  # 包简短的描述
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cl0udG0d/Fofa-hack",

    packages=setuptools.find_packages(),

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
