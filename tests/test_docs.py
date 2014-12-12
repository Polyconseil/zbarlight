import os
import os.path
import shutil
import tempfile
import unittest

from docutils.core import publish_cmdline
from sphinx.cmdline import main as sphinx_cmdline


def test_rst(file_path):
    publish_cmdline(
        writer_name='null',
        argv=['--exit-status=1', '--report=1', file_path]
    )


def test_sphinx(doc_path):
    build_dir = tempfile.mkdtemp()
    return_code = sphinx_cmdline([
        'sphinx-build',
        '-W', '-n', '-q',
        '-b', 'html',
        '-d', os.path.join(build_dir, 'doctrees'),
        doc_path,
        os.path.join(build_dir, 'html')
    ])
    shutil.rmtree(build_dir)
    return return_code


class DocTestCase(unittest.TestCase):
    @staticmethod
    def relative_path(*args):
        return os.path.join(os.path.dirname(__file__), '..', *args)

    def test_readme(self):
        test_rst(self.relative_path('README.rst'))

    def test_changelog(self):
        test_rst(self.relative_path('ChangeLog.rst'))

    def test_docs(self):
        self.assertEqual(test_sphinx(self.relative_path('docs')), 0)
