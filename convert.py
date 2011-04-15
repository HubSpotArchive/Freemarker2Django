"""
Utilities for converting Freemare templates to Django.
"""
import os
import re

import freemarker
import java

import django

ARGS_RE = re.compile( r"""
    <(?: (?: (?:\#macro|\#function) \s+) | @ )
        (?P<name>[^/\s>]+)
        (?P<args>
            (?:\s+ [^/\s>]+ (?:
                \s* = \s* (?:
                    (?: [^/\s>"']+ ) | (?: " [^"]* " ) | (?: ' [^']* ' )

                )
            )?)*
        ) \s* /? >
        """,
    re.VERBOSE | re.IGNORECASE)

def make_block(block_name, block_args = ''):
    """Make a django block, optionally with arguments"""
    if block_args:
        block_args = ' ' + block_args

    return ' '.join((
        django.template.base.BLOCK_TAG_START,
        block_name + block_args,
        django.template.base.BLOCK_TAG_END))


def wrap_nested_content(block_name, nested_content, block_args=''):
    """Wrap a string nested_content in a matched block"""
    start = make_block('%s%s' % (block_name, block_args))
    end = make_block('end%s' % block_name)

    return ''.join((
        make_block(block_name, block_args),
        nested_content,
        make_block('end' + block_name)))

def make_django_var(variable_name):
    """Returns a Django variable tag"""
    return "%s %s %s" % (
        django.template.base.VARIABLE_TAG_START,
        variable_name.strip(),
        django.template.base.VARIABLE_TAG_END,
        )

# Basic rules for converting some simple boolean expressions
# Not likely to work long-term
BOOL_CONVERSIONS = [
        (re.compile(r'(?P<var>[^ ?]+)\?((trim\?)?length gt 0|has_content)'), '%(var)s'),
        (re.compile(r'(?P<var>[^= ?]+)[ ]*==?[ ]*True'), '%(var)s'),
        (re.compile(r'!(?P<var>[^ ?]+)'), 'not %(var)s'),
        ]
def convert_boolean(boolean):
    """Convert a FTL boolean string to a Django-style one"""
    boolean = boolean.replace("true", "True") \
            .replace("false", "False") \
            .replace("=", "==")

    for pattern, fmt in BOOL_CONVERSIONS:
        match = pattern.match(boolean)
        if match:
            return fmt % match.groupdict()

    return boolean


def convert_conditional(node):
    """Convert an <#if> node"""
    name, rest = node.description.split(' ', 1)
    condition = convert_boolean(rest)

    nested = freemarker_nodes_to_django(node.children())
    return wrap_nested_content('if', nested, condition)

def convert_macro(node):
    """This is a temporary version -- eventually, macros will be
    consumed to be converted into new files
    """
    nested = freemarker_nodes_to_django(node.children())
    return wrap_nested_content('macro', nested)

def convert_macro_call(node):
    """Convert a macro-call directive"""
    _, name = node.description.split(' ', 1)

    match = ARGS_RE.match(str(node))
    if match:
        _, args = match.groups()
        args = args.strip()
    else:
        args = ''

    if node.childCount:
        nested = freemarker_nodes_to_django(node.children())
        return wrap_nested_content(name, nested, args)

    return make_block(name, args)
        
"""These converters consume all their child nodes"""
RECURSIVE_NODE_CONVERTERS = {
        freemarker.core.ConditionalBlock: convert_conditional,
        freemarker.core.Macro: convert_macro,
        freemarker.core.UnifiedCall: convert_macro_call,
    }

DOLLAR_VAR_RE = re.compile(r".*?\{(.*)\}")
def convert_dollar_var(node):
    """Convert a FTL variable node"""
    matches = DOLLAR_VAR_RE.match(str(node))
    variable_name = matches.group(1)
    return make_django_var(variable_name)

def convert_comment(node):
    """Convert an FTL comment node"""
    return wrap_nested_content('comment', node.text) + '\n'

NESTED_RE = re.compile(r'<#nested \s* /? >',
        re.VERBOSE | re.IGNORECASE)
def convert_body_instruction(node):
    """Converts a BodyInstruction... whatever that means!"""
    if NESTED_RE.match(str(node)):
        return make_django_var('nested')
    else:
        import pdb; pdb.set_trace()

def convert_text(node):
    """Convert a text node"""
    if node.leaf:
        return str(node)
    else:
        print '...', str(type(node)),  str(dir(node))


"""These converters don't consume child nodes"""
NODE_CONVERTERS = {
        freemarker.core.DollarVariable: convert_dollar_var,
        freemarker.core.Comment: convert_comment,
        freemarker.core.TextBlock: convert_text,
        freemarker.core.BodyInstruction: convert_body_instruction,
        freemarker.core.ConditionalBlock: convert_conditional,
    }

def freemarker_node_to_django(node):
    """Convert one FTL node to a Django template string"""
    cls = node.__class__
    if cls in RECURSIVE_NODE_CONVERTERS:
        return RECURSIVE_NODE_CONVERTERS[cls](node)
    elif cls in NODE_CONVERTERS:
        output = NODE_CONVERTERS[cls](node)
    elif node.description == 'root element':
        output = ''
    else:
        output = str(node)
        import pdb; pdb.set_trace()
        print "--- %s: %s" % (cls, node.toString())

    if not output:
        output = '' # guard vs None

    return output + freemarker_nodes_to_django(node.children())

def freemarker_nodes_to_django(nodes):
    """Convert a sequence of FTL nodes to a Django template string"""
    if not nodes:
        return ''

    return ''.join([freemarker_node_to_django(node) for node in nodes])

def freemarker_to_django(template):
    """
    Converts a freemarker template to a Django template.
    """
    return str(freemarker_node_to_django(template.rootTreeNode))

def get_template(filename):
    """ Ideally, would like to be able to get this from a string 
    instead of a being so tied to the directory structure, but need to find a way for the Java
    freemarker Java libs to work with just a string... yet."""
    f = java.io.File(filename).canonicalFile
    conf = freemarker.template.Configuration()
    conf.setDirectoryForTemplateLoading(f.parentFile)
    template = conf.getTemplate(os.path.basename(filename))

    return template

