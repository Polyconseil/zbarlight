# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import os
import sys

import pkg_resources
import sphinx_rtd_theme


class _Zbarlight(object):
    """
    Fake zbarlight C extension

    Should be updated when C extension change.
    """
    def zbar_code_scanner(self, *args):
        pass

    def version(self):
        pass

    @classmethod
    def monkey_patch(cls):
        """Monkey path zbarlight C extension on Read The Docs"""
        on_read_the_docs = os.environ.get('READTHEDOCS', False)
        if on_read_the_docs:
            sys.modules['zbarlight._zbarlight'] = cls


_Zbarlight.monkey_patch()

project = u'zbarlight'
copyright = u'2014, Polyconseil'

version = pkg_resources.get_distribution('zbarlight').version
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
