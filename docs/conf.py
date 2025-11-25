import importlib.metadata
import os
import sys


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
        on_read_the_docs = os.environ.get("READTHEDOCS", False)
        if on_read_the_docs:
            sys.modules["zbarlight._zbarlight"] = cls


_Zbarlight.monkey_patch()

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
