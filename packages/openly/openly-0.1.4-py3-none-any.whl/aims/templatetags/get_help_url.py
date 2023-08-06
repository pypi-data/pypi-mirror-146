from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_help_url():
    # return a settings value
    return getattr(settings, 'HELP_URL', '')
