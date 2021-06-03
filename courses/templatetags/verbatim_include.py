from django import template
from django.template.loader import get_template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag()
def verbatim_include(name):
    """
    Example: {% verbatim_include "weblog/post.html" %}
    """
    template = get_template(name)
    return mark_safe(template.template.source)