#!/usr/bin/env python

import re
from setuptools import setup


def fread(filepath):
    with open(filepath) as f:
        return f.read()


def version():
    content = fread('kiqpoliveserver/__init__.py')
    pattern = r"__version__ = '([0-9\.dev]*)'"
    m = re.findall(pattern, content)
    return m[0]


setup(
    name='kiqpolivereload',
    version=version(),
    author='kiqpo',
    author_email='shajin.sha10@gmail.com',
    url='https://github.com/kiqpo',
    packages=['kiqpoliveserver'],
    description='Python live reload server build as part of kiqpo',
    long_description_content_type='text/markdown',
    long_description=fread('README.md'),
    install_requires=[
        'tornado',
    ],
    license='MTI',
    include_package_data=True,
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment :: Mozilla',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Debuggers',
    ]
)
