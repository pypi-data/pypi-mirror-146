from django.conf import settings
from django.template import Library


register = Library()


@register.simple_tag(takes_context=True)
def change_language(context, language_code):
    """ Returns the current page path localized to `language_code`. """

    if 'request' not in context:
        # happens when Django is handling an uncaught exception
        return ''
    path = context['request'].get_full_path()
    path_parts = path.split('/')
    if path_parts[1] in (language[0] for language in settings.LANGUAGES):
        path_parts[1] = language_code
    return '/'.join(path_parts)
