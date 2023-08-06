from . import get_dict


def add_common_text(request):
    '''Adds very commonly used common text values to the request context'''

    strings = get_dict('activity_or_program', 'activities_or_programs', lazy=True)
    return {
        'activity_singular': strings['activity_or_program'],
        'activity_singular_lower': strings['activity_or_program'].lower(),
        'activity_plural': strings['activities_or_programs'],
        'activity_plural_lower': strings['activities_or_programs'].lower()
    }
