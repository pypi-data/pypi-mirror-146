from django import template
from ..common_text import get

register = template.Library()


@register.filter()
def common_text(key):
    """ Retrieves the value for the given key in the common_text module """
    return get(key)


@register.filter()
def common_text_optional(key):
    """ Retrieves the value for the given key in the common_text module, or None if the key is not found"""
    try:
        return get(key)
    except (KeyError, AttributeError):
        return None
