from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.9'
DESCRIPTION = 'PloudOS API interactions like starting servers etc.'
LONG_DESCRIPTION = 'A PloudOS API wrapper that allows connecting to PloudOS accounts and interacting with the PloudOS API.'

# Setting up
setup(
    name="PloudosAPI",
    version=VERSION,
    author="TimMcCool",
    author_email="timmccool.scratch@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/x-rst",
    long_description=open('README.rst').read(),
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'ploudos', 'api', 'ploudos api', 'ploudos api wrapper'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
