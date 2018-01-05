#!/usr/bin/env python
import os
from setuptools import setup, Extension

setup(
    setup_requires=['setuptools>=30.3'],
    package_dir={  # FIXME: wait for https://github.com/pypa/setuptools/issues/1136
        '': 'src',
    },
    ext_modules=[
        Extension(
            name=str('zbarlight._zbarlight'),
            sources=[str('src/zbarlight/_zbarlight.c')],
            extra_compile_args=['-std=c99'],
            libraries=['zbar'],
            optional=os.environ.get('READTHEDOCS', False),  # Do not build on Read the Docs
        ),
    ],
)
