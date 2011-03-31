"""Writes a set of macros to disk, in a ready-for-django format"""

import os
import shutil
import errno

import django

def setup_tag_project(project_name='tag_project', app_name='tag_app'):
    django.core.management.call_command('startproject', project_name)
    django.core.management.call_command('startapp', app_name)
    
    root = os.path.join(os.getcwd(), project_name)
    template_dir = os.path.join(root, 'templates')
    tags_dir = os.path.join(root, app_name, 'templatetags')

    add_template_dir_to_settings(settings_file, template_dir)

    os.mkdir(template_dir)
    os.mkdir(tags_dir)
    os.copytree(os.path.join(os.dirname(__file__), 'templatetags'), tags_dir)

    return template_dir, tags_dir

def add_template_dir_to_settings(filename, template_dir):
    with open(filename) as f:
        settings_str = f.read()

    template_dirs_declaration = 'TEMPLATE_DIRS = ('
    before, after = settings_str.split(template_dirs_declaration, 1)
    path_str = "    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),"

    settings_str = "%(before)s%(template_dirs_declaration)s\n%(path_str)s%(after)s" % locals()
    with open(filename, 'w') as f:
        f.write(settings_str)

class TagWriter(object):
    def __init__(self, template_dir, tags_dir):
        self.template_dir = template_dir
        self.tags_dir = tags_dir

    def write(self, template_name, tags):
        """
        Creates a tag package `package_name`.py, and fills it with
        the given tags
        """
        self.make_python_file(template_name, tags.keys())

    def make_python_file(template_name, tag_names):
        """Create a skeleton Python tag file"""
        pyname = '%s.py' % template_name
        with open(os.path.join(self.tags_dir, pyname), 'w') as f:
