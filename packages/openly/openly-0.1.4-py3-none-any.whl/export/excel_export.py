from collections import OrderedDict
from datetime import date
from operator import itemgetter

from django.db.models import Count, Max, Q, Sum, Case, When, IntegerField
from django.contrib.sites.models import Site
from django.urls import reverse
from django.conf import settings

from aims import common_text, models as aims
from aims.utils import dictify_tuple_list
from profiles_v2.models import OrganisationProfile

from .export_writer import ExportTemplateWriter

from .flexible_time import DefaultDateRange, MyanmarDateRange, DefaultDates, MyanmarDates


def daterange(*args, **kwargs):
    if getattr(settings, "ROOT_COUNTRY_CODE", False) == "MM":
        return MyanmarDateRange(*args, **kwargs)
    return DefaultDateRange(*args, **kwargs)


def daterange_single_year(*args, **kwargs):
    if getattr(settings, "ROOT_COUNTRY_CODE", False) == "MM":
        return MyanmarDates(*args, **kwargs)
    return DefaultDates(*args, **kwargs)


STATUS_CODES = OrderedDict((
    (u'Completion', 3),
    (u'Implementation', 2),
    (u'Pipeline/identification', 1),
))


class DataExporter(object):
    """ Base class for exporting Activity/Transaction data into an excel spreadsheet

    Subclasses should implement the gen_data and get_writer methods specified below.
    """

    def gen_data(self, activities, transactions, **kwargs):
        """ Generate a tuple of tuples of excel data for the given activities and transactions.
        Where each inner-tuple represents a row in the spreadsheet.
        """

    def get_writer(self, **kwargs):
        """ Return an ExportTemplateWriter with the appropriate parameters."""
        return None

    def export(self, activities, transactions, **kwargs):
        """ Return a StringIO.StringIO to be written to an excel file containing export data
        for the given Activity and Transaction models.
        """
        data = self.gen_data(activities, transactions, **kwargs)
        writer = self.get_writer(**kwargs)
        output = writer.write_data(data, filters=kwargs.get('filters', None))
        return output


class DonorSummaryExporter(DataExporter):
    """ Generates a summary of each Organisation's past, present, and future projects."""

    def get_writer(self, **kwargs):
        return ExportTemplateWriter(
            'Donors Summary',
            [ExportTemplateWriter.WIDE_COLUMN_PARAMS,
             ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
             ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
             ExportTemplateWriter.MONEY_COLUMN_PARAMS,
             ExportTemplateWriter.MONEY_COLUMN_PARAMS,
             ExportTemplateWriter.MONEY_COLUMN_PARAMS,
             ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
             ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
             ExportTemplateWriter.MONEY_COLUMN_PARAMS,
             ExportTemplateWriter.MONEY_COLUMN_PARAMS,
             ExportTemplateWriter.MONEY_COLUMN_PARAMS,
             ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
             ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
             ExportTemplateWriter.MONEY_COLUMN_PARAMS,
             ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
             ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
             ExportTemplateWriter.MONEY_COLUMN_PARAMS,
             ExportTemplateWriter.MONEY_COLUMN_PARAMS,
             ExportTemplateWriter.MONEY_COLUMN_PARAMS],
            [['Donor',
              'Completed', None, None, None, None,
              'Implementing', None, None, None, None,
              'Proposed/Negotiation', None, None,
              'Total', None, None, None, None],
             [None,
              'Projects Reported', 'Projects Financed', 'Commitments', 'Disbursements',
              'Expenditures',
              'Projects Reported', 'Projects Financed', 'Commitments', 'Disbursements',
              'Expenditures',
              'Projects Reported', 'Projects Financed', 'Commitments',
              'Projects Reported', 'Projects Financed', 'Commitments', 'Disbursements',
              'Expenditures'
              ]],
            summary_columns={14: ('SUM', (1, 6, 11)),
                             15: ('SUM', (2, 7, 12)),
                             16: ('SUM', (3, 8, 13)),
                             17: ('SUM', (4, 9)),
                             18: ('SUM', (5, 10))},
            summary_rows=(('Total', 'SUM', (1, 3, 4, 5, 6, 8, 9, 10, 11, 13, 14, 16, 17, 18)),)
        )

    def gen_data(self, activities, transactions, **kwargs):
        # Find which organisations reported one of the given activities and how many they
        # reported on by activity status
        reporting_orgs = dictify_tuple_list(activities.values_list(
            'reporting_organisation__name', 'activity_status_id'
        ).annotate(
            Count('pk', distinct=True)  # number of projects
        ))
        # Find which organisations financed one of the given activities and how many they
        # financed by activity status
        financing_orgs = dictify_tuple_list(transactions.values_list(
            'provider_organisation__name', 'activity__activity_status_id', 'transaction_type'
        ).annotate(
            Count('activity_id', distinct=True),  # number of projects
            Sum('usd_value')  # total money committed/disbursed/expensed
        ))

        # Get all reporting and financing organisations and sort alphabetically by name
        organisations = sorted(list(set(list(reporting_orgs.keys()) + list(financing_orgs.keys()))))

        # For each organisation create a data-tuple with the reporting and financing info
        # broken down by activity status
        data = []
        for organisation in organisations:
            row = (organisation,)
            # If the organisation reported on projects get a {status: count} dict
            reported_projects_by_status = (dictify_tuple_list(reporting_orgs[organisation])
                                           if organisation in reporting_orgs
                                           else {})
            # If the organisation financed projects get a {status: finance type, count, value}
            # dict
            transactions_by_activity_status = (dictify_tuple_list(financing_orgs[organisation])
                                               if organisation in financing_orgs
                                               else {})
            # Summarize an organisations financial contributions to activities by their status
            for status_name in STATUS_CODES.keys():
                status_code = STATUS_CODES[status_name]
                num_reported = (reported_projects_by_status[status_code][0][0]
                                if status_code in reported_projects_by_status
                                else 0)
                if status_code in transactions_by_activity_status:
                    status_transactions = transactions_by_activity_status[status_code]
                    num_financed = sum(map(itemgetter(1), status_transactions))
                    commitments = sum(map(itemgetter(2),
                                          [t for t in status_transactions if t[0] == 'C']))
                    disbursements = sum(map(itemgetter(2),
                                            [t for t in status_transactions if t[0] == 'D']))
                    expenditures = sum(map(itemgetter(2),
                                           [t for t in status_transactions if t[0] == 'E']))
                else:
                    num_financed = commitments = disbursements = expenditures = 0

                # Handling for pre-implementation activities which will have no disbursements
                if status_name != 'Pipeline/identification':
                    row += (num_reported, num_financed, commitments, disbursements, expenditures)
                else:
                    row += (num_reported, num_financed, commitments)
            data.append(row)

        return data


class SectorSummaryExporter(DataExporter):
    """ Generates a summary of the number of projects and their financing by DAC Sector."""

    def get_writer(self, **kwargs):
        return ExportTemplateWriter(
            'Sectors Summary',
            [ExportTemplateWriter.WIDE_COLUMN_PARAMS,
             ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
             ExportTemplateWriter.MONEY_COLUMN_PARAMS,
             ExportTemplateWriter.MONEY_COLUMN_PARAMS,
             ExportTemplateWriter.MONEY_COLUMN_PARAMS,
             ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
             ExportTemplateWriter.MONEY_COLUMN_PARAMS,
             ExportTemplateWriter.MONEY_COLUMN_PARAMS,
             ExportTemplateWriter.MONEY_COLUMN_PARAMS,
             ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
             ExportTemplateWriter.MONEY_COLUMN_PARAMS,
             ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
             ExportTemplateWriter.MONEY_COLUMN_PARAMS,
             ExportTemplateWriter.MONEY_COLUMN_PARAMS,
             ExportTemplateWriter.MONEY_COLUMN_PARAMS],
            [['Sectors (OECD-DAC)',
              'Completed', None, None, None,
              'Implementing', None, None, None,
              'Proposed/Negotiation', None,
              'Total', None, None, None],
             [None,
              'Number of Projects', 'Commitments', 'Disbursements', 'Expenditures',
              'Number of Projects', 'Commitments', 'Disbursements', 'Expenditures',
              'Number of Projects', 'Commitments',
              'Number of Projects', 'Commitments', 'Disbursements', 'Expenditures'
              ]],
            summary_columns={11: ('SUM', (1, 5, 9)),
                             12: ('SUM', (2, 6, 10)),
                             13: ('SUM', (3, 7)),
                             14: ('SUM', (4, 8))},
            summary_rows=(('Total', 'SUM', (2, 3, 4, 6, 7, 8, 10, 12, 13, 14)),)
        )

    def gen_data(self, activities, transactions, **kwargs):
        # Get the number of activities of each relevant status by DAC-3 sector
        activitysectors = aims.ActivitySector.objects.filter(activity__in=activities)
        activities_by_sector = dictify_tuple_list(
            activitysectors.filter(
                vocabulary='DAC-3',
            ).values_list(
                'sector__category__name', 'activity__activity_status_id'
            ).annotate(
                Count('activity', distinct=True)  # number of activities
            )
        )

        # Special handling for activities that don't use DAC-3 vocabulary
        if activities.exclude(activitysector__vocabulary='DAC-3').exists():
            activities_by_sector['Not Specified'] = list(activities.exclude(
                activitysector__vocabulary='DAC-3'
            ).values_list(
                'activity_status_id'
            ).annotate(
                Count('pk', distinct=True)  # number of activities
            ))

        # Group transactions by activity DAC-3 sector and activity status
        transactions_by_sector = tuple(
            transactions.values_list(
                'activity__activitysector__vocabulary',
                'activity__activitysector__sector__category__name',
                'activity__activitysector__percentage',
                'activity__activity_status_id',
                'transaction_type',
                'activity_id',
                'usd_value',
            )
        )
        # Handle transactions attached to activities without a DAC-3 sector breakdown
        if transactions.exclude(activity__activitysector__vocabulary='DAC-3').exists():
            transactions_by_sector += tuple(
                [('DAC-3', 'Not Specified', 100.0) + tuple(t) for t in transactions.exclude(
                    activity__activitysector__vocabulary='DAC-3'
                ).values_list(
                    'activity__activity_status_id', 'transaction_type', 'activity_id'
                ).annotate(
                    Sum('usd_value')  # total commitments/disbursements/expenses
                )]
            )
        # Filter out vocabularies other than DAC-3
        transactions_by_sector = [t for t in transactions_by_sector if t[0] == 'DAC-3' and t[1] and t[6]]

        # Build a lookup table of activity : total percentage allocation to DAC3 sectors
        # This is used to correct for any activities where the sum of DAC-3 sectors is not equal to 100
        activity_dac3_sums = {activity[0]: activity[1] for activity in aims.Activity.objects.filter(activitysector__vocabulary='DAC-3').annotate(Sum('activitysector__percentage')).values_list('pk', 'activitysector__percentage__sum')}
        # Where an activity has "no" DAC-3s it comes as 100% "Not Specified"
        for t in transactions_by_sector:
            if t[1] == 'Not Specified':
                activity_dac3_sums[t[5]] = 100

        # Convert to dictionary keyed off sector name and adjust value by percentage allocated
        # to sector for activity
        transactions_by_sector = dictify_tuple_list(
            [(t[1], t[3], t[4], float(t[2]) / float(activity_dac3_sums[t[5]]) * float(t[6])) for t in transactions_by_sector if t[2] and t[6] and activity_dac3_sums[t[5]]]
        )

        # Get the sector names
        sectors = sorted(list(activities_by_sector.keys()))

        # Create a data-tuple for each sector with the financing information for projects
        # in each of the relevant phases
        data = []
        for sector in sectors:
            row = (sector,)

            # Get the activity and transaction information for this sector and store by status
            activities_by_status = (dictify_tuple_list(activities_by_sector[sector])
                                    if sector in activities_by_sector
                                    else {})
            transactions_by_status = (dictify_tuple_list(transactions_by_sector[sector])
                                      if sector in transactions_by_sector
                                      else {})

            # For each status add the number of projects and financing to the row
            for status_name in STATUS_CODES.keys():
                status_code = STATUS_CODES[status_name]
                num_projects = (activities_by_status[status_code][0][0]
                                if status_code in activities_by_status
                                else 0)
                if status_code in transactions_by_status:
                    commitments = sum(map(itemgetter(1),
                                          [t for t in transactions_by_status[status_code] if t[0] == 'C']))
                    disbursements = sum(map(itemgetter(1),
                                            [t for t in transactions_by_status[status_code] if t[0] == 'D']))
                    expenditures = sum(map(itemgetter(1),
                                           [t for t in transactions_by_status[status_code] if t[0] == 'E']))
                else:
                    commitments = disbursements = expenditures = 0.0

                # Handling for pre-implementation activities which will have no disbursements
                if status_name != 'Pipeline/identification':
                    row += (num_projects, commitments, disbursements, expenditures)
                else:
                    row += (num_projects, commitments)
            data.append(row)

        return data


class ActivityExporter(DataExporter):
    """ General class for exporting data about activities

    Users can specify a subset of the column parameters/column titles if the activities have
    been filtered, e.g. by sector or location.
    """
    DEFAULT_COLUMN_PARAMS = {
        'Aid Type': ExportTemplateWriter.WIDE_COLUMN_PARAMS,
        'Finance Type': ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
        'Status': ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
        'Currency': ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
        'Commitment USD': ExportTemplateWriter.MONEY_COLUMN_PARAMS,
        'Disbursement USD': ExportTemplateWriter.MONEY_COLUMN_PARAMS,
        'Reporting Partner': ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
        'Financing Partner': ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
        'Implementing Partner': ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
        'Partner Ministry': ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
        'Sector (OECD)': ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
        common_text.get('non_iati_sector_title'): ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
        'Location (State/Region)': ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
        'Start Date': {'width': 15},
        'End Date': {'width': 15},
        'Comment': ExportTemplateWriter.TEXT_COLUMN_PARAMS,
    }
    DEFAULT_COLUMN_TITLES = ('Aid Type', 'Finance Type', 'Status', 'Currency', 'Commitment USD', 'Disbursement USD', 'Reporting Partner', 'Financing Partner', 'Implementing Partner', 'Partner Ministry', 'Sector (OECD)', common_text.get('non_iati_sector_title'), 'Location (State/Region)', 'Start Date', 'End Date', 'Comment')
    DEFAULT_TITLE = 'Activities'

    def __init__(self,
                 column_params=DEFAULT_COLUMN_PARAMS,
                 column_titles=DEFAULT_COLUMN_TITLES,
                 title=DEFAULT_TITLE,
                 **kwargs):
        DataExporter.__init__(self, **kwargs)
        self.column_params = column_params
        self.column_titles = column_titles
        self.title = title

    def get_writer(self, **kwargs):
        return ExportTemplateWriter(self.title,
                                    (ExportTemplateWriter.WIDE_COLUMN_PARAMS,) +
                                    tuple((self.column_params[col] for col in self.column_titles)),
                                    (('Project',) + self.column_titles,))

    def gen_data(self, activities, transactions, **kwargs):
        rows = {}
        transaction_filter = {'pk__in': [transaction.pk for transaction in transactions]}

        # Create a dict for each activity keyed off the possible column titles containing
        # the appropriate activity field and store this under row[activity.title]
        for activity in activities:
            rows[activity.title] = {
                'Aid Type': activity.aid_type,
                'Finance Type': activity.finance_type,
                'Status': activity.status,
                'Currency': activity.currency,
                'Commitment USD': activity.total_commitment_usd,
                'Disbursement USD': activity.disbursements(transaction_filter),
                'Reporting Partner': activity.reporting_partner,
                'Financing Partner': activity.funding_partners,
                'Implementing Partner': activity.implementing_partners,
                'Partner Ministry': activity.partner_ministries,
                'Sector (OECD)': activity.sector_breakdown,
                common_text.get('non_iati_sector_title'): activity.sector_working_group,
                'Location (State/Region)': activity.locations,
                'Start Date': activity.start_date,
                'End Date': activity.end_date,
                'Comment': ""
            }

        # Convert rows to a data array
        data = []
        for activity in sorted(rows.keys()):
            data.append((activity,) + tuple([rows[activity][col] for col in self.column_titles]))

        return data

    # Preset configurations
    PARTNER_COLUMN_TITLES = ('Aid Type', 'Finance Type', 'Status', 'Currency', 'Commitment USD', 'Disbursement USD', 'Financing Partner', 'Implementing Partner', 'Partner Ministry', 'Sector (OECD)', common_text.get('non_iati_sector_title'), 'Location (State/Region)', 'Start Date', 'End Date', 'Comment')

    SECTOR_COLUMN_TITLES = ('Aid Type', 'Finance Type', 'Status', 'Currency', 'Commitment USD', 'Disbursement USD', 'Reporting Partner', 'Financing Partner', 'Implementing Partner', 'Partner Ministry', 'Location (State/Region)', 'Start Date', 'End Date', 'Comment')


class ActivityAnnualBreakdown(DataExporter):
    """ Export information about activities including yearly financing."""

    def __init__(self, years=list(range(2011, 2020)), **kwargs):
        """ User can specify which years to summarize."""
        DataExporter.__init__(self, **kwargs)
        self.years = years

    def get_writer(self,
                   **kwargs):
        column_params = [ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
                         ExportTemplateWriter.WIDE_COLUMN_PARAMS,
                         ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
                         ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
                         ExportTemplateWriter.TEXT_COLUMN_PARAMS,
                         ExportTemplateWriter.TEXT_COLUMN_PARAMS,
                         ExportTemplateWriter.TEXT_COLUMN_PARAMS,
                         ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
                         ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
                         ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
                         ExportTemplateWriter.DEFAULT_COLUMN_PARAMS]
        column_titles = [['ID', 'Activity Title', 'Status', 'Reporting', 'Financing',
                          'Extending', 'Implementing', 'Planned Start Date', 'Planned End Date',
                          'Actual Start Date', 'Actual End Date'],
                         [None, None, None, None, None, None, None, None, None, None, None]]
        num_group_fields = 11
        title = 'Annual Commitment & Disbursement By Activity'

        # Add parameters and titles for each year to summarize
        for year_label in daterange(min(self.years), max(self.years)).get_all_quarters():

            # Add two columns for "Commitment" and "Disbursement"
            column_params += 2 * (ExportTemplateWriter.MONEY_COLUMN_PARAMS,)
            column_titles[0] += (year_label, None)
            column_titles[1] += ('Commitment', 'Disbursement')

        # Add parameters and titles for the columns summarizing all years included
        column_params.extend(2 * [ExportTemplateWriter.MONEY_COLUMN_PARAMS])
        column_titles[0].extend(['Total', None])
        column_titles[1].extend(['Commitment', 'Disbursement'])

        # Summary columns should be total commitments and disbursements for the years specified
        commitment_total_index = num_group_fields + 2 * len(self.years)
        disbursement_total_index = num_group_fields + 2 * len(self.years) + 1
        summary_columns = {commitment_total_index: ('SUM', tuple(range(num_group_fields, num_group_fields + 2 * len(self.years), 2))),
                           disbursement_total_index: ('SUM', tuple(range(num_group_fields + 1, num_group_fields + 2 * len(self.years), 2)))}

        # Summary row should be total commitments and disbursements for each year specified
        summary_rows = (('Total', 'SUM', tuple(range(num_group_fields,
                                                     num_group_fields + 2 + 2 * len(self.years)))),)

        # Add parameters and titles for contact information
        column_params.extend(3 * [ExportTemplateWriter.DEFAULT_COLUMN_PARAMS])
        column_titles[0].extend(['Contact Name', 'Contact Phone', 'Contact Email'])
        column_titles[1].extend([None, None, None])

        return ExportTemplateWriter(title,
                                    column_params,
                                    column_titles,
                                    summary_columns=summary_columns,
                                    summary_rows=summary_rows)

    def gen_data(self, activities, transactions, **kwargs):
        # Fetch relevant fields for each activity
        activity_tuples = activities.values_list(
            'pk', 'internal_identifier', 'activity_status__name', 'reporting_organisation__name', 'start_actual',
            'end_actual', 'start_planned', 'end_planned'
        )
        # Get the english titles for all activities
        titles = dictify_tuple_list(
            aims.Title.objects.filter(language='en').values_list('activity', 'title')
        )
        # Get all participating organisations and their role for each activity
        activity_participating_orgs = dictify_tuple_list(
            aims.ActivityParticipatingOrganisation.objects.values_list('activity',
                                                                       'organisation__name',
                                                                       'role')
        )
        # Get relevant transaction information and store by activity
        transactions_by_activity = dictify_tuple_list(
            transactions.values_list('activity', 'transaction_type', 'transaction_date',
                                     'usd_value')
        )
        # Get all contacts per activity
        contacts = dictify_tuple_list(
            aims.ContactInfo.objects.values_list('activity', 'person_name', 'telephone', 'email')
        )

        # Generate a tuple of relevant information for each activity
        data = []
        for activity in activity_tuples:
            if activity[0] in activity_participating_orgs:
                # If there are participating orgs find the names of the funding, extending,
                # and implementing organisations
                funding = ', '.join(
                    map(itemgetter(0),
                        [apo for apo in activity_participating_orgs[activity[0]] if apo[1] == 'Funding']
                        )
                )
                extending = ', '.join(
                    map(itemgetter(0),
                        [apo for apo in activity_participating_orgs[activity[0]] if apo[1] == 'Extending']
                        )
                )
                implementing = ', '.join(
                    map(itemgetter(0),
                        [apo for apo in activity_participating_orgs[activity[0]] if apo[1] == 'Implementing']
                        )
                )
            else:
                # Otherwise set these to ''
                funding = extending = implementing = ''

            # Write basic activity data to row
            row = (
                (activity[0], titles[activity[0]][0][0] if activity[0] in titles else '') +
                activity[1:3] + (funding, extending, implementing) +
                tuple([date.isoformat() if date else '' for date in activity[3:]])
            )

            activity_transactions = transactions_by_activity[activity[0]]

            # For each fiscal year get the activity's commitments and disbursements and
            # append to row
            # TODO: MOH-475
            daterange_years = daterange(min(self.years), max(self.years))
            iterate_over = daterange_years.get_all_years()
            for year_label, year_info in iterate_over.items():

                for q, i in enumerate(year_info):
                    begin, end = i

                    commitment = sum(
                        map(itemgetter(2),
                            [t for t in activity_transactions
                                if (t[0] == 'C' and t[1] and begin <= t[1].isoformat() and t[1].isoformat() <= end and t[2] != '')])
                    )
                    disbursement = sum(
                        map(itemgetter(2),
                            [t for t in activity_transactions
                                if (t[0] == 'D' and t[1] and begin <= t[1].isoformat() and t[1].isoformat() <= end and t[2] != '')])
                    )
                    row += tuple([commitment if commitment else 0, disbursement if disbursement else 0])

            # Get a contact for the activity and append to the row
            if activity[0] in contacts:
                contact_info = contacts[activity[0]][0]
            else:
                contact_info = (None, None, None)
            row += contact_info
            data.append(row)

        return data


class AnnualBreakdownExporter(DataExporter):
    """ Base class for exporters that summarize the finances of grouped activities.

    Subclasses should implement the get groups and get_transactions_by_group methods which
    define how to split the Activity models into groups of Activity models and how to
    get the transactions associated with that group. If the group is defined by more than
    one field then get_group_key should also be implemented to extract the unique fields
    defining a group given one of the tuples returned by get_groups.

    Arguments:
    title -- Header for the data export
    column_params -- Column parameters for the group fields returned by get_groups
    column_titles -- Column titles for the group fields returned by get_groups

    Keyword Arguments:
    years -- The fiscal years overwhich to summarize the activity groups
    quarterly -- Should the yearly breakdowns be quarterly?
    """

    def __init__(self,
                 title,
                 column_params,
                 column_titles,
                 years=list(range(2011, 2020)),
                 quarterly=False,
                 **kwargs):
        DataExporter.__init__(self, **kwargs)
        self.title = title.replace('Annual', 'Quarterly') if quarterly else title
        self.column_params = column_params
        self.column_titles = column_titles
        self.num_group_fields = len(self.column_params)

        self.years = years
        self.quarterly = quarterly

    def get_writer(self, **kwargs):
        # Base column parameters/titles
        column_params = self.column_params
        column_titles = list(self.column_titles)

        # multiple = 8 if self.quarterly else 2  # Number of columns per year
        # Count the number of columns to sum for C, D
        financial_columns_count = 0

        # For each year append the column parameters/titles
        for year_label, year_quarters in daterange(min(self.years), max(self.years)).get_all_quarters().items():
            if self.quarterly:
                # Add two columns per quarter for "Commitment" and "Disbursement"
                for q, i in enumerate(year_quarters):
                    column_titles[0] += ('{} Q{}'.format(year_label, q + 1), None)
                    column_titles[1] += ('Commitment', 'Disbursement')
                    column_params += (ExportTemplateWriter.MONEY_COLUMN_PARAMS,)
                    column_params += (ExportTemplateWriter.MONEY_COLUMN_PARAMS,)
                    financial_columns_count += 2

            else:
                # Add two columns for "Commitment" and "Disbursement"
                column_params += 2 * (ExportTemplateWriter.MONEY_COLUMN_PARAMS,)
                column_titles[0] += (year_label, None)
                column_titles[1] += ('Commitment', 'Disbursement')
                financial_columns_count += 2

        # Append the summary column parameters/titles
        column_params += 2 * (ExportTemplateWriter.MONEY_COLUMN_PARAMS,)
        column_titles[0] += ('Total', None)
        column_titles[1] += ('Commitment', 'Disbursement')

        # Define the summary columns to be the sum of the commitments/disbursements respectively
        commitment_total_index = self.num_group_fields + financial_columns_count
        disbursement_total_index = self.num_group_fields + financial_columns_count + 1
        summary_columns = {
            commitment_total_index: (
                'SUM',
                tuple(range(self.num_group_fields,
                            self.num_group_fields + financial_columns_count,
                            2))
            ),
            disbursement_total_index: (
                'SUM',
                tuple(range(self.num_group_fields + 1,
                            self.num_group_fields + financial_columns_count,
                            2))
            )
        }

        # Add a row with the total commitments/disbursements for each time interval
        summary_rows = (('Total',
                         'SUM',
                         tuple(range(self.num_group_fields,
                                     self.num_group_fields + 2 + financial_columns_count))),)

        # Add the parameters and title for the last time each group had an Activity updated
        column_params += (ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,)
        column_titles[0] += ('Last Updated',)
        column_titles[1] += (None,)

        return ExportTemplateWriter(self.title,
                                    column_params,
                                    column_titles,
                                    summary_columns=summary_columns,
                                    summary_rows=summary_rows)

    def gen_data(self, activities, transactions, **kwargs):
        # Get the tuples defining each group of activities and the transactions per group
        groups = self.get_groups(activities)
        transactions_by_group = self.get_transactions_by_group(transactions.filter(usd_value__gt=0))

        # Generate a row summarizing the finances for each group per time interval
        data = []
        for group in groups:
            row = group[:-1]  # Add group data to row excluding 'Last Updated', the last column
            key = self.get_group_key(group)

            # Get the commitments and disbursements for each group for each time interval

            daterange_years = daterange(min(self.years), max(self.years))
            iterate_over = daterange_years.get_all_quarters() if self.quarterly else daterange_years.get_all_years()
            for year_label, year_quarters in iterate_over.items():

                for q, i in enumerate(year_quarters):
                    commitment = 0
                    disbursement = 0
                    begin, end = i
                    if key not in transactions_by_group:
                        row += tuple([0, 0])
                        continue

                    for t in transactions_by_group[key]:
                        has_values = t[1] and t[2]
                        in_range = begin <= t[1].isoformat() <= end

                        if not in_range or not has_values:
                            continue

                        if t[0] == 'C':
                            commitment += t[2]
                        elif t[0] == 'D':
                            disbursement += t[2]

                    row += tuple([commitment, disbursement])

            # Add 'last_modified'
            row += (group[-1],)

            data.append(row)

        return data

    @staticmethod
    def get_groups(activities):
        """ Return tuples containing each of the groups in activities."""

    @staticmethod
    def get_transactions_by_group(transactions, group_field='activity'):
        """ Return all of the transactions per group as a dictionary."""
        return dictify_tuple_list(transactions.values_list(group_field, 'transaction_type', 'transaction_date', 'usd_value'))

    @staticmethod
    def get_group_key(group):
        """ Extract the fields defining a group from a group-tuple. Should serve as the key to
        the dict returned by get_transactions_by_group. By default this is the first element.
        """
        return group[0]


class DevelopmentPartnerAnnualBreakdown(AnnualBreakdownExporter):
    """ Export the yearly or quarterly financing of projects grouped by the reporting org."""

    def __init__(self, years=list(range(2011, 2020)), quarterly=False, **kwargs):
        AnnualBreakdownExporter.__init__(
            self,
            'Annual Commitment & Disbursement By Development Partner',
            (ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
             ExportTemplateWriter.WIDE_COLUMN_PARAMS),
            (('ID', 'Development Partner'), (None, None)),
            years=years,
            quarterly=quarterly,
            **kwargs
        )

    @staticmethod
    def get_groups(activities):
        """ Return tuples (reporting org id, reporting org name, last updated activity by org)
        for each reporting organisation contained in activities
        """
        return activities.order_by('reporting_organisation__name')\
            .values_list('reporting_organisation_id', 'reporting_organisation__name')\
            .annotate(Max('last_updated_datetime'))  # last updated

    @staticmethod
    def get_transactions_by_group(transactions):
        """ Return transactions by reporting organisation in a dict"""
        return AnnualBreakdownExporter.get_transactions_by_group(
            transactions, group_field='activity__reporting_organisation_id'
        )


class StateAnnualBreakdown(AnnualBreakdownExporter):
    """ Export the yearly or quarterly financing of projects grouped by state."""

    def __init__(self, years=list(range(2011, 2020)), quarterly=False, **kwargs):
        AnnualBreakdownExporter.__init__(
            self,
            'Annual Commitment & Disbursement By State/Region',
            (ExportTemplateWriter.WIDE_COLUMN_PARAMS,),
            (('State/Region',), (None,)),
            years=years,
            quarterly=quarterly,
            **kwargs
        )

    @staticmethod
    def get_groups(activities):
        """ Return tuples of state names and the last updated activity in the state. Special
        handling to include nation-wide activities first and group activities that do not
        include a location or set their location to nation-wide.
        """
        # Nation-wide activities have adm_country_adm1 field 'Nation-wide'
        nation_wide = activities.filter(
            location__adm_country_adm1='Nation-wide'
        ).values_list(
            'location__adm_country_adm1'
        ).annotate(
            Max('last_updated_datetime')  # last updated
        )

        # Get all other adm_country_adm1 values not matching the above scenarios
        states = tuple(
            activities.exclude(
                location__adm_country_adm1__in=['Nation-wide', '']
            ).filter(
                location__isnull=False
            ).order_by(
                'location__adm_country_adm1'
            ).values_list(
                'location__adm_country_adm1'
            ).annotate(
                Max('last_updated_datetime')  # last updated
            )
        )

        # Consider location unspecified if no Location exists for an Activity or if
        # adm_country_adm1 is ''
        last_unspecified_update = activities.filter(
            Q(location__isnull=True) | Q(location__adm_country_adm1='')
        ).aggregate(
            last_updated=Max('last_updated_datetime')
        )['last_updated']

        if last_unspecified_update is not None:
            return tuple(nation_wide) + states + (('Not Specified', last_unspecified_update),)
        else:
            return tuple(nation_wide) + states

    @staticmethod
    def get_transactions_by_group(transactions):
        """ Get the transactions associated with each state with special handling for
        activities whose location is unspecified or state name is set to ''. We include
        the Location.percentage field because Transaction models are not broken down by
        Location. If a Location object isn't specified we set this percentage to 100.0 for
        the artificial 'Not Specified' state.
        """
        # Transactions for states that are specified
        transactions_by_state = tuple(
            transactions.exclude(
                activity__location__adm_country_adm1=''
            ).filter(
                activity__location__isnull=False
            ).values_list(
                'activity__location__adm_country_adm1', 'activity__location__percentage',
                'transaction_type', 'transaction_date', 'usd_value'
            )
        )
        # Transactions where the state isn't specified but a Location (and hence percentage)
        # is given
        transactions_by_state += tuple(
            [('Not Specified',) + tuple(t) for t in transactions.filter(
                activity__location__adm_country_adm1=''
            ).values_list(
                'activity__location__percentage', 'transaction_type', 'transaction_date',
                'usd_value'
            )]
        )
        # Transactions not attached to any Location are assigned to 'Not Specified'
        transactions_by_state += tuple(
            [('Not Specified', 100.0) + tuple(t) for t in transactions.filter(
                activity__location__isnull=True
            ).values_list(
                'transaction_type', 'transaction_date', 'usd_value'
            )]
        )
        return dictify_tuple_list([(t[0], t[2], t[3], float(t[1]) / 100 * float(t[4])) for t in transactions_by_state if t[4]])


class TownshipAnnualBreakdown(AnnualBreakdownExporter):
    """ Export the yearly or quarterly financing of projects by state and township."""

    def __init__(self, years=list(range(2011, 2020)), quarterly=False, **kwargs):
        AnnualBreakdownExporter.__init__(
            self,
            'Annual Commitment & Disbursement By Township',
            (ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
             ExportTemplateWriter.DEFAULT_COLUMN_PARAMS),
            (('State/Region', 'Township'), (None, None)),
            years=years,
            quarterly=quarterly,
            **kwargs
        )

    @staticmethod
    def get_groups(activities):
        """ Return tuples of state and township names and the last updated activity in the
        township. Special handling to include nation-wide activities first and grouP
        activities that do not include a location or set their location to nation-wide.
        """
        # Nation-wide activities have adm_country_adm1 field 'Nation-wide'
        nation_wide = activities.filter(
            location__adm_country_adm1='Nation-wide'
        ).values_list(
            'location__adm_country_adm1', 'location__adm_country_adm2'
        ).annotate(
            Max('last_updated_datetime')  # last updated
        )

        # Get all other (state, township) values not matching the above scenarios
        townships = tuple(
            activities.exclude(
                location__adm_country_adm1__in=['Nation-wide', '']
            ).filter(
                location__isnull=False
            ).order_by(
                'location__adm_country_adm1', 'location__adm_country_adm2'
            ).values_list(
                'location__adm_country_adm1', 'location__adm_country_adm2'
            ).annotate(
                Max('last_updated_datetime')  # last updated
            )
        )

        # Consider location unspecified if no Location exists for an Activity or if
        # adm_country_adm1 is ''
        last_unspecified_update = activities.exclude(
            location__adm_country_adm1=''
        ).filter(
            location__isnull=True
        ).aggregate(
            last_updated=Max('last_updated_datetime')
        )['last_updated']

        if last_unspecified_update is not None:
            return tuple(nation_wide) + townships + (('Not Specified', '', last_unspecified_update),)
        else:
            return tuple(nation_wide) + townships

    @staticmethod
    def get_transactions_by_group(transactions):
        """ Get the transactions associated with each township with special handling for
        activities whose location is unspecified or state name is set to ''. Because
        transactions do not include location data we use the percentage in Location models to
        estimate the commitment/disbursement in a township.
        """
        # Transactions by township
        transactions_by_township = tuple(
            transactions.exclude(
                activity__location__adm_country_adm1=''
            ).filter(
                activity__location__isnull=False
            ).values_list(
                'activity__location__adm_country_adm1', 'activity__location__adm_country_adm2',
                'activity__location__percentage', 'transaction_type', 'transaction_date',
                'usd_value'
            )
        )
        # Transactions where the state is given as '' we assign to 'Not Specified' with the
        # percentage given in the Location object
        transactions_by_township += tuple(
            [('Not Specified', '') + tuple(t) for t in transactions.filter(
                activity__location__adm_country_adm1=''
            ).values_list(
                'activity__location__percentage', 'transaction_type', 'transaction_date',
                'usd_value'
            )]
        )
        # Transactions whose Activity has no Location are fully assigned to 'Not Specified'
        transactions_by_township += tuple(
            [('Not Specified', '', 100.0) + tuple(t) for t in transactions.filter(
                activity__location__isnull=True
            ).values_list(
                'transaction_type', 'transaction_date', 'usd_value'
            )]
        )
        return dictify_tuple_list([((t[0], t[1]), t[3], t[4], float(t[2]) / 100 * float(t[5]))
                                   for t in transactions_by_township if t[5]])

    @staticmethod
    def get_group_key(group):
        return (group[0], group[1])


class SectorAnnualBreakdown(AnnualBreakdownExporter):
    """ Export the yearly or quarterly finances of projects by DAC Sector."""

    def __init__(self, years=list(range(2011, 2020)), quarterly=False, **kwargs):
        AnnualBreakdownExporter.__init__(self,
                                         'Annual Commitment & Disbursement By Sector',
                                         (ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
                                          ExportTemplateWriter.DEFAULT_COLUMN_PARAMS),
                                         (('Code', 'Sector'), (None, None)),
                                         years=years,
                                         quarterly=quarterly,
                                         **kwargs)

    @staticmethod
    def get_groups(activities):
        """ Get all DAC-3 sector codes and names for Activity models in activities. Special
        handling is required for Activity objects that either have no associated
        ActivitySector models or whose ActivitySector models don't break down activities by
        the DAC-3 vocabulary.
        """
        # Get all sector codes/names for Activity models in activities. Include the vocabulary
        # since we will later filter down to the DAC-3 vocabulary
        groups = tuple(
            activities.order_by(
                'activitysector__sector__category__name'
            ).values_list(
                'activitysector__vocabulary', 'activitysector__sector__category__code',
                'activitysector__sector__category__name'
            ).annotate(
                Max('last_updated_datetime')  # last updated
            )
        )

        last_unspecified_update = activities.exclude(
            activitysector__vocabulary='DAC-3'
        ).aggregate(
            last_updated=Max('last_updated_datetime')
        )['last_updated']

        if last_unspecified_update is not None:
            # Add a 'Not Specified' sector for all Activity models without a DAC-3 breakdown
            groups += (('DAC-3', '', 'Not Specified', last_unspecified_update),)

        # Filter out groups corresponding to vocabularies other than DAC-3
        return [g[1:] for g in [g for g in groups if g[0] == 'DAC-3' and g[1] is not None]]

    @staticmethod
    def get_transactions_by_group(transactions):
        """ Get the transactions associated with each DAC-3 sector with special handling for
        transactions whose activity either doesn't specify any sectors or whose sectors
        don't use DAC-3 vocabulary. Because transactions are not broken down by sector, the
        percentage in ActivitySector is used to estimate the amount of a transaction's value
        assigned to each of the activity's sectors.
        """
        # Get transaction information by sector
        transactions_by_sector = tuple(
            transactions.values_list(
                'activity__activitysector__vocabulary',
                'activity__activitysector__sector__category__code',
                'activity__activitysector__percentage', 'transaction_type',
                'transaction_date', 'usd_value')
        )
        # Handle transactions attached to activities without a DAC-3 sector breakdown
        transactions_by_sector += tuple(
            [('DAC-3', '', 100.0) + tuple(t) for t in transactions.exclude(
                activity__activitysector__vocabulary='DAC-3'
            ).values_list(
                'transaction_type', 'transaction_date', 'usd_value'
            )]
        )
        # Filter out vocabularies other than DAC-3
        transactions_by_sector = [t[1:] for t in [t for t in transactions_by_sector if t[0] == 'DAC-3' and t[1] is not None]]
        return dictify_tuple_list([(t[0], t[2], t[3], float(t[1] or 0) / 100 * float(t[4])) for t in transactions_by_sector if t[4]])


class SectorWorkingGroup(DataExporter):
    """ Export the Activity models associated with a sector working group ('RO' vocabulary).
    """

    def __init__(self, sector, **kwargs):
        DataExporter.__init__(self, **kwargs)
        self.sector = sector

    def get_writer(self, **kwargs):
        return ExportTemplateWriter(self.sector.name + ' ' + common_text.get('non_iati_sector_title'),
                                    (ExportTemplateWriter.WIDE_COLUMN_PARAMS,
                                     ExportTemplateWriter.WIDE_COLUMN_PARAMS,
                                     ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
                                     ExportTemplateWriter.MONEY_COLUMN_PARAMS,
                                     ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
                                     ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
                                     ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
                                     ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
                                     ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
                                     ExportTemplateWriter.WIDE_COLUMN_PARAMS,
                                     ExportTemplateWriter.DEFAULT_COLUMN_PARAMS),
                                    (('Reporting Organisation',
                                      'Activity',
                                      'Sector',
                                      'Total Budget',
                                      'State/Region',
                                      'Start Date',
                                      'End Date',
                                      'Contact Name',
                                      'Contact Phone',
                                      'Contact Email',
                                      'Last Updated'),))

    def gen_data(self, activities, transactions, **kwargs):
        # Get activity information for activities associated with a sector working group
        activity_tuples = activities.filter(
            activitysector__sector__in=aims.NationalSector.objects.all()
        ).values_list(
            'pk', 'reporting_organisation__name', 'start_actual', 'end_actual',
            'last_updated_datetime', 'commitmenttotal__dollars'
        )
        # Get states associated with each activity
        locations = dictify_tuple_list(
            activities.values_list('pk', 'location__adm_country_adm1').distinct()
        )
        # Get English titles by activity
        titles = dictify_tuple_list(
            aims.Title.objects.filter(language='en').values_list('activity', 'title')
        )
        # Get contacts associated with each activity
        contacts = dictify_tuple_list(
            aims.ContactInfo.objects.values_list('activity', 'person_name', 'telephone', 'email')
        )

        # Generate a data-tuple for each activity
        data = []
        for activity in activity_tuples:
            title = titles[activity[0]][0][0] if activity[0] in titles else ''
            location = ', '.join(
                map(itemgetter(0), locations[activity[0]])
            ) if activity[0] in locations else ''
            start_date = activity[2].isoformat() if activity[2] else ''
            end_date = activity[3].isoformat() if activity[3] else ''
            if activity[0] in contacts:
                contact_info = contacts[activity[0]][0]
            else:
                contact_info = (None, None, None)
            row = (
                (activity[1], title, self.sector.name, activity[5], location) +
                (start_date, end_date) +
                contact_info +
                (activity[4],)
            )
            data.append(row)
        return data


class DevelopmentPartnerProfile(DataExporter):
    """ Get all contacts grouped by Organisation."""

    def get_writer(self, **kwargs):
        return ExportTemplateWriter('Development Partner Profile',
                                    [ExportTemplateWriter.WIDE_COLUMN_PARAMS,
                                     ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
                                     ExportTemplateWriter.TEXT_COLUMN_PARAMS,
                                     ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
                                     ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
                                     ExportTemplateWriter.DEFAULT_COLUMN_PARAMS],
                                    [['Development Partner',
                                      'Title', 'Address', 'Phone Number', 'Email', 'Fax']],
                                    )

    def gen_data(self, activities, transactions, **kwargs):
        data = []
        for organisation_profile in OrganisationProfile.objects.order_by('organisation').filter(organisation__in=aims.Partner.objects.all()).values_list('organisation__name', 'contact_info__title', 'contact_info__address', 'contact_info__phone_number', 'contact_info__email', 'contact_info__fax'):
            data.append(organisation_profile)
        return data


class ActivitiesWithoutDate(DataExporter):
    """ All activities that do not appear in the dashboard because they don't have a date.

    'no date' is a combination of no start and end date, as well as no dated transaction.
    See aims.models.filter_activities_by_daterange for how date filtering works.
    """

    def __init__(self, date_columns):
        self.date_columns = date_columns
        self.title = 'Activities without a date' if date_columns else 'Activities absent from the dashboard'

    def get_writer(self, **kwargs):
        column_titles = [['Reporting Organisation', 'Activity Title', 'Activity ID', 'Activity Partner ID', 'Activity Link',
                          'Actual Start Date', 'Actual End Date', 'Planned Start Date', 'Planned End Date']]
        column_params = [ExportTemplateWriter.WIDE_COLUMN_PARAMS,
                         ExportTemplateWriter.WIDE_COLUMN_PARAMS,
                         ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
                         ExportTemplateWriter.WIDE_COLUMN_PARAMS] + [ExportTemplateWriter.DEFAULT_COLUMN_PARAMS] * 4
        return ExportTemplateWriter(self.title,
                                    column_params=column_params,
                                    column_titles=column_titles)

    def gen_data(self, *args, **kwargs):
        base_url = 'http://{}'.format(Site.objects.get_current())
        data = []
        for activity in self.activities:
            activity_link = base_url + reverse('edit_activity', kwargs={'pk': activity.pk})
            row = [activity.reporting_partner, activity.title, activity.pk, activity.internal_identifier, activity_link]
            dates = [activity.start_actual, activity.end_actual, activity.start_planned, activity.end_planned]
            for d in dates:
                if d is None:
                    row.append(None)
                else:
                    row.append(d.strftime('%Y-%m-%d'))
            data.append(row)
        return data

    @property
    def activities(self):
        """ Returns activities that have a null date in one or more of the self.date_columns.

        If self.date_columns is empty, returns all activities that don't appear in the dashboard.
        """
        if not self.date_columns:
            return self.activities_absent_from_dashboard
        no_date_filter = Q(**{self.date_columns[0]: None})
        for date_column in self.date_columns[1:]:
            no_date_filter = no_date_filter | Q(**{date_column: None})

        return aims.Activity.objects.filter(no_date_filter)\
                                    .prefetch_related('title_set')\
                                    .select_related('reporting_organisation')

    @property
    def activities_absent_from_dashboard(self):
        """ Returns a queryset of all activities that won't appear in the dashboard. """
        all_activities_pk = aims.Activity.objects.all().values_list('pk', flat=True)
        activities_with_date_pk = aims.filter_activities_by_daterange(aims.Activity.objects.all(),
                                                                      start_date=date(1901, 1, 1), end_date=date(2099, 12, 31)
                                                                      ).values_list('pk', flat=True)
        activities_without_date_pk = set(all_activities_pk) - set(activities_with_date_pk)
        return aims.Activity.objects.filter(pk__in=activities_without_date_pk)\
                                    .prefetch_related('title_set')\
                                    .select_related('reporting_organisation')


class ActivitiesWithoutTransaction(DataExporter):
    """ Report activities that have no transactions or no transaction of a certain type. """

    def __init__(self, transaction_type=None):
        if transaction_type is None:
            self.activities = self.activities_without_transaction
            self.title = 'Activities without transactions'
        else:
            self.activities = self.activities_without_transaction_type(transaction_type)
            self.title = 'Activities without commitments'

    def get_writer(self, **kwargs):
        column_titles = [['Reporting Organisation', 'Activity Title', 'Activity ID', 'Activity Partner ID', 'Activity Link']]
        column_params = [ExportTemplateWriter.WIDE_COLUMN_PARAMS,
                         ExportTemplateWriter.WIDE_COLUMN_PARAMS,
                         ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
                         ExportTemplateWriter.DEFAULT_COLUMN_PARAMS,
                         ExportTemplateWriter.WIDE_COLUMN_PARAMS]
        return ExportTemplateWriter(self.title,
                                    column_params=column_params,
                                    column_titles=column_titles)

    def gen_data(self, *args, **kwargs):
        base_url = 'http://{}'.format(Site.objects.get_current())
        data = []
        for activity in self.activities:
            activity_link = base_url + reverse('edit_activity', kwargs={'pk': activity.pk})
            data.append([activity.reporting_partner, activity.title, activity.id, activity.internal_identifier, activity_link])
        return data

    @property
    def activities_without_transaction(self):
        """ Returns all activities that have no transactions at all. """
        activities = aims.Activity.objects.annotate(transaction_count=Count('transaction'))\
                                          .filter(transaction_count=0)
        return activities.prefetch_related('title_set').select_related('reporting_organisation')

    def activities_without_transaction_type(self, transaction_type):
        """ Returns all activities that have no transactions of a certain type. """
        activities = aims.Activity.objects.annotate(transaction_count=Sum(
            Case(
                When(transaction__transaction_type_id=transaction_type, then=1),
                default=0, output_field=IntegerField()
            ))).filter(transaction_count=0)
        return activities.select_related('reporting_organisation')\
                         .prefetch_related('title_set')


class ActivitiesWithoutBudget(ActivitiesWithoutTransaction):
    """ Report activities that have no budgets """

    def __init__(self):
        DataExporter.__init__(self)
        self.activities = self.activities_without_budget
        self.title = 'Activities without transactions'

    @property
    def activities_without_budget(self):
        """ Returns all activities that have no transactions at all. """
        activities = aims.Activity.objects.annotate(budget_count=Count('budget'))\
                                          .filter(budget_count=0)
        return activities.prefetch_related('title_set').select_related('reporting_organisation')
