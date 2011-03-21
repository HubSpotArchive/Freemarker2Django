"""
Utilities for converting Freemare templates to Django.
"""
import os
import re

import freemarker
import java

import django

def freemarker_to_django(template):
    """
    Converts a freemarker template to a Django template.
    """
    # N.B currently using replaces to swap out values...
    # Ideally would like to do a builder style,
    # but hacking around a template not having children if
    # it is just vanilla text.
    output = template.toString()

    children = template.rootTreeNode.children()
    for child in children:
        if child.__class__ == freemarker.core.DollarVariable:
            # TODO, should probably break out into a get variable name method
            matches = re.compile(r".*?\{(.*)\}").match(child.toString())
            variable_name = matches.group(1)
            django_variable = "%s %s %s" % (
                django.template.base.VARIABLE_TAG_START,
                variable_name,
                django.template.base.VARIABLE_TAG_END,
                )
            output = output.replace(child.toString(), django_variable)

    return output

def get_template(filename):
    """ Ideally, would like to be able to get this from a string 
    instead of a being so tied to the directory structure, but need to find a way for the Java
    freemarker Java libs to work with just a string... yet."""
    f = java.io.File(filename).canonicalFile
    conf = freemarker.template.Configuration()
    conf.setDirectoryForTemplateLoading(f.parentFile)
    template = conf.getTemplate(os.path.basename(filename))

    return template

