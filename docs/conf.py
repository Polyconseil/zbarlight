# -*- coding: utf-8 -*-
import os.path

import sphinx_rtd_theme

templates_path = []
source_suffix = '.rst'
master_doc = 'index'

project = u'zbarlight'
copyright = u'2014, Polyconseil'

with open(os.path.join(os.path.dirname(__file__), '..', 'VERSION')) as version_file:
    version = version_file.read().strip()
release = version

pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = []
