"""
Tests for convert utilities.
"""

import unittest

import convert

FREEMARKER_BASIC_HTML = """
<html>
  <div>
    <p>
      Hello, World!
    </p>
  </div>
</html>
"""

EXPECTED_DJANGO_BASIC_HTML = """
<html>
  <div>
    <p>
      Hello, World!
    </p>
  </div>
</html>
"""

class TestConvert(unittest.TestCase):
    
    def testBasicConvert(self):
        """ Tests conversion with no tokens are macros. """
        output = convert.freemarker_to_django(FREEMARKER_BASIC_HTML)
        self.assertEquals(EXPECTED_DJANGO_BASIC_HTML, output)
        
if __name__ == '__main__':
    unittest.main()
