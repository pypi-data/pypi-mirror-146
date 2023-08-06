from django import template

register = template.Library()


@register.filter(name='to_class_name')
def to_class_name(value):
    return "{module_name}.{class_name}".format(module_name=value.__class__.__module__,
                                               class_name=value.__class__.__name__)
