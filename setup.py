#!/usr/bin/env python

from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys
import io

import pychatbot


def read(filename):
    with open(filename) as file:
        return file.read()


def get_requirements(req):
    if req.startswith('-r'):
        for subreq in get_requirements(req.split()[1]):
            yield subreq
    else:
        yield req


setup(
    name='pychatbot',
    version=pychatbot.__version__,
    author=pychatbot.__author__,
    author_email=pychatbot.__email__,
    description='A lib to create chatbots',
    url='http://github.com/greenkey/pychatbot/',
    packages=['pychatbot', 'pychatbot.endpoints'],
    include_package_data=True,
    platforms='any',
    keywords=['chatbot', 'telegram'],
    tests_require=get_requirements('-r requirements-dev.txt'),
    install_requires=get_requirements('-r requirements.txt'),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
