"""
Tests for convert utilities.
"""

import os
import unittest

import convert

RESOURCE_DIR = os.path.join(os.path.dirname(__file__), 'resources')

FREEMARKER_BASIC_HTML_NAME = 'freemarker_basic_html.ftl'

DJANGO_BASIC_HTML_NAME = 'django_basic_html.html'

FREEMARKER_BASIC_VARIABLE_NAME = 'freemarker_basic_variable.ftl'

DJANGO_BASIC_VARIABLE_NAME = 'django_basic_variable.html'

class TestConvert(unittest.TestCase):
    
    def testBasicConvert(self):
        """ Tests conversion with no tokens are macros. """
        template = convert.get_template(os.path.join(RESOURCE_DIR, FREEMARKER_BASIC_HTML_NAME))
        output = convert.freemarker_to_django(template)

        f = open(os.path.join(RESOURCE_DIR, DJANGO_BASIC_HTML_NAME))
        expected = f.read()
        f.close()

        self.assertEquals(expected, output)

    def testConvertBasicVariable(self):
        """ Tests conversion of variable to something that Django can understand. """
        template = convert.get_template(os.path.join(RESOURCE_DIR, FREEMARKER_BASIC_VARIABLE_NAME))
        output = convert.freemarker_to_django(template)
        f = open(os.path.join(RESOURCE_DIR, DJANGO_BASIC_VARIABLE_NAME))
        expected = f.read()
        f.close()
        self.assertEquals(expected, output)
        
if __name__ == '__main__':
    unittest.main()
