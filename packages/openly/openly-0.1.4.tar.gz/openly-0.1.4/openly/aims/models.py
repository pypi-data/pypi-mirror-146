import logging
import uuid
import warnings
from collections import namedtuple
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Union
from django.db.models.expressions import Value

import requests
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models, transaction
from django.db.models import (
    DO_NOTHING, Aggregate, Case, CharField, F, Func, JSONField, Max, OuterRef, Q, Subquery, Sum, TextField, Value as V,
    When,
)
from django.db.models.functions import Coalesce, Concat
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import get_language, gettext_lazy as _, ugettext
from model_utils.models import TimeStampedModel
from oipa.models import OipaActivityLink
from sentry_sdk import capture_exception
from simple_locations.models import Area

from aims import common_text

from . import managers
# from .viewed_models import AidTypeAggregate, ActivityCurrency, ActivityAidTypeBreakdown, ActivityCommitment, LocationGeodata, TransactionValueLocationView, TransactionValueUsd, TransactionValueLocationSector, CommitmentTotal  # noqa: F401
from .openly_roles import OPENLY_SECTOR_TYPE_IATI, OPENLY_SECTOR_TYPES

logger = logging.getLogger(__name__)

ORIGINAL_TYPE = 'original'
PENDING_TYPE = 'pending'
DIFFERENCE_TYPES = (
    (ORIGINAL_TYPE, _("original")),
    (PENDING_TYPE, _("pending")),
)

openly_required_to_publish = ('title', 'description', 'status', 'start_date', 'sector', 'location', 'commitment')

SubAnnotations = Mapping[str, Subquery]


class Narrative(models.Model):
    # references an actual related model which has a corresponding narrative
    related_content_type = models.ForeignKey(ContentType, related_name='related_agent', on_delete=models.CASCADE)
    related_object_id = models.IntegerField(
        verbose_name='related object',
        null=True,
        db_index=True)
    related_object = GenericForeignKey('related_content_type', 'related_object_id')

    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)

    language = models.ForeignKey('aims.Language', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return "%s" % self.content[:30]

    class Meta:
        index_together = [('related_content_type', 'related_object_id')]

    def save(self, *args, **kwargs):
        instance = super(Narrative, self).save(*args, **kwargs)
        # Remove existing Narrative instances for the same object + language
        self.__class__.objects.filter(
            related_content_type__id=self.related_content_type_id,
            related_object_id=self.related_object_id,
            language=self.language
        ).exclude(pk=self.pk).delete()
        return instance


class NarrativeMixinManager(models.Manager):
    def get_queryset(self):
        return super(NarrativeMixinManager, self).get_queryset().prefetch_related('narratives')


class NarrativeMixin(models.Model):
    """
    Class mixin which simply provides a "narratives" field for consistent narrative naming
    """
    narratives = GenericRelation('aims.Narrative', content_type_field='related_content_type', object_id_field='related_object_id')

    class Meta:
        abstract = True

    objects = NarrativeMixinManager()


class GeographicLocationClass(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class DisbursementChannel(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.TextField()

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class TransactionType(models.Model):
    code = models.CharField(primary_key=True, max_length=2)
    name = models.CharField(max_length=40)
    description = models.TextField()

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class DescriptionType(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class Vocabulary(models.Model):
    code = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=140)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class ArrayAgg(Aggregate):
    function = 'ARRAY_AGG'
    template = '%(function)s(DISTINCT %(expressions)s)'

    def convert_value(self, value, expression, connection, context):
        if not value:
            return []
        return value


class ArrayLength(Func):
    function = 'ARRAY_LENGTH'
    name = 'Array_Length'
    template = '%(function)s(%(expressions)s, %(index)s)'


class ArrayFirst(Func):
    function = ''
    name = ''
    template = '(%(expressions)s) [1]'


class ActivityFinanceManager(models.Manager):
    """
    Adds queryset to get total activity financial data, allowing filtering on both
    Activity and Transaction

    Appended to the Activity info is filtered from the related Transactions.
        'dollars' and 'natural'.
    Additionally a Subquery is inclulded for "chosen currency".

    Example usage:
    To get "Commitments since 2014":
    Activity.finance.get_queryset(
        dict( transaction_type='C', transaction_date__gte='2014-01-01')
    ).values_list('id', 'dollars', 'natural')

    Activity.finance.get_queryset(
        dict(transaction_type='C'),
        dict(end_planned__gte='2019-01-01')
    ).values('id', 'dollars', 'natural')
    """

    def get_queryset(self, transactionfilter=None, activityfilter=None):

        # The first filter will be applied to transactions related to this activity;
        # the second is applied to the activity.
        if transactionfilter:
            if not activityfilter:
                activityfilter = {}
            activityfilter.update({'transaction__%s' % k: i for k, i in transactionfilter.items()})

        qs = super(ActivityFinanceManager, self).get_queryset()
        if activityfilter:
            qs = qs.filter(**activityfilter)

        return qs.annotate(
            dollars=Sum('transaction__usd_value'),
            natural=Sum('transaction__value'),
        )


class ActivityStatus(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    order = models.SmallIntegerField(unique=True, null=True,
                                     help_text='Used to order the status options in dropdowns and filters.')
    name = models.CharField(max_length=50)
    language = models.CharField(max_length=2, default='en', help_text='Legacy field')

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)

    class Meta:
        verbose_name_plural = "Activity Statuses"


class RegionVocabulary(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class CollaborationType(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    language = models.CharField(max_length=2)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class FlowType(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class FinanceTypeCategory(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class FinanceType(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=220)
    category = models.ForeignKey(FinanceTypeCategory, on_delete=models.CASCADE)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class TiedStatus(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    description = models.TextField()

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class ActivityScope(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class AIMSManager(models.Manager):

    def get_queryset(self,):
        """ Just return all objects with openly status of published """
        return super(AIMSManager, self).get_queryset().filter(openly_status=StatusEnabledLocalData.OPENLY_STATUS_PUBLISHED)

    def with_drafts(self,):
        """ Returns published and draft activities."""
        return super(AIMSManager, self).get_queryset().filter(openly_status__in=[
            StatusEnabledLocalData.OPENLY_STATUS_DRAFT, StatusEnabledLocalData.OPENLY_STATUS_PUBLISHED])

    def editables(self):
        """Things we want shown in the editor. """
        return super(AIMSManager, self).get_queryset().filter(openly_status__in=[
            StatusEnabledLocalData.OPENLY_STATUS_PUBLISHED,
            StatusEnabledLocalData.OPENLY_STATUS_DRAFT,
            StatusEnabledLocalData.OPENLY_STATUS_BLANK,
            StatusEnabledLocalData.OPENLY_STATUS_REVIEW])

    def all_openly_statuses(self) -> QuerySet:
        """ Return all objects """
        return super(AIMSManager, self).get_queryset().exclude(openly_status=StatusEnabledLocalData.OPENLY_STATUS_ARCHIVED)

    def drafts(self,):
        """ Return all objects set as draft """
        return super(AIMSManager, self).get_queryset().filter(openly_status=StatusEnabledLocalData.OPENLY_STATUS_DRAFT)

    def iatixml(self,):
        """ Return all objects read from iati xml"""
        return super(AIMSManager, self).get_queryset().filter(openly_status=StatusEnabledLocalData.OPENLY_STATUS_IATIXML)

    def archived(self,):
        """ Return all "deleted" objects """
        return super(AIMSManager, self).get_queryset().filter(openly_status=StatusEnabledLocalData.OPENLY_STATUS_ARCHIVED)

    def clear_blank_activities(self):
        """ Delete all objects with a "blank" status """
        logger.debug("clear_blank_activities called")
        return super().get_queryset().filter(openly_status=StatusEnabledLocalData.OPENLY_STATUS_BLANK).delete()


class Currency(models.Model):
    code = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=2)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class CurrencyQuerySet(QuerySet):

    def closest_to(self, rate_date):
        closest_greater_qs = self.filter(date__gte=rate_date).order_by('date')
        closest_less_qs = self.filter(date__lt=rate_date).order_by('-date')

        try:
            try:
                closest_greater = closest_greater_qs[0]
            except IndexError:
                return closest_less_qs[0]

            try:
                closest_less = closest_less_qs[0]
            except IndexError:
                return closest_greater_qs[0]
        except IndexError:
            raise self.model.DoesNotExist("There is no closest object"
                                          " because there are no objects.")

        if closest_greater.date - rate_date > rate_date - closest_less.date:
            return closest_less
        else:
            return closest_greater


class CurrencyManager(models.Manager):

    def get_queryset(self):
        return CurrencyQuerySet(self.model, using=self._db)

    def closest_to(self, rate_date):
        return self.get_query_set().closest_to(rate_date)

    def fetch(self, date, currency_list, base_currency='USD'):
        """
        >>> CurrencyExchangeRate.objects.fetch('2011-01-01', 'NZD')
        <CurrencyQuerySet [<CurrencyExchangeRate: NZD -> USD : 0.77847607>]>
        >>> CurrencyExchangeRate.objects.fetch('2011-01-01', ['NZD', 'CAD'])
        <CurrencyQuerySet [<CurrencyExchangeRate: CAD -> USD : 1.00277971>, <CurrencyExchangeRate: NZD -> USD : 0.77847607>]>
        """
        if isinstance(currency_list, str):
            currency_list = [currency_list]
        try:
            api_key = getattr(settings, 'OPEN_EXCHANGE_API_KEY')
        except KeyError:
            raise

        # Avoid fetching currencies we already have - this causes an unhappy database
        # and unneccessary processing
        existing_currencies = self.filter(date=date, base_currency_id__in=currency_list).values_list('base_currency_id', flat=True)
        currency_set = set(currency_list).difference(set(existing_currencies))

        if len(currency_set) != 0:
            api_address = 'http://openexchangerates.org/api/historical/{date}.json'
            address = api_address.format(date=date)
            params = {'app_id': api_key, 'symbols': ','.join(currency_set)}
            request = requests.get(address, params=params)
            if request.status_code == 200:
                rates = request.json()['rates']
                for code, rate in rates.items():
                    self.create(rate=1 / rate, currency_id=base_currency, base_currency_id=code, date=date)
            else:
                try:
                    message = request.json()['description']
                except:  # noqa: E722
                    message = "Received a non success code from %s" % (address,)
                warnings.warn(message)

        return self.filter(date=date, base_currency_id__in=currency_list)


class CurrencyExchangeRate(models.Model):
    base_currency = models.ForeignKey(Currency, verbose_name=_("Base Currency"), related_name='base_currencies', on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, verbose_name=_("Exchange Currency"), related_name="exchange_currencies", on_delete=models.CASCADE)
    rate = models.DecimalField(verbose_name=_("Exchange Rate"), decimal_places=8, max_digits=16)
    date = models.DateField()

    objects = CurrencyManager()

    class Meta:
        db_table = 'aims_currency_exchange_rate'
        unique_together = (("base_currency", "currency", "date"),)

    def __str__(self,):
        return "%s -> %s : %s" % (self.base_currency.code, self.currency.code, self.rate)

    @classmethod
    def get_or_create_from_api(cls, base_currency: Currency, currency: Currency, date: datetime.date) -> float:

        try:
            currency_exchange_rate = cls.objects.get(base_currency=base_currency, currency=currency, date=date)
            return currency_exchange_rate.rate
        except cls.DoesNotExist:
            pass

        api_key = getattr(settings, 'OPEN_EXCHANGE_API_KEY')
        api_address = 'http://openexchangerates.org/api/historical/{date}.json'.format(date=date.isoformat())
        request = requests.get(api_address, params={'app_id': api_key, 'base_currency': base_currency.pk, 'symbols': [currency.pk]})
        rate = request.json()['rates'][currency.pk]
        currency_exchange_rate = CurrencyExchangeRate(base_currency=base_currency, currency=currency, date=date, rate=rate)
        currency_exchange_rate.save()
        return currency_exchange_rate.rate

    @classmethod
    def convert(cls, base_currency: Currency, currency: Currency, date: datetime.date, value: Decimal) -> float:
        rate = cls.get_or_create_from_api(base_currency, currency, date)
        return Decimal(value) / Decimal(rate)


class TransactionValueLocation(models.Model):
    activity = models.ForeignKey('aims.Activity', related_name='transaction_value_for_location', null=True, blank=True, on_delete=models.CASCADE)
    transaction = models.ForeignKey('aims.Transaction', related_name='transaction_value_for_location', null=True, blank=True, on_delete=models.CASCADE)
    location = models.ForeignKey('aims.Location', related_name='transaction_value_for_location', null=True, blank=True, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, null=True, blank=True, on_delete=models.CASCADE)
    value = models.FloatField(null=True, blank=True)
    dollars = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'aims_transaction_value_location'


class LocalDataMixin(models.Model):
    """
    This is a misnomer, it adds auto date_created and date_modified fields
    to any model.
    """

    date_created = models.DateField(verbose_name=_('Date Created'), auto_now_add=True, null=True, blank=True)
    date_modified = models.DateField(verbose_name=_('Last Modified'), null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        now = timezone.now().date()
        self.date_modified = now
        return super(LocalDataMixin, self).save(*args, **kwargs)


class StatusEnabledLocalData(LocalDataMixin):

    OPENLY_STATUS_IATIXML = 'iatixml'
    OPENLY_STATUS_DRAFT = 'draft'
    OPENLY_STATUS_PUBLISHED = 'published'
    OPENLY_STATUS_ARCHIVED = 'archived'
    OPENLY_STATUS_BLANK = 'blank'  # used when an activity is first created, but not yet edited
    OPENLY_STATUS_REVIEW = 'review'
    OPENLY_STATUSES = (
        (OPENLY_STATUS_IATIXML, _('IATI XML')),
        (OPENLY_STATUS_DRAFT, _('Draft')),
        (OPENLY_STATUS_PUBLISHED, _('Published')),
        (OPENLY_STATUS_ARCHIVED, _('Archived')),
        (OPENLY_STATUS_BLANK, _('Blank')),
        (OPENLY_STATUS_REVIEW, _('Under review')),
    )

    openly_status = models.CharField(choices=OPENLY_STATUSES, default='iatixml', max_length=12)

    objects = AIMSManager()

    class Meta:
        abstract = True

    def get_status_display(self):
        return dict(self.OPENLY_STATUSES).get(self.openly_status, self.openly_status)


# iati derived models
class PolicyMarker(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class SectorCategory(TimeStampedModel):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    openly_type = models.CharField(choices=OPENLY_SECTOR_TYPES, default=OPENLY_SECTOR_TYPE_IATI, max_length=8)
    withdrawn = models.BooleanField(null=False, default=False)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class Sector(TimeStampedModel):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(SectorCategory, null=True, blank=True, on_delete=models.CASCADE)
    withdrawn = models.BooleanField(null=False, default=False)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class NationalSector(Sector):
    """ proxy class for sector to return all national sector categories """
    class Meta:
        proxy = True
    objects = managers.NationalSectorManager()


class IATISector(Sector):
    """ proxy class for sector to return all iati sector categories """
    class Meta:
        proxy = True
    objects = managers.IATISectorManager()
    dac_3 = managers.IATIDAC3SectorManager()
    dac_5 = managers.IATIDAC5SectorManager()


class SectorTier(models.Model):
    '''
    Reference a Sector to 'Tier' levels
    '''
    sector = models.OneToOneField('sector', primary_key=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, unique=True)
    tier_label = models.CharField(max_length=128)
    tier_I = models.ForeignKey('sector', related_name='tier_I', blank=True, null=True, on_delete=models.CASCADE)
    tier_II = models.ForeignKey('sector', related_name='tier_II', blank=True, null=True, on_delete=models.CASCADE)
    tier_III = models.ForeignKey('sector', related_name='tier_III', blank=True, null=True, on_delete=models.CASCADE)
    tier_IV = models.ForeignKey('sector', related_name='tier_IV', blank=True, null=True, on_delete=models.CASCADE)
    tier_V = models.ForeignKey('sector', related_name='tier_V', blank=True, null=True, on_delete=models.CASCADE)
    tier_VI = models.ForeignKey('sector', related_name='tier_VI', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.name)
    '''
    # Import SectorTier script
    import csv
    cls.objects.all().delete()
    for line in csv.DictReader(open('/home/josh/Documents/tiers_III.csv')):
        try:
            Sector.objects.get_or_create(pk=line['sector_id'], name=line['name'])
        except:
            pass
    for line in csv.DictReader(open('/home/josh/Documents/tiers_III.csv')):
        pops = [ k for k in line if line[k] == '']
        for pop in pops:
            line.pop(pop)
        line.pop('tier')
        s = SectorTier(**line)
        s.save()
    '''


class NationalSectorCategory(SectorCategory):
    """ proxy class for sector category to return all national sector categories """
    class Meta:
        proxy = True
    objects = managers.NationalSectorCategoryManager()


class IATISectorCategory(SectorCategory):
    """ proxy class for sector category to return all iati sector categories """
    class Meta:
        proxy = True
    objects = managers.IATISectorCategoryManager()


class ValueType(models.Model):
    code = models.CharField(primary_key=True, max_length=2)
    name = models.CharField(max_length=40)
    description = models.TextField()

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class OrganisationType(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class Organisation(TimeStampedModel):
    code = models.CharField(primary_key=True, max_length=80)
    abbreviation = models.CharField(max_length=80, default="")
    type = models.ForeignKey(OrganisationType, null=True, blank=True, on_delete=models.CASCADE)
    reported_by_organisation = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=250, default="")
    original_ref = models.CharField(max_length=80, default="")
    iati_sync_enabled = models.BooleanField(null=False, default=False)  # used for enabling IATI sync for an organisation
    is_admin = models.BooleanField(null=False, default=False)  # used for endorsements. In plov: Ministry of Finance
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, limit_choices_to={'parent': None},)

    def __str__(self) -> str:
        return self.name

    def total_activities(self) -> int:
        return self.activity_set.count()

    @cached_property
    def full_name(self) -> str:
        if self.parent:
            return '{}, {}'.format(self.name, self.parent.name)
        return self.name

    @cached_property
    def reporting_activities_count(self) -> int:
        return self.activity_reporting_organisation.count()

    @cached_property
    def participating_activities_count(self) -> int:
        warnings.warn('This property uses a potentially slow set() op on a queryset', DeprecationWarning)
        return len(set([apo.activity_id for apo in self.activityparticipatingorganisation_set.all()]))

    @cached_property
    def activities_with_providing_transactions_count(self) -> int:
        warnings.warn('This property uses a potentially slow set() op on a queryset', DeprecationWarning)
        return len(set([t.activity_id for t in self.transaction_providing_organisation.all()]))

    @cached_property
    def activities_with_receiving_transactions_count(self) -> int:
        warnings.warn('This property uses a potentially slow set() op on a queryset', DeprecationWarning)
        return len(set([t.activity_id for t in self.transaction_receiving_organisation.all()]))

    @cached_property
    def associated_activities(self) -> QuerySet:
        return Activity.objects.filter(Q(reporting_organisation_id=self.pk) | Q(participating_organisation__pk=self.pk)).distinct()

    @property
    def sectors(self):
        # TODO: This is an ugly hack to make sure we access the correct translation of a
        # sector's name because django-modeltranslation doesnt patch related managers
        return ', '.join(Sector.objects.filter(pk__in=self.associated_activities.values_list('sector__pk', flat=True).distinct()).values_list('name', flat=True))

    @cached_property
    def locations(self) -> str:
        # Filter to include areas with an activity where this
        # Organisation is reporting or participating
        areas = Area.objects.filter(Q(
            area_activities__activity__openly_status='published', area_activities__activity__reporting_organisation=self.pk) | Q(
            area_activities__activity__openly_status='published', area_activities__activity__participating_organisation=self)).distinct()
        q = Q()
        # Also include areas which are ancestors/descendants
        # This uses a simplified version of the MPTT "get_family" method
        for lft, rght, tree_id in areas.values_list('lft', 'rght', 'tree_id'):
            q = q | Q(lft__lte=lft, rght__gte=rght, tree_id=tree_id) | Q(lft__gte=lft, rght__lte=rght, tree_id=tree_id)
        if areas.count() == 0:
            return 'Not Specified'
        areas = Area.objects.filter(q).distinct()
        names = areas.values_list('name', flat=True)

        return ', '.join(list(names))

    @cached_property
    def deprecated_locations(self) -> str:
        '''
        Remove post closure of openly_mohinga#470
        '''
        warnings.warn('Activity.deprecated_locations will be removed in Openly @ django 3', DeprecationWarning)
        locations = set()
        for activity in self.associated_activities:
            try:
                for location in activity.location_set.all():
                    for area in location.area.get_family().values_list('name', flat=True):
                        locations.add(area)
            except AttributeError:
                pass
        if len(locations) == 0:
            return 'Not Specified'
        else:
            return ', '.join(list(locations))

    @cached_property
    def people(self) -> str:
        if hasattr(self, 'profile'):
            return ', '.join(self.profile.people.exclude(name='').values_list('name', flat=True))
        if hasattr(self, 'profile_old'):
            try:
                return ', '.join(self.profile_old.first().persons.exclude(name='').values_list('name', flat=True))
            except AttributeError:
                pass
        return ''

    def can_create_activity(self, user: User) -> bool:
        if user.is_superuser:
            return True
        if user.organisation is None:
            return False
        if user.organisation.is_admin:
            return True
        if self.code in user.userorganisation.organisations.values_list('code', flat=True):
            return True
        return False

    @property
    def is_ministry(self) -> bool:
        return self.type_id == 100

    @cached_property
    def activities_for_review(self) -> QuerySet:
        activities = Activity.objects.editables().filter(openly_status=Activity.OPENLY_STATUS_REVIEW)
        if self.is_admin:
            return activities
        return activities.filter(
            participating_organisations__role='Accountable',
            participating_organisations__organisation=self)

    @cached_property
    def count_activities(self) -> int:
        ''' Return the count of activities this organisation is involved in '''
        return apps.get_model('aims', 'Activity').objects.filter(
            Q(reporting_organisation=self) | Q(participating_organisations__organisation=self)
        ).count()

    @property
    def activities(self) -> Tuple[QuerySet['Activity'], Tuple[str]]:
        '''
        Return all activities associated with an Organisation and the relationship
        to the organisation
        >>> Organisation.objects.get(pk='CH-4').activities
        '''

        def title_subquery(include_descriptions: bool = True) -> Dict[str, Subquery]:
            '''
            Multilingual titles without any wierd models
            '''
            annotations = []
            title = apps.get_model('aims', 'Title').objects
            description = apps.get_model('aims', 'Description').objects
            languages = getattr(settings, 'LANGUAGES', ('en',))
            for c in languages:
                field_name = 'title_%s' % (c[0],)
                subquery = title.filter(language_id=c, activity_id=OuterRef('pk'))
                annotations.append((field_name, Subquery(subquery.values('title')[:1])))
                if not include_descriptions:
                    continue
                field_name = 'description_%s' % (c[0],)
                subquery = description.filter(language_id=c, activity_id=OuterRef('pk'), type__name='General')
                annotations.append((field_name, Subquery(subquery.values('description')[:1])))
            return {name: sq for name, sq in annotations}

        def role_subquery() -> SubAnnotations:
            '''
            Attach a participating organisation role as 'role' field to the
            activity
            '''
            participants = apps.get_model('aims', 'ActivityParticipatingOrganisation').objects
            role_query = participants.filter(organisation=self, activity_id=OuterRef('pk'))
            role_values = role_query.values('role__name')[:1]
            role_subquery = Subquery(role_values)
            return {'role': role_subquery}

        def sectors() -> SubAnnotations:
            s = Activity.objects\
                .filter(activitysector__sector__in=apps.get_model('aims', 'IatiSector').objects.all())\
                .filter(pk=OuterRef('pk'))\
                .annotate(sector_category_names=ArrayAgg('activitysector__sector__category__name'))\
                .values('sector_category_names')

            return {'sector_category_names': Subquery(s, output_field=ArrayField(CharField()))}

        def commitment_subquery() -> SubAnnotations:
            s = Activity.objects\
                .filter(transaction__transaction_type='C')\
                .filter(pk=OuterRef('pk'))\
                .annotate(commitment_total=Sum('transaction__usd_value')).values('commitment_total')[:1]
            return {'commitment_total': Subquery(s, output_field=models.DecimalField(max_digits=15, decimal_places=2))}

        def oipa_sync_subquery() -> SubAnnotations:
            links = OipaActivityLink.objects.exclude(oipa_fields=[]).filter(activity_id=OuterRef('id'))
            return {'iati_sync': Subquery(links.values('activity_id')[:1])}

        def locations_subquery() -> SubAnnotations:
            s = Activity.objects\
                .filter(pk=OuterRef('pk'))\
                .annotate(area_ids=ArrayAgg('location__area'))\
                .values('area_ids')

            return {'area_ids': Subquery(s, output_field=ArrayField(CharField()))}

        activities = Activity.objects.annotate(
            **role_subquery(),
            **title_subquery(),
            **sectors(),
            **commitment_subquery(),
            **locations_subquery(),
        )

        labels = (
            *role_subquery().keys(),
            *title_subquery().keys(),
            *sectors().keys(),
            *commitment_subquery().keys(),
            *locations_subquery().keys(),
        )  # type: Tuple[str]

        if getattr(settings, 'OIPA_SYNC_ENABLED', False):
            activities = activities.annotate(**oipa_sync_subquery())
            labels = labels + (*oipa_sync_subquery().keys(),)

        # Return a queryset and the labels of applied annotations
        activities_filtered = activities.filter(
            Q(role__isnull=False) | Q(reporting_organisation=self)
        )
        return activities_filtered, labels


class OrganisationActivityBudgetsUsd(models.Model):
    code = models.CharField(max_length=80, primary_key=True)
    act_id = models.ForeignKey('aims.Activity', related_name='budget_set_usd', db_column='act_id', on_delete=DO_NOTHING)
    year = models.CharField(max_length=4)
    quarter = models.CharField(max_length=1)
    currency = models.CharField(max_length=3),
    value = models.DecimalField(decimal_places=2, max_digits=15)
    usd_value = models.DecimalField(decimal_places=2, max_digits=15)

    class Meta:
        managed = False
        db_table = 'aims_organisation_budgets_usd'

    def __str__(self) -> str:
        return "%s - %s - %s - %s" % (self.code, self.act_id, self.year, self.quarter)


class UserOrganisation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisations = models.ManyToManyField(Organisation, related_name='users')
    title = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self) -> str:
        return ''


class Partner(Organisation):
    ''' Proxy class that returns all partner organisations. '''
    class Meta:
        proxy = True
    objects = managers.PartnerOrganisationManager()

    @property
    def logo(self) -> str:
        if hasattr(self, 'profile'):
            try:
                return self.profile.logo.url
            except ValueError:
                return ''
        else:
            return ''

    @property
    def profile_url(self) -> str:
        return reverse('organisation_profile', args=[self.pk])


class GovernmentOrganisation(Organisation):
    ''' Proxy class that returns all government organisations. '''
    class Meta:
        proxy = True
    objects = managers.GovernmentOrganisationManager()


class LocalMinistry(Organisation):
    ''' Proxy class that returns all local ministries. '''
    class Meta:
        proxy = True
    objects = managers.LocalMinistryManager()


def generate_daterange_filter(start_date: date, end_date: date, related_model: bool = False, **kwargs: Dict[str, Any]) -> Q:
    """
    Return a filter for Activity models corresponding to a date range
    This returns a Q object which filters on a number of different fields
    including activity transaction

    Different filters can be turned on or off wia kwargs
    Filters are by default on activity dates, activity timeline, and transaction dates

    For Activity model no options are required
    For related models use the 'related_model' field to filter
    """

    def q(**k: Any) -> Q:
        """
        Make a Q object from a dict, optionally prefix values in the dict
        for a related field
        """
        if not prefix:
            return Q(**k)
        d = {'%s__%s' % (prefix, k): v for k, v in dict(**k).items()}  # type: Dict[str, Any]
        return Q(d)

    prefix = kwargs.get('prefix', None)
    if not prefix and related_model:
        prefix = 'activity'

    # A Transaction of this activity occurs during the timeframe
    # If the model __is__ a Transaction use the first option there. Don't append "activity" to the filter values.
    if kwargs.get('model_is_transaction', False):
        transaction = Q(transaction_date__gte=start_date, transaction_date__lte=end_date)
    else:
        transaction = q(transaction__isnull=False, transaction__transaction_date__gte=start_date, transaction__transaction_date__lte=end_date)

    # The activity is supposed to start within the date range
    start_planned = q(start_actual__isnull=True, start_planned__gte=start_date, start_planned__lte=end_date)

    # The activity started within the date range
    start_actual = q(start_actual__gte=start_date, start_actual__lte=end_date)

    # The activity is supposed to end within the date range
    end_planned = q(end_actual__isnull=True, end_planned__gte=start_date, end_planned__lte=end_date)

    # The activity ended within the date range
    end_actual = q(end_actual__gte=start_date, end_actual__lte=end_date)

    timeline = (
        # The activity's planned or actual timeline contains the date range
        ((q(start_actual__isnull=True)
          & q(start_planned__lte=start_date)) |
         q(start_actual__lte=start_date))
        & (q(end_actual__isnull=True)
           & q(end_planned__gte=end_date)) |
        q(end_actual__gte=end_date)
    )

    returns = Q()
    if kwargs.get('filter_on_activity_dates', True):
        returns = returns | start_planned | start_actual | end_planned | end_actual
    if kwargs.get('filter_on_timeline', True):
        returns = returns | timeline
    if kwargs.get('filter_on_transaction', True):
        returns = returns | transaction

    return returns


def filter_activities_by_daterange(activities: QuerySet, start_date: date, end_date: date) -> QuerySet:
    """ Filter to Activity models corresponding to a date range

    An Activity belongs to a date range if the Activity has any Transaction that lies
    within the date range or if the Activity's planned or actual timeline intersects
    the date range.
    """
    return activities.filter(generate_daterange_filter(start_date, end_date)).distinct()


class Activity(StatusEnabledLocalData):

    HierarchyChoices = models.IntegerChoices('HierarchyChoices', 'Parent Child')
    DateDetailChoices = models.IntegerChoices('DateDetailChoices', 'Year Month Day')
    ActivityDateTypeChoices = models.IntegerChoices('ActivityDateTypeChoices', 'PLANNED_START ACTUAL_START PLANNED_END ACTUAL_END')

    id = models.CharField(primary_key=True, max_length=150)
    iati_identifier = models.CharField(max_length=150, null=True, blank=True)
    internal_identifier = models.CharField(max_length=150, null=True, blank=True)
    default_currency = models.ForeignKey('aims.Currency', null=True, blank=True, related_name="default_currency", on_delete=models.CASCADE)
    hierarchy = models.SmallIntegerField(choices=HierarchyChoices.choices, default=1, null=True)
    last_updated_datetime = models.CharField(max_length=100, default="")  # This field is populated by an IATI XML import, don't trust it
    linked_data_uri = models.CharField(max_length=100, default="", blank=True, null=True)
    reporting_organisation = models.ForeignKey('aims.Organisation', null=True, blank=True, related_name="activity_reporting_organisation", on_delete=models.CASCADE)
    secondary_publisher = models.BooleanField(default=False)
    activity_status = models.ForeignKey('aims.ActivityStatus', null=True, blank=True, on_delete=models.CASCADE)

    start_planned = models.DateField(null=True, blank=True, default=None)
    end_planned = models.DateField(null=True, blank=True, default=None)
    start_actual = models.DateField(null=True, blank=True, default=None)
    end_actual = models.DateField(null=True, blank=True, default=None)

    start_planned_detail = models.IntegerField(null=True, blank=True, default=None, choices=DateDetailChoices.choices)
    end_planned_detail = models.IntegerField(null=True, blank=True, default=None, choices=DateDetailChoices.choices)
    start_actual_detail = models.IntegerField(null=True, blank=True, default=None, choices=DateDetailChoices.choices)
    end_actual_detail = models.IntegerField(null=True, blank=True, default=None, choices=DateDetailChoices.choices)

    participating_organisation = models.ManyToManyField('aims.Organisation', through="aims.ActivityParticipatingOrganisation")
    policy_marker = models.ManyToManyField('aims.PolicyMarker', through="aims.ActivityPolicyMarker")
    sector = models.ManyToManyField('aims.Sector', through="aims.ActivitySector")
    recipient_country = models.ManyToManyField('geodata.Country', through="aims.ActivityRecipientCountry")
    recipient_region = models.ManyToManyField('geodata.Region', through="aims.ActivityRecipientRegion")
    tag = models.ManyToManyField('aims.Tag', through="aims.ActivityTag")

    collaboration_type = models.ForeignKey('aims.CollaborationType', null=True, blank=True, on_delete=models.CASCADE)
    default_flow_type = models.ForeignKey('aims.FlowType', null=True, blank=True, on_delete=models.CASCADE)
    default_aid_type = models.ForeignKey('aims.AidType', null=True, blank=True, on_delete=models.CASCADE)
    default_finance_type = models.ForeignKey('aims.FinanceType', null=True, blank=True, on_delete=models.CASCADE)
    default_tied_status = models.ForeignKey('aims.TiedStatus', null=True, blank=True, on_delete=models.CASCADE)
    xml_source_ref = models.CharField(max_length=200, default="")
    total_budget_currency = models.ForeignKey('aims.Currency', null=True, blank=True, related_name="total_budget_currency", on_delete=models.CASCADE)
    total_budget = models.DecimalField(max_digits=15, decimal_places=2, null=True, default=None, db_index=True)

    capital_spend = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=None)
    scope = models.ForeignKey('aims.ActivityScope', null=True, blank=True, on_delete=models.CASCADE)
    iati_standard_version = models.CharField(max_length=30, default="")
    completion = models.FloatField(null=True)  # This caches the completion factor, NOT the completion messages. We decided that ATM breaking it out into a separate model is overkill.

    @property
    def profile_url(self) -> str:
        return reverse('activity_profile', args=[self.pk])

    @property
    def total_commitment_usd(self) -> Decimal:
        warnings.warn('Deprecated total_commitment_usd: please use commitmenttotal.dollars', DeprecationWarning)
        return self.commitmenttotal.dollars

    @property
    def total_commitment_currency(self) -> Decimal:
        warnings.warn('Deprecated total_commitment_currency: please use commitmenttotal.currency', DeprecationWarning)
        return self.commitmenttotal.currency

    @property
    def total_commitment(self) -> Decimal:
        warnings.warn('Deprecated total_commitment: please use commitmenttotal.value', DeprecationWarning)
        return self.commitmenttotal.value

    finance = ActivityFinanceManager()

    class Meta:
        verbose_name_plural = "activities"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(Activity, self).__init__(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.id}'

    @cached_property
    def title(self) -> Optional[str]:
        titles = self.title_set.all()  # type: QuerySet
        current_lang = get_language()
        default = ''
        for title in titles:
            if title.language_id == current_lang and len(title.title.strip()) > 0:
                return title.title
            if not title.language_id and title.title:
                default = title.title
            elif default is None:
                default = title.title
        if default == '':
            return None
        return default

    def _get_description(self, type_code: int) -> str:
        """ Returns the description in the current language of `type_code`.

        `type_code` is the DescriptionType code.
        If no description exists for the current language, but another description exists for another language,
        then the other language will be used.
        """

        current_language = get_language()
        descriptions = [d for d in self.descriptions if d.type_id == type_code]  # type: Sequence[Description]
        if not descriptions:
            # no description for this type of any language
            return ''

        descriptions_for_language = [d for d in descriptions if d.language_id == current_language]
        if descriptions_for_language:
            # bingo, we have a description of the right type and language
            description = descriptions_for_language[0]
        else:
            description = descriptions[0]

        return f'{description.description}'

    # TODO check this is right in the new standard - maybe remove magic numbers
    @property
    def general_description(self,):
        return self._get_description(1)

    @property
    def objective_description(self,):
        return self._get_description(2)

    @property
    def target_group_description(self,):
        return self._get_description(3)

    @property
    def sectors(self) -> "QuerySet['ActivitySector']":
        return self.activitysector_set.filter(sector__in=IATISector.objects.all())

    @property
    def sector_categories(self) -> "set['SectorCategory']":
        # return self.sectors
        return set(s.sector.category for s in self.sectors)

    @cached_property
    def descriptions(self) -> QuerySet:
        return self.description_set.all()

    @property
    def national_sectors(self) -> QuerySet:
        return self.activitysector_set.filter(sector__in=NationalSector.objects.all())

    @cached_property
    def publish_errors(self, cache: bool = True):

        # The "original" openly, mohinga, uses these publish requirements

        # Projectbank et al are less fussy, and can be overridden with 'REQUIRED_TO_PUBLISH' setting
        required_to_publish = getattr(settings, 'REQUIRED_TO_PUBLISH', openly_required_to_publish)

        requirements = {
            'title': lambda self: self.title_set.exclude(title='').exists(),
            'description': lambda self: self.description_set.exclude(description='').exists(),
            'status': lambda self: self.activity_status is not None,
            'start_date': lambda self: self.start_planned is not None,
            'sector': lambda self: self.sectors.exists(),
            'any_sector': lambda self: self.activitysector_set.exists(),  # (dird) Accept any sector to publish
            'location': lambda self: self.location_set.exists(),
            'commitment': lambda self: self.transaction_set.filter(transaction_type_id='C').exists() or not getattr(settings, 'FINANCIAL_DATA_EXISTS', False),
            'end_date': lambda self: self.end_planned is not None
        }  # type: Dict[str, Any]
        return [k for k in required_to_publish if requirements[k](self) is False]

    @property
    def aid_type(self):
        return self.default_aid_type.name if self.default_aid_type is not None else "Not Specified"

    @property
    def finance_type(self):
        return self.default_finance_type.name if self.default_finance_type is not None else "Not Specified"

    @property
    def status(self):
        return self.activity_status.name if self.activity_status is not None else "Not Specified"

    @property
    def currency(self):
        return self.default_currency.name if self.default_currency is not None else "Not Specified"

    @property
    def reporting_partner(self):
        return self.reporting_organisation.name if self.reporting_organisation is not None else "Not Specified"

    @property
    def sector_names(self):
        names = ', '.join([(s[0] if s[0] is not None else "Not Specified") for s in self.sectors.values_list('sector__name', 'percentage')])
        return names if names != '' else "Not Specified"

    @property
    def sector_breakdown(self):
        breakdown = ' '.join([(s[0] if s[0] is not None else "Not Specified") + " (" + (s[1].to_eng_string() if s[1]
                                                                                        is not None else "0.0") + ")" for s in self.sectors.values_list('sector__name', 'percentage')])
        return breakdown if breakdown != '' else "Not Specified"

    @property
    def start_date(self):
        if self.start_actual:
            return self.start_actual.strftime('%Y/%m/%d')
        elif self.start_planned:
            return self.start_planned.strftime('%Y/%m/%d')
        else:
            return "Not Specified"

    @property
    def end_date(self):
        if self.end_actual:
            return self.end_actual.strftime('%Y/%m/%d')
        elif self.end_planned:
            return self.end_planned.strftime('%Y/%m/%d')
        else:
            return "Not Specified"

    @cached_property
    def participating_orgs(self):
        return list(self.participating_organisations.all())

    @cached_property
    def implementing(self):
        return OrganisationHelper.find_organisation_in_role(self.participating_orgs, 'implementing')

    @cached_property
    def funding(self):
        return OrganisationHelper.find_organisation_in_role(self.participating_orgs, 'funding')

    @cached_property
    def extending(self):
        return OrganisationHelper.find_organisation_in_role(self.participating_orgs, 'extending')

    @cached_property
    def funding_partners(self):
        funders = [org.organisation.name if org.organisation else org.name
                   for org in OrganisationHelper.find_organisations_in_role(self.participating_orgs, 'funding')]
        if len(funders) == 0:
            return "Not Specified"
        else:
            return ', '.join(funders)

    @cached_property
    def implementing_partners(self):
        implementors = [org.organisation.name if org.organisation else org.name
                        for org in OrganisationHelper.find_organisations_in_role(self.participating_orgs, 'implementing')]
        if len(implementors) == 0:
            return "Not Specified"
        else:
            return ', '.join(implementors)

    @cached_property
    def implementing_partners_list(self):
        implementors_list = OrganisationHelper.find_organisations_in_role(self.participating_orgs, 'implementing')
        return [org.organisation for org in implementors_list if org.organisation]

    @cached_property
    def partner_ministries(self):
        accountables = [org.name for org in [
            org for org in OrganisationHelper.find_organisations_in_role(self.participating_orgs, 'accountable') if
            org.organisation is not None and org.organisation.type_id is not None
            and org.organisation.type_id == 100
        ]]
        if len(accountables) == 0:
            return "Not Specified"
        else:
            return ', '.join(accountables)

    @cached_property
    def sector_working_group(self):
        working_groups = [sector.sector.name for sector in self.activitysector_set.exclude(sector__isnull=True).filter(sector__in=NationalSector.objects.all())]
        if len(working_groups) == 0:
            return "Not Specified"
        else:
            return ', '.join(working_groups)

    @cached_property
    def locations(self):
        locations = [loc.name for loc in self.location_set.all()]
        if len(locations) == 0:
            return "Not Specified"
        else:
            return ', '.join(locations)

    def disbursements(self, transaction_filters={}):
        disbursements = self.transaction_set.filter(Q(transaction_type_id='E') | Q(transaction_type_id='D'), **transaction_filters)
        return disbursements.aggregate(disbursements=Sum('usd_value'))['disbursements'] if len(disbursements) > 0 else 0.0

    def clean_location_percentages(self):
        model_percentages = self.location_set.values_list('id', 'percentage')
        Location.objects.clean_grouped_percentages(model_percentages)

    def clean_activity_sector_percentages(self):
        for vocabulary in self.activitysector_set.values_list('vocabulary', flat=True):
            vocabulary_percentages = self.activitysector_set.filter(
                vocabulary=vocabulary
            ).values_list('id', 'percentage')
            ActivitySector.objects.clean_grouped_percentages(vocabulary_percentages)

    cleaner = managers.ActivityManager()

    @property
    def is_completed(self):
        return (self.status in ['Completion', 'Post-completion'])

    @property
    def completion_percentage(self):
        return self.completion_checks[0]

    @property
    def completion_tasks(self):
        return self.completion_checks[1]

    @cached_property
    def organisation_roles(self):
        return set(self.participating_organisations.values_list('role__name', flat=True))

    @cached_property
    def completion_checks(self):
        checks = []

        # Exclude this check for the sake of a new Activity with a pre-set reporting organisation
        # having zero completion
        if not self.reporting_organisation:
            checks += [(lambda a: True, _('The reporting organisation has not been specified.'))]
        # Require certain fields depending on the status of the activity

        if self.status in ['Pipeline/identification']:
            # Pipeline/identification does not require a date
            pass

        if self.status in ['Implementation', 'Completion', 'Post-completion']:
            checks += [
                (lambda a: not a.end_planned, _('Set a Planned End Date.')),
                (lambda a: not a.start_planned, _('Set a Planned Start Date.')),
                (lambda a: not a.start_actual, _('Set an Actual Start Date.')),
            ]

        if self.is_completed:  # Conditionally exclude this check so that a new Activity will have zero completion
            checks += [(lambda a: not a.end_actual, _('Set an Actual End Date.'))]

        if not getattr(settings, 'FINANCIAL_DATA_EXISTS', False):
            checks += [
                (lambda a: 'Funding' not in a.organisation_roles,
                 _('Add a Participating Organisation with role "Funding".')),
            ]
        checks += [
            (lambda a: 'Implementing' not in a.organisation_roles,
             _('Add a Participating Organisation with role "Implementing".')),
            (lambda a: 'Accountable' not in a.organisation_roles,
             _('Add a Participating Organisation with role "Accountable".')),
        ]
        if getattr(settings, 'FINANCIAL_DATA_EXISTS', False):
            checks += [
                (lambda a: 'Extending' not in a.organisation_roles,
                 _('Add a Participating Organisation with role "Extending".')),
            ]

        checks.append((lambda a: not a.location_set.exists(), _('Add a Location.')))

        if getattr(settings, 'FINANCIAL_DATA_EXISTS', False):
            checks += [
                (lambda a: 'Funding' not in a.organisation_roles,
                 _('Add a Transaction with a Provider Organisation.')),
                (lambda a: not a.transaction_set.filter(transaction_type__name='Disbursement').exists(),
                 _('Add a Disbursement Transaction.')),
                (lambda a: not a.default_currency,
                 _('Set a Default Currency.')),
                (lambda a: not a.default_aid_type,
                 _('Set a Default Aid Type.')),
                (lambda a: not a.default_flow_type,
                 _('Set a Default Flow Type.')),
            ]

        checks.append(
            (lambda a: not a.contactinfo_set.exclude(person_name='').exclude(telephone='').exclude(email='').exists(),
             _('Add a Contact with all of the following attributes set: Name, Telephone, Email address.')),
        )
        if getattr(settings, 'EDITOR_HAS_DOCUMENTS_TAB', True):
            checks.append((lambda a: not a.documentlink_set.exists(), _('Add a Document.')))

        tasks = []
        for check, task_message in checks:
            try:
                if check(self):
                    tasks.append(str(task_message))
            except ValueError:  # thrown when accessing a ManyToMany field on a model that is unsaved
                pass
        completion_percentage = int((1 - len(tasks) / len(checks)) * 100)
        return completion_percentage, tasks

    @property
    def commitments(self):
        return self.transaction_set.filter(transaction_type_id='C')

    def get_endorsements(self):
        """ Return a dict of organisation id -> date endorsed """
        endorsements = self.activityendorsement_set.filter(organisation__activityparticipatingorganisation__role='Accountable').distinct()
        return {e.organisation_id: str(e.created_on) for e in endorsements}

    def is_endorsed_by(self, organisation):
        return self.activityendorsement_set.filter(organisation=organisation).exists()

    @property
    def endorsement_status(self):
        potential_endorsers = self.participating_organisations.filter(role='Accountable')
        target_endorsements_count = potential_endorsers.count()
        # this filter guards against endorsements for organisations now removed from the accountable partners
        endorsements_count = self.activityendorsement_set.filter(organisation__activityparticipatingorganisation__in=potential_endorsers).count()

        if target_endorsements_count == 0:
            return ugettext('Not applicable')
        if endorsements_count == target_endorsements_count:
            return ugettext('Fully')
        if endorsements_count == 0:
            return ugettext('None')
        else:
            return ugettext('Partially')

    @property
    def iati_sync_enabled(self):
        if getattr(settings, 'OIPA_SYNC_ENABLED', False):
            # note: this is called in the activity manager, if you modify this query be careful not to cause the manager
            # to make one query per activity
            try:
                return self.oipaactivitylink.oipa_fields != []
            except OipaActivityLink.DoesNotExist:
                return False
        else:
            return False

    @property
    def submitted_for_review_timestamp(self):
        return self.activitylogmessage_set.filter(body__type='status_change', body__to='review')\
            .aggregate(Max('tstamp'))['tstamp__max']

    def can_change_openly_status(self, user: User, to_status: str) -> bool:
        """
        This method is used in the `ActivityDeserializer` class to determine whether a user
        is permitted to alter the openly status of this activity. A return value of `False`
        raises a PermissionError.

        This has different nuances in different implementations of openly.
         - dird uses a Permission defined as a ACTIVITY_PUBLISH_PERMISSION setting
         to determine who can access
         - some openlies have an `Endorsement` or `Review` process
         - some openlies permit any User from the reporting organisation to
         publish
         - some openlies permis any User from an "admin" organisation to
         publish
        """
        if user.is_superuser:
            return True

        # Permit users to publish when there is a defined permission which they have been granted
        user_permission_key = getattr(settings, 'ACTIVITY_PUBLISH_PERMISSION', None)
        # Check whether the user is in the activity reporting organisation
        user_organisation = self.reporting_organisation.users.filter(user=user).exists()
        # Check whether the user is in a designated "admin" organisation
        user_admin = Organisation.objects.filter(is_admin=True, users__user=user).exists()
        endorsements = getattr(settings, 'ENDORSEMENT_ENABLED', False)
        # For project editors with "Review" functionality

        if self.openly_status == 'blank' and to_status == 'draft':
            return True
        if user_permission_key:
            # This takes precedence over other checks
            # otherwise DIRD will allow all users to publish
            # The user has the permission as defined in settings
            # Any user can set a "blank" activity to "draft" (dird #868)
            return user.has_perm(user_permission_key)
        elif endorsements and user_admin:
            # The user is a part of an "admin" organisation
            # responsible for publishing
            return True
        elif endorsements and user_organisation and to_status != 'published':
            # The User is a part of eg a donor organisation;
            # The donor can do everything but publish
            return True
        elif user_organisation and not endorsements:
            # The user is in a reporting organisation, and endorsement
            # by a higher authority is not required (endorsments are off)
            return True
        return False

    def __date_display(self, field: str) -> Optional[str]:
        """
        Returns a ISO date or "shortened" ISO date where
        a date has been specified with less precision.
        """
        datefield = getattr(self, field)  # type: Optional[date]
        precision = getattr(self, F'{field}_detail')  # type: Optional[int]
        fmt = '%Y-%m-%d'  # Specify the formatting string passed to strftime

        if not datefield:
            return None
        if not precision:
            fmt = '%Y-%m-%d'
        elif precision == self.DateDetailChoices.Day:
            fmt = '%Y-%m-%d'
        elif precision == self.DateDetailChoices.Month:
            fmt = '%Y-%m'
        elif precision == self.DateDetailChoices.Year:
            fmt = '%Y'
        return datefield.strftime(fmt)

    @property
    def start_planned_display(self):
        return self.__date_display("start_planned")

    @property
    def end_planned_display(self):
        return self.__date_display("end_planned")

    @property
    def start_actual_display(self):
        return self.__date_display("start_actual")

    @property
    def end_actual_display(self):
        return self.__date_display("end_actual")


class CommitmentTotal(models.Model):
    '''
    This model stores a currency, value and dollars-value field for Activity
    This is useful in situations where we wish to cheaply know the Total Commitment value for an activity
    and where a QuerySet might be slower or more difficult to work with

    This ought to be triggered whenever a transaction.value, transaction.usd_value, transaction.currency changes
    It also ought to be very safe to run at high frequency

    '''
    activity = models.OneToOneField('aims.Activity', primary_key=True, related_name='commitmenttotal', on_delete=models.CASCADE)
    currency = models.ForeignKey('aims.Currency', null=True, blank=True, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    dollars = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return '{} {}{} ${}USD'.format(self.activity_id, self.value, self.currency, self.dollars)

    @classmethod
    def finance_annotate(cls, *args, **kwargs):
        '''
        Using subqueries, update all relevant and changed fields of this model

        This depends on 'usd_value' fields having correct values so you may want to run the
        methods to update per-transaction finance information first
        '''
        values = ('pk', 'currency_id', 'dollars', 'value')
        activity_id = kwargs.get('activity', None)

        def get_annotated_activities() -> Tuple[QuerySet, QuerySet]:
            '''
            Get activities for which the CommitmentTotal is out of date (1st queryset returned)
            and activities for which the CommitmentTotal is not present (2nd queryset returned)
            '''
            if activity_id:
                activities = Activity.objects.all_openly_statuses().filter(pk__in=[activity_id], transaction__transaction_type='C')
            else:
                activities = Activity.objects.all_openly_statuses().filter(transaction__transaction_type='C')

            # Order of annotation is important here
            activities = activities.annotate(
                currencies=ArrayAgg('transaction__currency_id')) \
                .annotate(currencycount=ArrayLength('currencies', index=1)) \
                .annotate(all_currencies_match=Case(
                    When(currencycount=1, then=ArrayFirst('currencies')),
                    output_field=TextField())) \
                .annotate(
                    currency_id=Coalesce('all_currencies_match', Value('USD'))) \
                .annotate(
                    dollars=Coalesce(Sum('transaction__usd_value'), Value(0))) \
                .annotate(
                    value=Case(
                        When(currencycount=1, then=Sum('transaction__value')),
                        default=F('dollars')
                    )
            )

            # Delete any outdated values
            outdated = activities.exclude(
                commitmenttotal__dollars=F('dollars'),
                commitmenttotal__value=F('value'),
                commitmenttotal__currency_id=F('currency_id')
            )

            create = activities.filter(commitmenttotal__isnull=True)

            # Returns two Activity QuerySets
            logger.debug('%s activities have outdated CommitmentTotal values', outdated.count())
            logger.debug('%s activities to have Created or replaced CommitmentTotals', create.count())
            return outdated, create

        @transaction.atomic
        def do_transaction():
            '''
            Atomically update the CommitmentTotal table
            '''
            outdated, create = get_annotated_activities()
            create_values = create.values(*values)
            outdated_values = outdated.values(*values)

            logger.info('Running update queries on CommitmentTotal table')
            cls.objects.filter(activity__in=outdated).delete()
            cls.objects.bulk_create([cls(**c) for c in create_values])
            cls.objects.bulk_create([cls(**c) for c in outdated_values])
            # Avoid the situation where we might have an "Activity" with no related "ActivityFinanceAnnotation"

            not_set = Activity.objects.all_openly_statuses().filter(commitmenttotal__isnull=True)
            logger.debug('Additional activities with no CommitmentTotal: %s' % not_set.count())
            cls.objects.bulk_create([cls(**{'pk': a.pk, 'currency_id': 'USD', 'dollars': 0, 'value': 0}) for a in not_set])
            logger.info('Returning from activity update')
        try:
            do_transaction()
        except:  # noqa
            logger.warn('Commitment Totals update failed - maybe a conflict between triggers')
        assert Activity.objects.all_openly_statuses().filter(commitmenttotal__isnull=True).count() == 0


class ActivityEndorsement(models.Model):

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('activity', 'organisation')
        permissions = (
            ("can_edit_endorsements_and_status", "Can do anything involving endorsements and publication status"),
        )

    def __str__(self):
        return '%s / %s @ %s' % (self.organisation, self.activity, self.created_on.isoformat())

    def asdictforjson(self):
        return dict(activity=self.activity.pk, organisation=self.organisation.pk, created_on=self.created_on.isoformat())


class ActivityLogmessageManager(models.Manager):
    """
    Provide querysets to generate formatting strings for
    ActivityLogmessage instances
    """
    use_in_migrations = True

    def get_queryset(self, *args, **kwargs):

        return super().get_queryset(*args, **kwargs).annotate(
            title=F('user__userorganisation__title'),
            author=Coalesce(
                Concat('user__first_name', V(' '), 'user__last_name'),
                F('user__username')
            ),
            log_type=F('body__type')
        ).prefetch_related(
            "user__userorganisation__organisations"
        ).select_related('user', 'organisation')


class ActivityLogmessage(models.Model):
    """
    Kitchen sink timestamped JSON metadata for changes to Activities.
    No structure is imposed by the schema, however, the logic of converting the JSON
    into a translated user-representable string is dependent on a proper body["type"]
    declaration, which is used for dispatching to the appropriate formatting function.
    """

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    tstamp = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    body = JSONField()  # this dict should at least have a key 'type'

    # Keys we often use are:
    # tab : Union[str, List[str]]
    # uid: Primary key to user, used for the 'ForeignKey' in the view
    # type_: What log message this is
    # org_id: Primary key to organisation, used for the 'ForeignKey' in the view

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='+')
    organisation = models.ForeignKey(Organisation, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='+')

    # The LogInfoManager adds title, author and log type to the fields and provides important select and prefetch
    objects = ActivityLogmessageManager()

    def save(self, *args, **kwargs):
        """
        Previous implementations only allowed for User ID and Organisation ID to
        be includes as JSON properties in body. This method uses those IDs and sets
        the User, Organisation from those properties if they exist.
        """

        if "uid" in self.body and self.user_id != self.body.get("uid"):
            try:
                self.user = User.objects.get(pk=self.body.get("uid"))
            except User.DoesNotExist:
                logger.error("Could not save log User Id - maybe an invalid PK was passed")

        if "org_id" in self.body and self.organisation_id != self.body.get("org_id"):
            try:
                self.organisation = Organisation.objects.get(pk=self.body.get("org_id"))
            except Organisation.DoesNotExist:
                logger.error("Could not save log Organisation Id - maybe an invalid PK was passed")

        super().save(*args, **kwargs)

    def __str__(self):
        msg, params = self.message()
        return msg.format(**params)

    @property
    def tab_name(self) -> str:
        body_tab = self.body.get('tab', None)
        if body_tab is None:
            return ''  # This should not happen except in developement
        if len(body_tab) == 1:
            return body_tab[0]
        else:
            # for the Finances tab, body_tab is like ['Finances & Budgets', 'Transactions']
            return _('{1} in {0}').format(*body_tab)

    @property
    def serialized(self):
        warnings.warn("Use ActivityLogMessageSerializer", DeprecationWarning)
        return {
            "author": self.user.get_username(),  # Added in the manager
            "message": str(self),
            "time_stamp": self.tstamp.isoformat(),
            "type": self.body["type"],
        }

    @classmethod
    def from_editor(cls, activity: Union[Activity, str], user: Union[int, User], tab: Union[str, List[str]], extra: Optional[Dict[str, Any]] = {}):
        """
        Create a log message in the format used for the ActivityEditor
        """
        try:
            alm = cls()
            alm.activity = activity if isinstance(activity, Activity) else Activity.objects.all_openly_statuses().get(pk=activity)
            alm.body = dict(
                type="editor_save",
                tab=[tab] if isinstance(tab, str) else tab,
                uid=user.id if isinstance(user, User) else user,
                **extra,
            )
            alm.save()
        except Exception as E:
            if settings.DEBUG:
                raise  # Be Noisy in development
            capture_exception(E)  # Be silent to user, but ping us on production
            return
        logger.debug(f"Log message {alm.pk} saved from {alm.activity_id}")
        logger.debug(f"{alm.body}")
        return alm

    @classmethod
    def from_editor_request(cls, request, activity: Union[Activity, str], *args, **kwargs):
        return cls.from_editor(
            activity=activity,
            tab=request.headers.get("X-Editor-Tab"),
            user=request.user,
            *args,
            **kwargs
        )

    def user_organisations(self):
        try:
            return ','.join(list(self.user.userorganisation.organisations.values_list('name', flat=True)))
        except AttributeError:
            return None

    def message(self) -> Tuple[str, dict]:
        """
        Return the id, a translatable string, and formatting parameters
        """

        try:
            body = self.body  # type: Dict
            log_type = body.get('type')  # type: str

            if log_type == 'creation':
                message = _('Created this {activity}')
                params = dict(activity=common_text.get('activity_or_program'))

            elif log_type == 'comment':
                message = body.get('comment')
                params = dict()

            elif log_type == 'editor_save':
                message = _('Edited {tabname}')
                params = dict(tabname=self.tab_name)

            elif log_type == 'status_change':
                message = _('Changed the status from {from_status} to {to_status}')
                params = dict(from_status=body['from'], to_status=body['to'])

            elif log_type == 'endorsement':
                message = _('Endorsement {action} by {organisation}')
                params = dict(organisation=self.organisation, action={'add': _('added'), 'del': _('removed')}[body['action']])

            else:
                warnings.warn("Unhandled log message type: %s", log_type)

        except Exception as E:
            warnings.warn(f'{E}')
            warnings.warn("Unhandled log message content: %s", self.id)

        return message, params


class OrganisationHelper(object):
    ''' provides helper methods for finding an organisation '''

    ROLE_CACHE = None

    @classmethod
    def get_role_id(cls, rolename):
        """returns the database id for a given role name

        :rolename: the human readable name of the role
        :returns: the id of the matchin role or None

        """
        if cls.ROLE_CACHE is None:
            cls.ROLE_CACHE = OrganisationRole.objects.values('code', 'name')
        for role in cls.ROLE_CACHE:
            if rolename.lower() in role['name'].lower():
                return role['code']
        return None

    @classmethod
    def find_organisation_in_role(cls, participating_orgs, role):
        """finds an organisation in an participating_orgs list of a particular role
        :participating_orgs: participating orgs from an activity
        :role: a human readable organisation rolename
        :returns: an org in the role from the list

        """
        role_id = cls.get_role_id(role)
        for participating_org in participating_orgs:
            if participating_org.role_id == role_id:
                return participating_org.name
        return None

    @classmethod
    def find_organisations_in_role(cls, participating_orgs, role):
        """finds all organisations in an particpating_orgs list of a particular role
        :particpating_orgs: participating orgs from an activity
        :role: a human readable organisation rolename
        :returns: an org in the role from the list

        """
        role_id = cls.get_role_id(role)
        return [org for org in participating_orgs if org.role_id == role_id]


class ActivityDateType(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=200)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class ActivityParticipatingOrganisation(models.Model):
    activity = models.ForeignKey('aims.Activity', related_name="participating_organisations", on_delete=models.CASCADE)
    organisation = models.ForeignKey('aims.Organisation', null=True, blank=True, on_delete=models.CASCADE)
    role = models.ForeignKey('aims.OrganisationRole', null=True, blank=True, on_delete=models.CASCADE)
    name = models.TextField(default="", null=True, blank=True)

    class Meta:
        unique_together = (('activity', 'organisation', 'role'),)

    def __str__(self,):
        return "%s: %s - %s" % (self.activity, self.organisation, self.name)

    def save(self, *args, **kwargs):
        if self.organisation:
            self.name = self.organisation.name
        super(ActivityParticipatingOrganisation, self).save(*args, **kwargs)


class PolicySignificance(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class ActivityPolicyMarker(models.Model):
    policy_marker = models.ForeignKey('aims.PolicyMarker', null=True, blank=True, on_delete=models.CASCADE)
    alt_policy_marker = models.CharField(max_length=200, default="", null=True, blank=True)
    activity = models.ForeignKey('aims.Activity', on_delete=models.CASCADE)
    vocabulary = models.ForeignKey('aims.Vocabulary', null=True, blank=True, on_delete=models.CASCADE)
    policy_significance = models.ForeignKey('aims.PolicySignificance', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self,):
        return "%s - %s" % (self.activity, self.policy_marker)


class ActivitySector(TimeStampedModel):
    activity = models.ForeignKey('aims.Activity', on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, null=True, blank=True, on_delete=models.CASCADE)
    alt_sector_name = models.CharField(max_length=200, default="")
    vocabulary = models.ForeignKey('aims.Vocabulary', null=True, blank=True, on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=None)
    objects = managers.ActivitySectorManager()

    class Meta:
        unique_together = (('activity', 'sector'),)

    def __str__(self,):
        return "%s - %s" % (self.activity, self.sector)


class TagVocabulary(models.Model):
    """ A category of tags, for example, the SDG targets. """
    code = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=140)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class Tag(TimeStampedModel):
    """ A potential tag for activities. For example, a specific SDG target. """
    code = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=2048)
    vocabulary = models.ForeignKey('aims.TagVocabulary', on_delete=models.CASCADE)

    def __str__(self,):
        return self.name


class ActivityTag(TimeStampedModel):
    """ The link between activities and tags. """
    activity = models.ForeignKey('aims.Activity', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('activity', 'tag'),)

    def __str__(self,):
        return '%s - %s' % (self.activity, self.tag)

    @classmethod
    def set_for_activity(cls, activity: 'Activity', sources: Iterable[str]):
        '''Reset the Tags for a particular activity'''
        sets = {
            'has': set(cls.objects.filter(activity=activity).values_list('tag', flat=True)),
            'wants': set(sources)
        }
        sets['delete'] = sets['has'] - sets['wants']
        sets['create'] = sets['wants'] - sets['has']
        # We want this to be a "all pass or all fail"
        with transaction.atomic():
            cls.objects.filter(activity=activity, tag__in=sets['delete']).delete()
            for fs in sets['create']:
                cls.objects.create(activity=activity, tag=Tag.objects.get(pk=fs))


class ContactInfo(models.Model):
    uuid = models.UUIDField(blank=True, null=True, unique=True, default=uuid.uuid4)
    activity = models.ForeignKey('aims.Activity', on_delete=models.CASCADE)
    person_name = models.CharField(max_length=100, default="")
    organisation = models.CharField(max_length=200, default="")
    telephone = models.CharField(max_length=100, default="")
    email = models.TextField(default="")
    mailing_address = models.TextField(default="")
    website = models.CharField(max_length=255, default="")
    contact_type = models.ForeignKey('aims.ContactType', null=True, blank=True, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=150, default="")

    def __str__(self,):
        return "%s - %s" % (self.activity, self.person_name)


class ActivityWebsite(models.Model):
    activity = models.ForeignKey('aims.Activity', on_delete=models.CASCADE)
    url = models.CharField(max_length=150)

    def __str__(self,):
        return "%s - %s" % (self.activity, self.url)


class OtherIdentifier(models.Model):
    activity = models.ForeignKey('aims.Activity', on_delete=models.CASCADE)
    owner_ref = models.CharField(max_length=100, default="")
    owner_name = models.CharField(max_length=100, default="")
    identifier = models.CharField(max_length=100)

    def __str__(self,):
        return "%s - %s" % (self.activity, self.identifier)


class ActivityRecipientCountry(models.Model):
    activity = models.ForeignKey('aims.Activity', on_delete=models.CASCADE)
    country = models.ForeignKey('geodata.Country', on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=None)

    def __str__(self,):
        return "%s - %s" % (self.activity, self.country)


class ActivityRecipientRegion(models.Model):
    activity = models.ForeignKey('aims.Activity', on_delete=models.CASCADE)
    region = models.ForeignKey('geodata.Region', on_delete=models.CASCADE)
    region_vocabulary = models.ForeignKey('aims.RegionVocabulary', default=1, on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=None)

    def __str__(self,):
        return "%s - %s" % (self.activity, self.region)


class PlannedDisbursement(models.Model):
    activity = models.ForeignKey('aims.Activity', on_delete=models.CASCADE)
    period_start = models.CharField(max_length=100, default="")
    period_end = models.CharField(max_length=100, default="")
    value_date = models.DateField(null=True)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.ForeignKey('aims.Currency', null=True, blank=True, on_delete=models.CASCADE)
    updated = models.DateField(null=True, default=None)

    def __str__(self,):
        return "%s - %s" % (self.activity, self.period_start)


class RelatedActivityType(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class RelatedActivity(models.Model):
    current_activity = models.ForeignKey('aims.Activity', related_name="related_activities", on_delete=models.CASCADE)
    type = models.ForeignKey(RelatedActivityType, max_length=200, null=True, blank=True, on_delete=models.CASCADE)
    ref = models.CharField(max_length=200, default="")
    text = models.TextField(default="")

    def __str__(self,):
        return "%s - %s" % (self.current_activity, self.type)


class FileFormat(models.Model):
    code = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class DocumentCategoryCategory(models.Model):
    code = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=100)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class DocumentCategory(models.Model):
    code = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(DocumentCategoryCategory, on_delete=models.CASCADE)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class DocumentLink(LocalDataMixin):
    activity = models.ForeignKey('aims.Activity', on_delete=models.CASCADE, null=True, blank=True)
    organisation = models.ForeignKey('aims.Organisation', on_delete=models.CASCADE, null=True, blank=True)
    url = models.TextField(max_length=500)
    file_format = models.ForeignKey('aims.FileFormat', null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="")
    categories = models.ManyToManyField('aims.DocumentCategory', blank=True)
    iso_date = models.DateField(null=True, blank=True)
    language = models.ForeignKey('aims.Language', null=True, blank=True, default=None, on_delete=models.CASCADE)
    private = models.BooleanField(null=True)
    types = models.ManyToManyField('aims.ResourceType', related_name='resources', related_query_name='resource')
    supported_by = models.CharField(max_length=255, default="")
    endorsed_by = models.CharField(max_length=255, default="")
    audience = models.CharField(max_length=255, default="")

    def __str__(self,):
        return "%s - %s" % (self.activity, self.url)


DEFAULT_LANGUAGE_CODE = 'en'  # TODO: Move to settings?

StagedNarrative = namedtuple('StagedNarrative', 'content, language, field_name, related_field_name')


class NarratedModel(models.Model):
    """
    IATI allows a number of very similar "text tag" fields. This framework builds on Zimmerman's IATI models
    (for proper relational modelling and code sharing) and adds handlers for getting/setting (for simplicity especially within
    our editor / exports).

    When a model inherits from this class,
    it receives a property '_narrative_language'
    which acts as a staging point for changes to a Narrative (title, description, or notes)
    with a 'language' and 'content'.

    On saving the model, this is iterated through and the related
    intermediate model to Narrative and instance of Narrative are created or updated as
    necessary.
    """

    class Meta:
        abstract = True

    # Temporary storage for a Narrative to stage
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._narratives = []

    # The language which narratives will be saved in - note this is accessible through 'narrative_language property'
    _narrative_language = DEFAULT_LANGUAGE_CODE

    def set_narrative_language(self, language):
        self._narrative_language = language

    def get_narrative_language(self):
        return self._narrative_language
    narrative_language = property(get_narrative_language, set_narrative_language)

    # Getter function for a narrative with a given field name and language
    def _get_narrative(self, field_name, language):
        try:
            return getattr(self, field_name).narratives.get(language=language or self.narrative_language).content
        except (Narrative.DoesNotExist, AttributeError):
            return None
        except Narrative.MultipleObjectsReturned:
            logger.error('Expected a single narrative for %s %s', self, field_name)
            contents = getattr(self, field_name).narratives.filter(language=language or self.narrative_language)
            logger.error('Content options: %s', contents.values_list('content', flat=True))
            return contents.order_by('id').first().content

    # Stage a Narrative object for saving
    def _set_narrative(self, content: str, language: str, field_name: str, related_field_name: str) -> None:
        self._narratives.append(StagedNarrative(content, language or self.narrative_language, field_name, related_field_name))

    # Post-save, run through the _narratives array and create them.
    def _save_narratives(self):
        for narrative_data in self._narratives:
            if hasattr(self, narrative_data.field_name):
                through_model = getattr(self, narrative_data.field_name)
            else:
                through_model = self._meta.get_field(narrative_data.field_name).related_model.objects.create(**dict({narrative_data.related_field_name: self}))

            narrative = through_model.narratives.get_or_create(
                language_id=narrative_data.language or self._narrative_language,
                activity=self.get_activity()
            )[0]
            if not narrative.content or narrative.content == '':
                narrative.delete()
            narrative.content = narrative_data.content or ''
            narrative.save()
        self._narratives = []

    def save(self, *args, **kwargs):
        super(NarratedModel, self).save(*args, **kwargs)
        self._save_narratives()


class Result(NarratedModel):
    activity = models.ForeignKey('aims.Activity', related_name="results", on_delete=models.CASCADE)
    type = models.ForeignKey('iati_codelists.ResultType', null=True, blank=True, default=None, on_delete=models.CASCADE)
    aggregation_status = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return "Result"

    def get_activity(self):
        return self.activity

    # These handle Narrative fields for Title and Description which
    # provides a more "traditional" interface for retrieving translated fields.

    def _get_title(self, language=None):
        return self._get_narrative('resulttitle', language)

    def _set_title(self, content, language=None):
        self._set_narrative(content, language, field_name='resulttitle', related_field_name='result')

    def _get_description(self, language=None):
        return self._get_narrative('resultdescription', language)

    def _set_description(self, content: str, language: str = None):
        self._set_narrative(content, language, field_name='resultdescription', related_field_name='result')

    title = property(_get_title, _set_title)
    description = property(_get_description, _set_description)


class ResultTitle(NarrativeMixin):
    result = models.OneToOneField(Result, on_delete=models.CASCADE)

    def get_activity(self):
        return self.result.activity


class ResultDescription(NarrativeMixin):
    result = models.OneToOneField(Result, on_delete=models.CASCADE)

    def get_activity(self):
        return self.result.activity


class ResultIndicator(NarratedModel):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    baseline_year = models.IntegerField(null=True, blank=True, default=None)
    baseline_value = models.CharField(null=True, blank=True, default=None, max_length=100)
    measure = models.ForeignKey(
        'iati_codelists.IndicatorMeasure',
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
    )
    ascending = models.BooleanField(default=True)

    # This is not part of the IATI standard
    # This field should auto update when a narrative or resultindicator is created or updated,
    # and when a ResultIndicator is created or updated
    last_updated = models.DateField(null=True, blank=True)

    def get_activity(self):
        return self.result.activity

    def __str__(self):
        return "baseline year: %s" % self.baseline_year

    # These handle Narrative fields for Title, Description, and BaselineComment which
    # provides a more "traditional" interface for retrieving translated fields.

    def _get_title(self, language=None):
        return self._get_narrative('resultindicatortitle', language)

    def _set_title(self, content, language=None):
        self._set_narrative(content, language, field_name='resultindicatortitle', related_field_name='result_indicator')

    def _get_description(self, language=None):
        return self._get_narrative('resultindicatordescription', language)

    def _set_description(self, content, language=None):
        self._set_narrative(content, language, field_name='resultindicatordescription', related_field_name='result_indicator')

    def _get_baselinecomment(self, language=None):
        return self._get_narrative('resultindicatorbaselinecomment', language)

    def _set_baselinecomment(self, content, language=None):
        self._set_narrative(content, language, field_name='resultindicatorbaselinecomment', related_field_name='result_indicator')

    title = property(_get_title, _set_title)
    description = property(_get_description, _set_description)
    comment = property(_get_baselinecomment, _set_baselinecomment)
    uuid = models.UUIDField(default=uuid.uuid4)


class SimpleResultIndicator(ResultIndicator):
    """
    Proxy model adding 'target' and 'actual' methods
    for the simpler result indicators we use for DIRD
    """

    class Meta:
        proxy = True

    def _get_target(self):
        ri = self.resultindicatorperiod_set.first()
        if ri:
            return ri.target

    def _get_actual(self):
        ri = self.resultindicatorperiod_set.first()
        if ri:
            return ri.actual

    def _set_target(self, target):
        ri = self.resultindicatorperiod_set.first() or ResultIndicatorPeriod.objects.create(result_indicator=self)
        ri.target = target
        ri.save()

    def _set_actual(self, actual):
        ri = self.resultindicatorperiod_set.first() or ResultIndicatorPeriod.objects.create(result_indicator=self)
        ri.actual = actual
        ri.save()

    target = property(_get_target, _set_target)
    actual = property(_get_actual, _set_actual)


class ResultIndicatorReference(models.Model):
    result_indicator = models.ForeignKey(ResultIndicator, on_delete=models.CASCADE)
    code = models.CharField(max_length=255)
    vocabulary = models.ForeignKey('iati_vocabulary.IndicatorVocabulary', on_delete=models.CASCADE)
    vocabulary_uri = models.URLField(null=True, blank=True)

    def get_activity(self):
        return self.result_indicator.result.activity


class ResultIndicatorTitle(NarrativeMixin):
    result_indicator = models.OneToOneField(ResultIndicator, on_delete=models.CASCADE)
    primary_name = models.CharField(
        max_length=255,
        null=False,
        blank=True,
        default="",
        db_index=True)

    def get_activity(self):
        return self.result_indicator.result.activity


class ResultIndicatorDescription(NarrativeMixin):
    result_indicator = models.OneToOneField(ResultIndicator, on_delete=models.CASCADE)

    def get_activity(self):
        return self.result_indicator.result.activity


class ResultIndicatorBaselineComment(NarrativeMixin):
    result_indicator = models.OneToOneField(ResultIndicator, on_delete=models.CASCADE)

    def get_activity(self):
        return self.result_indicator.result.activity


class ResultIndicatorKeyProgressStatement(NarrativeMixin):
    result_indicator = models.OneToOneField(ResultIndicator, on_delete=models.CASCADE)

    def get_activity(self):
        return self.result_indicator.result.activity


class ResultIndicatorPeriod(NarratedModel):
    result_indicator = models.ForeignKey(ResultIndicator, on_delete=models.CASCADE)
    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)

    target = models.DecimalField(max_digits=25, decimal_places=10, null=True, blank=True)
    actual = models.DecimalField(max_digits=25, decimal_places=10, null=True, blank=True)

    def _get_actualcomment(self, language=None):
        return self._get_narrative('resultindicatorperiodactualcomment', language)

    def _set_actualcomment(self, content, language=None):
        self._set_narrative(content, language, field_name='resultindicatorperiodactualcomment', related_field_name='result_indicator_period')

    actual_comment = property(_get_actualcomment, _set_actualcomment)

    def _get_targetcomment(self, language=None):
        return self._get_narrative('resultindicatorperiodtargetcomment', language)

    def _set_targetcomment(self, content, language=None):
        self._set_narrative(content, language, field_name='resultindicatorperiodtargetcomment', related_field_name='result_indicator_period')

    target_comment = property(_get_targetcomment, _set_targetcomment)

    def __str__(self):
        return "target: %s, actual: %s" % (self.target, self.actual)

    def get_activity(self):
        return self.result_indicator.result.activity


class ResultIndicatorPeriodTargetLocation(models.Model):
    result_indicator_period = models.ForeignKey(ResultIndicatorPeriod, on_delete=models.CASCADE)
    ref = models.CharField(max_length=50)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.ref

    def get_activity(self):
        return self.result_indicator_period.result_indicator.result.activity


class ResultIndicatorPeriodActualLocation(models.Model):
    result_indicator_period = models.ForeignKey(ResultIndicatorPeriod, on_delete=models.CASCADE)
    ref = models.CharField(max_length=50)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.ref

    def get_activity(self):
        return self.result_indicator_period.result_indicator.result.activity


class ResultIndicatorPeriodTargetDimension(models.Model):
    result_indicator_period = models.ForeignKey(ResultIndicatorPeriod, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return "%s: %s" % (self.name, self.value)

    def get_activity(self):
        return self.result_indicator_period.result_indicator.result.activity


class ResultIndicatorPeriodActualDimension(models.Model):
    result_indicator_period = models.ForeignKey(ResultIndicatorPeriod, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return "%s: %s" % (self.name, self.value)

    def get_activity(self):
        return self.result_indicator_period.result_indicator.result.activity


class ResultIndicatorPeriodTargetComment(NarrativeMixin):
    result_indicator_period = models.OneToOneField(ResultIndicatorPeriod, on_delete=models.CASCADE)

    def get_activity(self):
        return self.result_indicator_period.result_indicator.result.activity


class ResultIndicatorPeriodActualComment(NarrativeMixin):
    result_indicator_period = models.OneToOneField(ResultIndicatorPeriod, on_delete=models.CASCADE)

    def get_activity(self):
        return self.result_indicator_period.result_indicator.result.activity


class Description(models.Model):
    activity = models.ForeignKey('aims.Activity', on_delete=models.CASCADE)
    description = models.TextField(default="", max_length=40000)
    language = models.ForeignKey('aims.Language', null=True, blank=True, on_delete=models.CASCADE)
    type = models.ForeignKey('aims.DescriptionType', related_name="description_type", null=True, blank=True, on_delete=models.CASCADE)
    rsr_description_type_id = models.IntegerField(null=True, default=None)  # remove

    class Meta:
        unique_together = (('activity', 'type', 'language'),)

    def __str__(self,):
        return "%s - %s" % (self.activity, self.type)


class BudgetStatus(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=20)


class BudgetType(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    language = models.CharField(max_length=2)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class Budget(models.Model):
    activity = models.ForeignKey('aims.Activity', on_delete=models.CASCADE)
    type = models.ForeignKey(BudgetType, null=False, default=1, on_delete=models.CASCADE)
    status = models.ForeignKey(BudgetStatus, null=False, default=1, on_delete=models.CASCADE)
    period_start = models.DateField(blank=True, null=True, default=None)
    period_end = models.DateField(blank=True, null=True, default=None)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    value_date = models.DateField(null=True, default=None)
    currency = models.ForeignKey('aims.Currency', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self,):
        return "%s - %s" % (self.activity, self.period_start)

    usd_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    objects = managers.QuarterlyBudgetsManager()


class BudgetExchangeRate(models.Model):

    budget = models.OneToOneField('aims.Budget', primary_key=True, on_delete=models.CASCADE)
    exchangerate = models.ForeignKey('aims.CurrencyExchangeRate', on_delete=models.CASCADE)

    objects = managers.BudgetExchangeRateManager()


class TransactionExchangeRate(models.Model):

    transaction = models.OneToOneField('aims.Transaction', primary_key=True, on_delete=models.CASCADE)
    exchangerate = models.ForeignKey('aims.CurrencyExchangeRate', on_delete=models.CASCADE)

    objects = managers.TransactionExchangeRateManager()


class Condition(models.Model):
    activity = models.ForeignKey('aims.Activity', on_delete=models.CASCADE)
    text = models.TextField(default="")
    type = models.ForeignKey('aims.ConditionType', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self,):
        return "%s - %s" % (self.activity, self.type)


class Title(models.Model):
    activity = models.ForeignKey('aims.Activity', on_delete=models.CASCADE)
    title = models.CharField(max_length=2000, db_index=True)
    language = models.ForeignKey('aims.Language', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self,):
        return "%s - %s" % (self.activity, self.title)

    class Meta:
        unique_together = (('activity', 'language'),)


class ConditionType(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    language = models.CharField(max_length=2)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class Location(models.Model):
    activity = models.ForeignKey('aims.Activity', on_delete=models.CASCADE)
    ref = models.CharField(max_length=200, default="")  # new in v1.04
    name = models.TextField(max_length=1000, default="")
    type = models.ForeignKey('aims.LocationType', null=True, blank=True, related_name="deprecated_location_type", on_delete=models.CASCADE)  # deprecated as of v1.04
    type_description = models.CharField(max_length=200, default="")
    description = models.TextField(default="")
    activity_description = models.TextField(default="")
    description_type = models.ForeignKey('aims.DescriptionType', null=True, blank=True, on_delete=models.CASCADE)
    adm_country_iso = models.ForeignKey('geodata.Country', null=True, blank=True, on_delete=models.CASCADE)  # deprecated as of v1.04
    adm_country_adm1 = models.CharField(max_length=100, default="")  # deprecated as of v1.04
    adm_country_adm2 = models.CharField(max_length=100, default="")  # deprecated as of v1.04
    adm_country_name = models.CharField(max_length=200, default="")  # deprecated as of v1.04
    adm_code = models.CharField(max_length=255, default="")  # new in v1.04
    adm_vocabulary = models.ForeignKey('aims.GeographicVocabulary', null=True, blank=True, related_name="administrative_vocabulary", on_delete=models.CASCADE)  # new in v1.04
    adm_level = models.IntegerField(null=True, default=None)  # new in v1.04
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=None)
    latitude = models.CharField(max_length=70, default="")  # deprecated as of v1.04
    longitude = models.CharField(max_length=70, default="")  # deprecated as of v1.04
    precision = models.ForeignKey('aims.GeographicalPrecision', null=True, blank=True, on_delete=models.CASCADE)
    gazetteer_entry = models.CharField(max_length=70, default="")  # deprecated as of v1.04
    gazetteer_ref = models.ForeignKey('aims.GazetteerAgency', null=True, blank=True, on_delete=models.CASCADE)  # deprecated as of v1.04
    location_reach = models.ForeignKey('aims.GeographicLocationReach', null=True, blank=True, on_delete=models.CASCADE)  # new in v1.04
    location_id_vocabulary = models.ForeignKey('aims.GeographicVocabulary', null=True, blank=True, related_name="location_id_vocabulary", on_delete=models.CASCADE)  # new in v1.04
    location_id_code = models.CharField(max_length=255, default="")  # new in v1.04
    point_srs_name = models.CharField(max_length=255, default="")  # new in v1.04
    point_pos = models.CharField(max_length=255, default="")  # new in v1.04
    exactness = models.ForeignKey('aims.GeographicExactness', null=True, blank=True, on_delete=models.CASCADE)  # new in v1.04
    feature_designation = models.ForeignKey('aims.LocationType', null=True, blank=True, related_name="feature_designation", on_delete=models.CASCADE)  # new in v1.04
    location_class = models.ForeignKey('aims.GeographicLocationClass', null=True, blank=True, on_delete=models.CASCADE)  # new in v1.04
    area = models.ForeignKey(Area, null=True, related_name='area_activities', on_delete=models.CASCADE)
    objects = managers.LocationManager()

    class Meta:
        ordering = ('id',)

    def __str__(self,):
        return "%s - %s" % (self.activity, self.name)


class LocationTypeCategory(models.Model):
    code = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class LocationType(models.Model):
    code = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)
    description = models.TextField(default="")
    category = models.ForeignKey('aims.LocationTypeCategory', on_delete=models.CASCADE)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class IATISourceRef(models.Model):
    ref = models.CharField(
        max_length=70)
    title = models.CharField(max_length=255, default="")
    url = models.CharField(
        max_length=255,
        unique=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now_add=True, editable=False)
    last_found_in_registry = models.DateTimeField(default=None, null=True)
    activity_count = models.IntegerField(null=True, default=None)
    is_parsed = models.BooleanField(null=False, default=False)

    class Meta:
        verbose_name_plural = "IATI XML sources"
        ordering = ["ref"]

    def __str__(self):
        return self.ref


class DocumentUpload(TimeStampedModel):

    def document_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/activity_<id>/<filename>

        documentlink = instance.documentlink

        if documentlink.organisation:
            organisation = documentlink.organisation_id

        elif instance.user:
            try:
                organisation = instance.user.userorganisation.organisations.first().pk
            except (UserOrganisation.DoesNotExist, Organisation.DoesNotExist):
                organisation = 'none'

        activity = documentlink.activity_id or 'none'

        return 'by_organisation/{0}/by_activity/{1}/{2}'.format(organisation, activity, filename)

    def activity_path(self, *args, **kwargs):
        '''
        Backwards compatibility
        '''
        return self.document_path(*args, **kwargs)

    doc = models.FileField(upload_to=activity_path)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    documentlink = models.OneToOneField('aims.DocumentLink', primary_key=True, related_name='upload', on_delete=models.CASCADE)


class DocumentNarrative(models.Model):
    document = models.ForeignKey('aims.DocumentLink', related_name='narrative', on_delete=models.CASCADE)
    description = models.TextField(default="", max_length=40000)
    language = models.ForeignKey('aims.Language', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('document', 'language'),)


# Monkeypatch django auth User with method retrieving an attached organisation if one exists
@property
def organisations(user) -> "QuerySet[Organisation]":
    if hasattr(user, 'userorganisation'):
        return user.userorganisation.organisations.all()
    else:
        return Organisation.objects.none()


@property
def organisation(user) -> Union[Organisation, None]:
    return user.organisations.first() if user.organisations else None


@property
def organisation_count(user):
    return len(user.organisations)


setattr(User, 'organisations', organisations)
setattr(User, 'organisation', organisation)
setattr(User, 'organisation_count', organisation_count)


# Migrated iati models
class AidTypeFlag(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class GeographicVocabulary(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=255)
    description = models.TextField(default="")
    category = models.CharField(max_length=50)
    url = models.TextField(default="")

    def __str__(self,):
        return "%s - %s" % (self.activity, self.type)


class GeographicalPrecision(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=80)
    description = models.TextField()

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class GazetteerAgency(models.Model):
    code = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=80)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class GeographicLocationReach(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=80)

    def __str__(self,):
        return "%s - %s" % (self.activity, self.type)


class GeographicExactness(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=160)
    description = models.TextField(default="")
    category = models.CharField(max_length=50)
    url = models.TextField(default="")

    def __str__(self,):
        return "%s - %s" % (self.activity, self.type)


class OrganisationIdentifier(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    abbreviation = models.CharField(max_length=30, default=None, null=True)
    name = models.CharField(max_length=250, default=None, null=True)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class PublisherType(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class VerificationStatus(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class BudgetIdentifier(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=160)
    category = models.CharField(max_length=120)
    sector = models.CharField(max_length=100)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class BudgetIdentifierSectorCategory(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=160)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class BudgetIdentifierSector(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=160)
    category = models.ForeignKey('aims.BudgetIdentifierSectorCategory', on_delete=models.CASCADE)


class LoanRepaymentPeriod(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class LoanRepaymentType(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=40)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class OrganisationRegistrationAgency(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=160)
    description = models.TextField(default="")
    category = models.CharField(max_length=10)
    category_name = models.CharField(max_length=120)
    url = models.TextField(default="")

    def __str__(self,):
        return "%s - %s" % (self.activity, self.type)


class Ffs(models.Model):
    activity = models.ForeignKey('aims.Activity', on_delete=models.CASCADE)
    extraction_date = models.DateField(null=True, default=None)
    priority = models.BooleanField(default=False)
    phaseout_year = models.IntegerField(null=True)

    def __str__(self,):
        return "%s" % (self.extraction_date)


class FfsForecast(models.Model):
    ffs = models.ForeignKey(Ffs, on_delete=models.CASCADE)
    year = models.IntegerField(null=True)
    currency = models.ForeignKey('aims.Currency', on_delete=models.CASCADE)
    value_date = models.DateField(null=True, default=None)
    value = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self,):
        return "%s" % (self.year)


class CrsAdd(models.Model):
    activity = models.ForeignKey('aims.Activity', on_delete=models.CASCADE)
    aid_type_flag = models.ForeignKey('aims.AidTypeFlag', on_delete=models.CASCADE)
    aid_type_flag_significance = models.IntegerField(null=True, default=None)

    def __str__(self,):
        return "%s" % (self.id)


class CrsAddLoanTerms(models.Model):
    crs_add = models.ForeignKey(CrsAdd, on_delete=models.CASCADE)
    rate_1 = models.IntegerField(null=True, default=None)
    rate_2 = models.IntegerField(null=True, default=None)
    repayment_type = models.ForeignKey(LoanRepaymentType, null=True, blank=True, on_delete=models.CASCADE)
    repayment_plan = models.ForeignKey(LoanRepaymentPeriod, null=True, blank=True, on_delete=models.CASCADE)
    repayment_plan_text = models.TextField(default="")
    commitment_date = models.DateField(null=True, default=None)
    repayment_first_date = models.DateField(null=True, default=None)
    repayment_final_date = models.DateField(null=True, default=None)

    def __str__(self,):
        return "%s" % (self.crs_add_id)


class CrsAddLoanStatus(models.Model):
    crs_add = models.ForeignKey(CrsAdd, on_delete=models.CASCADE)
    year = models.IntegerField(null=True, default=None)
    value_date = models.DateField(null=True, default=None)
    currency = models.ForeignKey('aims.Currency', null=True, blank=True, on_delete=models.CASCADE)
    interest_received = models.DecimalField(null=True, default=None, max_digits=15, decimal_places=2)
    principal_outstanding = models.DecimalField(null=True, default=None, max_digits=15, decimal_places=2)
    principal_arrears = models.DecimalField(null=True, default=None, max_digits=15, decimal_places=2)
    interest_arrears = models.DecimalField(null=True, default=None, max_digits=15, decimal_places=2)

    def __str__(self,):
        return "%s" % (self.year)


class BudgetIdentifierVocabulary(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class CountryBudgetItem(models.Model):
    activity = models.ForeignKey('aims.Activity', on_delete=models.CASCADE)
    vocabulary = models.ForeignKey(BudgetIdentifierVocabulary, null=True, on_delete=models.CASCADE)
    vocabulary_text = models.CharField(max_length=255, default="")
    code = models.CharField(max_length=50, default="")
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=None)
    description = models.TextField(default="")

    def __str__(self,):
        return "%s - %s" % (self.activity, self.code)


class AidTypeCategory(models.Model):
    code = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class AidType(models.Model):
    code = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(AidTypeCategory, on_delete=models.CASCADE)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class OrganisationRole(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class Language(models.Model):
    code = models.CharField(primary_key=True, max_length=2)
    name = models.CharField(max_length=80)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class ContactType(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=40)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class Transaction(models.Model):
    activity = models.ForeignKey('aims.Activity', null=True, blank=True, on_delete=models.CASCADE)
    aid_type = models.ForeignKey('aims.AidType', null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(default="", null=True, blank=True)
    description_type = models.ForeignKey('aims.DescriptionType', null=True, blank=True, on_delete=models.CASCADE)
    disbursement_channel = models.ForeignKey('aims.DisbursementChannel', null=True, blank=True, on_delete=models.CASCADE)
    finance_type = models.ForeignKey('aims.FinanceType', null=True, blank=True, on_delete=models.CASCADE)
    flow_type = models.ForeignKey('aims.FlowType', null=True, blank=True, on_delete=models.CASCADE)
    provider_organisation = models.ForeignKey('aims.Organisation', related_name="transaction_providing_organisation", null=True, blank=True, on_delete=models.CASCADE)
    provider_organisation_name = models.CharField(max_length=255, default="", null=True, blank=True)
    provider_activity = models.CharField(max_length=100, null=True)
    receiver_organisation = models.ForeignKey('aims.Organisation', related_name="transaction_receiving_organisation", null=True, blank=True, on_delete=models.CASCADE)
    receiver_organisation_name = models.CharField(max_length=255, default="")
    tied_status = models.ForeignKey('aims.TiedStatus', null=True, blank=True, on_delete=models.CASCADE)
    transaction_date = models.DateField(null=True, default=None)
    transaction_type = models.ForeignKey('aims.TransactionType', null=True, blank=True, on_delete=models.CASCADE)
    value_date = models.DateField(null=True, default=None)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.ForeignKey('aims.Currency', null=True, blank=True, on_delete=models.CASCADE)
    ref = models.CharField(max_length=255, default="")

    date_created = models.DateTimeField(verbose_name=_('Date Created'), auto_now_add=True, null=True)
    date_modified = models.DateTimeField(verbose_name=_('Last Modified'), auto_now=True, null=True)

    # ValueFieldManager provides a 'update_usd_value' function to update the 'usd_value' field
    # Transaction.objects.update_usd_value()
    # Before running this you may wish to run TransactionExchangeRate.objects.fetch_currency_rates()
    objects = managers.TransactionManager()

    usd_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self,):
        return "%s: %s - %s" % (self.activity, self.transaction_type, self.transaction_date)

    @property
    def openly_status(self):
        return self.activity.openly_status

    def validate_usd_value(self):
        """
        Check and update an existing usd_value field, for individual saves
        For bulk ops please use the manager
        """
        # Verify that an exchange rate for the date/currency exists
        # Requires a call to openexchangerate API

        if not self.currency_id:
            calculated_value = None
        elif self.currency_id == 'USD':
            if self.usd_value != self.value:
                calculated_value = self.value
            else:
                calculated_value = self.value
        else:
            exchangerate = CurrencyExchangeRate.objects.fetch(date=self.value_date, currency_list=self.currency_id).first()
            if exchangerate:
                TransactionExchangeRate.objects.filter(transaction=self).delete()
                TransactionExchangeRate.objects.create(transaction=self, exchangerate=exchangerate)
                calculated_value = self.value * exchangerate.rate
            else:
                calculated_value = None
        if (calculated_value and not self.usd_value):
            if (calculated_value != self.usd_value):
                logger.debug('Transaction usd value updated %s %s', self.usd_value, calculated_value)
                self.usd_value = calculated_value
                self.save()
        elif calculated_value and abs(calculated_value - self.usd_value) >= 0.01:
            logger.debug('Transaction usd value updated %s %s', self.usd_value, calculated_value)
            self.usd_value = calculated_value
            self.save()
        elif not calculated_value:
            logger.warning('Unable to set exchange rate for %s %s', self.currency_id, self.value_date)

    def save(self, *args, **kwargs):
        '''
        Override the save method to prevent setting
        the "provider organisation" to None only if it already exists
        '''

        if 'dird_templates' in settings.INSTALLED_APPS:
            # The Expenditures model extends Transaction
            # and does not make use of the ProviderOrganisation field
            return super().save(*args, **kwargs)

        if self.provider_organisation:  # Carry on save
            return super().save(*args, **kwargs)

        else:  # Try to prevent null values in the database by retaining `provider_organisation` on save
            logger.warn('Attempted to save Transaction %s - Activity %s - with no Provider Organisation', self.pk, self.activity_id)
            try:
                self.provider_organisation = Transaction.objects.get(pk=self.pk).provider_organisation
            except Transaction.DoesNotExist:
                pass
        if not self.provider_organisation:
            logger.error('Transaction %s - Activity %s - provider_organisation does not exist in the save request or db', self.pk, self.activity_id)
        else:
            logger.info('Transaction %s - Activity %s - A provider organisation was retained', self.pk, self.activity_id)

        try:
            assert self.provider_organisation
        except AssertionError:
            if settings.DEBUG:
                raise
            else:
                # Throw a Sentry error when blank. We don't want this ever to be blank
                capture_exception()

        return super().save(*args, **kwargs)


class ResultIndicatorType(models.Model):
    """
    This is Not an IATI model, it's something which Josh and Sergio hacked up

    :param display: One of "Narrative" or "Values" as a hint to front end how to display an indicator card
    :param sector: Group to put this card into for filtering
    :param result_indicator: Foreign key on ResultIndicator

    :todo: Set sector to a proper FK

    """

    display_choices = (
        ("Narrative", "Narrative"),
        ("Values", "Values")
    )

    sector_choices = (
        ("Health", "Health"),
        ("Education", "Education"),
        ("Water & Sanitation", "Water & Sanitation"),
        ("Social Protection", "Social Protection"),
        ("Nutrition", "Nutrition"),
        ("Gender", "Gender"),
        ("Disability", "Disability"),
        ("Multi-sectoral", "Multi-sectoral"),
    )

    # result = models.OneToOneField('aims.Result')
    result_indicator = models.ForeignKey('aims.ResultIndicator', on_delete=models.CASCADE)
    display = models.TextField(choices=display_choices)
    sector = models.TextField(choices=sector_choices)
    target = models.TextField(null=True, blank=True)
    # visible = models.BooleanField(default=True)


class ResourceType(models.Model):
    """
    This is a per-site implementation for categorizing documents outside of IATI's somewhat limited models
    """
    title = models.TextField()
    description = models.TextField()
