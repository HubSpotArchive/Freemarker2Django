"""
Some helper utils for other unit tests
"""

from __future__ import with_statement

import os
import convert
from unittest import TestCase

RESOURCE_DIR = os.path.join(os.path.dirname(__file__), 'resources')

def resource(filename):
    return os.path.join(RESOURCE_DIR, filename)

def get_template(filename):
    return convert.get_template(resource(filename))

def read_file(filename):
    with open(resource(filename)) as f:
        contents = f.read()

    return contents

class BaseTest(TestCase):
    def assertEqualsStr(self, expected, actual):
        """Some Windows machines just like to mess things up for everyone"""
        self.assertEquals(expected.replace('\r', '').strip(),
                          actual.replace('\r', '').strip())
