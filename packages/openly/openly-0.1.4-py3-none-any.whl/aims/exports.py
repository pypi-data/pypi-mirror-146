from collections import defaultdict
from datetime import date
from typing import Any, Dict, Optional, Union

# type checking import
from django.db.models import query  # noqa: F401

from django.conf import settings
from django.db.models import Count, Sum, Func, F, QuerySet
from django.http import HttpResponse
from django.utils.translation import get_language, gettext_lazy as _

from aims import base_utils, common_text, models as aims
from aims import aggregates


def org_title(activity: Dict[str, str]) -> str:
    if not activity['reporting_organisation_id']:
        return ""
    if activity['reporting_organisation__name']:
        return activity['reporting_organisation__name']
    if activity['reporting_organisation__name']:
        return activity['reporting_organisation__name']
    if activity['reporting_organisation_id']:
        return activity['reporting_organisation_id']
    return ''


def some_sectors(sectors: QuerySet):
    out_sectors = []
    for s in sectors:
        percentage = s['percentage']
        if s['sector__name'] is None:
            sector = base_utils.UNKNOWN_SECTOR_NAME
        else:
            sector = s['sector__name']
        if percentage is None:
            percentage = base_utils.UNKNOWN_PERCENTAGE
        else:
            percentage = "%.2f" % percentage
        out_sectors.append("%s %s%%" % (str(sector), percentage))
    return "|".join(out_sectors)


def activity_objective(objectives, activity: aims.Activity, preferred_language: Union[str, None] = None):
    if activity not in objectives:
        return ""
    if len(objectives[activity]) == 1:
        return objectives[activity][0]['description']

    objectives = objectives[activity]

    # preferred language
    for objective in objectives:
        if preferred_language and objective['language_id'] and objective['language_id'] == preferred_language:
            return objective['description']

    # default language
    for objective in objectives:
        if objective['language_id'] and objective['language_id'] in settings.LANGUAGE_CODE:
            return objective['description']
    # first objective
    return objectives[0]['description']


def some_title(titles, preferred_language=None):
    if len(titles) < 1:
        return str(_("no title"))
    if len(titles) == 1:
        return titles[0]['title']

    # preferred language
    for title in titles:
        if preferred_language and title['language_id'] and title['language_id'] == preferred_language:
            return title['title']

    # default language
    for title in titles:
        if title['language_id'] and title['language_id'] in settings.LANGUAGE_CODE:
            return title['title']
    # first title
    return titles[0]['title']


def some_description(descriptions, preferred_language=None):
    if len(descriptions) < 1:
        return str(_("no description"))
    if len(descriptions) == 1:
        return descriptions[0]['description']

    # preferred language
    for description in descriptions:
        if preferred_language and description['language_id'] and description['language_id'] == preferred_language:
            return description['description']

    # default language
    for description in descriptions:
        if description['language_id'] and description['language_id'] in settings.LANGUAGE_CODE:
            return description['description']

    # first description
    return descriptions[0]['description']


def some_organisations(organisations: QuerySet):
    names = [org.get('organisation__name') or org.get('name', '') for org in organisations]
    return '| '.join(list(set(names)))


def export_activities(activities: QuerySet, transactions: QuerySet, **kwargs: Dict[str, Any]):
    """
       ACTIVITY ID, TITLE, SECTOR, STATUS, TOTAL BUDGET,
       REPORTING ORGANIZATION, START DATE, END DATE
        CONTACT.name, CONTACT.telephone, CONTACT.email
        - reporting org: show the name (or abbrev if none or code if none)
        - status : show the status name
        - show the sector names and their percents
        - multiple sectors in the same column (until I know different)
    """
    from xlwt import Workbook
    response = HttpResponse(content_type='application/vnd.ms-excel')
    today = date.today()
    response['Content-Disposition'] = 'attachment; filename=activities_%s.xls' % today.strftime('%Y_%m_%d')

    def add_summary_sheet(workbook: Optional[Workbook]):
        summary_sheet = workbook.add_sheet("Summary")
        row = 0
        for row_data in kwargs.get('summary'):
            col = 0
            for column in row_data:
                summary_sheet.write(row, col, str(column))
                col += 1
            row += 1

    # sql = connection.cursor().mogrify(*transactions.query.sql_with_params()).decode()
    def filtered_transaction_amounts():
        amounts = {}
        for pk, value, ttype in transactions.values_list('activity', 'usd_value', 'transaction_type_id'):
            value = value or 0
            if pk not in amounts:
                amounts[pk] = {'count': 0, 'commitment': 0, 'disbursement': 0}
            amounts[pk]['count'] += 1
            if ttype == 'C':
                amounts[pk]['commitment'] += value
            if ttype == 'D':
                amounts[pk]['disbursement'] += value
        return amounts

    filtered_amounts = filtered_transaction_amounts()

    def transactions_property(activity_id: str, transactions_property: str) -> int:
        return filtered_amounts.get(activity_id, {}).get(transactions_property, 0)

    workbook = Workbook()
    if kwargs.get('summary'):
        add_summary_sheet(workbook)
    sheet = workbook.add_sheet("Activities")

    # Comment out for now as it prevents Numbers (and Excel?) from puting the data in their proper columns
    # header = [str(_('Filtered activities')), today.strftime('%Y/%m/%d')]
    # writer.writerow(header)

    columns = [
        str(_("id")),
        str(_("Title")),
        str(_('Description')),
        str(_('Objective')),
        str(_("Sector")),
        common_text.get('non_iati_sector_title'),
        str(_("Status")),
        str(_("Collaboration Type")),
        str(_("Aid Type Categories")),
        str(_("Finance Types")),
        str(_("Total Commitment")),
        str(_("Total Disbursement")),
        str(_("Total Commitment USD")),
        str(_("Total Disbursement USD")),
        str(_("Transaction count")),
        str(_("Filtered Commitment USD")),
        str(_("Filtered Disbursement USD")),
        str(_("Filtered Transaction count")),
        str(_("Reporting Organisation")),
        str(_("Financing")),
        str(_('Extending')),
        str(_('Implementing')),
        str(_('Partner Ministry')),
        str(_('State/Region')),
        str(_('Township')),
        str(_("Planned Start date")),
        str(_("Planned End date")),
        str(_("Actual Start date")),
        str(_("Actual End date")),
        str(_("Contact Name")),
        str(_("Contact Phone")),
        str(_("Contact Email")),
        str(_("IATI Identifer")),
        str(_("IATI Linked")),
        str(_("IATI Sync")),
    ]

    for column_index, column in enumerate(columns):
        sheet.write(0, column_index, column)

    current_language = get_language()

    sectors_activities = defaultdict(list)  # type: Dict[str, Any]
    for sector in aims.ActivitySector.objects.select_related('sector').filter(sector__in=aims.IATISector.objects.all())\
            .values('activity_id', 'sector__name', 'percentage'):
        sectors_activities[sector['activity_id']].append(sector)

    national_sectors_activities = defaultdict(list)  # type: Dict[str, Any]
    for sector in aims.ActivitySector.objects.select_related('sector').filter(sector__in=aims.NationalSector.objects.all())\
            .values('activity_id', 'sector__name', 'percentage'):
        national_sectors_activities[sector['activity_id']].append(sector)

    titles_activities = defaultdict(list)  # type: Dict[str, Any]
    for title in aims.Title.objects.values('activity_id', 'title', 'language_id'):
        titles_activities[title['activity_id']].append(title)

    desc_activities = defaultdict(list)  # type: Dict[str, Any]
    for description in aims.Description.objects.values('activity_id', 'description', 'language_id'):
        desc_activities[description['activity_id']].append(description)

    objectives = defaultdict(list)  # type: Dict[str, Any]
    for objective in aims.Description.objects.filter(type_id=2).values('activity_id', 'description', 'language_id'):
        objectives[objective['activity_id']].append(objective)

    organisations = defaultdict(lambda: defaultdict(list))  # type: Dict[Any, Any]
    for organisation in aims.ActivityParticipatingOrganisation.objects.values('activity_id', 'role_id', 'organisation__name', 'name'):
        organisations[organisation['activity_id']][organisation['role_id']].append(organisation)

    location_activities = defaultdict(list)  # type: Dict[str, Any]
    for location in aims.Location.objects.values('activity_id', 'adm_country_adm1', 'adm_country_adm2', 'percentage'):
        location_activities[location['activity_id']].append(location)

    contact_activities = defaultdict(list)  # type: Dict[str, Any]
    for contact in aims.ContactInfo.objects.values('activity_id', 'person_name', 'telephone', 'email'):
        contact_activities[contact['activity_id']].append(contact)

    outcomes_activities = defaultdict(list)  # type: Dict[str, Any]
    for outcome in aims.Result.objects.filter(type__name="Outcome")\
            .prefetch_related('resulttitle__narratives', 'resultdescription__narratives'):
        outcomes_activities[outcome.activity_id].append(
            {
                'activity_id': outcome.activity_id,
                'title': outcome.title,
                'description': outcome.description
            }
        )

    disbursement_transactions = aims.Transaction.objects.filter(transaction_type__code='D')\
                                                        .values('activity_id')\
                                                        .annotate(Sum('usd_value'), Sum('value'))

    total_disbursement_in_dollars = {total['activity_id']: total['usd_value__sum']
                                     for total in disbursement_transactions}

    total_disbursement = {total['activity_id']: total['value__sum']
                          for total in disbursement_transactions}

    activities = activities\
        .annotate(transaction_count=Count('transaction'))\
        .values(
            'pk',
            'iati_identifier',
            'activity_status__name',
            'reporting_organisation_id',
            'reporting_organisation__name',
            'collaboration_type__name',
            'start_planned',
            'end_planned',
            'start_actual',
            'end_actual',
            'commitmenttotal__dollars',
            'commitmenttotal__value',
            'transaction_count',
        )  # type: query.ValuesQuerySet[Any, Dict[str, Any]]

    activities_iati_sectors = {a[0]: a[1] for a in aims.Activity.objects.all().annotate(s=aggregates.sector_subquery()).values_list('id', 's')}
    activities_national_sectors = {a[0]: a[1] for a in aims.Activity.objects.all().annotate(s=aggregates.sector_subquery(national=True)).values_list('id', 's')}
    activities_iati_sync = {}  # type: Dict[str, bool]

    if 'oipa' in settings.INSTALLED_APPS:
        activities_iati_sync = {a[0]: a[1] for a in aims.Activity.objects.all().annotate(s=Func(F('oipaactivitylink__oipa_fields'), 1, function='array_length')).values_list('id', 's')}
    commitments = aims.Transaction.objects.all().filter(transaction_type_id='C', usd_value__isnull=False)
    by_aidtype_activity = aggregates.Aggregates(commitments).aid_type_category_percentage()
    by_financetype = aggregates.Aggregates(commitments).fin_type_category_percentage()
    # aid_type_breakdown_percent = aggregates.with_aidtypecategory(transactions=commitments)
    # finance_type_breakdown_percent = aggregates.with_financetypecategory(transactions=commitments)

    def aid_categories_stringify(activity: Dict[str, str]):
        items = by_aidtype_activity.get(activity['pk'], None)
        if not items:
            return ''
        if len(items) == 1:
            return next(iter(items))
        return '|'.join('{} {}%'.format(name.lower().capitalize(), cat_percent) for name, cat_percent in items.items())

    def finance_type_stringify(activity: Dict[str, str]):
        items = by_financetype.get(activity['pk'], None)
        if not items:
            return ''
        if len(items) == 1:
            return next(iter(items)).lower().capitalize()
        return '|'.join('{} {}%'.format(name.lower().capitalize(), cat_percent) for name, cat_percent in items.items())

    for index, activity in enumerate(activities):
        title = some_title(titles_activities[activity['pk']], current_language)\
            if activity['pk'] in titles_activities else ""
        description = some_description(desc_activities[activity['pk']], current_language) \
            if activity['pk'] in desc_activities else ""
        reporting_org = org_title(activity)

        if activity['pk'] in contact_activities:
            contact = contact_activities[activity['pk']][0]
            contact_name = contact['person_name'] if contact['person_name'] else ""
            contact_phone = contact['telephone'] if contact['telephone'] else ""
            contact_email = contact['email'] if contact['email'] else ""
        else:
            contact_name, contact_phone, contact_email = "", "", ""

        try:
            financing_organisation = some_organisations(organisations[activity['pk']]["Funding"])
        except KeyError:
            financing_organisation = ""

        try:
            extending_organisation = some_organisations(organisations[activity['pk']]["Extending"])
        except KeyError:
            extending_organisation = ""

        try:
            implementing_organisation = some_organisations(organisations[activity['pk']]["Implementing"])
        except KeyError:
            implementing_organisation = ""

        try:
            ministry = some_organisations(organisations[activity['pk']]["Accountable"])
        except KeyError:
            ministry = ""

        if activity['pk'] in outcomes_activities:
            outcomes = outcomes_activities[activity['pk']]
            outcome = " | ".join([outcome['description'] for outcome in outcomes if outcome['description']])
        else:
            outcome = ""

        regions = defaultdict(int)  # type: Dict[str, int]
        townships = defaultdict(int)  # type: Dict[str, int]

        for location in location_activities.get(activity['pk'], []):
            region = location.get('adm_country_adm1')
            subregion = location.get('adm_country_adm2')
            percentage = location.get('percentage', 100) or 100
            if region:
                regions[region] += percentage
            if subregion:
                townships[subregion] += percentage

        state_region = " | ".join(['{0} - {1}%'.format(loc, percentage) for loc, percentage in regions.items()])
        township = " | ".join(['{0} - {1}%'.format(loc, percentage) for loc, percentage in townships.items()])

        if activity['activity_status__name']:
            activity_status_name = activity['activity_status__name']
        else:
            activity_status_name = ""

        disbursement_in_dollars = total_disbursement_in_dollars[activity['pk']]\
            if activity['pk'] in total_disbursement_in_dollars else 0

        disbursement = total_disbursement[activity['pk']] if activity['pk'] in total_disbursement else 0

        objective = activity_objective(objectives, activity['pk'], current_language)

        line = [
            "%s" % activity['pk'],
            "%s" % title,
            "%s" % description,
            "%s" % objective,
            "%s" % activities_iati_sectors[activity['pk']],
            "%s" % activities_national_sectors[activity['pk']],
            "%s" % activity_status_name,
            "%s" % str(activity['collaboration_type__name']) if activity['collaboration_type__name'] else "",
            aid_categories_stringify(activity),
            finance_type_stringify(activity),
            activity['commitmenttotal__value'],
            disbursement,
            activity['commitmenttotal__dollars'],
            disbursement_in_dollars,
            activity['transaction_count'],

            # Filtered transaction fields
            transactions_property(activity['pk'], 'commitment'),
            transactions_property(activity['pk'], 'disbursement'),
            transactions_property(activity['pk'], 'count'),

            "%s" % reporting_org,
            "%s" % financing_organisation,
            "%s" % extending_organisation,
            "%s" % implementing_organisation,
            "%s" % ministry,
            "%s" % state_region,
            "%s" % township,
            "%s" % (activity['start_planned'] or ""),
            "%s" % (activity['end_planned'] or ""),
            "%s" % (activity['start_actual'] or ""),
            "%s" % (activity['end_actual'] or ""),
            "%s" % contact_name,
            "%s" % contact_phone,
            "%s" % contact_email,
            "%s" % (activity['iati_identifier'] or ""),
            "%s" % (bool(activities_iati_sync.get(activity['pk'], False))),
        ]

        for column_number, cell_value in enumerate(line):
            sheet.write(index + 1, column_number, cell_value)

    workbook.save(response)
    # from django.shortcuts import render_to_response as render
    # return render('base.html')
    return response
