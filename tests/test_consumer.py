"""
Tests for the macro consumer
"""

import os
import unittest

from test_utils import get_template, BaseTest
from macro_consumer import MacroConsumer

TESTS = [
    # (file, [(macro_name, args, template) ...])
    ('freemarker_elements.ftl', [
        ('bold', '', '<b>{{ nested }}</b>'),
        ]),
        ]


class TestConsumer(BaseTest):
    def test_all(self):
        for ftl_filename, macros in TESTS:
            consumer = MacroConsumer(get_template(ftl_filename))
            found_macros = set(consumer.macros.keys())
            for name, args, template in macros:
                assert name in consumer.macros, "Missed macro %s" % name
                found_macros = found_macros ^ set([name])

                actual_args, actual_template = consumer.macros[name]
                self.assertEqualsStr(args, actual_args)
                self.assertEqualsStr(template, actual_template)
            assert not found_macros, "Found unexpected macros: %s" % \
                    ', '.join(found_macros)

if __name__ == '__main__':
    unittest.main()