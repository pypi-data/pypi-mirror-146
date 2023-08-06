# coding: utf-8

from pathlib import Path

from setuptools import setup, find_packages

NAME = "osparcAPIcontrol"
VERSION = "0.0.6"
README = Path("README.md").read_text()

setup(
    name=NAME,
    version=VERSION,
    description=f"tools to interact with osparc API",
    author="Konohana",
    author_email="msteiner@itis.swiss",
    url="https://git.speag.com/msteiner/osparcapicontrol.git",
    keywords=["OpenAPI", "OpenAPI-Generator", "osparc", "web API"],
    packages=find_packages(exclude=["test", "tests"]),
    install_requires=['osparc', 'tenacity'],
    include_package_data=True,
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
)
