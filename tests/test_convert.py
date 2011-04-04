"""
Tests for convert utilities.
"""

import os
import unittest

import convert
from test_utils import resource, read_file, BaseTest

FREEMARKER_BASIC_HTML_NAME = 'freemarker_basic_html.ftl'

DJANGO_BASIC_HTML_NAME = 'django_basic_html.html'

FREEMARKER_BASIC_VARIABLE_NAME = 'freemarker_basic_variable.ftl'

DJANGO_BASIC_VARIABLE_NAME = 'django_basic_variable.html'

FREEMARKER_BASIC_COMMENT_NAME = 'freemarker_basic_comment.ftl'

DJANGO_BASIC_COMMENT_NAME = 'django_basic_comment.html'

class TestConvert(BaseTest):
    def testBasicConvert(self):
        """ Tests conversion with no tokens are macros. """
        template = convert.get_template(resource(FREEMARKER_BASIC_HTML_NAME))
        output = convert.freemarker_to_django(template)

        expected = read_file(DJANGO_BASIC_HTML_NAME)
        self.assertEqualsStr(expected, output.replace('\r', ''))

    def testConvertBasicVariable(self):
        """ Tests conversion of variable to something that Django can understand. """
        template = convert.get_template(resource(FREEMARKER_BASIC_VARIABLE_NAME))
        output = convert.freemarker_to_django(template)
        expected = read_file(DJANGO_BASIC_VARIABLE_NAME)
        self.assertEqualsStr(expected, output)

    def testConvertBasicVariable(self):
        """ Tests conversion of variable to something that Django can understand. """
        template = convert.get_template(resource(FREEMARKER_BASIC_COMMENT_NAME))
        output = convert.freemarker_to_django(template)
        expected = read_file(DJANGO_BASIC_COMMENT_NAME)
        self.assertEqualsStr(expected, output)
        
if __name__ == '__main__':
    unittest.main()
