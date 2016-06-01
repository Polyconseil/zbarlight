# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import os.path
try:
    from subprocess import check_output
except ImportError:
    def check_output(*popenargs, **kwargs):  # from python 2.7
        from subprocess import PIPE, Popen, CalledProcessError
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = Popen(stdout=PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise CalledProcessError(retcode, cmd, output=output)
        return output

import sphinx_rtd_theme

project = u'zbarlight'
copyright = u'2015, Polyconseil'

version = check_output(
    ['python', 'setup.py', '--version'],
    cwd=os.path.join(os.path.dirname(__file__), '..'),
).decode()
release = version

extensions = ['sphinx.ext.intersphinx', 'sphinx.ext.autodoc', 'sphinx.ext.napoleon']
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pillow': ('https://pillow.readthedocs.io/en/latest', None),
}

templates_path = []
source_suffix = '.rst'
master_doc = 'index'

pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = []
