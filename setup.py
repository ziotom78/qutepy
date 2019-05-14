# -*- encoding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qutepy",
    version="0.0.1",
    author="Maurizio Tomasi",
    author_email="ziotom78@gmail.com",
    description="Python package to access QuteDB via its REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ziotom78/qutepy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
