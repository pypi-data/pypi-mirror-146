# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="enhanced-ipython",
    version="0.0.1",
    description="An enhanced IPython shell.",
    long_description=readme,
    author="Alex Hutz",
    author_email="frostiiweeb@gmail.com",
    url="https://github.com/FrostiiWeeb/enhanced-ipython",
    license=license,
    packages=find_packages(exclude=("tests", "docs")),
    install_requires=requirements,
    entry_points={
        "console_scripts": ["eipython=eipython.__main__:run"],
    },
)
