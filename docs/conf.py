import importlib.metadata

project = "zbarlight"
copyright = "2014, Polyconseil"

version = importlib.metadata.version("zbarlight")
release = version

extensions = ["sphinx.ext.intersphinx", "sphinx.ext.autodoc", "sphinx.ext.napoleon"]
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pillow": ("https://pillow.readthedocs.io/en/latest", None),
}

templates_path = []
source_suffix = ".rst"
master_doc = "index"

pygments_style = "sphinx"
html_theme = "sphinx_rtd_theme"
html_static_path = []
