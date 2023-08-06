from ast import Mod
from http import HTTPStatus
import logging
import os
import re
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Union
import warnings
from wsgiref.util import FileWrapper

from django.conf import settings
from django.contrib.postgres.aggregates import ArrayAgg
from django.core.files.temp import NamedTemporaryFile
from django.core.management import call_command
from django.db.models import QuerySet
from django.db.models import Count, F, Func, IntegerField, Max, Min, OuterRef, Q, Subquery, Sum, Value
from django.db.models.functions import Coalesce, Greatest, Least
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from aims.utils import render
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, View
from el_pagination.views import AjaxListView
from haystack.views import SearchView as HayStackSearchView
from simple_locations.models import Area

from aims import base_utils, models as aims
from aims.aggregates import Aggregates, AggregatesFactory, fy_annotation_lookup, financial_year_annotations, fy_annotation_prerequisites
from aims.exports import export_activities
from aims.views import FilterFormView, set_financial_year
from geodata import models as geodata

from . import forms

from sentry_sdk import capture_exception

logger = logging.getLogger(__name__)


class HttpResponseNoContent(HttpResponse):
    status_code = 204


class CastInt(Func):
    """ Trivial cast-to-int for postgres. Prevents JSON doing annoying things serializing Decimal types
    like dying or returning a string
    """
    template = '(%(expressions)s)::int'
    output_field = IntegerField()


def context_processor_site_context(request):
    """ Custom template context processor to add site name """
    return settings.OPENLY_SITE_CONTEXT


class CommitmentByLocation(FilterFormView):
    """
    Outputs JSON of total commitment and number of activities per area, aggregated to the child areas
    of the current view's "area_id" kwargs
    """

    def get(self, request, *args: Sequence[Any], **kwargs: Mapping[str, Any]):
        self.set_attributes(request, *args, **kwargs)
        activity_list = self.get_queryset(*args, **kwargs) or aims.Activity.objects.all()

        area_id = kwargs.get('area_id', 1)
        transaction_list = aims.TransactionValueLocation.objects.filter(
            location__area__in=Area.objects.get(pk=area_id).get_descendants(),
            activity__in=activity_list
        ).values_list('activity', 'location__area__lft', 'location__area__rght', 'dollars')

        commitments = {}
        for area in Area.objects.filter(parent__id=area_id):
            commitments[area.id] = {'commit': 0}
            activities = []
            for activity, lft, rght, dollars in transaction_list:
                if area.lft <= lft and rght <= area.rght:
                    commitments[area.id]['commit'] += dollars
                    if activity not in activities:
                        activities.append(activity)
            commitments[area.id]['count_activity'] = len(activities)

        return JsonResponse(commitments)


def csrf_failure(request, reason: str = ''):
    template = loader.get_template('403.html')
    return HttpResponseForbidden(template.render({}), content_type='text/html')


class AidBy(FilterFormView):
    """ Base view for date filtered activity dashboards """

    page_template = "dashboard/activity_page.html"
    template_name = "dashboard/aid_by.html"

    def __init__(self):
        FilterFormView.__init__(self)
        self.object_list: QuerySet = None
        if not getattr(settings, 'USE_SIMPLE_LOCATIONS', False):
            self.location_by_name = True

    def get(self, request, *args, **kwargs):
        '''
        Openly #16: Do not include 'debt relief' by default
        Modified to include 'Finance Type' as debt relief, and to be consistent
        when dates are changed
        '''
        has_keys = bool(len(request.GET.keys()))
        dates_only = set(request.GET.keys()) == {'start', 'end'}
        if request.GET and not dates_only:
            return super().get(request, *args, **kwargs)

        # Drop any 'aid type = debt relief'
        no_debt_relief = aims.AidTypeCategory.objects.exclude(code='F')  # raise MagicNumberWarning()
        no_debt_relief_list = no_debt_relief.values_list('name', flat=True)
        no_debt_relief_strings = ['aid_type_category=' + n.replace(' ', '_').replace('-', '_').lower() for n in no_debt_relief_list]

        # Also drop 'finance type = debt relief'
        finance_no_debt_relief = aims.FinanceTypeCategory.objects.exclude(code=600)  # raise MagicNumberWarning()
        finance_no_debt_relief = no_debt_relief.values_list('name', flat=True)
        no_debt_relief_strings.extend(['finance_type_category=' + n.replace(' ', '_').replace('-', '_').lower() for n in finance_no_debt_relief])

        querystring = '&'.join(no_debt_relief_strings)
        # Append to the 'get' request, or write a new one
        if has_keys:
            redirect_url = request.build_absolute_uri() + '&' + querystring
        else:
            redirect_url = request.build_absolute_uri() + '?' + querystring
        return redirect(redirect_url)

    def process_context(self, context: Dict[str, Any], request):
        """ Additional processing for GET requests beyond setting the context.

        We need special handling for the case of exports or AJAX requests. In the case of exports
        we don't need to re-render the page, we should generate an excel sheet of the filtered
        activities. In the case of an AJAX request to view a specific activity we use a different
        template.
        """

        if not self.get_allow_empty() and len(self.object_list) == 0:
            msg = _('Empty list and ``%(class_name)s.allow_empty`` is False.')
            raise Http404(msg % {'class_name': self.__class__.__name__})

        if self.is_export():
            try:
                return export_activities(context['object_list'], self.get_transactions(), summary=self.build_export_summary())
            except ModuleNotFoundError as E:
                """
                This is raised when optional dependency "xlwt" is not installed.
                Downgrade to a warning and sentry
                """
                capture_exception(E)
                return HttpResponseNoContent(f'{E}')

        if request.is_ajax():
            self.template_name = self.page_template
        try:
            context['site_name'] = settings.OPENLY_SITE_CONTEXT['site_name']
        except KeyError:
            warnings.warn('Settings missing an OPENLY_SITE_CONTEXT object')
            context['site_name'] = 'Openly'

        context['project_name'] = getattr(settings, 'PROJECT_NAME', 'Openly')

        return self.render_to_response(context)

    def is_export(self):
        return 'export' in self.request.GET

    def get_context_data(self, **kwargs: Union[None, Mapping[Any, Any]]) -> Dict[str, Any]:
        context = super(AidBy, self).get_context_data(**kwargs)
        context['for_render'] = 'render' in self.request.GET
        if hasattr(self.request.user, 'userorganisation'):
            context['userorganisation'] = self.request.user.organisation

        # The 'true' list has some quite complex annotations
        # which slow down these aggregations
        # Where possible use 'simple_objects' rather than 'self.object_list'
        simple_objects = aims.Activity.finance.filter(**self.queryset_filters())

        context['count'] = simple_objects.count()
        # Set dates for "Show All Dates" UI.
        # We use the earliest / latest "Planned Activity" dates, falling back to ALL activities, falling back
        # to 1990 - 2050
        dates = simple_objects.aggregate(
            max_date=Greatest(Max('end_actual'), Max('end_planned')),
            min_date=Least(Min('start_actual'), Min('start_planned'))
        )
        if dates['max_date']:
            context['max_date'] = dates['max_date'].strftime("%b %Y")
            context['max_date_iso'] = dates['max_date'].isoformat()
        else:
            logger.debug('No "max_date" determined. Use random hardcoded value')
            context['max_date'] = 'Dec 2050'
            context['max_date_iso'] = '2050-12-31'

        if dates['min_date']:
            context['min_date'] = dates['min_date'].strftime("%b %Y")
            context['min_date_iso'] = dates['min_date'].isoformat()
        else:
            logger.debug('No "min_date" determined. Use random hardcoded value')
            context['min_date'] = 'Jan 1990'
            context['min_date_iso'] = '1990-01-01'

        assert 'min_date' in context and 'max_date' in context
        assert 'min_date_iso' in context and 'max_date_iso' in context

        context['project_name'] = getattr(settings, 'PROJECT_NAME', "")
        if 'organisation' not in context:
            context['organisation'] = None
        if 'current_donor' not in context:
            context['current_donor'] = None
        return context


class AidBySummary(AidBy):
    """
    Diagnostic view to show/explain how aggregates are generated
    """

    def get_context_data(self, *args, **kwargs):
        context = super(AidBy, self).get_context_data(**kwargs)
        self.template_name = "dashboard/summary.html"
        transactions = aims.Transaction.objects.filter(**self.transaction_filters())
        commitments = transactions.filter(transaction_type='C')
        data = Aggregates(commitments).to_dict()
        data['filters'] = self.transaction_filters()
        context['chart_data'] = data
        context['data'] = render(data)
        return context


class AidBySector(AidBy):
    """ Sector specific dashboard """

    def get_context_data(self, **kwargs):
        context = super(AidBySector, self).get_context_data(**kwargs)

        self.template_name = "dashboard/aid_by_sector.html"
        context['page_title'] = _('Aid By Sector')
        context['by'] = 'sector'

        if self.category:
            if not self.category == base_utils.UNKNOWN_CATEGORY_CODE:
                context['category'] = get_object_or_404(aims.SectorCategory, code=self.category)
            else:
                context['category'] = {'name': base_utils.UNKNOWN_CATEGORY_NAME, 'code': base_utils.UNKNOWN_CATEGORY_CODE}
            context['filter_name'] = 'category'
            context['filter_value'] = self.category
        if self.sector:
            context['sector'] = get_object_or_404(aims.SectorCategory, code=self.sector)

        # Charts with aggregation and annotation
        context['categories'] = aims.SectorCategory.objects.all().values_list('name', 'code',).order_by('name')
        # shorten category names
        context['categories'] = [(re.sub(" and ", " & ", cat[0], flags=re.IGNORECASE), cat[1]) for cat in context['categories']]

        if self.request.is_ajax() or self.is_export():
            return context

        data = AggregatesFactory.aggregates(transaction_type='C', **self.transaction_filters()).to_dict()
        totals_by_type = AggregatesFactory.aggregates(**self.transaction_filters()).by_transaction_type()
        data['total'] = {t['name']: t['dollars'] for t in totals_by_type}
        context['total_commitments'] = base_utils.prettify(data['total'].get('commitment', 0))
        context['total_disbursements'] = base_utils.prettify(data['total'].get('disbursement', 0))

        if context['total_commitments'][0] == 0:
            context['executed'] = 0
        else:
            try:
                context['executed'] = (context['total_disbursements'][0] / context['total_commitments'][0]) * 100
            except BaseException:
                context['executed'] = 0
        context['data'] = render(data)
        return context


class AidByLocation(AidBy):
    """ Location specific dashboard """

    def __init__(self):
        AidBy.__init__(self)
        if not getattr(settings, 'USE_SIMPLE_LOCATIONS', False):
            self.location_by_name = False

    def get_context_data(self, **kwargs):
        context = super(AidByLocation, self).get_context_data(**kwargs)
        self.template_name = "dashboard/aid_by_location.html"

        context['page_title'] = _('Aid By Location')
        context['by'] = 'location'

        # early out to avoid getting unnecessary data
        if self.request.is_ajax() or self.is_export():
            return context

        data = AggregatesFactory.aggregates(transaction_type='C', **self.transaction_filters()).to_dict()
        totals_by_type = AggregatesFactory.aggregates(**self.transaction_filters()).by_transaction_type()
        data['total'] = {t['name']: t['dollars'] for t in totals_by_type}
        context['total_commitments'] = base_utils.prettify(data['total'].get('commitment', 0.0))
        context['total_disbursements'] = base_utils.prettify(data['total'].get('disbursement', 0.0))

        location_info = self.get_location_info()
        context.update(location_info)
        context['data'] = render(data)
        return context


class GeoJson(AidBy):

    def get(self, request, *args, **kwargs):
        self.set_attributes(request, *args, **kwargs)

        if self.state:
            area = Area.objects.get(code=self.state)
        else:
            area = Area.objects.filter(level=0).first()
        simplify = float(request.GET.get('simplify', 1e-4))
        dp = int(request.GET.get('dp', 3))
        transactions = self.get_transactions()

        return JsonResponse(Aggregates(transactions).as_geojson(area=area, simplify=simplify, dp=dp))


class AidByMinistry(AidBy):
    """ Ministry specific dashboard """

    def get_context_data(self, **kwargs):
        context = super(AidByMinistry, self).get_context_data(**kwargs)
        self.template_name = "dashboard/aid_by_ministry.html"
        context['page_title'] = _('Aid By Ministry')
        context['by'] = 'ministry'
        ministry = kwargs.get(context['by'])

        if ministry:
            current_ministry = get_object_or_404(aims.Organisation, code=ministry)
            context['current_ministry'] = current_ministry
            context['filter_name'] = 'ministry'
            context['filter_value'] = current_ministry.code

        # early out to avoid getting unnecessary data
        if self.request.is_ajax() or self.is_export():
            return context

        data = AggregatesFactory.aggregates(transaction_type='C', **self.transaction_filters()).to_dict()
        totals_by_type = AggregatesFactory.aggregates(**self.transaction_filters()).by_transaction_type()
        data['total'] = {t['name']: t['dollars'] for t in totals_by_type}
        context['total_commitments'] = base_utils.prettify(data['total'].get('commitment', 0))
        context['total_disbursements'] = base_utils.prettify(data['total'].get('disbursement', 0))

        context['ministry_list'] = aims\
            .ActivityParticipatingOrganisation.objects.exclude(organisation__name=None)\
            .filter(role='Accountable', organisation__type__name='National Ministry')\
            .values_list('organisation__code', 'organisation__name')\
            .distinct()
        context['data'] = context['data'] = render(data)

        return context


class AidByDonor(AidBy):
    """ Donor specific dashboard """

    def get_context_data(self, **kwargs):
        context = super(AidByDonor, self).get_context_data(**kwargs)
        self.template_name = "dashboard/aid_by_donor.html"
        context['page_title'] = _('Aid By Donor')
        context['by'] = 'donor'

        donor = kwargs.get('donor', None)
        donor_unknown = (donor == base_utils.UNKNOWN_DONOR_CODE)
        if donor:

            if donor_unknown:
                context['current_donor'] = {
                    'name': base_utils.UNKNOWN_DONOR_NAME,
                    'code': base_utils.UNKNOWN_DONOR_CODE}
            elif aims.Organisation.objects.filter(code=donor).exists():
                org = aims.Organisation.objects.get(code=donor)
                tmp = base_utils.arrange_donor_info_row(org, 0)
                context['current_donor'] = {
                    'name': tmp[3],
                    'code': tmp[2]
                }

            context['filter_name'] = 'donor'
            context['filter_value'] = donor

        context['donors'] = aims\
            .Transaction.objects.exclude(provider_organisation__name=None)\
            .values_list('provider_organisation__code', 'provider_organisation__name')\
            .distinct()\
            .order_by('provider_organisation__name')

        # early out to avoid getting unnecessary data
        if self.request.is_ajax() or self.is_export():
            return context

        data = AggregatesFactory.aggregates(transaction_type='C', **self.transaction_filters()).to_dict()
        totals_by_type = AggregatesFactory.aggregates(**self.transaction_filters()).by_transaction_type()
        data['total'] = {t['name']: t['dollars'] for t in totals_by_type}
        context['donors_commitment'] = base_utils.prettify(data['total'].get('commitment', 0))
        context['donors_disbursement'] = base_utils.prettify(data['total'].get('disbursement', 0))

        context['data'] = context['data'] = render(data)
        context['donors_count'] = len(data['by']['donor'])
        return context


class Exporter(View):

    def get(self, request, *args, **kwargs):
        method = kwargs['method']

        if method == "PNG" or method == "PDF":

            url = "{0}?{1}&render".format(request.GET['path'], request.GET['query'])
            title = request.GET['title']

            tmp_suffix = "." + title + "." + method.lower()
            return_name = title + "." + datetime.now().isoformat() + "." + method.lower()
            newfile = NamedTemporaryFile(suffix=tmp_suffix)

            call_command('scraper', settings.SCRAPER_URL + url, newfile.name)

            mime_type = 'application/pdf' if method == "PDF" else 'image/png'

            wrapper = FileWrapper(newfile)
            response = HttpResponse(wrapper, content_type=mime_type)
            response['Content-Disposition'] = 'attachment; filename=%s' % return_name
            response['Content-Length'] = os.path.getsize(newfile.name)
            return response

        else:
            return None


class SearchView(AjaxListView, HayStackSearchView):

    template_name = 'search/search.html'
    page_template = 'search/result.html'
    form_class = forms.ActivitySearchForm
    load_all = True
    searchqueryset = None

    def get_queryset(self, *args, **kwargs):

        self.form = self.build_form()
        self.query = self.get_query()
        return self.get_results()

    def get_context_data(self, *args, **kwargs):

        context = super(SearchView, self).get_context_data(**kwargs)
        context['page_title'] = _('Search')
        context['page_template'] = self.page_template
        context['form'] = self.form

        if self.request.is_ajax():
            self.template_name = self.page_template

        context['search_term'] = self.request.GET.get('q', '')

        return context


class QueryBuilder(TemplateView):
    template_name = 'dashboard/query_builder.html'

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['start_date'], context['end_date'] = set_financial_year(self.request.session)
        context['fy_end_month'] = getattr(settings, 'FINANCIAL_YEAR_ENDS', 12)
        context['project_name'] = getattr(settings, 'PROJECT_NAME', "")

        # Set dates for "Show All Dates" UI.
        # We use the earliest / latest "Planned Activity" dates, falling back to ALL activities, falling back
        # to 1990 - 2050
        max_dates_list = [
            aims.Activity.objects.all().aggregate(Max('end_actual'))['end_actual__max'],
            aims.Activity.objects.all().aggregate(Max('end_planned'))['end_planned__max']
        ]
        max_date = max([d for d in max_dates_list if d is not None], default=None)
        if max_date:
            context['max_date'] = max_date.strftime("%b %Y")
            context['max_date_iso'] = max_date.isoformat()
        else:
            logger.debug('No "max_date" determined. Use random hardcoded value')
            context['max_date'] = 'Dec 2050'
            context['max_date_iso'] = '2050-12-31'

        min_dates_list = [
            aims.Activity.objects.all().aggregate(Min('start_actual'))['start_actual__min'],
            aims.Activity.objects.all().aggregate(Min('start_planned'))['start_planned__min']
        ]
        min_date = min([d for d in min_dates_list if d is not None], default=None)
        if min_date:
            context['min_date'] = min_date.strftime("%b %Y")
            context['min_date_iso'] = min_date.isoformat()
        else:
            logger.debug('No "min_date" determined. Use random hardcoded value')
            context['min_date'] = 'Jan 1990'
            context['min_date_iso'] = '1990-01-01'

        assert 'min_date' in context and 'max_date' in context
        assert 'min_date_iso' in context and 'max_date_iso' in context

        return context


class QueryBuilderData(View):

    @staticmethod
    def stringify_keys(list_of_dicts, keys):
        """ For each dictionary in `list_of_dicts`, transforms the elemets found as `keys` into strings.

        For example, this should be called on DateField or DecimalField.
        """
        for object_representation in list_of_dicts:
            for key in keys:
                python_value = object_representation[key]
                if python_value is not None:
                    object_representation[key] = str(object_representation[key])

    def get(self, request, format=None):
        return JsonResponse(self.get_data())

    def get_data(self):
        data = {}

        statuses = aims.ActivityStatus.objects.values('code', 'name')
        transaction_types = aims.TransactionType.objects.values('code', 'name')
        aid_types = aims.AidType.objects.values('code', 'name', 'category_id')
        aid_type_categories = aims.AidTypeCategory.objects.values('code', 'name')
        finance_type_categories = aims.FinanceTypeCategory.objects.values('code', 'name')
        finance_types = aims.FinanceType.objects.values('code', 'name', 'category_id')
        document_categories = aims.DocumentCategory.objects.values('code', 'name')
        activities_queryset = aims.Activity.objects.all().prefetch_related('activitysector__sector__category')
        activities = activities_queryset\
            .values('id', 'iati_identifier', 'internal_identifier', 'reporting_organisation_id', 'activity_status_id', 'start_planned', 'start_actual', 'end_planned', 'end_actual', 'completion', 'date_created', 'date_modified')\
            .annotate(budget_total=Coalesce(Sum('budget_set_usd__usd_value'), Value(0))) \
            .annotate(document_categories=ArrayAgg('documentlink__categories__code'))\
            .annotate(docs_uploaded=Count('documentlink', distinct=True))\
            .annotate(mou_docs=Subquery(aims.DocumentLink.objects.filter(
                categories__code__in=["A09", "B13"], activity_id=OuterRef('id'))
                .values('id')
                .annotate(cnt=Count('id'))
                .values('cnt'),
                output_field=IntegerField()
            ))

        if 'oipa' in settings.INSTALLED_APPS:
            activities = activities.annotate(iati_sync=Func(F('oipaactivitylink__oipa_fields'), 1, function='array_length'))
            for a in activities:
                a['iati_sync'] = True if a['iati_sync'] else False

        titles = aims.Title.objects.values('activity_id', 'title', 'language')
        locations = aims.Location.objects.values('activity_id', 'adm_country_adm1', 'adm_country_adm2', 'adm_code', 'name', 'percentage')
        townships = geodata.Adm2Region.objects.values('region_id', 'region__name', 'code', 'name', 'region__adm1_code')

        transactions = list(
            aims.Transaction.objects
                .prefetch_related('activity', 'usd_value', 'aid_type')
                .annotate(**fy_annotation_prerequisites())
                .annotate(fy=financial_year_annotations())
                .all()
                .values('id', 'activity_id', 'activity__activity_status_id', 'activity__default_aid_type_id', 'activity__reporting_organisation_id', 'activity__reporting_organisation__name', 'activity__default_finance_type_id', 'transaction_type_id', 'aid_type_id', 'aid_type__category_id', 'finance_type_id', 'usd_value', 'provider_organisation_id', 'provider_organisation__name', 'receiver_organisation_id', 'transaction_date', 'fy')
                .filter(activity__in=activities_queryset)
        )

        for t in transactions:
            t['usd_value'] = round(float(t['usd_value'] or 0), 2)

        activity_sectors = aims.ActivitySector.objects.values('activity_id', 'sector_id', 'percentage')

        organisations = aims.Organisation.objects.values('code', 'name', 'abbreviation')
        participating_organisations = aims.ActivityParticipatingOrganisation.objects.values('activity_id', 'role', 'organisation_id')

        if getattr(settings, 'ACCOUNTABLE_PARTNERS_LOCAL_MINISTRIES', False):
            # Filter so that if ACCOUNTABLE_PARTNERS_LOCAL_MINISTRIES, only Government ministries show in the 'By Partner Ministry' list
            accountable_is_government = Q(role="Accountable", organisation__in=aims.LocalMinistry.objects.all()) | ~Q(role="Accountable")
            participating_organisations = participating_organisations.filter(accountable_is_government)

        # convert the date and Decimal objects to strings
        self.stringify_keys(transactions, keys=['transaction_date'])
        self.stringify_keys(locations, keys=['percentage'])
        self.stringify_keys(activities, keys=['start_planned', 'start_actual', 'end_planned', 'end_actual'])
        self.stringify_keys(activity_sectors, ['percentage'])

        data['activity_sector_categories'] = defaultdict(list)
        for activity_sectorcat in aims.SectorCategory.objects \
                .exclude(sector__activitysector__vocabulary_id='RO') \
                .annotate(activity=F('sector__activitysector__activity'),
                          percentage=CastInt(Sum('sector__activitysector__percentage'))) \
                .values('activity', 'percentage', 'code'):
            data['activity_sector_categories'][activity_sectorcat.pop('activity')].append(activity_sectorcat)

        data['sector_categories'] = {s['code']: s['name'] for s in aims.SectorCategory.objects.exclude(code=1).values('code', 'name')}
        data['transactions'] = transactions
        data['transaction_fy_lookup'] = fy_annotation_lookup()
        data['activities'] = list(activities)
        data['titles'] = list(titles)
        data['locations'] = list(locations)
        data['townships'] = list(townships)
        data['activity_sectors'] = list(activity_sectors)
        data['participating_organisations'] = list(participating_organisations)
        data['document_categories'] = list(document_categories)
        data['statuses'] = list(statuses)
        data['transaction_types'] = list(transaction_types)
        data['aid_types'] = list(aid_types)
        data['aid_type_categories'] = list(aid_type_categories)
        data['finance_types'] = list(finance_types)
        data['finance_type_categories'] = list(finance_type_categories)
        data['sectors'] = list(aims.Sector.objects.values('code', 'name', 'category__name', 'category__code'))
        data['organisations'] = list(organisations)

        # Add 'national sectors' - in Myanmer, these are SWGs
        data['national_sectors'] = list(aims.NationalSector.objects.all().values('code', 'name', 'category__name', 'category__code'))
        data['national_sector_percentage'] = list(aims.ActivitySector.objects.filter(sector__in=aims.NationalSector.objects.all()).values('activity', 'percentage', 'sector'))

        return data


class WelcomeJS(TemplateView):
    template_name = "welcome.js"
    content_type = "application/javascript"
