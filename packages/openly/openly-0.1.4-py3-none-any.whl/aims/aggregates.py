import logging
from collections import defaultdict
from itertools import groupby, product
from operator import itemgetter
from typing import Any, Dict, Iterable, Optional, Sequence, Tuple, Union

from django.db import connection

from dataquality.aggregates import Lower, SumOverPartition
from django.conf import settings  # TODO: Simple locations deprecation
from django.contrib.postgres.aggregates.general import StringAgg
from django.db.models import (
    Case, Count, F, FloatField, Func, OuterRef, QuerySet, Subquery, Sum, TextField, Value as V, When,
)
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Cast, Concat
from django.db.models.functions.datetime import ExtractMonth, ExtractYear, TruncMonth
from django.utils.safestring import mark_safe
from oipa.models import OipaActivityLink
from rest_framework.renderers import JSONRenderer
from simple_locations.models import Area

from aims import models as aims

from . import geo_aggregates
from .openly_roles import OPENLY_SECTOR_TYPE_IATI, OPENLY_SECTOR_TYPE_NATIONAL

logger = logging.getLogger(__name__)

Anno = Dict[str, Dict[Any, Any]]

'''
This package contains functions to return Transactions annotated with 'sum for activity' for different options

Most of these would return a queryset
These can be decorated with 'breakdown' to return a dict
These can further be wrapped in 'render' to return safe-marked JSON using DRF's lovely renderer (which helps with datetimes and Decimals)
'''


class Round(Func):
    '''
    Call postgres's ROUND function for 2 decimal places
    '''
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 2)'


class RoundOne(Func):
    '''
    Call postgres's ROUND function for 1 decimal place
    '''
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 1)'


def annotate_values(queryset: QuerySet, *fields: Tuple[str, Tuple[str]]) -> QuerySet:
    '''
    This is similar to the built-in .values() method of queryset
    It takes a tuple of 2-element tuples of field names and reassignments
    The first element of each tuple is the "original" name; the [1] element is the assigned name
    This lets us change the shape of the return from the 'values' function, without requiring iterating
    through a list of values
    '''
    #  Generate a set of reassigned names, and the values to return
    annotate_fields = {key_map[1]: F(key_map[0]) for key_map in fields if key_map[0] != key_map[1]}
    returned_values = [key_map[1] for key_map in fields]
    return queryset.annotate(**annotate_fields).values(*returned_values)


def activity_aidtypecategory(activity: aims.Activity) -> QuerySet:
    transactions = activity.transaction_set.all()
    return Aggregates(transactions).by_aid_type_category()


def percentage_breakdown(objects: QuerySet, value_field: str, percentage_field: str, key_field: str) -> Anno:
    '''
    Returns a nested dict with percentage values
    Keyed by 'key_field' and 'percentage_field', value is a dict of items
    Example: Breakdown of [usd_value] per [activity_id] by [aid type category name]:

    >>> objects = Transaction.objects.filter(activity__in=Activity.objects.all_openly_statuses()[8:15])
    >>> value_field = 'usd_value'
    >>> percentage_field = 'aid_type__category__name'
    >>> key_field = 'activity_id'
    >>> percentage_breakdown(t, 'usd_value', 'aid_type__category__name', 'activity_id')

        {...
        'MM-FERD-ID1468': {'Budget support': 50.0,
        'Core contributions and pooled programmes and funds': 50.0},
        'MM-FERD-ID3819': {'Project-type interventions': 100.0},
        ...}
    '''

    f = {('%s__isnull' % percentage_field): False}
    queryset = percentage(objects.filter(**f), (value_field, key_field, percentage_field)).order_by(key_field)
    values = queryset.values(key_field, percentage_field, 'percent')
    return {i: {'%s' % (k[percentage_field]): k['percent'] for k in j} for i, j in groupby(values, lambda item: item.pop(key_field))}


def percentage_breakdown_as_string(objects: QuerySet, value_field: str, percentage_field: str, key_field: str) -> Anno:
    '''
    Returns a dict of dicts with percentage values: keyed by 'key_field' and 'percentage_field', value is a string rep of items
    This takes the output of percentage_breakdown() and converts the returned values to a string

    >>> objects = Transaction.objects.filter(activity__in=Activity.objects.all_openly_statuses()[8:15])
    >>> value_field = 'usd_value'
    >>> percentage_field = 'aid_type__category__name'
    >>> key_field = 'activity_id'
    >>> percentage_breakdown_as_string(t, 'usd_value', 'aid_type__category__name', 'activity_id')
    >>> {'MM-FERD-2271': 'Budget support',
        'MM-FERD-2626': 'Budget support 21.4%|Project-type interventions 78.6%',
        'MM-FERD-ID0396': 'Core contributions and pooled programmes and funds',
        'MM-FERD-ID1063': 'Project-type interventions',
        'MM-FERD-ID1468': 'Core contributions and pooled programmes and funds 50.0%|Budget support 50.0%',
        'MM-FERD-ID3819': 'Project-type interventions',
        'MM-FERD-ID58': 'Experts and other technical assistance'}
    '''
    def stringify(items: Dict[str, Any], delimiter: str = '|') -> str:
        if not items:
            return ''
        if len(items) == 1:
            return next(iter(items))
        return delimiter.join('{} {}%'.format((name or 'None').lower().capitalize(), cat_percent) for name, cat_percent in items.items())

    breaks = percentage_breakdown(objects, value_field, percentage_field, key_field)
    return {aid: stringify(items) for aid, items in breaks.items()}


def many_to_many_as_annotation(
        objects: QuerySet,
        related_model: str = 'activity__location',
        zero_annotate: Sequence[Union[F, V]] = (V(None,),),
        single_annotate: Sequence[Union[F, V]] = (F('activity__location__name',),),
        many_annotate: Sequence[Union[F, V]] = (F('activity__location__name'), V('('), F('activity__location__pk'), V(')')),
        separator: str = ',',
        annotation_name: str = 'anno') -> QuerySet:
    '''
    Takes a related model, tuples for annotation formatting under different conditions, and a separator
    This "denormalises" many-to-many relationships, combining the output into a single formatted text field

    An example, consider a fields of "locations" for "transaction".
    This could be represented by "No locations", a place name "Myanmar" where there is one location or "Shan state (20%), Rakhine state(20%)" when more than
    one location is linked to a transaction.
    zero_annotate, single_annotate and many_annotate are lists of 'F' (field names) and 'V' (values - literal strings) to concatenate.
    These are then StringAgg'ed together.
    This handles the cases of no objects, single object, and plural objects.

    In this example related_model is activity_location. The formatting string ('single_annotate') is F('activity__location__name'):
        the 'location name field' linked via activity.
    When more than one location exists, the formatting string takes a tuple of F() and V() inputs to create the output.
    '''

    def agg(fields: Any) -> Func:
        '''
        Format and concatenate fields depending on the values passed.
        By using a list unpacking we can concatenate multiple fields and values together to create very
        flexible representations of a many-to-many relationship without leaving the ORM.
        '''
        output_field = TextField()  # type: Any
        if len(fields) < 2:
            return StringAgg(*fields, separator, output_field=output_field)
        return StringAgg(Concat(*fields), separator, output_field=output_field)

    # Conditional output for the related models depending on whether there are zero, one or many related fields
    output_field = TextField()  # type: Any
    anno_function = Case(
        When(**{'%s__count' % related_model: 0}, then=agg(zero_annotate)),
        When(**{'%s__count' % related_model: 1}, then=agg(single_annotate)),
        When(**{'%s__count__gt' % related_model: 1}, then=agg(many_annotate)),
        output_field=output_field
    )

    annotate_count = objects.annotate(Count(related_model))  # type: QuerySet
    return annotate_count.annotate(**{annotation_name: anno_function})


def location_hierarchy_anno(prefix: str = 'area', suffix: str = 'name', max_level: int = 2):
    '''
    Provide an annotation dict to set us up with a separate column for each AreaType
    in order to annotate anything linked to SimpleLocations

    The default prefix of "area" works with a Location QS
    However you may of course use "location__area" or "activity__location__area"
    for an Activity QS or Transaction QS resp.

    The default suffix of "name" will give as an example on mohinga
    3 new columns: 'country_name', 'township_name', 'state_name'
    However you may choose str=None for a 'country' (id) field,
    or 'code' or any other field on Area

    >>> Location.objects.annotate(location_hierarchy_anno())
    >>> Activity.objects.annotate(location_hierarchy_anno(prefix='location__area', suffix=None))
    >>> Transaction.objects.annotate(location_hierarchy_anno(prefix='activity__location__area', suffix='code'))
    '''

    def level_to_areatype():
        '''
        Area has a "level" which is automatically determined.
        This should have a 1-to-1 relationship with an AreaType aka area.kind
        We can use that to dynamically generate our annotation field names
        '''
        qs = Area.objects.order_by().distinct('kind').values_list('level', 'kind__name')
        return list(qs.values_list('level', 'kind__name'))

    def lvl(level: int):
        '''
        Give us an unpackable to provide a level
        This will return a really simple one-element dict
        for a "When" query
        '''
        return {'%s__level' % (prefix,): level}

    def thn(level: int = 0):
        '''
        Return a field name modified with prefix, suffix and a few '__parent' things
        If level is one, will return the level above the prefix
        The default settings will return
            thn(0) = F(area__name)
            thn(1) = F(area__parent__name)
        '''
        field_name = prefix + ('__parent' * level)
        if suffix:
            field_name = field_name + '__' + suffix
        return F(field_name)

    def list_of_when(levels: int, diff: int):
        '''
        Return a list of "When" objects with "Then" clauses
        to pick certain fields based on the relationship in the hierarchy
        '''

        whens = []
        for level in range(levels):
            if level - diff >= 0:
                whens.append(When(**lvl(level), then=thn(level - diff)))
        return whens

    annotation = {}
    for level, name in level_to_areatype():
        if suffix:
            name = name + '_' + suffix
        annotation[name] = Case(*list_of_when(max_level + 1, level), default=None)
    return annotation


def activity_sector_category(objects: QuerySet) -> QuerySet:
    """
    Django ORM rocks here, drawing a list of concatenated "Sector" per "activity"
    """
    return many_to_many_as_annotation(
        objects=objects or aims.Activity.objects.all_openly_statuses(),
        related_model='activitysector__sector',
        zero_annotate=(V(None,),),
        single_annotate=(F('activitysector__sector__name',),),
        many_annotate=(F('activitysector__sector__name'), V('('), F('activitysector__percentage'), V('%)'),),
    )


def activity_sector_category_subquery(activities: Optional[QuerySet] = None, category_type: Optional[str] = None, outerref: str = 'activity') -> Subquery:
    '''
    Wraps the 'many_to_many_as_annotation' funtion above as a Subquery on TransactionQuerySet
    >>> from aims.aggregates import activity_sector_category_subquery as cats
    >>> Transaction.objects.all.annotate(cats = cats())

    If you have multiple catagories (ie "Local sectors" on Mohinga) you probably wish to filter activities
    to a single SectorCategory
    >>> from aims.openly_roles import OPENLY_SECTOR_TYPE_IATI
    >>> Activity.objects.filter(activitysector__sector__category__openly_type=OPENLY_SECTOR_TYPE_IATI)
    '''
    if not activities:
        activities = aims.Activity.objects.all_openly_statuses()  # type: QuerySet
    if category_type:
        assert category_type in ['iati', 'national']
        activities = activities.filter(activitysector__sector__category__openly_type=category_type)

    return Subquery(activity_sector_category(activities).filter(pk=OuterRef(outerref)).values('anno')[:1], output_field=TextField())


def activity_commitment_total_subquery(activities: Optional[QuerySet] = None, transaction_type: str = 'C', outerref: str = 'pk'):
    '''
    Get the commitment total as an annotation on Activity field
    transaction_type to 'D' for Disbursements
    '''
    if not activities:
        activities = aims.Activity.objects.all_openly_statuses()  # type: QuerySet
    activities = activities.filter(transaction__transaction_type__pk=transaction_type).annotate(anno=Sum('transaction__usd_value'))
    return Subquery(activities.filter(pk=OuterRef(outerref)).values('anno')[:1], output_field=TextField())


def activity_oipa_sync_subquery():
    '''
    Return set of Subqueries for oipa_sync associated with an
    Activity queryset
    '''
    links = OipaActivityLink.objects.exclude(oipa_fields=[]).filter(activity_id=OuterRef('id'))
    return Subquery(links.values('activity_id')[:1])


def activity_name_subquery(outerref: str = 'activity') -> Subquery:
    return Subquery(aims.Activity.objects.all_openly_statuses().filter(pk=OuterRef(outerref)).annotate(anno=StringAgg(Concat(F('title__title'), V(' ('), F('id'), V(') ')), delimiter=', ')).values('anno')[:1], output_field=TextField())


def activity_organisations_subquery_list(outerref: str = 'pk') -> Dict[str, Subquery]:
    '''
    Returns a set of Subqueries to activity participating organisations
    Default OuterRef is to 'pk': i.e. it works on an Activity queryset
    For a Transaction queryset, use 'outerref=activity'
    '''
    roles = list(aims.OrganisationRole.objects.all().values_list('code', flat=True))
    subqueries = {}
    for role in roles:
        subquery_source = aims.Activity.objects.filter(pk=OuterRef(outerref), participating_organisations__role_id=role)
        abbreviation_array = subquery_source.annotate(array=StringAgg('participating_organisations__organisation__abbreviation', delimiter=', '))
        subquery = Subquery(abbreviation_array.values('array')[:1], output_field=TextField())
        subqueries['participating_organisations_%s' % (role.lower(),)] = subquery
    return subqueries


def dictfetchall(cursor: connection.cursor) -> Iterable[Dict[str, Any]]:
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]  # type: list[str]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def sector_category_sum(categories: QuerySet, activities: QuerySet, transactions: QuerySet) -> str:
    '''
    Returns a QS of "dollars" annotated onto "sector category"
    '''
    with_dollars = categories.filter(
        sector__activitysector__activity__in=activities,
        sector__activitysector__activity__transaction__in=transactions
    ).annotate(
        dollars=Sum(F('sector__activitysector__percentage') * F('sector__activitysector__activity__transaction__usd_value') * V(0.01))
    ).values('code', 'name', 'dollars')
    return with_dollars


def organisation_commitment_by_sector(org_id: str) -> str:
    categories = aims.IATISectorCategory.objects.all()
    transactions = aims.Transaction.objects.filter(transaction_type='C', activity__activity_status='2', activity__openly_status="published")
    activities = aims.Activity.objects.filter(reporting_organisation_id=org_id)
    # Expect that the logged value (total transactions) equals the total transactions after grouping (accounting for rounding, missing percentage / sector allocation)
    return sector_category_sum(categories, activities, transactions)


def percentage(objects: QuerySet, fields: Sequence[str] = ('usd_value', 'activity_id', 'aid_type__category')):
    '''
    Annotate a query set with a "percentage" summary.
    This requires min three fields.

    The value you wish to percentage or fraction (ie dollars) PLUS
    The fields you with to sum (ie activity and aid_type__category) PLUS
    The fields you wish to divide by (ie aid_type__category)

    '''

    # Generate a sum over partition, for the 'value' field, of activity ID and the target field
    fields_maingroup = [F(f) for f in fields[:-1]]
    fields_subgroup = [F(f) for f in fields]

    annotated_objects = objects.annotate(
        dollars_category=SumOverPartition(*fields_subgroup, output_field=FloatField()),
        dollars_activity=SumOverPartition(*fields_maingroup, output_field=FloatField())
    )
    distinct = annotated_objects.distinct(*fields[1:])  # We would potentially have many results - trim these down to one-per-activity

    percent_annotate = distinct.annotate(
        percent=RoundOne(Case(
            When(dollars_activity=0, then=0),
            When(dollars_category=F('dollars_activity'), then=100),
            default=F('dollars_category') / F('dollars_activity') * 100,
        ))
    )

    return percent_annotate


class AggregatesFactory:

    @staticmethod
    def aggregates(**kwargs: Dict[str, Any]):
        """
        Return an Aggregates class with parameters set based on filter parameters
        As of now - asks for the default aggregates to include or exclude locations / sectors
        """
        keys = kwargs.keys()

        default_by_location = True in [i.startswith('activity__location__') for i in keys]

        default_by_sector = True in [i.startswith('activity__sector__') for i in keys]

        all_by_activity = kwargs.pop('all_by_activity', False)

        transactions = aims.Transaction.objects.filter(**kwargs)
        return Aggregates(transactions, default_by_location=default_by_location, default_by_sector=default_by_sector, all_by_activity=all_by_activity)


class Aggregates:

    '''
    Aggregates can be tricky beasts
    Complicating things here are cases where we multiply by percentage fields for location and sector
    Depending on which aggregate we're calculating and what our filtering is this can have undesirable effects

    There are four scenarios:
    Normal transactions
    Account for %Location
    Account for %Sector
    Account for %Sector and %Location

    Here are some interesting things to do
    >>> from aims.aggregates import Aggregates
    >>> a = Aggregates(Transaction.objects.all)
    >>> a.sum_by('provider_organisation').values('provider_organisation__name', 'dollars_category')

    '''

    def __init__(
            self,
            transactions: QuerySet,
            categories: Tuple[str] = tuple(),
            default_by_location: bool = False,
            default_by_sector: bool = False,
            all_by_activity: bool = False,
    ):

        self.source_transactions = transactions
        self.default_by_sector = default_by_sector
        self.default_by_location = default_by_location
        self.all_by_activity = all_by_activity  # Breakdown everything with an additional "by activity" parameter

        # These annotation/filters are used to create some complex QuerySets
        iati_sectors = dict(activity__activitysector__sector__category__openly_type=OPENLY_SECTOR_TYPE_IATI)  # type: Dict[str, str]
        national_sectors = dict(activity__activitysector__sector__category__openly_type=OPENLY_SECTOR_TYPE_NATIONAL)  # type: Dict[str, str]
        location_annotate = dict(value_field=F('activity__location__percentage') * F('usd_value') / V(100.0))  # type: Dict[str, Any]
        sector_annotate = dict(value_field=F('activity__activitysector__percentage') * F('usd_value') / V(100.0))  # type: Dict[str, Any]
        sector_and_location_annotate = dict(
            value_field=F('activity__activitysector__percentage') * F('activity__location__percentage') / V(10000.0) * F('usd_value')
        )  # type: Dict[str, Any]

        # These 'querysets' are used for aggregations where we do need to account for Location ans/or Sector and/or both location and sector
        self.transactions_with_location = transactions.annotate(**location_annotate)
        self.transactions_with_sector = transactions.filter(**iati_sectors).annotate(**sector_annotate)
        self.transactions_with_sector_and_location = transactions.filter(**iati_sectors).annotate(**sector_and_location_annotate)

        # In addition we face the challenge of "Local sectors", which are separate, non-IATI sector categories!
        self.transactions_with_national_sector = transactions.filter(**national_sectors).annotate(**sector_annotate)
        self.transactions_with_national_sector_and_location = transactions.filter(**national_sectors).annotate(**sector_and_location_annotate)

        # For many aggregates we don't directly refer to the value of the sector or location value BUT if filtered, we need to calculate it
        # If an activity has no percentages, they will be dropped from the queries and we will spend days trying to work out why numbers don't add up
        # So it's important to use these querysets ONLY when filtered if you value your sanity
        # Here we set the "default" queryset of self.transactions, dependent on the advice provided in 'filters'

        if default_by_location and default_by_sector:
            self.transactions = self.transactions_with_sector_and_location
        elif default_by_location:
            self.transactions = self.transactions_with_location
        elif default_by_sector:
            self.transactions = self.transactions_with_sector
        else:  # We annotate this to consistently refer to a value field
            self.transactions = transactions.annotate(value_field=F('usd_value'))

        self.render_categories = categories

        self.categories = dict(
            ministry=self.by_ministry,
            donor=self.by_donor,
            status=self.by_activity_status,
            location=self.by_location,
            category=self.by_iati_sector_category,
            local_category=self.by_national_sector_category,
            transaction_type=self.by_transaction_type
        )  # type: Dict[str, QuerySet]

        # TODO: Simple locations deprecation
        if not getattr(settings, 'USE_SIMPLE_LOCATIONS', False):
            self.categories['location'] = self.by_adm_code

    def sum_by(self, group_field: str, transactions: Optional[QuerySet] = None, value_field: str = 'value_field', by_activity: bool = False):
        transactions = transactions or self.transactions
        if self.all_by_activity or by_activity:
            return transactions.annotate(
                dollars_category=SumOverPartition(value_field, 'activity', group_field, output_field=FloatField())
            ).distinct('activity', group_field)
        return transactions.annotate(
            dollars_category=SumOverPartition(value_field, group_field, output_field=FloatField())
        ).distinct(group_field)

    def by_transaction_type(self) -> QuerySet:
        '''
        Returns breakdown by activity status with lowercase transaction type name
        '''
        group_field = 'transaction_type'
        name_field = 'transaction_type__name'
        sums = self.sum_by(group_field)
        sums = self.sum_by(group_field).annotate(transaction_type_name=Lower(F(name_field)))
        return self.rekey(sums, group_field, 'transaction_type_name')

    def by_ministry(self) -> QuerySet:
        ''' "National Ministry Accountable Commitments"
        This is a bit mohinga-specific
        '''
        group_field = 'activity__participating_organisations__organisation__code'
        name_field = 'activity__participating_organisations__organisation__name'

        # We could add this to the transaction set in class, but it is very specific to Mohinga
        annotated = self.transactions.filter(
            activity__participating_organisations__role_id='Accountable',
            activity__participating_organisations__organisation__type__name='National Ministry'
        )
        sums = self.sum_by(group_field, annotated)
        return self.rekey(sums, group_field, name_field)

    def by_donor(self) -> QuerySet:
        group_field = 'provider_organisation__code'
        name_field = 'provider_organisation__name'
        sums = self.sum_by(group_field, self.transactions)
        return self.rekey(sums, group_field, name_field)

    def by_activity_status(self) -> QuerySet:
        group_field = 'activity__activity_status'
        name_field = 'activity__activity_status__name'
        sums = self.sum_by(group_field, self.transactions)
        return self.rekey(sums, group_field, name_field)

    def by_aid_type_category(self) -> QuerySet:
        group_field = 'aid_type__category__code'
        name_field = 'aid_type__category__name'
        sums = self.sum_by(group_field, self.transactions)
        return self.rekey(sums, group_field, name_field)

    def aid_type_category_percentage(self) -> Anno:
        '''
        Percentage allocation of transactions as nested dict
        keyed by activity id and aid_type__category__name
        '''
        return self.category_percentage_by_activity(percentage_field='aid_type__category__name')

    def fin_type_category_percentage(self) -> Anno:
        '''
        Percentage allocation of transactions as nested dict
        keyed by activity id and finance_type__category__name
        '''
        return self.category_percentage_by_activity(percentage_field='finance_type__category__name')

    def category_percentage_by_activity(self, percentage_field: str = 'aid_type__category__name') -> Anno:
        '''
        Nominate a field to return a "percentage breakdown" value by activity
        '''
        return percentage_breakdown(
            objects=self.transactions,
            value_field='usd_value',
            percentage_field=percentage_field,
            key_field='activity_id'
        )

    def category_percentage_by_activity_str(self, percentage_field: str = 'aid_type__category__name') -> Anno:
        '''
        Nominate a field to return a "percentage breakdown" value as a string
        '''
        return percentage_breakdown_as_string(
            objects=self.transactions,
            value_field='usd_value',
            percentage_field=percentage_field,
            key_field='activity_id'
        )

    def finance_type_categories_string(self) -> Anno:
        '''
        Percentage allocation of transactions as nested dict
        keyed by activity id, value returned is a string
        '''
        def stringify(items):
            if not items:
                return ''
            if len(items) == 1:
                return next(iter(items))
            return '|'.join('{} {}%'.format((name or 'None').lower().capitalize(), cat_percent) for name, cat_percent in items.items())

        return {activity_id: stringify(items) for activity_id, items in self.aid_type_category_percentage().items()}

    def annotate_transaction_locations(self) -> QuerySet:
        return many_to_many_as_annotation(
            objects=self.transactions,
            related_model='activity__location',
            zero_annotate=(V('None'),),
            single_annotate=(F('activity__location__name'),),
            many_annotate=(
                F('activity__location__name'),
                V('('),
                F('activity__location__percentage'),
                V('%)')
            ),
            annotation_name='locations'
        )

    def annotate_sectors(self) -> QuerySet:
        sector_type = OPENLY_SECTOR_TYPE_IATI
        return many_to_many_as_annotation(
            objects=self.transactions.filter(activity__activitysector__sector__category__openly_type=sector_type),
            related_model='activity__activitysector__sector',
            zero_annotate=(V('None'),),
            single_annotate=(F('activity__activitysector__sector__name'),),
            many_annotate=(
                F('activity__activitysector__sector__name'),
                V('('),
                F('activity__activitysector__percentage'),
                V('%)')
            ),
            annotation_name='sectors'
        )

    def annotate_organisations(self, role: aims.OrganisationRole) -> QuerySet:
        '''
        Annotate activity's related organisations to a Transaction QuerySet
        Role might be OrganisationRole.objects.get(name='Implementing') or similar
        '''

        return many_to_many_as_annotation(
            objects=self.transactions.filter(activity__participating_organisations__role=role),
            related_model='activity__participating_organisation',
            zero_annotate=(V('None'),),
            single_annotate=(
                F('activity__participating_organisation__name'),
                V('('),
                F('activity__participating_organisation__code'),
                V(')')
            ),
            many_annotate=(
                F('activity__participating_organisation__name'),
                V('('),
                F('activity__participating_organisation__code'),
                V(')')
            )
        )

    def annotate_all_organisation_roles(self) -> Anno:
        '''
        This was a bit tricky to keep in ORM-land
        so we drop into Python to return a collection of transaction id's with
        organisation types annotated.
        '''
        returning_object = {}
        for ot in aims.OrganisationRole.objects.all():
            for pk, anno in self.annotate_organisations(ot).values_list('pk', 'anno'):
                if pk not in returning_object:
                    returning_object[pk] = {}
                returning_object[pk][ot.name] = anno
        return returning_object

    def by_location(self) -> QuerySet:
        group_field = 'activity__location__area'
        if self.default_by_sector:
            transactions = self.c_and_location
        else:
            transactions = self.transactions_with_location
        sums = self.sum_by(group_field, transactions)
        return self.rekey(sums, group_field)

    def by_location_with_subareas(self, area: Area) -> Anno:
        if self.default_by_sector:
            transactions = self.c_and_location
        else:
            transactions = self.transactions_with_location

        return transaction_by_location_with_subareas(transactions, area)

    def as_geojson(self, area: Area, **kwargs):
        sums = self.by_location_with_subareas(area)
        simplify = float(kwargs.get('simplify', 1e-4))
        dp = int(kwargs.get('dp', 3))
        return geo_aggregates.as_geojson(area.get_children(), simplify, dp, additional_properties=sums)

    def by_adm_code(self) -> QuerySet:
        group_field = 'activity__location__adm_code'
        if self.default_by_sector:
            transactions = self.transactions_with_sector_and_location
        else:
            transactions = self.transactions_with_location
        sums = self.sum_by(group_field, transactions)
        return self.rekey(sums, group_field)

    def by_iati_sector_category(self) -> QuerySet:
        group_field = 'activity__activitysector__sector__category__code'
        name_field = 'activity__activitysector__sector__category__name'

        if self.default_by_location:
            transactions = self.transactions_with_sector_and_location
        else:
            transactions = self.transactions_with_sector
        sums = self.sum_by(group_field, transactions)
        return self.rekey(sums, group_field, name_field)

    def by_iati_sector(self) -> QuerySet:
        group_field = 'activity__activitysector__sector__code'
        name_field = 'activity__activitysector__sector__name'

        if self.default_by_location:
            transactions = self.transactions_with_sector_and_location
        else:
            transactions = self.transactions_with_sector
        sums = self.sum_by(group_field, transactions)
        return self.rekey(sums, group_field, name_field)

    def by_national_sector_category(self) -> QuerySet:
        group_field = 'activity__activitysector__sector__category__code'
        name_field = 'activity__activitysector__sector__category__name'

        if self.default_by_location:
            transactions = self.transactions_with_national_sector_and_location
        else:
            transactions = self.transactions_with_national_sector
        sums = self.sum_by(group_field, transactions)
        return self.rekey(sums, group_field, name_field)

    def by_national_sector(self) -> QuerySet:
        group_field = 'activity__activitysector__sector__code'
        name_field = 'activity__activitysector__sector__name'

        if self.default_by_location:
            transactions = self.transactions_with_national_sector_and_location
        else:
            transactions = self.transactions_with_local_sector
        sums = self.sum_by(group_field, transactions)
        return self.rekey(sums, group_field, name_field)

    def to_dict(self) -> Dict[Any, Any]:
        categories = self.render_categories or self.categories.keys()
        sum_total = self.transactions.aggregate(Sum('value_field'))['value_field__sum'] or 0
        data = defaultdict(dict)  # type = Dict[Any, Dict[Any, Any]]

        for label in categories:
            by = self.categories[label]()
            sort_dollars = sorted(by, key=itemgetter('dollars'), reverse=True)

            data['by'][label] = sort_dollars
            data['total'][label] = sum([value or 0 for value in by.values_list('dollars', flat=True)])
            data['unassigned'][label] = sum_total - data['total'][label] or 0
            # Most aggregates should expect to have zero (or parhaps a small, rounding-error variance) as "unassigned"

        # Special case for location handling
        # This is a little bit tricky as it requires aggregating "up" based on
        # Location.adm_code or Location.area.id
        if 'location' in data['by']:
            areas = [dict(a) for a in Area.objects.values('lft', 'rght', 'id', 'code', 'name')]
            for area in areas:
                area['dollars'] = 0
            for loc in data['by']['location']:
                try:
                    area = [a for a in areas if a['code'] == loc['code']][0]
                    area['dollars'] += loc['dollars']
                except IndexError:
                    logger.warning('Area error: Location code %s', loc['code'])
                    logger.warning('SimpleLocations.Area object missing with code %s', loc['code'])
                    areas.append({'code': loc['code'], 'dollars': loc['dollars']})
                    area = areas[-1]

                # Also add the "location value" to all parent areas
                # In SimpleLocation terms, this is a simple math equation
                for other_area in areas:
                    if 'lft' not in area or 'lft' not in other_area:  # Check that we are in fact looking at MPTT-type models
                        continue
                    if other_area['lft'] < area['lft'] and other_area['rght'] > area['rght']:
                        other_area['dollars'] += loc['dollars']

        # Don't waste bytes delivering "Location" where value is zero
        data['by']['location_with_subareas'] = [a for a in areas if a['dollars'] != 0]

        return data

    def to_json(self):
        return mark_safe(JSONRenderer().render(self.to_dict()))

    def rekey(self, queryset: QuerySet, code_field: Optional[str] = None, name_field: Optional[str] = None, dollar_field: str = 'dollars_category'):
        rekey_set = []
        if dollar_field:
            rekey_set.append((dollar_field, 'dollars'))
        if code_field:
            rekey_set.append((code_field, 'code'))
        if name_field:
            rekey_set.append((name_field, 'name'))
        if self.all_by_activity:
            rekey_set.append(('activity', 'activity'))
        return annotate_values(queryset, *rekey_set)


def state_pcode_to_isocode(field_name='state_code', anno_name='iso'):
    '''
    Myanmar's "pcodes" do not align well to iso codes. This annotation
    provides a mapping.

    >>> annotate(foo = state_pcode_to_isocode(anno_name='iso'))

    '''
    if getattr(settings, 'PROJECT_NAME', None) != _('Mohinga'):
        case = V('Not implemented', output_field=TextField())
        if anno_name:
            return {anno_name: case}
        return case

    field_name = 'state_code'
    # The first field is the "current" MIMU
    # The second is the "legacy" fields we may reference (Mohinga only)
    translations = (
        ('MMR005', 'MM-01'),
        ('MMR007', 'MM-02'),
        ('MMR009', 'MM-03'),
        ('MMR010', 'MM-04'),
        ('MMR006', 'MM-05'),
        ('MMR013', 'MM-06'),
        ('MMR017', 'MM-07'),
        ('MMR001', 'MM-11'),
        ('MMR002', 'MM-12'),
        ('MMR003', 'MM-13'),
        ('MMR004', 'MM-14'),
        ('MMR011', 'MM-15'),
        ('MMR012', 'MM-16'),
        ('MMR014', 'MM-17'),
        ('MMR018', 'MM-18'),

        # Note that Bago and Shan may cause some confusion:
        # Sometimes these are counted as a single location
        # and at other times these are separated into multiple areas
        ('MMR111', 'MM-02'),  # Bago (MMR111) = East(MMR007) + West (MMR008) = MM-02 in legacy codes
        ('MMR222', 'MM-17'),  # Shan (MMR222) = 014, 015, 016 = MM-17 in legacy codes

    )
    whens = [When(**{field_name: pcode, 'then': V(isocode)}) for pcode, isocode in translations]
    case = Case(*whens, output_field=TextField())
    if anno_name:
        return {anno_name: case}
    return case


class date_as_quarter(Func):
    '''
    Format a date as calendar quarter - as in "2014q1"

    >>> Transaction.objects.annotate(q=date_as_quarter('value_date')).values('q')
    >>> QuerySet [{'q': '2014q1'}, {'q': '2012q4'}, {'q': '2015q2'}, {'q': '2016q1'}, {'q': '2017q3'}, {'q': '2018q1'}, {'q': '2018q1'}, {'q': '2018q1'}, {'q': '2013q2'}, {'q': '2017q1'}, {'q': '2017q4'}, {'q': '2012q4'}, {'q': '2013q3'}, {'q': '2013q1'}, {'q': '2017q1'}, {'q': '2017q3'}, {'q': '2018q2'}, {'q': '2008q2'}, {'q': '2018q2'}, {'q': '2014q3'}, '...(remaining elements truncated)...']>
    '''
    function = 'DATE_PART'
    template = ''' '' || %(function)s('year', %(expressions)s) || 'q' || %(function)s('quarter', %(expressions)s)'''


class date_as_decimal_quarter(Func):
    '''
    Format a date as calendar quarter - as in "2014.1"
    '''
    function = 'DATE_PART'
    template = ''' %(function)s('year', %(expressions)s)  + (%(function)s('quarter', %(expressions)s) / 10)'''


def sector_tiers(path: str = 'activity__activitysector__sector__sectortier') -> Anno:
    '''
    Return a map of sector tier codes and sector tier names
    This assumes annotation of a Transaction queryset. If not 'transaction', change the path to suit your needs.
    '''

    anno = {}
    tiers = 'II III IV V VI'.split()

    for tier in tiers:
        anno['tier_%s' % (tier,)] = F('%s__tier_%s' % (path, tier))
        anno['tier_%s__name' % (tier,)] = F('%s__tier_%s__name' % (path, tier))

    return anno


def sector_subquery(activities: Optional[QuerySet] = None, national: bool = False, **kwargs: Any) -> Subquery:
    '''
    Returns a SubQuery keyed to outerref

    activities is a QuerySet of aims.Activity - if not provided will use objects.all()
    national switches between IATI sectors and "national" sectors using
    the values in openly_roles.py

    >>> acts = Activity.objects.annotate(sector_working_groups = sector_subquery(national=True), iati_sectors = sector_subquery())
    >>> for a in acts[:20]:
    >>>     print('%s \n\t %s \n\t%s' % (a, a.sector_working_groups, a.iati_sectors))

    See https://github.com/catalpainternational/openly-notebooks/blob/master/sector_subquery.ipynb
    '''
    if national:
        sector_type = OPENLY_SECTOR_TYPE_NATIONAL
    else:
        sector_type = OPENLY_SECTOR_TYPE_IATI

    activities = activities or aims.Activity.objects.all()
    # Generally we won't want to see IATI and national sectors in the same field/column
    activities = activities.filter(activitysector__sector__category__openly_type=sector_type)
    related_model = 'activitysector__sector'
    name_field = 'activitysector__sector__name'
    pc_field = 'activitysector__percentage'
    # If another annotations name uses 'sectors', set this as a kwarg to prevent conflicting annotation names
    annotation_name = kwargs.get('annotation_name', 'sectors')
    outerref = kwargs.get('outerref', 'pk')

    # many_to_many_as_annotation is an annotation method which conditionally formats fields with
    # 0, 1, >1 relationships differently
    annotation = many_to_many_as_annotation(
        objects=activities,
        related_model=related_model,
        zero_annotate=(V('None'),),
        single_annotate=(F(name_field),),
        many_annotate=(F(name_field), V('('), F(pc_field), V('%)')),
        annotation_name=annotation_name
    ).filter(pk=OuterRef(outerref))

    return Subquery(annotation.values('sectors')[:1])


def fy_annotation_prerequisites():
    '''
    Lazy developer likes to go
    >>> Transaction.objects.annotate(**fy_annotations_prerequisites())
    '''
    return{
        'year': ExtractYear('transaction_date'),
        'month': ExtractMonth('transaction_date')
    }


def financial_year_annotations(format: str = "short", **kwargs):
    '''
    Transaction 'Financial Year' annotations
    These rather complex CASE statements address the decision to change Myannar's Financial Year start month from
    2018.
    This returns one of two CASE statements depending on whether you like long or short format

    Usage:
    >>> Transaction.objects.annotate(**fy_annotation_prerequisites()).annotate(fy=financial_year_annotations()).values('id','fy')
    Apologies this could be very confusing. I simplified it as much as possible
    '''

    fy_old_end = kwargs.get('fy_end', 3)  # month in which the financial year formerly ended (March)
    fy_new_end = kwargs.get('fy_new_end', 9)  # month in which the financial year now ends (September)

    if getattr(settings, 'PROJECT_NAME', None) == _('Mohinga'):
        # Myanmar's financial year changed in 2018
        fy_break = kwargs.get('fy_break', 2018)  # year in which the financial year alteration took place (2018)

    else:
        # We always use the "old" value (generally March)
        fy_break = 3000

    fy_old_start = fy_old_end + 1
    fy_new_start = fy_new_end + 1

    # The period in between the end of the old regime and the start of the new financial years
    intermission = dict(
        year=fy_break, month__gt=fy_old_end, month__lt=fy_new_start
    )

    def year(diff: int = 0):
        if not diff:
            return Cast(F('year'), TextField())
        return Cast(F('year') + diff, TextField())

    def year_range(diff: int = 0):
        return Concat(year(diff), V('/'), year(diff + 1))

    def long_year_range(diff: int = 0, month: int = 10):
        start = '-{:02d}'.format(month)
        end = '-{:02d}'.format((month + 11) % 12,)
        return Concat(year(diff), V(start), V(' - '), year(diff + 1), V(end))

    def long_year_range_year_of_break():
        '''
        Special case formatting for the year of the break
        Should return
            2018-04 - 2018-10
        '''
        start = '-{:02d}'.format(fy_old_start)
        end = '-{:02d}'.format(fy_new_end)
        return Concat(year(), V(start), V(' - '), year(), V(end))

    def short_fys():
        return Case(
            When(**intermission, then=year()),
            When(year__lte=fy_break, month__lte=fy_old_end, then=year_range(-1)),
            When(year__lt=fy_break, month__gt=fy_old_end, then=year_range()),
            When(year__gte=fy_break, month__lte=fy_new_end, then=year_range(-1)),
            When(year__gte=fy_break, month__gt=fy_new_end, then=year_range()),
            soutput_field=TextField(),
        )

    def long_fys():
        return Case(
            # Special case handles the 6 months in fy_break which are outside of the financial years
            When(**intermission, then=long_year_range_year_of_break()),
            When(year__lte=fy_break, month__lte=fy_old_end, then=long_year_range(-1, fy_old_start)),
            When(year__lt=fy_break, month__gt=fy_old_end, then=long_year_range(0, fy_old_start)),
            When(year__gte=fy_break, month__lte=fy_new_end, then=long_year_range(-1, fy_new_start)),
            When(year__gte=fy_break, month__gt=fy_new_end, then=long_year_range(0, fy_new_start)),
            output_field=TextField(),
        )

    if format == 'long':
        return long_fys()
    else:
        return short_fys()


def fy_annotation_lookup(transactions: Optional[QuerySet] = None) -> Dict[str, str]:
    '''
    Returns a 'FY Lookup' query
    This is used in the Query Builder to set a Date Range based on Financial Year
    as well as providing a nice interface to test that the ridiculously complex CASEs work properly
    '''

    transactions = transactions or aims.Transaction.objects.all()

    # Drop null dates and some duplicate entries for Financial Years
    q = transactions.filter(transaction_date__isnull=False).annotate(
        key=TruncMonth('transaction_date')
    ).distinct('key')

    q = q.annotate(
        **fy_annotation_prerequisites()
    ).annotate(
        fy=financial_year_annotations(),
        fy_long=financial_year_annotations('long')
    )
    # Returns a dict with keys like "2017/2018: 2017-04 - 2018-03"
    # This is JSONified for QueryBuilder and querybuilder.js should be checked
    # before altering return value here
    return {i['fy']: i['fy_long'] for i in q.distinct('fy').values('fy', 'fy_long')}


def transaction_by_location_with_subareas(transactions: QuerySet, area: Area) -> Anno:
    '''
    Returns a dict of Area and descendants' PKs, dollars assigned directly, dollars assigned to sub areas, dollars direct and sub
    Takes a QuerySet of Transactions, the Area to return (plus its subs), and returns a dict
    '''

    def get_transactions():
        transaction_values = transactions.values('activity__location').annotate(
            dollars=Sum(F('activity__location__percentage') * F('usd_value') * V(0.01))
        ).values('activity__location', 'dollars', 'activity__location__area__lft', 'activity__location__area__rght')
        return transaction_values

    def get_areas():
        area_values = area.get_descendants(
            include_self=True
        ).values(
            'pk', 'lft', 'rght', 'name'
        )
        return area_values

    transaction_values = get_transactions()
    area_values = get_areas()

    additional_properties = {a['pk']: {'dollars': 0, 'area_dollars': 0, 'subarea_dollars': 0, 'name': a['name']} for a in area_values}

    for t, a in product(transaction_values, area_values):
        # Our friendly geoJSON generator will turn "dollars" into strings, because that's how it handles decimals
        # We're probably OK with integers, we don't need cents / partial currencies
        if not t['dollars']:
            continue
        try:
            dollars = int(t['dollars'])
            if a['lft'] <= t['activity__location__area__lft'] and a['rght'] >= t['activity__location__area__rght']:
                additional_properties[a['pk']]['dollars'] += dollars

                if a['lft'] == t['activity__location__area__lft']:
                    additional_properties[a['pk']]['area_dollars'] += dollars

                else:
                    additional_properties[a['pk']]['subarea_dollars'] += dollars
        except TypeError:
            logger.warn('TypeError in transaction_by_location_with_subareas')

    return additional_properties
