from datetime import date, datetime
from time import strptime
from typing import Dict, List, Any, Mapping, Optional, Sequence, Union
import warnings  # Type hints

from django.conf import settings
from django.db.models import QuerySet
from django.db.models import Prefetch, Sum, F
from el_pagination.views import AjaxListView

import aims.base_utils as base_utils
import aims.models
from geodata.models import Adm1Region, Adm2Region
from simple_locations.models import Area

from .forms import FilterForm, object_choices
from .models import Activity, Transaction, AidTypeCategory
import logging
logger = logging.getLogger(__name__)


def set_financial_year(session=None, fy_end=None, now=None, date_format='%b %Y'):
    """
    Set and/or return the settings for the start and end of the date filter
    on querybuilder and dashboard pages
    Returns a human readable date format
    """
    # If FINANCIAL_YEAR setting, use the current FY if it's more than half way through the year
    # otherwise use the previous FY
    if not session:
        session = {}

    if 'start' in session and 'end' in session:
        return session['start'], session['end']

    now = now or datetime.now()
    fy_end = fy_end or getattr(settings, 'FINANCIAL_YEAR_ENDS', 12)
    while fy_end > 12:
        fy_end = fy_end - 12
    fy_start = fy_end + 1
    if fy_start > 12:
        fy_start = fy_start - 12
    start = datetime(now.year, fy_start, 1)
    while start.year >= now.year and fy_start > now.month:
        start = datetime(start.year - 1, fy_start, 1)
    while 0 < (now - start).days < 180:
        start = datetime(start.year - 1, fy_start, 1)

    end = min(now, datetime(start.year + 1, fy_end, 1))

    # This is a hack for Plov-staging
    if getattr(settings, 'PROJECT_NAME', None) == 'Plov':
        start = datetime(2015, 1, 1)

    return start.strftime(date_format), end.strftime(date_format)


class FilterFormView(AjaxListView):
    """ Base View for filtering to consistent subsets of IATI Activities and Transactions.

    The FilterFormView allows for filtering on various Activity and Transaction attributes
    by setting GET request keywords. GET requests are used, as opposed to POST requests, so
    that users can pass links to specific data sets. This is not the behavior of Django
    FormViews so the FilterFormView instead includes a FilterForm in its context which is
    used in Django templates to enumerate the allowed keywords and choices.

    Subclasses can provide additional filtering by implementing get_form to return a
    FilterForm subclass with the additional parameters. They must also define a setter
    for these parameters and implement set_attributes to call these new setters.

    Subclasses can perform additional context processing by implementing process_context.
    """

    def __init__(self):
        self.finance_type_categories = []
        self.aid_type_categories = []
        self.activity_statuses = []
        self.filter_form_data = {}  # Needed to populate form with current choices
        self.ministry = None
        self.donor = None
        self.sector = None
        self.category = None
        self.state = None
        self.start_date = None
        self.end_date = None

        # Caching these at the start of the view saves ~ 20 queries
        self.aidtypecategory_count = aims.models.AidTypeCategory.objects.count()
        self.financetypecategory_count = aims.models.FinanceTypeCategory.objects.count()

    """ Setters for filtering based on GET request keywords
    """

    def set_state(self, **kwargs):
        """
        This is tricky as "state=" may refer to a state by id or name
        Internally we want to use an id
        """

        # Extract "state" parameter as part of the GET or from kwargs. Else assign 'None'
        if 'state' in self.request.GET and self.request.GET['state'] != '':
            state = self.request.GET['state']
        elif 'state' in kwargs:
            state = kwargs.get('state')
        else:
            state = None

        self.filter_form_data['state'] = state

        if not state:
            self.state = None
            return

        # Set "self.state" to the value of state if it is a code such as MMR001
        if Adm1Region.objects.filter(adm1_code=state).count() == 1 or Area.objects.filter(code=state).count() == 1:
            self.state = state

        # Not a code. Try to match 'Name'
        elif Adm1Region.objects.filter(name=state).count() == 1:
            self.state = Adm1Region.objects.get(name=state).adm1_code
        elif Area.objects.filter(name=state).count() == 1:
            self.state = Area.objects.get(name=state).code
        else:
            # Not a code, no name match
            raise TypeError('Expected ADM1region or Area code or name, got %s' % state)

    def set_param(self, param, **kwargs):
        value = kwargs.get(param, self.request.GET.get(param, None))
        if value == '':
            value = None
        setattr(self, param, value)
        self.filter_form_data[param] = value

    def _set_category(self, query_param, property_name, objects, **kwargs):
        """
        ""
        This functions similar to a ModelChoiceField except that is uses "name" as
        a proxy for pk for easier human readability

        :param query_param: The 'get' parameter to read the model choices from
        :param property_name: The property of 'self' to assign choices to: displayed in the export filter
        :param objects: objects which may be selected (a queryset)
        :param default: dict of "defaults" if no options are selected (default: all objects)
        :return:
        """
        choose = object_choices(objects, **kwargs)

        setattr(self, property_name, [])
        self_prop = getattr(self, property_name)

        select = self.filter_form_data[query_param] = self.request.GET.getlist(query_param, [])

        for selection in select:  # Choices from client
            if selection not in choose:  # Ensure selection is one of the objects, a key in the "choose" dict
                continue
            self_prop.append(choose[selection])

        if len(self_prop) == 0:
            default = kwargs.get('default', choose)  # The default is all objects selected unless overridden above by 'default'
            self_prop.extend(default.values())
            self.filter_form_data[query_param] = list(default.keys())

        return self_prop, self.filter_form_data[query_param]

    def set_activity_status(self, **kwargs):
        self._set_category(
            query_param='activity_status',
            property_name='activity_statuses',
            objects=aims.models.ActivityStatus.objects.all(),
            cache_key='set_activity_status',
            #  Dashboards should not automatically filter by status
            # default={'implementation': 2}
        )

    def set_aid_type_category(self, **kwargs):
        """
        Set the aid type categories which are selected / to query on
        """
        self._set_category(
            query_param='aid_type_category',
            property_name='aid_type_categories',
            objects=AidTypeCategory.objects.all(),
            cache_key='set_aid_type_category',
        )

    def set_finance_type_category(self, **kwargs):
        """
        Set the finance type categories which are selected / to query on
        """
        self._set_category(
            query_param='finance_type_category',
            property_name='finance_type_categories',
            objects=aims.models.FinanceTypeCategory.objects.all(),
            cache_key='set_finance_type_category',
        )

    def set_date_range(self, **kwargs):
        """ Allows filtering Activity models by date

        Because dates are not included the FilterForm they require additional special
        handling. If the GET request includes a 'start' or 'end' in MM/YYYY format the
        appropriate endpoint is set and this is embedded in the request session under the
        same keyword. If not then the request session is checked for a previously set
        endpoint. If not located here the defaults used are January first of the previous
        year and the last day of the current month.
        """
        self.start_date, self.end_date = set_financial_year(self.request.session)
        if 'start' in self.request.GET:
            self.start_date = self.request.GET['start']
        elif 'start' in self.request.session:
            self.start_date = self.request.session['start']

        if self.start_date:
            try:
                start_date = strptime(self.start_date, "%b %Y")
                self.request.session['start'] = self.start_date
                self.start_date = date(int(start_date.tm_year), int(start_date.tm_mon), 1)
            except Exception as E:
                warnings.warn(F'Unhandled exception: {E}')
                self.start_date = None

        if 'end' in self.request.GET:
            self.end_date = self.request.GET['end']
        elif 'end' in self.request.session:
            self.end_date = self.request.session['end']

        if self.end_date:
            try:
                end_date = strptime(self.end_date, "%b %Y")
                self.request.session['end'] = self.end_date
                self.end_date = date(int(end_date.tm_year), int(end_date.tm_mon), 1)
                self.end_date = base_utils.last_day_of_month(self.end_date)
            except Exception as E:
                warnings.warn(F'Unhandled exception: {E}')
                self.end_date = None

        self.start_date = self.start_date or date(datetime.now().year - 1, 1, 1)
        self.end_date = self.end_date or datetime.now()
        self.filter_form_data['start_date'] = self.start_date
        self.filter_form_data['end_date'] = self.end_date

    def set_attributes(self, request, *args, **kwargs):
        self.set_date_range(**kwargs)
        self.set_finance_type_category(**kwargs)
        self.set_aid_type_category(**kwargs)
        self.set_activity_status(**kwargs)
        self.set_state(**kwargs)
        self.set_param('ministry', **kwargs)
        self.set_param('sector', **kwargs)
        self.set_param('donor', **kwargs)
        self.set_param('category', **kwargs)

    def build_export_summary(self):

        def add_rows(key: str, value: Any):
            """
            Append rows to the export summary data.
            This is intended to provide a more human readable
            interpretation of the filtering options.
            """

            def add_row(*args: List[str]):
                """
                Add elements to the export summary
                Generally this function should be called like
                >> add_row(title, string)
                """
                export_summary.append(args)

            simple_lookup = dict(
                transaction_date__lte="Transaction date on or before",
                activity__activity_status__in="Activity status",
                activity__openly_status="Activity \"published\" state",
                transaction_date__gte="Transaction date on or after",
                finance_type__category__in='Finance type category',
                activity__activitysector__sector__code__startswith='Activity sector',
                activity__participating_organisation__code='Participating organisation',
                aid_type__category_id__in='Aid type category',
                provider_organisation__code='Provider organisation'
            )

            if key == 'activity__activity_status__in':
                m = aims.models.ActivityStatus
                included_status = m.objects.filter(pk__in=value)
                excluded_status = m.objects.exclude(pk__in=value)
                add_row(
                    simple_lookup.get(key, key),
                    ', '.join(included_status.values_list('name', flat=True))
                )
                if excluded_status:
                    add_row(
                        simple_lookup.get(key, key) + ' is not',
                        ', '.join(excluded_status.values_list('name', flat=True))
                    )

            elif key == 'finance_type__category__in':
                m = aims.models.FinanceTypeCategory
                included_status = m.objects.filter(pk__in=value)
                excluded_status = m.objects.exclude(pk__in=value)
                add_row(
                    simple_lookup.get(key, key),
                    ', '.join(included_status.values_list('name', flat=True))
                )
                if excluded_status:
                    add_row(
                        simple_lookup.get(key, key) + ' is not',
                        ', '.join(excluded_status.values_list('name', flat=True))
                    )

            elif key == 'aid_type__category_id__in':
                m = aims.models.AidTypeCategory
                included_status = m.objects.filter(pk__in=value)
                excluded_status = m.objects.exclude(pk__in=value)
                add_row(
                    simple_lookup.get(key, key),
                    ', '.join(included_status.values_list('name', flat=True))
                )
                if excluded_status:
                    add_row(
                        simple_lookup.get(key, key) + ' is not',
                        ', '.join(excluded_status.values_list('name', flat=True))
                    )

            elif key == 'activity__openly_status':
                pass

            elif key == 'activity__activitysector__sector__code__startswith':
                included_status = aims.models.ActivitySector.objects.filter(pk__in=value).values_list('sector__name', flat=True)
                add_row(
                    simple_lookup.get(key, key),
                    ', '.join(included_status)
                )

            elif key in ['activity__participating_organisation__code', 'provider_organisation__code']:
                add_row(
                    simple_lookup.get(key, key),
                    aims.models.Organisation.objects.get(pk=value).name
                )

            elif key in simple_lookup:
                add_row(simple_lookup[key], value)

            else:
                add_row(key, value)

        export_summary = []
        for f in self.transaction_filters().items():
            add_rows(*f)
        return export_summary

    def get_form(self):
        """ Gets the form passed by the context.

        Subclasses that wish to use a subclass of FilterForm should implement this returning
        the appropriate form.
        """
        return FilterForm(self.filter_form_data)

    def queryset_date_filters(self, prefix):
        if self.start_date or self.end_date:
            return aims.models.generate_daterange_filter(self.start_date, self.end_date)
        return None

    def queryset_filters(self, extra: Optional[Sequence[Any]] = None, **kwargs: Dict[str, Any]) -> Mapping[str, Union[str, int, Sequence[Any]]]:
        """
        Return a dict of filters to apply for this queryset
        This is suitable for 'activity'.
        Recode the filter for another, related, table by appending 'prefix'
        """

        prefix_activity = kwargs.pop('prefix_activity', '')
        prefix_transaction = kwargs.pop('prefix_transaction', 'transaction__')

        filter_on_activity = {}  # Simple key-value filters
        filter_on_transaction = {}
        filter_on_location = {}

        filter_on_activity['activity_status__in'] = self.activity_statuses
        filter_on_activity['openly_status'] = 'published'

        if self.state is not None:

            uses_simple_locations = getattr(settings, 'USE_SIMPLE_LOCATIONS', False)
            prefix_location = kwargs.pop(
                'prefix_location',
                'location__'
            )

            if uses_simple_locations:
                suffix_location = 'area__code__in'
                try:
                    states = Area.objects.get(code=self.state).get_descendants(include_self=True).values_list('code', flat=True)
                except Area.DoesNotExist as e:
                    raise Area.DoesNotExist('Tried code: %s', self.state) from e
                filter_on_location['%s%s' % (prefix_location, suffix_location)] = states
                logger.debug(filter_on_location)
            else:
                #  When a state (ie ADM1region) is specified
                suffix_location = 'adm_code__in'
                states = [adm2.code for adm2 in Adm2Region.objects.filter(region_id=self.state)]
                states.append(self.state)
                filter_on_location['%s%s' % (prefix_location, suffix_location)] = states

        if self.ministry is not None:
            filter_on_activity['participating_organisation__code'] = self.ministry
        if self.sector is not None:
            filter_on_activity['activitysector__sector__code__startswith'] = self.sector
        if self.category is not None:
            filter_on_activity['activitysector__sector__category__code'] = int(self.category)
        if self.finance_type_categories is not None and (len(self.finance_type_categories) < self.financetypecategory_count):
            # The len(..) < .count() ensures that when all finance types are selected,
            # we also show activities where transaction__finance_type__category=None
            filter_on_transaction['finance_type__category__in'] = self.finance_type_categories
        if self.aid_type_categories is not None and (len(self.aid_type_categories) < self.aidtypecategory_count):
            # The len(..) < .count() ensures that when all aid types are selected,
            # we also show activities where transaction__aid_type__category_id=None
            filter_on_transaction['aid_type__category_id__in'] = self.aid_type_categories
        if self.donor is not None:
            filter_on_transaction['provider_organisation__code'] = self.donor

        if self.start_date:
            filter_on_transaction['transaction_date__gte'] = self.start_date
        if self.end_date:
            filter_on_transaction['transaction_date__lte'] = self.end_date

        filter_on_transaction = {'%s%s' % (prefix_transaction, k): v for k, v in filter_on_transaction.items()}
        filter_on_activity = {'%s%s' % (prefix_activity, k): v for k, v in filter_on_activity.items()}

        filters = {}
        filters.update(filter_on_transaction)
        filters.update(filter_on_activity)
        filters.update(filter_on_location)
        if extra:
            filters.update(extra)  # Add any other filters you might wish to have
        logger.debug(filters)
        return filters

    def transaction_filters(self, **kwargs):
        """Return filters suitable to do Transaction.filter(**this)"""
        return self.queryset_filters(prefix_activity='activity__', prefix_transaction='', prefix_location='activity__location__', **kwargs)

    def location_filters(self, **kwargs):
        """Return filters suitable to do Location.filter(**this)"""
        return self.queryset_filters(prefix_activity='activity__', prefix_transaction='activity__transaction__', prefix_location='', **kwargs)

    def transaction_sum(self, type='C'):
        f = self.transaction_filters(extra={'transaction_type_id': type})
        transactions = Transaction.objects.filter(**f)
        aggregate = transactions.aggregate(sum=Sum('usd_value'))
        return aggregate['sum'] or 0.0

    def related_activity_filter(self):
        """Return filters suitable to do Table.filter(**this) where the table has an FK to activity"""
        return self.queryset_filters(prefix_activity='activity__', prefix_transaction='activity__transaction__')

    def get_queryset(self, *args: None, **kwargs: None) -> QuerySet:
        return Activity.finance.filter(**self.queryset_filters()).prefetch_related(
            Prefetch('participating_organisations',
                     queryset=aims.models.ActivityParticipatingOrganisation.objects.filter(role='Funding').order_by('id')),
            Prefetch('sector',
                     queryset=aims.models.Sector.objects.filter(category__openly_type='iati')
                     .select_related('category').distinct('activity', 'category'),
                     to_attr='prefetch_sector_categories'),
            'title_set',
            'sector',
            'transaction_set__provider_organisation',
            'commitmenttotal',
            'commitmenttotal__currency'
        ).select_related('activity_status').distinct().order_by('-dollars', 'pk')

    def deprecated_get_transactions(self, activities: Union[QuerySet, None] = None):
        """ Return Transaction models matching GET request parameters.

        In addition to the Transaction-specific filters applied, the Transaction objects
        must correspond to one of the Activity models if passed

        """
        transactions = Transaction.objects.filter(activity__in=activities or self.get_queryset())
        if self.finance_type_categories is not None and (
                len(self.finance_type_categories) < aims.models.FinanceTypeCategory.objects.count()):
            transactions = transactions.filter(
                finance_type__category__in=self.finance_type_categories
            )
        if self.donor is not None:
            transactions = transactions.filter(provider_organisation__code=self.donor)
        return transactions

    def get_transactions(self, *args, **kwargs):
        """ Return Transaction models matching GET request parameters.

        In addition to the Transaction-specific filters applied, the Transaction objects
        must correspond to one of the Activity models if passed

        """

        if args or kwargs:
            return self.deprecated_get_transactions(*args, **kwargs)

        filters = self.transaction_filters()
        return Transaction.objects.filter(**filters)

    def filter_activities_by_daterange(self, activity_queryset):
        return aims.models.filter_activities_by_daterange(activity_queryset, self.start_date, self.end_date)

    def get_context_data(self, **kwargs):
        """ Mostly vanilla AjaxListView context that includes a date range and form

        'start_date' -- The start date currently used when filtering
        'end_date' -- The end ate currently used when filtering
        'filter_form' -- The form used to define allowable filter parameters in a GET request

        Note that currently the start/end date are not included in the filter form by default
        so they are separately set in the context. This is done so they can be set separately
        from the rest of the form, although this will likely change soon.
        """
        context = super(FilterFormView, self).get_context_data(**kwargs)
        context['start_date'] = self.start_date.strftime('%b %Y')
        context['end_date'] = self.end_date.strftime('%b %Y')
        self.form = self.get_form()
        context['filter_form'] = self.form
        context['filter_form_active'] = not self.is_filter_default()
        return context

    def is_filter_default(self):
        return len(self.filter_form_data) == 1 and 'activity_status' in self.filter_form_data and len(self.filter_form_data['activity_status']) == 1 and self.filter_form_data['activity_status'][0] == 'implementation'

    def get(self, request, *args, **kwargs):
        self.set_attributes(request, *args, **kwargs)
        self.object_list = self.get_queryset(*args, **kwargs)

        context = self.get_context_data(object_list=self.object_list,
                                        page_template=self.page_template, **kwargs)
        return self.process_context(context, request)

    def process_context(self, context, request):
        return self.render_to_response(context)

    def get_location_info(self):
        """
        Returns a dict of values which may be used in the template
        related to the current Location
        :return:
        """
        context = {}
        has_state = True if self.state else False
        uses_simple = getattr(settings, 'USE_SIMPLE_LOCATIONS', False)

        if uses_simple:
            states_queryset = Area.objects.filter(parent__code=settings.ROOT_COUNTRY_CODE).order_by('name').annotate(adm1_code=F('code'))
        else:
            states_queryset = Adm1Region.objects.exclude(name='').order_by('name')
        context['states'] = states_queryset.values('adm1_code', 'name')

        if uses_simple and has_state:
            state = Area.objects.get(code=self.state)
            context.update(
                current_state=state,
                filter_name='location',
                filter_value=state.code,
                location=state,
            )

        elif uses_simple and not has_state:
            context.update(location=Area.objects.filter(code=settings.ROOT_COUNTRY_CODE))

        elif not uses_simple and has_state:
            state = Adm1Region.objects.get(adm1_code=self.state)
            context.update(
                current_state=state,
                filter_name='location',
                filter_value=state.adm1_code,
                st_current=state.adm1_code,
                st_center=state.geom.centroid,
                current_extent=state.geom.extent,
                # commitments_by_location=self.commitment_by_location(as_list=True),
                json_borders="mm_townships.json"
            )

        elif not uses_simple and not has_state:
            context.update(
                json_borders="mm_states.json",
                # commitments_by_location=self.commitment_by_location(as_list=True),
            )

        return context
