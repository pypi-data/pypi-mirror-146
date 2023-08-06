from django import forms
from django.apps import apps
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils.translation import gettext_lazy as _

from django.core.cache import cache

from .models import Organisation, SectorCategory, AidTypeCategory
from aims import models as aims
import logging
logger = logging.getLogger(__name__)  # 'aims.forms' for logging


def object_choices(objects, cache_time: int = 60 * 60 * 24, cache_key: str = None, **kwargs):
    """
    Generate dict or tuple choices for models which have a Name attribute to use as a querystring
    This functions like a ModelChoiceField except uses the 'name' like a proxy PK for
    a more human readable filter
    """
    def create_key(input_string):
        """Create a "proxy key" which functions like a pk between the form and business logic"""
        return input_string.lower().replace(' ', '_').replace('-', '_').replace('/', '_')

    def cache_and_return(return_value):
        if cache_time and cache_key:
            cache.set(cache_key, return_value, cache_time)
            logger.debug('%s %s', cache_key, cache_time)
        else:
            logging.warn('not caching an object_choices')
        return return_value

    if 'cache_time' and 'cache_key':
        cached_value = cache.get(cache_key)
        if cached_value:
            logger.debug('%s %s[:10] %s', cache_key, cached_value, cache_time)
            return cached_value

    return_type = kwargs.get('type', 'dict')
    if return_type == 'dict':
        return cache_and_return({create_key(cat.name): cat.pk for cat in objects})
    elif return_type == 'choices':
        choices = []
        for cat in objects:
            name = _(cat.name) or ''
            if kwargs.get('capitalize', False):
                name = name.capitalize()
            choices.append((create_key(cat.name), name))
        return cache_and_return(set(choices))

def STATE_CHOICES():
    return BLANK_CHOICE_DASH + [(area.code, area.name) for area in apps.get_model('simple_locations', 'area').objects.filter(level=1)]


def finance_type_category_choices():
    return object_choices(aims.FinanceTypeCategory.objects.order_by('name'), type='choices', capitalize=True, cache_key='finance_type_category_choices')


def activity_status_choices():
    return object_choices(aims.ActivityStatus.objects.order_by('name'), type='choices', cache_key='activity_status_choices')


def aid_type_category_choices():
    return object_choices(AidTypeCategory.objects.order_by('name'), type='choices', cache_key='aid_type_category_choices')


class FilterForm(forms.Form):
    """ General form for frontend components that wish to filter activities and transactions
    """
    finance_type_category = forms.MultipleChoiceField(
        choices=finance_type_category_choices,
        widget=forms.CheckboxSelectMultiple,
        required=False)
    activity_status = forms.MultipleChoiceField(
        choices=activity_status_choices,
        widget=forms.CheckboxSelectMultiple,
        required=False)
    aid_type_category = forms.MultipleChoiceField(
        choices=aid_type_category_choices,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    state = forms.ChoiceField(choices=STATE_CHOICES, required=False)
    ministry = forms.ModelChoiceField(
        Organisation.objects.filter(
            activityparticipatingorganisation__role='Accountable').distinct().order_by('name'),
        required=False)
    sector = forms.ModelChoiceField(
        SectorCategory.objects.order_by('code').exclude(code=1).distinct(), required=False)
    donor = forms.ModelChoiceField(Organisation.objects.exclude(name='').order_by('name'), required=False)
