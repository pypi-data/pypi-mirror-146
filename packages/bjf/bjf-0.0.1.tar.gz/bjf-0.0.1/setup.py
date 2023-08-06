from setuptools import setup, find_packages
import codecs
import os

install_requires = [
    "click==8.1.0",
]


here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


VERSION = "0.0.1"

setup(
    name="bjf",
    version=VERSION,
    description="Simple in-place JSON Formatter",
    author="rohan winsor",
    long_description_content_type="text/markdown",
    long_description=long_description,
    author_email="rohan.w.charles@gmail.com",
    url="https://github.com/rohanwinsor/bjf",
    install_requires=install_requires,
    packages=find_packages(),
    license="MIT",
)
