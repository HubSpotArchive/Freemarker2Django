"""
MacroConverter takes in a Freemarker template and separates it into macros
"""

class Macro(object):
    """Holds a macro's name, arguments, defaults and content"""
    def __init__(self, name, args, content):
        self.name = name
        self.args = args
        self.content = content

class MacroConverter(object):
    def __init__(self, template):
        self.template = template
        self.macros = set()
        self.load_macros()

    def load_macros(self):
        pass
