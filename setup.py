#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from setuptools import setup, find_packages

REQUIREMENTS = [
    'python_version >= "3"',
]
def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version


__version__ = find_version('pc-bot/__init__.py')


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


setup(
    name='pc-bot',
    version=__version__,
    description='Telegram bot for managing PC remotely.',
    long_description=read("README.md"),
    license='MIT',
    author='Nikolai Oplachko',
    author_email='magnickolas@gmail.com',
    url='https://github.com/magnickolas/pc-bot',
    install_requires=REQUIREMENTS,
    packages=find_packages(exclude=('test*', )),
    include_package_data=True,
    zip_safe=False,
    package_data={},
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Topic :: Home Automation",
    ],
    keywords=["pc", "telegram", "bot"]
)
