# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import pkg_resources
import sphinx_rtd_theme


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
