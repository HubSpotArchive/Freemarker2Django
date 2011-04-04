"""
Tests for convert utilities.
"""

import os
import unittest

import templatetags
from test_utils import resource, read_file, BaseTest

EXAMPLE_TEMPLATE_TAGS_NAME = 'example_templatetags.py'

EXAMPLE_TEMPLATE_TAGS_PARAMS_MAP = [
    ('type', 'basic'),
    ('size', 'small'),
    ('next', False),
    ('enabled', True),
    ('id', ''),
    ('css_class', ''), 
    ('href', '#'),
    ]

class TestTemplateTagsGenerator(BaseTest):

    def test_basic_generator(self):
        """ Tests conversion with no tokens are macros. """
        generator = templatetags.generator.Generator('example', EXAMPLE_TEMPLATE_TAGS_PARAMS_MAP)

        expected = read_file(EXAMPLE_TEMPLATE_TAGS_NAME)
        self.assertEqualsStr(expected, generator.render())

if __name__ == '__main__':
    unittest.main()
