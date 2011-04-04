"""
A converter that translates macros to django templates
"""
import os
import re

import freemarker
import java
import django

import convert

class MacroConsumer(object):
    """
    Consumes a Freemarker template with macros, and breaks it into three
    parts: its name, arguments/defaults, and a Django template string for
    the equivalent tag.

    Example:
    consumer = MacroConsumer(template)
    for macro_name, macro in consumer.macros.items():
        args, template = macro
        print "Macro %(macro_name)s takes arguments %(args)s:" % locals()
        print template
    """

    def __init__(self, template):
        macro_nodes, comments = get_macros_and_comments(template.rootTreeNode)
        self.comments = comments
        self.macros = {}
        for macro in macro_nodes:
            # macro.argumentNames works fine, but macro.args is private,
            # so we have to hack around that fact
            name, args = convert.ARGS_RE.match(str(macro)).groups()
            self.macros[name] = (
                    self.convert_args(args.strip()),
                    convert.freemarker_nodes_to_django(macro.children()))

    def convert_args(self, args):
        return args.replace('true', 'True').replace('false', 'False')
        
def get_macros_and_comments(root):
    macros = []
    comments = []

    queue = [root]
    while queue:
        node = queue.pop(0)
        cls = node.__class__
        if cls == freemarker.core.Macro:
            macros.append(node)
        elif cls == freemarker.core.Comment:
            comments.append(node)
        else:
            # discard the node
            queue.extend(node.children())

    return macros, comments
