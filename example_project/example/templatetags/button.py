from django import template

from base import matched_inclusion_tag

register = template.Library()

@matched_inclusion_tag(register, 'button.html')
def button(type='basic', size='small', next=False, enabled=True, id='', css_class='', href='#'):
    return {
            'type': type,
            'size': size,
            'next': next,
            'enabled': enabled,
            'id': id,
            'css_class': css_class,
            'href': href,
        }

