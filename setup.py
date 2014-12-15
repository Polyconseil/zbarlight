#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import os.path

from setuptools import setup, find_packages, Extension


PACKAGE = 'zbarlight'

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'VERSION')) as version_file:
    VERSION = version_file.read().strip()
with open(os.path.join(here, 'README.rst')) as readme_file:
    README = readme_file.read()
with open(os.path.join(here, 'requirements-dev.txt')) as requirement_file:
    DEV_REQUIREMENTS = requirement_file.read().splitlines()

setup(
    name=PACKAGE,
    version=VERSION,
    description="A simple zbar wrapper",
    long_description=README,
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
    packages=find_packages(exclude=['docs']),
    ext_modules=[
        Extension('zbarlight', ['zbarlight.c'], libraries=['zbar']),
    ],
    include_package_data=True,
    zip_safe=False,
    setup_requires=[
        'setuptools',
    ],
    tests_require=DEV_REQUIREMENTS,
    test_suite='tests'
)
