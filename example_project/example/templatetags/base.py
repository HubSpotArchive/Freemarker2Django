# Convenience functions to make the django template syntax
# work better with some Freemarker idioms we're dependent on
#
# The matched_inclusion_tag code is a mix of inclusion_tag and the
# django documentation on parsing matched tags
# The kwargs parsing is lifted from the url built in tag


from inspect import getargspec
import re

from django import template
from django.template.context import Context
from django.utils.functional import curry

# Regex for token keyword arguments
kwarg_re = re.compile(r"(?:(\w+)=)?(.+)")

def matched_tag_compiler(params, defaults, name, node_class, parser, token):
    "Returns a template.Node subclass."
    bits = token.split_contents()[1:]
    bmax = len(params)
    def_len = defaults and len(defaults) or 0
    bmin = bmax - def_len
    if(len(bits) < bmin or len(bits) > bmax):
        if bmin == bmax:
            message = "%s takes %s arguments" % (name, bmin)
        else:
            message = "%s takes between %s and %s arguments" % (name, bmin, bmax)
        raise template.TemplateSyntaxError(message)

    args = []
    kwargs = {}
    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise template.TemplateSyntaxError("Malformed arguments to url tag")
            key, value = match.groups()
            if key:
                kwargs[key] = value
            else:
                args.append(value)

    nodelist = parser.parse(('end%s' % name,))
    parser.delete_first_token() # remove the {% endfoo %}
    return node_class(args, kwargs, nodelist)


def matched_inclusion_tag(library, file_name, context_class=Context, takes_context=False):
        def dec(func):
            params, xx, xxx, defaults = getargspec(func)
            if takes_context:
                if params[0] == 'context':
                    params = params[1:]
                else:
                    raise template.TemplateSyntaxError("Any tag function decorated with takes_context=True must have a first argument of 'context'")

            class InclusionNode(template.Node):
                def __init__(self, args, kwargs, nested_nodes):
                    self.args = map(template.Variable, args)
                    self.kwargs = dict([(k, template.Variable(v))
                            for k, v in kwargs.items()])
                    self.nested_nodes = nested_nodes

                def render(self, context):
                    context.push()
                    context['True'] = True
                    context['False'] = False
                    context['None'] = None

                    resolved_args = [var.resolve(context) for var in self.args]
                    resolved_kwargs = dict([(str(k), v.resolve(context))
                            for k, v in self.kwargs.items()])
                    context.pop()

                    if takes_context:
                        args = [context] + resolved_args
                    else:
                        args = resolved_args

                    dictionary = func(*args, **resolved_kwargs)
                    dictionary['nested'] = self.nested_nodes.render(context)

                    if not getattr(self, 'nodelist', False):
                        from django.template.loader import get_template, select_template
                        if not isinstance(file_name, basestring) and is_iterable(file_name):
                            t = select_template(file_name)
                        else:
                            t = get_template(file_name)
                        self.nodelist = t.nodelist
                    new_context = context_class(dictionary, autoescape=context.autoescape)
                    # Copy across the CSRF token, if present, because inclusion
                    # tags are often used for forms, and we need instructions
                    # for using CSRF protection to be as simple as possible.
                    csrf_token = context.get('csrf_token', None)
                    if csrf_token is not None:
                        new_context['csrf_token'] = csrf_token
                    return self.nodelist.render(new_context)

            compile_func = curry(matched_tag_compiler, params, defaults, getattr(func, "_decorated_function", func).__name__, InclusionNode)
            compile_func.__doc__ = func.__doc__
            library.tag(getattr(func, "_decorated_function", func).__name__, compile_func)
            return func
        return dec


