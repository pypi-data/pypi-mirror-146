import json
from django import template
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.safestring import mark_safe
from aims import base_utils


register = template.Library()


@register.filter
def person_render(person, token=None):

    template = 'profiles/person.html'
    context = {'person': person, 'STATIC_URL': settings.STATIC_URL}

    if token:
        context['csrf_token'] = token

    return render_to_string(template, context)


@register.filter
def contact_render(contact, token=None):

    template = 'profiles/contact.html'
    context = {'contact': contact, 'STATIC_URL': settings.STATIC_URL}

    if token:
        context['csrf_token'] = token

    return render_to_string(template, context)


@register.filter
def pretify_value(value):
    return base_utils.prettify_compact(value)


@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))
