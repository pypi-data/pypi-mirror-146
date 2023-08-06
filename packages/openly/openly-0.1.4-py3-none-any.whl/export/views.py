import collections
import io
import logging
from csv import writer as csvwriter
from datetime import date
from hashlib import sha1
from typing import Any, Dict, Iterable, Tuple, List
from django.http import JsonResponse
from django.conf import settings
from django.contrib.postgres.aggregates.general import StringAgg
from django.utils.translation import activate

import six
import sqlparse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import InvalidCacheBackendError, caches
from django.core.exceptions import FieldError
from django.db import connection
from django.db.models import F, TextField, QuerySet
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView, View
from profiles_v2.models import Person

from django.db.models import OuterRef, Subquery

from aims.aggregates import (
    Aggregates, activity_commitment_total_subquery, activity_name_subquery, activity_oipa_sync_subquery,
    activity_organisations_subquery_list, activity_sector_category_subquery, date_as_decimal_quarter,
    location_hierarchy_anno, sector_subquery, sector_tiers, state_pcode_to_isocode,
)
from aims.models import Activity, ActivitySector, ContactInfo, Location, Budget, Organisation, OrganisationRole, Sector, SectorCategory, Transaction, Title, Description, DescriptionType
from aims.views import FilterFormView
from aims import common_text

from .excel_export import (
    ActivitiesWithoutBudget, ActivitiesWithoutDate, ActivitiesWithoutTransaction, ActivityAnnualBreakdown,
    ActivityExporter, DevelopmentPartnerAnnualBreakdown, DevelopmentPartnerProfile, DonorSummaryExporter,
    SectorAnnualBreakdown, SectorSummaryExporter, SectorWorkingGroup, StateAnnualBreakdown, TownshipAnnualBreakdown,
)
from .forms import ExportForm


def all_subclasses(cls):
    '''
    Handy function to let us get nested subclasses
    '''
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


logger = logging.getLogger(__name__)


class QueryFilter:
    '''
    param: Request parameter
    field: field to filter on
    expr: a dunder method like '__in', '__eq'
    value: default filter value is none is provided
    description: Note to user why we filter like this

    Define a "QueryFilter" with a GET/POST parameter, field name, expression (like '__eq', '__in' etc, the filtering value, and a description)
    '''
    def __init__(self, param, field, expr='', value: Any = None, description: str = '', cast=str):
        self.param = param
        self.field = field
        self.expr = expr
        self.value = value
        self.description = description
        self.cast = cast


EXPORT_HEADERS = {
    'id': str(_("Identifier")),
    'activity': str(_(common_text.get("activity_or_program") + ' ID')),
    'activity_name_id': str(_("Activity")),
    'aid_type': str(_("Aid Type")),
    'title': str(_("Title")),
    'description': str(_('Description')),
    'status': str(_("Status")),
    'openly_status': str(_("Publish Status")),
    'collaboration_type': str(_("Collaboration Type")),
    'aid_type_category': str(_("Aid Type Categories")),
    'finance_type__name': str(_("Finance Type")),
    'flow_type__name': str(_("Flow Type")),
    'reporting_organisation': str(_("Reporting Organisation")),
    'start_planned': str(_("Planned Start Date")),
    'end_planned': str(_("Planned End Date")),
    'start_actual': str(_("Actual Start Date")),
    'end_actual': str(_("Actual End Date")),
    'currency__name': str(_('Currency Name')),
    'usd_value': str(_('USD Value')),
    'flow_type': str('Flow Type Id'),
    'provider_activity': str(_('Provider Activity')),
    'iso': str(_('ISO location code')),
    'oipaactivitylink__acitivity_id': str(_('IATI Activity Linked'))
}


def export_header(field):
    if field in EXPORT_HEADERS:
        return EXPORT_HEADERS.get(field)
    # Very simple 'humanize' function
    return field.replace('__', ' ').replace('_', ' ').title()


class ExportView(FilterFormView):
    """ View for generating data exports in excel format according to a variety of templates."""
    template_name = 'export/index.html'
    location_by_name = True
    report_type = ''  # Subclasses should override this
    data_quality_type = ''  # Subclass should override this

    def __init__(self):
        FilterFormView.__init__(self)
        self.object_list = None

    def process_context(self, context, request, *args, **kwargs):
        if self.form.is_valid():
            return self.generate_export(context['object_list'], *args, **kwargs)
        return self.render_to_response(context)

    def get_form(self):
        return ExportForm(self.filter_form_data)

    def get_queryset(self, *args, **kwargs):
        activities = super(ExportView, self).get_queryset(*args, **kwargs)
        if self.development_partner is not None:
            activities = activities.filter(reporting_organisation=self.development_partner)
        if self.sector_working_group is not None:
            activities = activities.filter(activitysector__sector=self.sector_working_group)
        return activities

    def set_attribute(self, attribute_name):
        if attribute_name in self.request.GET:
            setattr(self, attribute_name, self.request.GET[attribute_name])
            self.filter_form_data[attribute_name] = self.request.GET[attribute_name]
        else:
            setattr(self, attribute_name, None)

    def set_missing_dates(self, **kwargs):
        if 'missing_dates' in self.request.GET:
            self.missing_dates = self.request.GET.getlist('missing_dates')
        else:
            self.missing_dates = None
        self.filter_form_data['missing_dates'] = self.missing_dates

    def set_development_partner(self, **kwargs):
        if ('development_partner' in self.request.GET and self.request.GET['development_partner'] != ''):
            dp_id = self.request.GET['development_partner']
            self.development_partner = Organisation.objects.get(pk=dp_id)
            self.filter_form_data['development_partner'] = dp_id
        else:
            self.development_partner = None

    def set_sector_working_group(self, **kwargs):
        if ('sector_working_group' in self.request.GET and self.request.GET['sector_working_group'] != ''):
            swg_id = self.request.GET['sector_working_group']
            self.sector_working_group = Sector.objects.get(pk=swg_id)
            self.filter_form_data['sector_working_group'] = swg_id
        else:
            self.sector_working_group = None

    def set_attributes(self, request, *args, **kwargs):
        super(ExportView, self).set_attributes(request, *args, **kwargs)
        self.set_attribute('report_type')
        self.set_development_partner(**kwargs)
        self.set_sector_working_group(**kwargs)
        self.set_attribute('data_quality_type')
        self.set_missing_dates()

    def generate_export(self, activities, *args, **kwargs):
        transactions = self.get_transactions(activities)
        filebase_title = self.report_type

        # Get the appropriate exporter and file name base for the report type
        if self.report_type == 'donor_summary':
            exporter = DonorSummaryExporter()
        elif self.report_type == 'sector_summary':
            exporter = SectorSummaryExporter()
        elif self.report_type == 'development_partner_report':
            exporter = ActivityExporter(column_titles=ActivityExporter.PARTNER_COLUMN_TITLES,
                                        title=self.development_partner.name)
            filebase_title = self.development_partner
        elif self.report_type == 'sector_report':
            sector_name = SectorCategory.objects.get(code=self.sector).name
            exporter = ActivityExporter(column_titles=ActivityExporter.SECTOR_COLUMN_TITLES,
                                        title=sector_name)
            filebase_title = sector_name
        elif self.report_type == 'location_report':
            location = self.state if self.state is not None else 'All Locations'
            exporter = ActivityExporter(title=location)
            filebase_title = self.state if self.state is not None else 'All Locations'
        elif self.report_type == 'activity_annual_breakdown':
            exporter = ActivityAnnualBreakdown(years=list(range(self.start_date.year,
                                                                self.end_date.year + 1)))
        elif self.report_type == 'dp_annual_breakdown':
            exporter = DevelopmentPartnerAnnualBreakdown(years=list(range(self.start_date.year,
                                                                          self.end_date.year + 1)))
            filebase_title = 'development_partners_annual_breakdown'
        elif self.report_type == 'state_annual_breakdown':
            exporter = StateAnnualBreakdown(years=list(range(self.start_date.year,
                                                             self.end_date.year + 1)))
        elif self.report_type == 'township_annual_breakdown':
            exporter = TownshipAnnualBreakdown(years=list(range(self.start_date.year,
                                                                self.end_date.year + 1)))
        elif self.report_type == 'sector_annual_breakdown':
            exporter = SectorAnnualBreakdown(years=list(range(self.start_date.year,
                                                              self.end_date.year + 1)))
        elif self.report_type == 'dp_quarterly_breakdown':
            exporter = DevelopmentPartnerAnnualBreakdown(years=list(range(self.start_date.year,
                                                                          self.end_date.year + 1)),
                                                         quarterly=True)
            filebase_title = 'development_partners_quarterly_breakdown'
        elif self.report_type == 'state_quarterly_breakdown':
            exporter = StateAnnualBreakdown(years=list(range(self.start_date.year,
                                                             self.end_date.year + 1)),
                                            quarterly=True)
        elif self.report_type == 'township_quarterly_breakdown':
            exporter = TownshipAnnualBreakdown(years=list(range(self.start_date.year,
                                                                self.end_date.year + 1)),
                                               quarterly=True)
        elif self.report_type == 'sector_quarterly_breakdown':
            exporter = SectorAnnualBreakdown(years=list(range(self.start_date.year,
                                                              self.end_date.year + 1)),
                                             quarterly=True)
        elif self.report_type == 'sector_working_group':
            sector = self.sector_working_group
            exporter = SectorWorkingGroup(sector)
            filebase_title = sector.name + '_sector_working_group'
        elif self.report_type == 'development_partner_profile':
            exporter = DevelopmentPartnerProfile()
        elif self.report_type == 'data_quality':
            if self.data_quality_type == 'activities_without_date':
                exporter = ActivitiesWithoutDate(date_columns=self.missing_dates)
            elif self.data_quality_type == 'activities_absent_dashboard':
                exporter = ActivitiesWithoutDate(date_columns=[])
            elif self.data_quality_type == 'activities_without_transaction':
                exporter = ActivitiesWithoutTransaction()
            elif self.data_quality_type == 'activities_without_commitment':
                exporter = ActivitiesWithoutTransaction(transaction_type='C')
            elif self.data_quality_type == 'activities_without_budget':
                exporter = ActivitiesWithoutBudget()
            filebase_title = self.data_quality_type

        # Generate the data and add as attachment to response
        output = exporter.export(activities, transactions, filters=self.filter_form_data)
        output.seek(0)
        today = date.today()
        response = HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = 'attachment; filename="{}-{}.xlsx"'.format(
            filebase_title, today.strftime('%Y_%m_%d')
        )

        return response


class ExportSheet(View):
    '''
    This is a generic exporter function for a workbook
    which ought to make future exports a little easier
    '''

    def get_sheetname(self):
        if hasattr(self, 'sheetname'):
            return self.sheetname
        if hasattr(self, 'title'):
            return self.title

    def __init__(self, *args, **kwargs):
        super(ExportSheet, self).__init__(*args, **kwargs)
        # Assign cell formatting strings - usually date / monetary fields
        # {Label[str]: field parameters[dict]}
        self.cell_formats = {
            'iso_date': {'num_format': 'yyyy-mm-dd'},
            'currency_format': {'num_format': '$#,##0'},
            'percentage': {'num_format': '0%'},
            'bold': {'bold': True},
        }

        if 'cell_formats' in kwargs:
            self.cell_formats.update(kwargs.get('cell_formats'))
        # This is populated at a later time, as we nede to instantiate the workbook first
        # {Label[str] : Format[excel_fmt_object]}
        self.excel_formats = {}
        self.object_row = 1

        # Set the default headers. These are used
        # to generate default cache keys.
        self.cache_properties = {
            'format': kwargs.get('export_format', 'xlsx'),
            'module': self.__class__.__qualname__,
            'url': 'exports:%s' % (self.__class__.__qualname__,)
        }
        logger.debug('%s', self.cache_properties)

        # Set True to always refresh cache
        # This is useful to programatically 'force' a refresh
        self.always_refresh_cache = kwargs.get('always_refresh_cache', False)
        self.column_widths = {}

    def export_header(self, field: str) -> str:
        '''
        Return a "translated" or humanized field name
        '''
        if field in self.export_headers:
            return self.export_headers.get(field)
        elif field in EXPORT_HEADERS:
            return EXPORT_HEADERS.get(field)
        # Very simple 'humanize' function
        return field.replace('__', ' ').replace('_', ' ').title()

    @cached_property
    def domain(self):
        return self.request.META['HTTP_HOST']

    # Check which format you wish to have for a given field with this hash of fieldname and format string
    # The format string ought to correspond to a key in self.cell_formats and self.excel_formats
    # Add a format to the workbook, then reference it
    # {field_name[str]: format[str]}
    field_lookups = {}

    # Alter the content of a given field before writing with this hash of field name and mogrify function
    # Lookup table for function {field_name: function(object: list, field: int, request: Request)}
    # Eg
    # def activity_hyperlink(self, instance: Transaction, field: int, request) -> str:
    #    '''
    #    Returns the hyperlink to activity profile page
    #    '''
    #    return self.request.build_absolute_uri(reverse('activity_profile', kwargs={'activity_id': transaction[field]}))

    field_format_functions = {}

    # Lookup which write function to use write_datetime, write_url, write_string, write_rich_string etc
    # Check which functions are available in the "worksheet" class
    field_write_functions = {}

    # Map an "instance" of an object to a row based on its primary key
    object_row_map = {}

    # Map a field on the queryset to a column
    field_column_map = {}

    # Map a field to a header format
    export_headers = {}

    # In any subclass, this ought to be a Queryset
    queryset = None

    # Define which fields you want to include in the export
    # For simple use cases a list of values here is fine
    # For anything complex (relationships, annotations) you may overrride 'get_fields' instead
    fields = []

    # Define which fields you do NOT want in raw SQL
    # An example where this might be required is when 'pk' and 'id' fields are both specified,
    # but one is hacked to return a URL - for example Activity - this
    # would have the _same_ field name and content in the export
    skip_for_rawsql = ()

    exclude_pks = False

    # Set the maximum length of column (for large string aggregates)
    max_col_width = 100

    @property
    def cache(self):
        '''
        Return the Django cache backend to use
        Defaults to a backend called 'file' if it exists
        Else uses 'default'
        Set settings.CACHES['file'] to a FileBasedCache
        if you experience problems caching potentially large Excel files
        '''
        try:
            return caches['file']
        except InvalidCacheBackendError:
            logger.warn('No explicit "file" cache - your request will not be cached and may be very slow')
            return None

    @property
    def cache_key(self, **kwargs):
        '''
        Vary the cache response based on request (if any) headers
        cache_properties is set in the __init__ method but may be further updated by e.g. the 'get' method
        This allows caching to be performed within the request or by a scheduler outside of it
        '''
        # Get a sha hash of the 'cache_properties' dict
        key = sha1(repr(sorted(list(self.cache_properties.items()))).encode())
        return key.hexdigest()

    @property
    def get_cached(self):
        '''
        Return the cached object for this instance unless
        always_refresh_cache is True, in which case pretend there is no cache
        '''
        if self.always_refresh_cache is True:
            logger.debug('always_refresh_cache is true')
            return
        key = self.cache_key
        if not self.cache:
            return None
        cached = self.cache.get(self.cache_key)
        if not cached:
            logger.debug('%s Cache miss', key)
        logger.debug('%s Cache hit', key)
        return cached

    def set_cache(self, content, timeout=3600):
        if self.cache:
            key = self.cache_key
            logger.debug('%s Cache setting', key)
            self.cache.set(self.cache_key, content, timeout)
        return content

    def generate_response(self):
        '''
        Return and optionally cache a response
        This is outside of the main 'get' method to be independent of 'self.request' in
        order to allow task-scheduled caching
        '''
        export_format = self.cache_properties.get('format')
        if export_format == 'xlsx':
            workbook = self.get_cached or self.set_cache(self.create_workbook())
            response = HttpResponse(workbook, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=%s.xlsx" % (self.get_filename(),)
        elif export_format == 'csv':
            workbook = self.get_cached or self.set_cache(self.create_csv())
            response = HttpResponse(workbook, content_type="text/csv")
            response['Content-Disposition'] = "attachment; filename=%s.csv" % (self.get_filename(),)
        elif export_format == 'csv_raw':
            #  Variant of 'csv' which includes no header translation
            #  for reading programmatically
            workbook = self.get_cached or self.set_cache(self.create_csv(unformatted_headers=True))
            response = HttpResponse(workbook, content_type="text/csv")
            response['Content-Disposition'] = "attachment; filename=%s.csv" % (self.get_filename(),)
        elif export_format == 'json':
            qs = self.get_filtered_queryset()
            fields = self.get_write_fields()
            values = qs.values(*fields)
            response = JsonResponse(list(values), safe=False)
        else:
            logger.debug('%s', self.cache_properties)
            raise TypeError('Unhandled export type -- %s' % (export_format,))
        return response

    def array_handler(self, content: Iterable) -> str:
        '''
        This is a 'handler' for ArrayFields
        returned as part of the queryset
        '''
        return ', '.join(content)

    @classmethod
    def get_queryset(cls):  # -> Queryset
        '''
        You very probably wish to override this
        Unless you have a simple use case, where you could override
        self.queryset in your subclass
        '''
        return cls.queryset

    def get_filtered_queryset(self) -> QuerySet:
        filters = self.get_filters()
        excludes = self.get_excludes()
        return self.get_queryset().filter(**filters).exclude(**excludes)

    @classmethod
    def get_annotations(cls):
        return {}

    def get_fields(self) -> List:
        fields = []
        fields.extend(self.fields)
        return fields

    def get_write_fields(self):
        fields = []
        for f in self.get_fields():
            if f.startswith('_') or f in fields:
                continue
            fields.append(f)
        return fields

    def writable(self, instance: Dict, field: str) -> Tuple[int, int, str]:
        '''
        Returns a row, col index, content to be written
        Formats content according to 'field_format_functions'
        '''
        col = self.field_column_map[field]
        if field in self.field_format_functions:
            content = self.field_format_functions[field](self, instance, field)
        else:
            content = instance.get(field)

        # Optionally - we can specify a content type
        if field in self.field_lookups:
            return col, content, self.excel_formats[self.field_lookups[field]]
        if 'default' in self.excel_formats:
            return col, content, self.excel_formats['default']
        return col, content

    def write(self, sheet, instance, field):
        '''
        Write a given field to an appropriately generated location
        '''
        # Retrieve a write function, default to "write"
        writer_func = getattr(sheet, self.field_write_functions.get('field', 'write'))
        col, content, *args = self.writable(instance, field)
        # Handle 'iterable' content: In case the content type here is a Postgres Array field, join
        if isinstance(content, collections.Iterable) and not isinstance(content, six.string_types):
            content = self.array_handler(content)
        writer_func(self.object_row, col, content, *args)

        content_length = len('%s' % (content))
        if col not in self.column_widths:
            self.column_widths[col] = content_length
        elif self.column_widths[col] < content_length:
            self.column_widths[col] = content_length
        if self.max_col_width < self.column_widths[col]:
            self.column_widths[col] = self.max_col_width

    def get_filename(self) -> str:
        '''
        You probably want to override this
        '''
        return 'test'

    def get(self, request, **kwargs):
        '''
        Update the "cache properties" dict with any request props and call generate_response
        '''
        for k in request.GET.keys():
            self.cache_properties[k] = request.GET.get(k)
        return self.generate_response()

    def update_excel_formats(self, workbook):
        self.excel_formats.update({fmt_reference: workbook.add_format(properties=properties) for fmt_reference, properties in self.cell_formats.items()})
        self.excel_formats['wrapped_text'] = workbook.add_format()
        self.excel_formats['wrapped_text'].set_text_wrap()
        self.excel_formats['default'] = workbook.add_format()
        for ex_fmt in self.excel_formats.values():
            ex_fmt.set_align('top')
            ex_fmt.set_align('left')

    def create_workbook(self):
        '''
        Return content suitable for an Excel workbook download or cache
        '''
        import xlsxwriter
        logger.debug('Generate Excel content')
        output = io.BytesIO()
        workbook = xlsxwriter.workbook.Workbook(output, {'in_memory': True})
        self.update_excel_formats(workbook)
        # Apply cell formats to the workbook
        self.sheets(workbook)
        workbook.close()
        output.seek(0)
        read = output.read()
        logger.debug('Generate Excel content Complete')
        return read

    def create_csv(self, unformatted_headers=False):
        '''
        Return content suitable for a CSV download or cache
        '''

        #  raise NotImplementedError
        output = io.StringIO()
        qs = self.get_filtered_queryset()
        fields = self.get_write_fields()
        # Allow "raw" header export for CSV
        if unformatted_headers:
            headers = fields
        else:
            headers = [self.export_header(field) for field in fields]
        csv_output = csvwriter(output)
        csv_output.writerow(headers)
        csv_output.writerows(qs.values_list(*fields))
        output.seek(0)
        read = output.read()
        logger.debug('Generate CSV content Complete')
        return read

    def write_queryset_to_sheet(self, sheet: "xlsxwriter.workbook.Worksheet", qs: QuerySet):
        '''
        One queryset as a worksheet
        '''
        import xlsxwriter
        fields = self.get_write_fields()
        if not fields:
            raise TypeError('Expected a list of fields; got %s', fields)

        # The 'pk' field is used to determine which row to write to
        # You need to include it in .fields or .get_fields() but if you don't like a raw id field
        # you can always modify and re-label it
        if 'pk' not in fields and not self.exclude_pks:
            logger.warning('For tracking row, a "pk" in required: One has been added for you')
            fields.append('pk')
        # Start by writing a header row
        self.object_row_map['HEADER'] = 0
        sheet.write_row(0, 0, [self.export_header(field) for field in fields], cell_format=self.excel_formats['bold'])
        for col, field in enumerate([self.export_header(field) for field in fields]):
            self.column_widths[col] = len('%s' % (field,))
        self.field_column_map = {field: col for col, field in enumerate(fields)}
        for instance in qs.values(*fields):
            for field in fields:
                self.write(sheet, instance, field)
            self.object_row += 1

        for column, width in self.column_widths.items():
            sheet.set_column(column, column, width + 4)

        row_height = getattr(self, 'row_height', None)
        if row_height:
            for rown in range(1, qs.count()):
                sheet.set_row(rown, row_height)

    def sheets(self, workbook: "xlsxwriter.Workbook"):
        '''
        This is for a single-sheet workbook
        Multiple sheet workbooks may use a
        different entry point
        '''
        sheet = workbook.add_worksheet()  # type: xlsxwriter.worksheet.Worksheet
        qs = self.get_filtered_queryset()  # type: QuerySet
        self.write_queryset_to_sheet(sheet, qs)

    def annotate_linked_fields(self, alternate_replace='_x_'):
        '''
        Default queryset might have multiple fields with the same name when we RawSQL things
        However we can make some annotations to help us name fields less conflicted-ly
        Returns a dict of {field-we-want-to-annotate : safe-field-name}
        Ideally, we'd use a single underscore but this could conflict
        For instance, Transaction.provider_organisation_name would conflict with Transaction.provider_organisation.name
        '''

        fields = self.get_write_fields()
        logger.debug('%s', fields)
        field_rewrite = {}
        for fieldname in fields:
            if fieldname.startswith('_'):
                continue
            if '__' not in fieldname:
                continue
            replace_fieldname = fieldname.replace('__', alternate_replace)
            logger.debug('%s -> %s', fieldname, replace_fieldname)
            if replace_fieldname in fields:
                replace_fieldname = fieldname.replace('__', alternate_replace)
            field_rewrite[fieldname] = replace_fieldname

        fieldnames_with_rewrites = [field_rewrite.get(field, field) for field in fields if field not in self.skip_for_rawsql]
        logger.debug('%s', field_rewrite)
        logger.debug('%s', fieldnames_with_rewrites)

        field_annotations = {v: F(k) for k, v in field_rewrite.items()}

        return field_annotations, fieldnames_with_rewrites

    def get_filters(self) -> Dict[str, Any]:
        '''
        Returns a hash of filter name, value
        Intention of this is to allow parametric (GET/POST) filtering
        '''
        filters = {}
        if not hasattr(self, 'request'):
            return filters
        # Iterate through the simple "kwarg_filters", which match a single value
        for kf in self.kwarg_filters:
            if kf in self.request.GET:
                filters[kf] = self.request.GET.get(kf)
        # Set more complex filters with QueryFilters
        # A QueryFilter object can alias fields, use 'gt', 'lt' etc, set default values
        for qf in self.query_filters:
            if qf.param in self.request.GET:
                filters[qf.field + qf.expr] = qf.cast(self.request.GET.get(qf.param))
            elif qf.value:
                filters[qf.field + qf.expr] = qf.value

        return filters

    kwarg_filters = ['pk', ]  # Simple equivalent to the QueryFilter below
    query_filters = (
        QueryFilter('mypkis', 'pk', '', None, "Example filter by PK", int),
    )

    def get_excludes(self) -> Dict[str, Any]:
        return {}

    def raw_sql(self, alternate_replace='_x_', unreplace=True, parse=True):
        '''
        Useful method to see what we're running as a queryset
        This method does some funky-bendy stuff to avoid an error where a 'related name' might conflict
        with a field on the model
        We see this with 'Transaction' where 'provider_organisation_name' is a field
        and 'provider__organisation__name' is a relation
        To include 'provider__organisation__name' as a field in our export
        we need to Annotate it a new name - can't keep '__', can't replace __ with _ either as it would conflict
        For that reason the slightly ungainly alternate_replace='_x_' indicates a relationship
        in our output query/view/table source
        You may choose to "unreplace" it or not depending on which would be less likely to
        cause confusion
        '''

        # Deconflict fieldnames
        anno, fields = self.annotate_linked_fields(alternate_replace)
        try:
            with connection.cursor() as c:
                sql, params = self.get_filtered_queryset()\
                    .annotate(**anno)\
                    .values(*fields)\
                    .query.sql_with_params()
                raw = c.mogrify(sql, params)
            if unreplace:
                logger.debug('Drop %s', alternate_replace)
                raw = raw.replace(alternate_replace.encode(), b'_')
            if parse:
                return sqlparse.format(raw, reindent=True, keyword_case='upper')
            return raw
        except FieldError:
            raise FieldError('Field may not exist on the specified model %s' % self.__class__.__qualname__)


class MultipleExportSheets(ExportSheet):
    '''
    Returns an excel workbook with more than one tab
    In many cases we want to dump a more comprehensive collection of data
    than a single sheet / CSV / json obj, for example 'Transactions' and 'Activities' in one export
    as we do in the QueryBuilder
    '''

    raw_sql = None

    def get_sheets(self):
        raise NotImplementedError('Override get_sheets in a subclass')

    def get(self, request, *args, **kwargs):
        '''
        Wrap the procedure of the child sheet's creations
        into one workbook
        '''

        def add_sheet(workbook, request, child_sheet_class):
            child_sheet_object = child_sheet_class(request=request, *args, **kwargs)
            sheetname = child_sheet_object.get_sheetname()
            child_sheet_object.update_excel_formats(workbook)  # This 'update excel formats' code modifies the parent workbook
            sheet = workbook.add_worksheet(sheetname)
            qs = child_sheet_object.get_filtered_queryset()
            child_sheet_object.write_queryset_to_sheet(sheet, qs)
        import xlsxwriter
        logger.debug('Generate Excel content')
        output = io.BytesIO()
        workbook = xlsxwriter.workbook.Workbook(output, {'in_memory': True})

        # Apply cell formats to the workbook
        for klass in self.get_sheets():
            add_sheet(workbook, request, klass)

        workbook.close()
        output.seek(0)
        read = output.read()
        logger.debug('Generate Excel content Complete')
        response = HttpResponse(read, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=%s.xlsx" % (self.get_filename(),)
        return response


class Comprehensive(LoginRequiredMixin, MultipleExportSheets):
    '''
    This exports a number of sheets useful for
    an Organisation birds-eye-view
    '''
    title = 'Activities, Budgets and Transactions'
    description = 'Download a workbook with Activity, Budget and Transaction summary data'
    description_list = [
        'Associated organisations',
        'Financial information'
    ]

    def get_filename(self):
        return 'Activities-Transactions-Budgets-Contacts'

    def get_sheets(self):
        return [ExportActivitiesWithDrafts, ExportBudgets, ExportTransactions, ExportContacts]


class ExportBudgets(LoginRequiredMixin, ExportSheet):
    '''
    Budgets
    '''
    title = 'Budgets'
    description = 'Download a list of all budgets.'
    description_list = [
        'Associated organisations',
        'Financial information'
    ]

    field_lookups = {
        'activity__end_planned': 'iso_date',
        'activity__start_planned': 'iso_date',
        'value_date': 'iso_date',
        'period_start': 'iso_date',
        'period_end': 'iso_date',
        'usd_value': 'currency_format',
    }

    query_filters = (
        QueryFilter(param='org', field='activity__reporting_organisation__abbreviation', description="Reporting Organisation's abbreviation"),
        QueryFilter(param='org_id', field='activity__reporting_organisation__code', description="Reporting Organisation's id"),
    )

    def get_fields(self):
        budget_fields = ['pk', 'type', 'type__name', 'value_date', 'period_start', 'period_end', 'usd_value']
        activity_fields = ['id', 'internal_identifier', 'iati_identifier', 'reporting_organisation', 'reporting_organisation__name', 'reporting_organisation__abbreviation', 'start_planned', 'end_planned']

        fields = []
        fields.extend([field for field in budget_fields])
        fields.extend(['activity__' + field for field in activity_fields])
        fields.extend(['quarter'])
        return fields

    def get_filename(self) -> str:
        return 'budgets'

    queryset = Budget.objects.filter(activity__openly_status='published').annotate(quarter=date_as_decimal_quarter('period_start'))


class ExportActivities(LoginRequiredMixin, ExportSheet):
    '''
    Excel worksheet containing list of all Activity objects
    '''

    title = common_text.get('activities_or_programs')
    description = 'Download a list of all activities.'
    description_list = [
        'Activity dates',
        'Associated organisations',
        'Summarised financial information'
    ]

    sheetname = title

    def activity_hyperlink(self, instance: Dict, field: str) -> str:
        '''
        Returns the hyperlink to activity profile page
        '''
        if instance.get('openly_status', None) != 'published':
            return
        protocol = self.request.scheme
        url = reverse('activity_profile', kwargs={'activity_id': instance[field]})
        return '%s://%s%s' % (protocol, self.domain, url)

    def __init__(self, *args, **kwargs):
        super(ExportActivities, self).__init__(*args, **kwargs)

    def get_filename(self) -> str:
        return 'activities'

    field_format_functions = {
        'pk': activity_hyperlink
    }

    field_write_functions = {
        'pk': 'write_url',
        'start_actual': 'write_datetime',
        'start_planned': 'write_datetime',
        'end_planned': 'write_datetime',
        'end_actual': 'write_datetime',
        'date_modified': 'write_datetime',
    }

    export_headers = {
        'pk': 'Activity URL',
        'id': 'Activity ID',
        'internal_identifier': 'Activity Partner ID',
    }

    skip_for_rawsql = ('pk',)
    queryset = Activity.objects.all()

    @classmethod
    def get_annotations(cls):
        annotations = {}
        annotations['activity_total_commitment'] = activity_commitment_total_subquery()
        annotations['activity_total_disbursement'] = activity_commitment_total_subquery(transaction_type='D')
        if 'oipa' in settings.INSTALLED_APPS:
            annotations['iati_sync'] = activity_oipa_sync_subquery()
        annotations.update(activity_organisations_subquery_list(outerref='pk'))
        return annotations

    @classmethod
    def get_queryset(cls):
        queryset = Activity.objects.all()
        return queryset.annotate(**cls.get_annotations())

    query_filters = (
        QueryFilter(param='org', field='reporting_organisation__abbreviation', description="Reporting Organisation's abbreviation"),
        QueryFilter(param='org_id', field='reporting_organisation__code', description="Reporting Organisation's id"),
    )

    fields = '''
        id
        pk
        internal_identifier
        iati_identifier
        default_currency
        _hierarchy
        date_modified
        _linked_data_uri
        reporting_organisation
        reporting_organisation__name
        reporting_organisation__abbreviation
        _secondary_publisher
        activity_status
        activity_status__name

        start_planned
        end_planned
        start_actual
        end_actual

        _participating_organisation
        _policy_marker
        _sector
        _recipient_country
        _recipient_region

        collaboration_type
        collaboration_type__name
        default_flow_type
        default_flow_type__name
        default_aid_type
        default_aid_type__name
        default_finance_type
        default_finance_type__name
        default_tied_status
        default_tied_status__name
        _xml_source_ref
        _total_budget_currency
        _total_budget

        _capital_spend
        _scope
        _iati_standard_version
        completion
        activity_total_commitment
        activity_total_disbursement
    '''.split()

    if 'oipa' in settings.INSTALLED_APPS:
        fields.append('iati_sync')

    field_lookups = {
        'end_planned': 'iso_date',
        'start_planned': 'iso_date',
        'end_actual': 'iso_date',
        'start_actual': 'iso_date',
        'date_modified': 'iso_date',
        'activity_total_commitment': 'currency_format',
        'activity_total_disbursement': 'currency_format',
    }

    def get_fields(self):
        fields = []
        fields.extend(self.fields)
        related_organisation_fields = ['participating_organisations_%s' % (role.lower(),) for role in list(OrganisationRole.objects.all().values_list('code', flat=True))]
        fields.extend(related_organisation_fields)
        return fields


class ExportActivitiesWithDrafts(ExportActivities):

    sheetname = 'Activities, all status'

    @classmethod
    def get_queryset(cls):
        queryset = Activity.objects.all_openly_statuses().all()
        annotations = {}
        annotations['activity_total_commitment'] = activity_commitment_total_subquery()
        annotations['activity_total_disbursement'] = activity_commitment_total_subquery(transaction_type='D')
        annotations['iati_sync'] = activity_oipa_sync_subquery()
        annotations.update(activity_organisations_subquery_list(outerref='pk'))
        return queryset.annotate(**annotations)

    def get_fields(self):
        fields = super().get_fields()
        fields.append('openly_status')
        return fields


class ExportActivitiesWithSector(ExportActivities):
    '''
    This provides an Activity export with additional fields describing
    IATI and National sectors
    '''

    title = 'Activities with Sectors'
    description = 'Download a list of all activities with sectors applied.'
    description_list = [
        'Activity dates',
        'Associated organisations',
        'Summarised financial information',
        'IATI and National sectors'
    ]

    def get_fields(self):
        fields = super().get_fields()
        fields.extend(['iati_sectors', 'national_sectors'])
        return fields

    @classmethod
    def get_annotations(cls):
        anno = super().get_annotations()
        anno.update({
            'iati_sectors': sector_subquery(),
            'national_sectors': sector_subquery(national=True)
        })
        logger.info(anno)
        return anno

    def get_queryset(self):
        anno = self.get_annotations()
        qs = super().get_queryset().annotate(**anno)
        return qs


class ExportTransactionSectors(LoginRequiredMixin, ExportSheet):
    '''
    Construct an export for Transaction Sector fields
    '''

    title = 'Transactions, with Sector breakdown'
    description = '''Download Transactions, disaggregated by Sectors.'''
    description_list = [
        'One row per distinct Transaction and Activity-Sector',
        'Use this data to see Transaction amounts per Activity, Sector or Sector Category'
    ]

    field_lookups = {
        'activity__start_planned': 'iso_date',
        'activity__end_planned': 'iso_date',
        'activity__start_actual': 'iso_date',
        'activity__end_actual': 'iso_date',
        'activity__date_modified': 'iso_date',
        'value_date': 'iso_date',
        'transaction_date': 'iso_date',
        'value_field': 'currency_format',
    }

    export_headers = {
        'pk': 'Transaction ID',
        'value_field': 'USD value for transaction in Activity Sector'
    }

    def get_filename(self) -> str:
        return 'transactionsectors'

    def get_fields(self):
        transaction_fields = ['pk', 'transaction_type', 'transaction_type__name', 'transaction_date', 'aid_type__category', 'aid_type__category__name']
        activity_fields = ['id', 'internal_identifier', 'iati_identifier', 'start_planned', 'end_planned', 'date_modified']
        orgs = ('provider_organisation', 'receiver_organisation', 'activity__reporting_organisation')
        orgs_fields = ('name', 'code', 'abbreviation')
        as_fields = ['percentage', ]
        as_sector_fields = ['name', 'code']
        as_category_fields = ['name', 'code']

        fields = []
        fields.extend(transaction_fields)
        fields.extend(['%s__%s' % (o, f) for o in orgs for f in orgs_fields])
        fields.extend(['activity__' + field for field in activity_fields])

        fields.extend(['activity__activitysector__' + field for field in as_fields])
        fields.extend(['activity__activitysector__sector__' + field for field in as_sector_fields])
        fields.extend(['activity__activitysector__sector__category__' + field for field in as_category_fields])

        # This calculation field is percentage * transaction value derived from the transactions_with_sector queryset
        fields.extend(['value_field', 'quarter', ])
        return fields

    @classmethod
    def get_queryset(cls):
        qs = Aggregates(Transaction.objects.filter(activity__openly_status='published')).transactions_with_sector
        return qs.annotate(**cls.get_annotations())

    @staticmethod
    def get_annotations():
        return {'quarter': date_as_decimal_quarter('transaction_date')}


class ExportBudgetSectors(LoginRequiredMixin, ExportSheet):
    '''
    Construct an export for Budget Sector fields
    '''

    title = 'Budgets, with Sector breakdown'
    description = '''Download Budgets, disaggregated by Sectors.'''
    description_list = [
        'One row per distinct Budget and Activity-Sector',
        'Use this data to see Budget amounts per Activity, Sector or Sector Category'
    ]

    field_lookups = {
        'value_date': 'iso_date',
        'period_start': 'iso_date',
        'period_end': 'iso_date',
        'value_field': 'currency_format',
    }

    export_headers = {
        'pk': 'Budget ID',
        'value_field': 'USD value for budget in Activity Sector'
    }

    def get_filename(self) -> str:
        return 'budgetsectors'

    def get_fields(self):
        budget_fields = ['pk', 'type', 'type__name', 'value_date', 'period_start', 'period_end']
        activity_fields = ['id', 'internal_identifier', 'iati_identifier', 'reporting_organisation', 'reporting_organisation__name', 'reporting_organisation__abbreviation', 'start_planned', 'end_planned', 'date_modified']
        as_fields = ['percentage', ]
        as_sector_fields = ['name', 'code']
        as_category_fields = ['name', 'code']

        fields = []
        fields.extend(budget_fields)
        fields.extend(['activity__' + field for field in activity_fields])
        fields.extend(['activity__activitysector__' + field for field in as_fields])
        fields.extend(['activity__activitysector__sector__' + field for field in as_sector_fields])
        fields.extend(['activity__activitysector__sector__category__' + field for field in as_category_fields])
        # This calculation field is percentage * transaction value derived from the transactions_with_sector queryset
        fields.extend(['value_field', 'quarter'])
        return fields

    @classmethod
    def get_queryset(cls):
        qs = Aggregates(Budget.objects.filter(activity__openly_status='published')).transactions_with_sector
        return qs.annotate(**{
            'quarter': date_as_decimal_quarter('value_date'),
        })


class ExportBudgetLocations(LoginRequiredMixin, ExportSheet):
    '''
    Construct an export for Budget Location fields
    '''

    title = 'Budgets, with Location breakdown'
    description = '''Download Budgets, disaggregated by Locations.'''
    description_list = [
        'One row per distinct Budget and Activity-Location',
        'Use this data to see Budget amounts per Activity, Township or State'
    ]

    field_lookups = {
        'value_date': 'iso_date',
        'period_start': 'iso_date',
        'period_end': 'iso_date',
        'period_end': 'iso_date',
        'value_field': 'currency_format',
    }

    export_headers = {
        'pk': 'Budget ID',
        'value_field': 'USD value for budget in Activity Location'
    }

    def get_filename(self) -> str:
        return 'budgetlocations'

    def get_fields(self):
        budget_fields = ['pk', 'type', 'type__name', 'value_date', 'period_start', 'period_end']
        activity_fields = ['id', 'internal_identifier', 'iati_identifier', 'reporting_organisation', 'reporting_organisation__name', 'reporting_organisation__abbreviation', 'start_planned', 'end_planned', 'date_modified']
        location_fields = ['percentage', 'adm_code', 'name']

        fields = []
        fields.extend([field for field in budget_fields])
        fields.extend(['activity__' + field for field in activity_fields])
        fields.extend(['activity__location__' + field for field in location_fields])

        # This calculation field is percentage * transaction value derived from the transactions_with_location queryset
        fields.extend(['value_field', 'iso', 'quarter', ])
        fields.extend(location_hierarchy_anno(prefix='activity__location__area', suffix='code').keys())
        fields.extend(location_hierarchy_anno(prefix='activity__location__area', suffix='name').keys())
        return fields

    @classmethod
    def get_queryset(cls):
        qs = Aggregates(Budget.objects.filter(activity__openly_status='published')).transactions_with_location
        qs = qs.annotate(**location_hierarchy_anno(prefix='activity__location__area', suffix='code'))
        qs = qs.annotate(**location_hierarchy_anno(prefix='activity__location__area', suffix='name'))
        qs = qs.annotate(**state_pcode_to_isocode())
        qs = qs.annotate(quarter=date_as_decimal_quarter('value_date'))
        return qs


class ExportTransactionLocations(LoginRequiredMixin, ExportSheet):
    '''
    Construct an export for Transaction Location fields
    '''

    title = 'Transactions, with Location breakdown'
    description = '''Download Transactions, disaggregated by Locations.'''
    description_list = [
        'One row per distinct Transaction and Activity-Location',
        'Use this data to see Transaction amounts per Activity, Township or State'
    ]

    field_lookups = {
        'activity__start_planned': 'iso_date',
        'activity__end_planned': 'iso_date',
        'activity__start_actual': 'iso_date',
        'activity__end_actual': 'iso_date',
        'activity__date_modified': 'iso_date',
        'value_date': 'iso_date',
        'transaction_date': 'iso_date',
        'value_field': 'currency_format',
    }

    export_headers = {
        'pk': 'Transaction ID',
        'value_field': 'USD value for transaction in Activity Location'
    }

    def get_filename(self) -> str:
        return 'transactionlocations'

    def get_fields(self):
        transaction_fields = ['pk', 'transaction_type', 'transaction_type__name', 'transaction_date', 'aid_type__category', 'aid_type__category__name']
        activity_fields = ['id', 'internal_identifier', 'iati_identifier', 'reporting_organisation__name', 'reporting_organisation', 'reporting_organisation__abbreviation', 'start_planned', 'end_planned']
        location_fields = ['percentage', 'adm_code', 'name']

        fields = []

        fields.extend([field for field in transaction_fields])
        fields.extend(['activity__' + field for field in activity_fields])
        fields.extend(['activity__location__' + field for field in location_fields])

        # This calculation field is percentage * transaction value derived from the transactions_with_location queryset
        fields.extend(['value_field', 'iso', 'quarter'])
        fields.extend(location_hierarchy_anno(prefix='activity__location__area', suffix='code').keys())
        fields.extend(location_hierarchy_anno(prefix='activity__location__area', suffix='name').keys())
        return fields

    @classmethod
    def get_queryset(cls):
        qs = Aggregates(Transaction.objects.filter(activity__openly_status='published')).transactions_with_location
        qs = qs.annotate(**location_hierarchy_anno(prefix='activity__location__area', suffix='code'))
        qs = qs.annotate(**location_hierarchy_anno(prefix='activity__location__area', suffix='name'))
        # Note: This may break horribly or give nonsense on non-myanmar hosts
        qs = qs.annotate(**state_pcode_to_isocode())
        return qs.annotate(**{
            'quarter': date_as_decimal_quarter('transaction_date'),
        })
        return qs


class ExportBudgetSectorLocations(LoginRequiredMixin, ExportSheet):
    '''
    Construct an export for Budget Sector and Location fields
    '''

    title = 'Budgets, with Sector and Location breakdown'
    description = '''Download Budgets, disaggregated by the related Activity's Sectors and Locations.'''
    description_list = [
        'One row per distinct Budget, Activity-Location, and Activity-Sector',
        'This is the largest and most detailed export for budgets',
        'Use this data to show aid flows by Sector and Location'
    ]

    field_lookups = {
        'value_date': 'iso_date',
        'period_start': 'iso_date',
        'period_end': 'iso_date',
        'value_field': 'currency_format',
    }

    export_headers = {
        'pk': 'Budget ID',
        'value_field': 'USD value for budget in Activity Location for Sector'
    }

    def get_filename(self) -> str:
        return 'budgetsectorlocations'

    def get_fields(self):
        budget_fields = ['pk', 'type', 'type__name', 'value_date', 'period_start', 'period_end']
        activity_fields = ['id', 'internal_identifier', 'iati_identifier', 'reporting_organisation__abbreviation', 'start_planned', 'end_planned']
        location_fields = ['percentage', 'adm_code', 'name']
        as_fields = ['percentage', ]
        as_sector_fields = ['name', 'code']
        as_category_fields = ['name', 'code']

        fields = []

        fields.extend([field for field in budget_fields])
        fields.extend(['activity__' + field for field in activity_fields])
        fields.extend(['activity__location__' + field for field in location_fields])
        fields.extend(['activity__activitysector__' + field for field in as_fields])
        fields.extend(['activity__activitysector__sector__' + field for field in as_sector_fields])
        fields.extend(['activity__activitysector__sector__category__' + field for field in as_category_fields])

        # This calculation field is percentage * transaction value derived from the transactions_with_sector_and_location queryset
        fields.extend(['value_field', 'iso', 'quarter'])
        fields.extend(location_hierarchy_anno(prefix='activity__location__area', suffix='code').keys())
        fields.extend(location_hierarchy_anno(prefix='activity__location__area', suffix='name').keys())

        return fields

    @classmethod
    def get_queryset(cls):
        qs = Aggregates(Budget.objects.filter(activity__openly_status='published')).transactions_with_sector_and_location
        qs = qs.annotate(**location_hierarchy_anno(prefix='activity__location__area', suffix='code'))
        qs = qs.annotate(**location_hierarchy_anno(prefix='activity__location__area', suffix='name'))
        qs = qs.annotate(**state_pcode_to_isocode())
        qs = qs.annotate(quarter=date_as_decimal_quarter('period_start'))
        return qs


class ExportTransactionSectorLocations(LoginRequiredMixin, ExportSheet):
    '''
    Construct an export for Transaction Location fields
    '''

    title = 'Transactions, with Sector and Location breakdown'
    description = '''Download Transactions, disaggregated by the related Activity's Sectors and Locations.'''
    description_list = [
        'One row per distinct Transaction, Activity-Location, and Activity-Sector',
        'This is the most detailed export',
        'Use this data to show aid flows by Sector and Location'
    ]

    field_lookups = {
        'activity__start_planned': 'iso_date',
        'activity__end_planned': 'iso_date',
        'activity__start_actual': 'iso_date',
        'activity__end_actual': 'iso_date',
        'activity__date_modified': 'iso_date',
        'value_date': 'iso_date',
        'transaction_date': 'iso_date',
        'date_modified': 'iso_date',
        'value_field': 'currency_format',
    }

    export_headers = {
        'pk': 'Transaction ID',
        'value_field': 'USD value for transaction in Activity Location for Sector'
    }

    def get_filename(self) -> str:
        return 'transactionsectorlocations'

    def get_fields(self):
        transaction_fields = ['pk', 'transaction_type', 'transaction_type__name', 'transaction_date', 'aid_type__category', 'aid_type__category__name']
        activity_fields = ['id', 'internal_identifier', 'iati_identifier', 'reporting_organisation__name', 'reporting_organisation', 'reporting_organisation__abbreviation', 'start_planned', 'end_planned', 'date_modified']
        location_fields = ['percentage', 'adm_code', 'name']
        as_fields = ['percentage', ]
        as_sector_fields = ['name', 'code']
        as_category_fields = ['name', 'code']

        fields = []

        fields.extend([field for field in transaction_fields])
        fields.extend(['activity__' + field for field in activity_fields])
        fields.extend(['activity__location__' + field for field in location_fields])
        fields.extend(['activity__activitysector__' + field for field in as_fields])
        fields.extend(['activity__activitysector__sector__' + field for field in as_sector_fields])
        fields.extend(['activity__activitysector__sector__category__' + field for field in as_category_fields])

        # This calculation field is percentage * transaction value derived from the transactions_with_sector_and_location queryset
        fields.extend(['value_field', ])
        fields.extend(location_hierarchy_anno(prefix='activity__location__area', suffix='code').keys())
        fields.extend(location_hierarchy_anno(prefix='activity__location__area', suffix='name').keys())
        fields.extend(['iso', 'quarter', ])

        return fields

    @classmethod
    def get_queryset(cls):
        qs = Aggregates(Transaction.objects.filter(activity__openly_status='published')).transactions_with_sector_and_location
        qs = qs.annotate(**location_hierarchy_anno(prefix='activity__location__area', suffix='code'))
        qs = qs.annotate(**location_hierarchy_anno(prefix='activity__location__area', suffix='name'))
        qs = qs.annotate(**state_pcode_to_isocode())
        qs = qs.annotate(quarter=date_as_decimal_quarter('transaction_date'))
        return qs


class ExportTransactions(LoginRequiredMixin, ExportSheet):

    title = 'Transactions'
    description = '''Download Transactions.'''
    description_list = [
        'One row per Transaction',
        'Use this data to see Transaction amounts per Activity'
    ]

    query_filters = (
        QueryFilter(param='org', field='activity__reporting_organisation__abbreviation', description="Reporting Organisation's abbreviation"),
        QueryFilter(param='org_id', field='activity__reporting_organisation__code', description="Reporting Organisation's id"),
    )

    field_write_functions = {
        'transaction_date': 'write_datetime',
        'value_date': 'write_datetime',
    }

    def activity_hyperlink(self, instance: Dict, field: str,) -> str:
        '''
        Returns the hyperlink to activity profile page
        '''
        protocol = 'https'
        url = reverse('activity_profile', kwargs={'activity_id': instance[field]})
        return '%s://%s%s' % (protocol, self.domain, url)

    def array_field(self, instance: Dict, field: str, request) -> str:
        '''
        Returns the hyperlink to activity profile page
        '''
        value = instance[field]
        separator = ', '
        if value:
            return separator.join(instance[field])
        return

    field_format_functions = {
        'activity': activity_hyperlink,
    }

    export_headers = {
        'pk': 'Transaction ID',
        'activity': 'Activity URL',
        'currency': 'Transaction Currency',
        'currency__name': 'Transaction Currency Name'
    }

    field_lookups = {
        'activity__start_planned': 'iso_date',
        'activity__end_planned': 'iso_date',
        'activity__start_actual': 'iso_date',
        'activity__end_actual': 'iso_date',
        'activity__date_modified': 'iso_date',
        'value_date': 'iso_date',
        'transaction_date': 'iso_date',
        'usd_value': 'currency_format',
        'activity_total_disbursement': 'currency_format',
        'activity_total_commitment': 'currency_format',
        'activity__completion': 'percentage',
    }

    def get_filename(self) -> str:
        return 'transactions'

    def get_fields(self):
        transaction_fields = '''
            pk
            activity_name
            activity
            aid_type
            aid_type__category
            aid_type__name
            aid_type__category__name
            description
            _description_type
            disbursement_channel
            disbursement_channel__name
            finance_type
            finance_type__name
            flow_type
            flow_type__name
            provider_organisation
            provider_organisation__name
            provider_organisation__abbreviation
            _provider_organisation_name
            provider_activity
            receiver_organisation
            receiver_organisation__name
            receiver_organisation__abbreviation
            _receiver_organisation_name
            tied_status
            tied_status__name
            transaction_date
            transaction_type
            transaction_type__name
            value_date
            _value
            usd_value
            currency
            currency__name
            _ref
        '''.split()

        activity_fields = '''
            _id
            internal_identifier
            iati_identifier
            default_currency
            hierarchy
            date_modified
            linked_data_uri
            reporting_organisation
            reporting_organisation__name
            reporting_organisation__abbreviation
            _secondary_publisher
            activity_status

            start_planned
            end_planned
            start_actual
            end_actual

            _participating_organisation
            _policy_marker
            _sector
            _recipient_country
            _recipient_region

            collaboration_type
            collaboration_type__name
            default_flow_type
            default_flow_type__name
            default_aid_type
            default_aid_type__name
            default_finance_type
            default_finance_type__name
            default_tied_status
            default_tied_status__name
            _xml_source_ref
            _total_budget_currency
            _total_budget

            _capital_spend
            _scope
            _iati_standard_version
            completion
        '''.split()
        fields = []
        fields.extend([field for field in transaction_fields if not field.startswith('_')])
        fields.extend(['activity__' + field for field in activity_fields if not field.startswith('_')])
        related_organisation_fields = ['participating_organisations_%s' % (role.lower(),) for role in list(OrganisationRole.objects.all().values_list('code', flat=True))]
        fields.extend(related_organisation_fields)
        fields.append('activity_sector_categories')
        fields.append('activity_total_commitment')
        fields.append('activity_total_disbursement')
        fields.append('quarter')

        return fields

    @staticmethod
    def get_annotations():
        annotations = {}
        annotations.update(activity_organisations_subquery_list(outerref='activity'))
        annotations['activity_name'] = activity_name_subquery()
        annotations['activity_sector_categories'] = activity_sector_category_subquery(outerref='activity', category_type='iati')
        annotations['activity_total_commitment'] = activity_commitment_total_subquery(outerref='activity')
        annotations['activity_total_disbursement'] = activity_commitment_total_subquery(outerref='activity', transaction_type='D')
        annotations['quarter'] = date_as_decimal_quarter('transaction_date')
        return annotations

    @classmethod
    def get_queryset(cls):
        '''
        This is going to get super funky :)
        Stay with me here...
        '''
        qs = Transaction.objects.filter(activity__openly_status='published')
        annotations = cls.get_annotations()
        qs = qs.annotate(**annotations)
        return qs


class TransactionsWithTiers(ExportTransactionSectors):

    title = 'Transactions, with extra Sector Tiers'
    description = '''Download Transactions.'''
    description_list = [
        'One row per Transaction',
        'Use this data to see Transaction amounts',
        'This includes Tiers II - VI'
    ]

    def get_fields(self):
        fields = super().get_fields()
        fields.extend(sector_tiers().keys())
        return fields

    @classmethod
    def get_annotations(cls):
        anno = super().get_annotations()
        anno.update(**sector_tiers())
        return anno

    def get_queryset(self):
        qs = Aggregates(Transaction.objects.filter(activity__openly_status='published')).transactions_with_sector
        annotations = self.get_annotations()
        qs = qs.annotate(**annotations)
        return qs


class ExportContacts(LoginRequiredMixin, ExportSheet):
    '''
    Excel worksheet: Contact details
    '''

    title = 'Contacts'
    description = 'Download contact details'
    description_list = []
    exclude_pks = True
    query_filters = (
        QueryFilter(param='org', field='organisation_profile__organisation__abbreviation', description="Organisation's abbreviation"),
        QueryFilter(param='org_id', field='organisation_profile__organisation__code', description="Organisation's id"),
    )

    @classmethod
    def get_queryset(cls):
        return Person.objects.all()

    def get_filename(self) -> str:
        return 'contacts'

    fields = '''
        name
        position
        email
        organisation_profile__organisation__name
    '''.split()


class SupersetSecretSquirrel(TemplateView):

    template_name = 'export/recreate_superset.sql'
    content_type = 'text'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['models'] = all_subclasses(ExportSheet)

        return context


class ExportActivitiesVerbose(ExportActivities):

    row_height = 120

    @classmethod
    def get_annotations(cls):

        def _anno(model, language, field, **_filter):
            return Subquery(
                model.objects.filter(
                    **_filter, language_id=language, activity_id=OuterRef("pk")
                ).values(field)[:1]
            )

        annotations = {}
        activate('en')

        for language_code, language_name in settings.LANGUAGES:
            annotations["%s_%s" % ("title", language_name.lower())] = _anno(
                Title, language_code, "title"
            )
            for dt in DescriptionType.objects.all():
                annotations["description_%s_%s" % (dt.name.replace(' ', '_'), language_name.lower())] = _anno(
                    Description, language_code, "description", type=dt
                )

        # Subquery-Annotate 'ActivitySector'
        annotations['sectors'] = Subquery(
            ActivitySector.objects.filter(
                activity_id=OuterRef("pk"),
                sector__category__openly_type='iati'
            ).values(
                'activity_id'
            ).annotate(
                anno=StringAgg('sector__name', delimiter='; ')
            ).values('anno')[:1],
            output_field=TextField()
        )

        annotations['locations'] = Subquery(
            Location.objects.filter(
                activity_id=OuterRef("pk")
            ).values(
                'activity_id'
            ).annotate(
                anno=StringAgg('name', delimiter='; ')
            ).values('anno')[:1],
            output_field=TextField()
        )
        return annotations

    @classmethod
    def get_queryset(cls):
        """
        Adds the Title and Description fields to our Excel sheet by means of subqueries
        """
        queryset = Activity.objects.all()
        return queryset.annotate(**cls.get_annotations())

    def get_fields(self):
        fields = """
            id
            pk
            date_modified
            start_planned
            end_planned
            activity_status__name
            total_budget

        """.split()

        fields.extend(self.get_annotations().keys())
        return fields

    def get(self, request, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        return super().get(request, **kwargs)

    def get_filters(self):
        filters = super().get_filters()
        if "id" in self.request.GET:
            filters['pk__in'] = self.request.GET.getlist('id')
        return filters


class ExportAllActivitiesVerbose(ExportActivitiesVerbose):

    @classmethod
    def get_queryset(cls):
        """
        Adds the Title and Description fields to our Excel sheet by means of subqueries
        """
        queryset = Activity.objects.editables()
        return queryset.annotate(**cls.get_annotations())

    def get_fields(self):
        fields = super().get_fields()
        fields.append('openly_status')
        return fields


class ExportActivitiesContacts(ExportSheet):

    sheetname = 'Contacts'
    exclude_pks = True

    @classmethod
    def get_queryset(cls):
        return ContactInfo.objects.filter(activity__openly_status='published').annotate(**cls.get_annotations())

    @classmethod
    def get_annotations(cls):
        annotations = super().get_annotations()
        activate('en')
        sq = Title.objects.filter(language_id='en', activity_id=OuterRef('activity_id')).values('title')
        annotations['{}_title'.format(common_text.get('activity_or_program'))] = Subquery(sq[:1])
        return annotations

    def get_fields(self):
        activate('en')
        fields = [
            'activity',
            '{}_title'.format(common_text.get('activity_or_program')),
            'person_name',
            'job_title',
            'organisation',
            'telephone',
            'email',
            'mailing_address',
            'website',
        ]
        return fields

    def get_filters(self):
        filters = super().get_filters()
        if "id" in self.request.GET:
            filters['activity_id__in'] = self.request.GET.getlist('id')
        return filters


class ExportPortal(TemplateView):
    '''
    Show exports in XLSX, CSV, (JSON?) format
    '''
    template_name = 'export/export_portal.html'
    classes = ExportSheet.__subclasses__()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['models'] = collections.OrderedDict()
        context['models']['tables'] = [ExportActivities, ExportActivitiesWithSector, ExportTransactions, ExportBudgets, ExportContacts]
        context['models']['transaction breakdowns by sector and/or location'] = [ExportTransactionSectors, TransactionsWithTiers, ExportTransactionLocations, ExportTransactionSectorLocations]
        context['models']['budget breakdowns by sector and/or location'] = [ExportBudgetSectors, ExportBudgetLocations, ExportBudgetSectorLocations]

        return context


class ExportProjectsAndContacts(MultipleExportSheets):
    """
    Exports an Excel workbook with sheets for Activity/Project and Contacts
    """

    title = "Projects"
    description = "Download a workbook with Project and Contact data"
    description_list = []

    def get_filename(self):
        return "projects_contacts"

    def get_sheets(self):
        return [ExportActivitiesVerbose, ExportActivitiesContacts]
