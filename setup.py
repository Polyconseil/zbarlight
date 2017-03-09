#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages, Extension


def read(file_path):
    with open(file_path) as fp:
        return fp.read()


setup(
    name='zbarlight',
    version='1.2',
    description="A simple zbar wrapper",
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: C',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Image Recognition',
    ],
    keywords=['zbar', 'QR code reader'],
    author='Polyconseil',
    author_email='opensource+zbarlight@polyconseil.fr',
    url='https://github.com/Polyconseil/zbarlight/',
    license='BSD',
    packages=find_packages(where='src', exclude=['docs', 'tests']),
    package_dir={'': str('src')},
    ext_modules=[
        Extension(
            name=str('zbarlight._zbarlight'),
            sources=[str('src/zbarlight/_zbarlight.c')],
            extra_compile_args=['-std=c99'],
            libraries=['zbar'],
            optional=os.environ.get('READTHEDOCS', False),  # Do not build on Read the Docs
        ),
    ],
    include_package_data=True,
    zip_safe=False,
    setup_requires=[
        'setuptools',
    ],
    install_requires=[
        'Pillow',
    ],
)
