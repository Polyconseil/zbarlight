#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import io
import os
import os.path
import re

from setuptools import setup, find_packages, Extension

PACKAGE = 'zbarlight'


def _open(*file_path):
    here = os.path.abspath(os.path.dirname(__file__))
    return io.open(os.path.join(here, *file_path), 'r', encoding='utf-8')


def get_version(package):
    version_pattern = re.compile(r"^__version__ = [\"']([\w_.-]+)[\"']$", re.MULTILINE)
    with _open(*(package.split('.') + ['__init__.py'])) as version_file:
        matched = version_pattern.search(version_file.read())
    return matched.groups()[0]


def get_long_description():
    with _open('README.rst') as readme_file:
        return readme_file.read()


REQUIREMENTS = [
    'Pillow',
]

setup(
    name=PACKAGE,
    version=get_version(PACKAGE),
    description="A simple zbar wrapper",
    long_description=get_long_description(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: C',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering :: Image Recognition',
    ],
    keywords=['zbar', 'QR code reader'],
    author='Polyconseil',
    author_email='opensource+%s@polyconseil.fr' % PACKAGE,
    url='https://github.com/Polyconseil/%s/' % PACKAGE,
    license='BSD',
    packages=find_packages(exclude=['docs', 'tests']),
    ext_modules=[
        Extension(
            str('zbarlight._zbarlight'),
            [str('zbarlight/_zbarlight.c')],
            extra_compile_args=['-std=c99'],
            libraries=['zbar'],
        ),
    ],
    include_package_data=True,
    zip_safe=False,
    setup_requires=[
        'setuptools',
    ],
    install_requires=REQUIREMENTS,
    tests_require=REQUIREMENTS + [
        'docutils',
        'Sphinx',
        'sphinx_rtd_theme',
    ],
    test_suite='tests'
)
