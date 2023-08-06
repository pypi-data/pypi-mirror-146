from __future__ import absolute_import
from __future__ import print_function
from setuptools import setup, find_packages
import distutils.text_file
from pathlib import Path
from typing import List

# Always prefer setuptools over distutils
import setuptools

def _parse_requirements(filename: str) -> List[str]:
    """Return requirements from requirements file."""
    # Ref: https://stackoverflow.com/a/42033122/
    return distutils.text_file.TextFile(filename=str(Path(__file__).with_name(filename))).readlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

print(find_packages())

setup(
    name='thingdl',
    version='1.1',
    packages=find_packages(),
    entry_points={
        "console_scripts": ["thingdl=thingdl.thingiverse_downloader:main"]
    },
    author="Sean Bailey",
    author_email="seanbailey518@gmail.com",
    description="This provides a utility to bulk download files from a thing in Thingiverse",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sean-bailey",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
install_requires=_parse_requirements('requirements.txt'),

)