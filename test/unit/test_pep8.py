import os
import os.path
import unittest
import pep8

# ignore stuff in virtualenvs or version control directories
ignore_patterns = ('.svn', '.git', 'bin', 'ENV', 'lib' + os.sep + 'python')


def ignore(dir):
    """Should the directory be ignored?"""
    for pattern in ignore_patterns:
        if pattern in dir:
            return True
    return False


class TestPep8(unittest.TestCase):

    """Run PEP8 on all files in this directory and subdirectories."""
    def test_pep8(self):
        style = pep8.StyleGuide(quiet=False)
        style.options.max_line_length = 140  # because it isn't 1928 anymore
        ignore_codes = (
            'E402',  # module level import not at top of file
        )
        style.options.ignore = style.options.ignore and ignore_codes

        errors = 0
        for root, _, files in os.walk('../../src'):
            if ignore(root):
                continue

            python_files = ["%s/%s" % (root, f) for f in files if f.endswith('.py')]

            result = style.check_files(python_files)
            errors += result.total_errors

        self.assertEqual(errors, 0, 'PEP8 style errors: %d' % errors)