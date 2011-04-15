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
        ('bold2', '', '<b>{{ nested }}</b>'),
        ('condition', '', '{% if True %}TRUTH{% endif %}'),
        ('recursion', '', '{% recursion %}'),
        ('nesting', '', '{% nesting %}woa{% endnesting %}'),
        ('withArgs', 'x', '{% withArgs 1 %}'),
        ('varArgs', 'x', '{% withArgs x %}'),
        ('manyStrings', 'x y', '{% withArgs x|add:" "|add:y %}'),
        ]),
    ('freemarker_boolean_translations.ftl', [
        ('not', '', '{% if not True %}y{% endif %}'),
        ('length', '', '{% if str %}y{% endif %}'),
        ('length2', '', '{% if str %}y{% endif %}'),
        ('truth', '', '{% if bool %}y{% endif %}'),
        ('truth2', '', '{% if bool %}y{% endif %}'),
        ('has_content', '', '{% if str %}y{% endif %}'),
        ('equals', '', '{% if str == "123" %}y{% endif %}'),
        ]),
    ('freemarker_arguments.ftl', [
        ('basic', 'a b', 'x'),
        ('defaults', 'a=1 b=2', 'x'),
        ('booldefault', 'x=True y=False', 'x'),
        ('slashes', 'enctype="application/x-www-form-urlencoded"', 'x'),
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
