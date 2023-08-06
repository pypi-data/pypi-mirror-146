from django import template
from django.conf import settings
from django.utils.translation import ugettext as _
import dateutil.parser

register = template.Library()


@register.filter()
def percentify(value):
    """value should be either None or 0.0 <= value <= 1.0"""
    if value is None:
        return 'N/A'
    else:
        return '{}%'.format(int(value * 100))


@register.filter()
def to_date(value):
    if value:
        value = value.strftime('%Y%m%d')
        return value


@register.filter()
def date_format(value):
    if value:
        value = value.strftime('%Y-%m-%d')
        return value


@register.filter
def parse_date(value):
    if value:
        return dateutil.parser.parse(value)


@register.filter()
def to_int(value):
    values = list(filter(str.isdigit, str(value)))
    if values:
        return values


@register.filter
def financing_organisation(activity):

    financing_organisation_name = ''
    financing_organisations = list(set(t.provider_organisation.name for t in activity.transaction_set.all() if
                                       t.provider_organisation_id is not None))

    if len(financing_organisations) > 1:
        financing_organisation_name = _('Multiple Donors')
    elif len(financing_organisations) > 0:
        financing_organisation_name = financing_organisations[0]

    return financing_organisation_name


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def import_allowed(organisation):
    if organisation.code in settings.IMPORT_ENABLED_ORG_CODES:
        return True
