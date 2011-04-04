"""
Generator for templatetags for a given macro.
"""

TEMPLATE = """from django import template

from base import matched_inclusion_tag

register = template.Library()

@matched_inclusion_tag(register, '%(macro_name)s.html')
def %(macro_name)s(%(formatted_kwargs)s):
    return {
%(formatted_map)s
        }
"""

MAP_INDENT = 8

class Generator(object):
    """
    Wrapper object for info abot the template tag that we are generating.
    """
    
    def __init__(self, macro_name, parameters_map):
        """
        @macro_name - The name of the macro the template tag is being formatted for.
        @parameters_map - Map of parameter names to default values.
                          (Actually a list of tuples so that we can emulate an ordered dict,
                          since Jython is at Python 2.5)
        """
        self.macro_name = macro_name
        self.parameters_map = parameters_map

    def _format_kwargs(self):
        values_map = []

        for key, _value in self.parameters_map:
            if _value == False:
                value = 'False'
            elif _value == True:
                value = 'True'
            elif _value == '':
                value = "''"
            else:
                value = "'%s'" % _value

            values_map.append((key, value))

        return ", ".join(["%s=%s" % (key, value) for key, value in values_map])

    def _format_map(self):
        return "\n".join(["%(indent)s'%(key)s': %(key)s," % {
                    'indent': MAP_INDENT * ' ',
                    'key': key,
                    } for key, value in self.parameters_map])

    def render(self):
        return TEMPLATE % {
            'macro_name': self.macro_name,
            'formatted_kwargs': self._format_kwargs(),
            'formatted_map': self._format_map(),
            }
