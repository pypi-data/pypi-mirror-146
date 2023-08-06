from datetime import date
import re
import warnings

from django.conf import settings
from django.db.models import Count, Sum, Value as V, F, Min, Max, Case, When
from django.utils.safestring import mark_safe

from aims.utils import render
from aims import base_utils, models as aims
import json
from rest_framework.utils.encoders import JSONEncoder  # To render JSON times and decimals

from collections import defaultdict, OrderedDict
from decimal import Decimal

DATE_LIMIT = getattr(settings, 'DATE_LIMIT', date(1900, 1, 1))


def activity_statuses(activity_queryset=None):
    '''
    aid_by: sector
    '''
    if activity_queryset is None:
        activity_queryset = aims.Activity.objects.all()

    activity_statuses = aims.ActivityStatus.objects.filter(activity__in=activity_queryset)\
                                                   .values('name', 'code')\
                                                   .annotate(value=Count('activity'))

    activity_statuses = str(activity_statuses).replace(" u'", " '")

    return activity_statuses


def total_commitments(transaction_queryset=None, activity_sector_queryset=None):
    '''
    aid_by: sector
            donor
            ministry
            location
    '''

    if transaction_queryset is None:
        transaction_queryset = aims.Transaction.objects

    if activity_sector_queryset is not None:
        total_commitment_sector = 0
        for activity_sector in activity_sector_queryset:

            transactions = transaction_queryset.filter(activity=activity_sector.activity,
                                                       transaction_type='C')

            if transactions:
                total_commitments = transactions.aggregate(Sum('usd_value'))['usd_value__sum']
                total_commitment_sector += (float(total_commitments or 0) * float(activity_sector.percentage or 0)) / 100
        total_commitments = total_commitment_sector
    else:
        total_commitments = transaction_queryset.filter(transaction_type="C")\
            .aggregate(Sum('usd_value'))
        total_commitments = total_commitments['usd_value__sum'] or 0.0

    return total_commitments


def total_disbursements(transaction_queryset=None):
    '''
    aid_by: sector
            donor
            ministry
            location
    '''
    if transaction_queryset is None:
        transaction_queryset = aims.Transaction.objects

    total_disbursements = transaction_queryset.filter(transaction_type="D")\
        .aggregate(Sum('usd_value'))
    total_disbursements = total_disbursements['usd_value__sum'] if total_disbursements['usd_value__sum'] else 0

    return total_disbursements


def donor_commitments(transaction_queryset=None, limit=20):
    '''
    aid_by: sector
            donor
            ministry
    '''

    if transaction_queryset is None:
        transaction_queryset = aims.Transaction.objects
    donor_commitments = transaction_queryset.filter(transaction_type='C')\
                                            .values('provider_organisation__abbreviation', 'provider_organisation__name',
                                                    'provider_organisation__code')\
                                            .annotate(Sum('usd_value'))\
                                            .order_by('-usd_value__sum')[:limit]

    donor_commitments = [{'name': donor['provider_organisation__abbreviation'] or donor['provider_organisation__name'] or 'Unidentified',
                          'value': donor['usd_value__sum'],
                          'code': donor['provider_organisation__code'] or base_utils.UNKNOWN_DONOR_CODE,
                          'pretty': base_utils.prettify_compact(donor['usd_value__sum'])}
                         for donor in donor_commitments]

    donor_commitments = str(donor_commitments).replace(" u'", " '")

    return donor_commitments


def percent_disbursed(total_commitments, total_disbursements):
    '''
    aid_by: sector
            donor
            location
    '''

    if total_commitments is None:
        total_commitments = 0

    if total_disbursements is None:
        total_disbursements = 0

    if total_commitments > 0:
        percent_disbursed = (100 * (total_disbursements / total_commitments)) if total_disbursements else 0
    else:
        percent_disbursed = 100 if total_disbursements > 0 else 0

    return percent_disbursed


def activities_by_ministry(activity_queryset=None, limit=3):
    '''
    aid_by: sector
            donor
            ministry
            location
    '''
    if activity_queryset is None:
        activity_queryset = aims.Activity.objects.all()
    activities_by_ministry = aims.ActivityParticipatingOrganisation.objects.filter(
        activity__in=activity_queryset, role='Accountable', organisation__type__name='National Ministry')\
        .exclude(organisation=None)\
        .values('organisation__name', 'organisation__code')\
        .annotate(value=Count('activity'), dollars=Sum('activity__transaction__usd_value'))\
        .order_by('-value')

    top_three = activities_by_ministry[:limit] if limit is not None else activities_by_ministry

    activities_by_ministry = [{'code': ministry['organisation__code'],
                               'name': re.sub("ministry of", "", ministry['organisation__name'], flags=re.IGNORECASE).strip(),
                               'value': ministry['value'],
                               'pretty': ministry['value']}
                              for code, ministry in enumerate(top_three)]

    # activities_by_ministry.append(the_rest)
    activities_by_ministry = str(activities_by_ministry).replace(" u'", " '")
    activities_by_ministry = str(activities_by_ministry).replace(" u\"", " \"")

    return activities_by_ministry


def commitment_by_category(activities, transactions, limit=3, json=True):
    '''
    aid_by: sector
            donor

    We get the total commitment
    Then we get the total number of activities
    We get the Sum of all the percentages by category
        divide that sum by the total number of activities and call it category_percent

    for each of the categories we multiply the total commitment by the category_percent
    '''

    # limit sectors examined to DAC-3 and DAC-5
    vocabularies = ['DAC-3', 'DAC-5']

    # Group transactions by activity DAC-3 sector and activity status
    transactions_by_sector = tuple(
        transactions.filter(transaction_type='C').values_list(
            'activity__activitysector__vocabulary',
            'activity__activitysector__sector__category__name',
            'activity__activitysector__sector__category__code',
            'activity__activitysector__percentage',
            'usd_value'
        )
    )

    # Handle transactions attached to activities without a DAC-3 sector breakdown
    unspecified_value = transactions.exclude(
        activity__activitysector__vocabulary__in=vocabularies
    ).filter(
        transaction_type='C'
    ).aggregate(
        Sum('usd_value')
    )['usd_value__sum']
    if unspecified_value is not None:
        transactions_by_sector += (('DAC-3', 'Not Specified', -1, 100.0, unspecified_value),)

    # Filter out vocabularies other than DAC-3 and adjust value by percentage
    transactions_by_sector = [t for t in transactions_by_sector if t[0] in vocabularies and t[1] is not None]
    transactions_by_sector = [(t[1], t[2], float(t[3] or 0) / 100 * float(t[4] or 0)) for t in transactions_by_sector]

    commitment_by_category = []
    for sector, code in set([(t[0], t[1]) for t in transactions_by_sector]):
        transactions_for_sector = [t for t in transactions_by_sector if t[0] == sector]
        value = sum([t[2] for t in transactions_for_sector])
        commitment_dict = {'name': sector,
                           'value': value,
                           'pretty': base_utils.prettify_compact(value),
                           'code': int(code)}

        commitment_by_category.append(commitment_dict)

    commitment_by_category = sorted(commitment_by_category, key=lambda item: item['value'], reverse=True)

    if json:
        commitment_by_category = sorted(commitment_by_category, key=lambda category: category['value'], reverse=True)[:limit]
        commitment_by_category = str(commitment_by_category).replace(" u'", " '").replace(' u"', ' "')

    return commitment_by_category


def commitments_by_state(activity_queryset, states_queryset):
    '''
    aid_by: state
    '''
    states = states_queryset.values('name', 'adm1_code')
    states_dict = {state['name'].lower(): state['adm1_code'] for state in states}
    commitments_by_location = {state['adm1_code']: 0 for state in states}

    locations = aims.TransactionValueLocation.objects.filter(activity__in=activity_queryset,
                                                             transaction__transaction_type='C')\
                                                     .exclude(location__adm_country_adm1__contains="Nation-wide")\
                                                     .exclude(location__adm_country_adm1='')\
                                                     .values('location__adm_country_adm1')\
                                                     .annotate(dollars=Sum('dollars'))

    for location in locations:
        state = location['location__adm_country_adm1'].lower()
        try:
            commitments_by_location[states_dict[state]] = base_utils.prettify_compact(location['dollars'])
        except KeyError:
            state = location['location__adm_country_adm1'].lower().split(' ')[0]
            commitments_by_location[states_dict[state]] = base_utils.prettify_compact(location['dollars'])
        commitments_by_location[states_dict[state] + '_natural'] = location['dollars']

    commitments_by_location = str(commitments_by_location).replace("u'", "'")

    return commitments_by_location


def commitments_percentage_by_state(activity, json=True):

    locations = aims.TransactionValueLocation.objects.filter(activity=activity)\
                                                     .filter(transaction__transaction_type='C')\
                                                     .exclude(location__adm_country_adm1='')\
                                                     .exclude(location__adm_country_adm1__contains="Nation-wide")\
                                                     .values('location__adm_country_adm1', 'location__adm_country_adm2', 'location__percentage')\
                                                     .annotate(dollars=Sum('dollars'))

    commitment_by_states = []
    for location in locations:
        commitment_by_states.append({
            'name': location['location__adm_country_adm2'] if location['location__adm_country_adm2'] else location['location__adm_country_adm1'],
            'percentage': location['location__percentage'],
            'total': base_utils.prettify_compact(location['dollars'])
        })

    if json:
        commitment_by_states = str(commitment_by_states).replace("u'", "'")

    return commitment_by_states


def commitments_by_township(activity_queryset, township_queryset):
    '''
    aid_by: township
    '''
    townships = township_queryset.values('name', 'code')
    township_dict = {township['name'].lower(): township['code'] for township in townships}
    commitments_by_township = {township['code']: 0 for township in townships}

    commitments_by_township_natural = {}
    for township in commitments_by_township:
        commitments_by_township_natural[township] = commitments_by_township[township]
        commitments_by_township_natural[township + '_natural'] = 0

    commitments_by_township = commitments_by_township_natural

    locations = aims.TransactionValueLocation.objects.filter(activity__in=activity_queryset).filter(activity__activity_status__code=2, transaction__transaction_type='C').exclude(location__adm_country_adm1__contains="Nation-wide").exclude(location__adm_country_adm2=None).values('pk', 'location__adm_country_adm2').annotate(dollars=Sum('dollars'))
    for location in locations:
        try:
            commitments_by_township[township_dict[location['location__adm_country_adm2'].lower()]] = base_utils.prettify_compact(location['dollars'])
            commitments_by_township[township_dict[location['location__adm_country_adm2'].lower()] + '_natural'] = location['dollars']
        except KeyError:
            pass

    commitments_by_township = str(commitments_by_township).replace("u'", "'")

    return commitments_by_township


def total_donors(activity_queryset):
    '''
    aid_by: donor
    '''

    total_donors = aims.Organisation.objects.filter(activityparticipatingorganisation__role="Funding")\
                                            .filter(activity__in=activity_queryset).values().distinct().count()
    return total_donors


def total_donors_by_type(activity_queryset=None):
    '''
    aid_by: donor
    '''
    if activity_queryset is None:
        activity_queryset = aims.Activity.objects.all()

    total_donors_by_type = aims.OrganisationType.objects.filter(
        organisation__activityparticipatingorganisation__activity__in=activity_queryset,
        organisation__activityparticipatingorganisation__role="Funding"
    ).values(
        'code', 'name'
    ).annotate(
        value=Count('organisation')
    )

    total_donors_by_type = str(total_donors_by_type).replace(" u'", " '")

    return total_donors_by_type


def commitment_by_status(activity_queryset=None):
    '''
    aid_by: location (duplicate)
    '''
    if activity_queryset is None:
        activity_queryset = aims.Activity.objects.all()

    commitment_by_status = aims.ActivityStatus.objects.filter(
        activity__in=activity_queryset,
        activity__transaction__transaction_type="C"
    ).values(
        'name', 'code'
    ).annotate(
        value=Sum('activity__transaction__usd_value')
    )

    commitment_by_status = [{
        'code': status['code'],
        'name': status['name'],
        'value': status['value'] or 0,
        'pretty': base_utils.prettify_compact(status['value'] or 0)}
        for status in commitment_by_status]

    commitment_by_status = str(commitment_by_status).replace(" u'", " '")

    return commitment_by_status


def loans_vs_grants(transaction_queryset=None):
    '''
    aid_by: donor
    '''
    if transaction_queryset is None:
        transaction_queryset = aims.Transaction.objects

    commitments = transaction_queryset.filter(transaction_type="C")
    loans = commitments.filter(finance_type__category=400).aggregate(Sum('usd_value'))
    grants = commitments.filter(finance_type__category=100).aggregate(Sum('usd_value'))
    other = commitments.exclude(finance_type__category__in=[100, 400]).aggregate(Sum('usd_value'))

    values = {
        'loans': loans.get('usd_value__sum') or 0,
        'grants': grants.get('usd_value__sum') or 0,
        'other': other.get('usd_value__sum') or 0
    }

    loans_vs_grants_array = [
        {'name': "Loans", 'code': 6, 'value': values['loans'], 'pretty': '$ {}'.format(base_utils.prettify_compact(values['loans']))},
        {'name': "Grants", 'code': 3, 'value': values['grants'], 'pretty': '$ {}'.format(base_utils.prettify_compact(values['grants']))},
        {'name': "Other", 'code': 7, 'value': values['other'], 'pretty': '$ {}'.format(base_utils.prettify_compact(values['other']))}
    ]

    return loans_vs_grants_array


def activity_statuses_total(activity_queryset=None, organisation=None):

    if activity_queryset is None:
        activity_queryset = aims.Activity.objects.all()

    activities = {status.code: {
        'name': status.name,
        'code': status.name.lower().replace('', ''),
        'value': 0,
        'activities': 0,
        'pretty': base_utils.prettify_compact(0)}
        for status in aims.ActivityStatus.objects.all()}

    activity_statuses = aims.ActivityStatus.objects.filter(
        activity__in=activity_queryset,
        activity__transaction__transaction_type="C",
        activity__transaction__provider_organisation=organisation,
        activity__start_actual__gte=DATE_LIMIT
    ).values(
        'name', 'code'
    ).annotate(
        value=Count('activity'),
        total=Sum('activity__transaction__usd_value')
    )

    for status in activity_statuses:
        try:
            code = status['code']
            activities[code]['value'] = float(status['total']) or 0
            activities[code]['activities'] = status['value']
            activities[code]['pretty'] = base_utils.prettify_compact(status['total'] or 0)
        except Exception as E:
            warnings.warn(F'Unhandled legacy exception: {E}')
            pass

    activities = list(activities.values())

    return activities


def percentage_by_status(activity_queryset=None, organisation=False, json=True):

    if activity_queryset is None:
        activity_queryset = aims.Activity.objects.all()

    activity_statuses = activity_statuses_total(activity_queryset, organisation)

    total = 0
    for status in activity_statuses:
        total += status['value']

    for status in activity_statuses:
        status['value'] = ((status['value'] * 100) / total) if total > 0 else 0
        status['pretty'] = '%s - %.2f%%' % (status['pretty'], status['value'])

    if json:
        activity_statuses = str(activity_statuses).replace(" u'", " '")

    return activity_statuses


def transactions_by_year(activity_queryset=None, organisation=None, activity_statuses=[2, ], json=True):

    if not activity_queryset:
        activity_queryset = aims.Activity.objects.all()

    transactions_queryset = aims.Transaction.objects.filter(
        provider_organisation=organisation,
        transaction_date__gte=DATE_LIMIT,
        activity__openly_status='published'
    ).order_by('transaction_date')

    transactions_year = []
    for transaction in transactions_queryset:
        if transaction.transaction_date and transaction.transaction_date.year not in transactions_year:
            transactions_year.append(transaction.transaction_date.year)

    transactions_by_year = []

    types_totals = {
        'C': 0,
        'D': 0,
        'E': 0,
        'O': 0
    }

    label_types = {
        'C': 'Commitments',
        'D': 'Disbursements',
        'E': 'Expenditures',
        'O': 'Others',
    }

    for transaction_year in transactions_year:

        totals_transactions = transactions_queryset.filter(transaction_date__year=transaction_year)\
            .values('transaction_type_id').annotate(total=Sum('usd_value'))

        current_year_totals = types_totals.copy()
        for totals in totals_transactions:
            if totals['transaction_type_id'] in current_year_totals:
                current_year_totals[totals['transaction_type_id']] += (totals['total'] or 0)
            else:
                current_year_totals['O'] += (totals['total'] or 0)

        for key, value in list(current_year_totals.items()):
            label = label_types[key]
            current_year_totals[label] = value
            del current_year_totals[key]
            current_year_totals[label + '_Pretty'] = base_utils.prettify_compact(value)

        current_year_totals['year'] = transaction_year

        transactions_by_year.append(current_year_totals)

    if json:
        transactions_by_year = str(transactions_by_year).replace(" u'", " '")

    return transactions_by_year


def commitment_disbursement_by_month_year(activity_queryset=None, as_json=True):

    if not activity_queryset:
        activity_queryset = aims.Activity.objects.all()

    transactions_queryset = aims.Transaction.objects.filter(
        activity__in=activity_queryset,
        transaction_type__in=["C", "D"],
        transaction_date__gte=DATE_LIMIT,
        activity__openly_status='published',
    ).order_by('transaction_date')

    first_date = None
    last_date = None
    if transactions_queryset:
        first_date = transactions_queryset.first().transaction_date
        last_date = transactions_queryset.last().transaction_date

    last_commitment = 0
    last_disbursement = 0
    transactions_by_month_year = []

    if first_date and last_date:

        first_date = date(first_date.year, first_date.month, 1)
        last_date = date(last_date.year, last_date.month, 1)

        while first_date <= last_date:
            total_commitments = transactions_queryset.filter(transaction_date__year=first_date.year, transaction_date__month=first_date.month,
                                                             transaction_type_id='C')\
                                                     .aggregate(total=Sum('usd_value'))

            total_disbursements = transactions_queryset.filter(transaction_date__year=first_date.year, transaction_date__month=first_date.month,
                                                               transaction_type_id='D')\
                                                       .aggregate(total=Sum('usd_value'))

            if total_commitments['total'] or total_disbursements['total']:

                last_commitment += (total_commitments['total'] or 0)
                last_disbursement += (total_disbursements['total'] or 0)

                transactions_by_month_year.append(
                    {
                        'month_year': first_date.strftime('%m/%Y'),
                        'Commitments': last_commitment or 0,
                        'Commitments_Pretty': base_utils.prettify_compact(last_commitment or 0),
                        'Disbursements': last_disbursement or 0,
                        'Disbursements_Pretty': base_utils.prettify_compact(last_disbursement or 0)
                    }
                )

            first_date = base_utils.add_months(first_date, 1)

    if as_json:
        transactions_by_month_year = render(transactions_by_month_year)

    return transactions_by_month_year


def transactions_by_month_year(activity_queryset=None) -> str:
    '''
    Returns a JSON structure of transactions, accumulating by month
    and divided into C, D, E and Other transaction types
    TODO: We're looping over "transaction date" here which ought to be trunc_month() instead (django 1.11+)
    '''
    transactions_queryset = aims.Transaction.objects.filter(
        activity__in=(activity_queryset or aims.Activity.objects.all()),
        transaction_date__gte=DATE_LIMIT,
        activity__openly_status='published',
    )

    sum_by_date = OrderedDict()
    default_return = render([])

    if not transactions_queryset:
        return default_return

    dates = transactions_queryset.aggregate(
        first=Min('transaction_date'), last=Max('transaction_date')
    )
    first_date, last_date = dates['first'], dates['last']

    if not first_date:
        return default_return

    # 'Main' types will get their own line/pie slice
    transaction_types = {'Commitments': 'C', 'Disbursements': 'D', 'Expenditures': 'E'}
    transactions = transactions_queryset.annotate(
        transaction_type_group=Case(
            When(transaction_type__in=transaction_types.values(), then=F('transaction_type')),
            default=V('Other')
        )
    ).annotate(Sum('usd_value'))

    # Add annotated 'Other' values - the dict value here should match the V('...') above
    transaction_types['Others'] = 'Other'

    # Collect cumulative amounts by time bucket and group
    cumulative_amounts = {}  # Container for cumulative amounts keyed by transacton year, month, and group
    cumulative_amounts_by_time = []  # Container of flags to see if a certain month has any value
    group_amount = defaultdict(Decimal)  # Temporary container for cumulative amount keyed by group

    for group, value, transaction_date in transactions.order_by('transaction_date').values_list('transaction_type_group', 'usd_value__sum', 'transaction_date'):
        if not value:
            continue
        date_key = transaction_date.strftime('%m/%Y')
        key = '%s-%s' % (date_key, group)
        group_amount[group] += value
        cumulative_amounts[key] = group_amount[group]
        cumulative_amounts_by_time.append(date_key)
    cumulative_amounts_by_time = set(cumulative_amounts_by_time)

    # Reset 'group_amount' for running through the structure above again
    group_amount = defaultdict(int)

    this_date = date(first_date.year, first_date.month, 1)
    while this_date <= last_date:
        date_key = this_date.strftime('%m/%Y')
        this_date = base_utils.add_months(this_date, 1)
        if date_key not in cumulative_amounts_by_time:
            # We do not want a structure full of zero's.
            continue

        sum_by_date[date_key] = {'month_year': date_key}
        for tr_type, tr_type_code in transaction_types.items():
            type_key = '%s-%s' % (date_key, tr_type_code)
            if type_key in cumulative_amounts:
                # Update the cumulative amount if we reach a month with a transaction
                group_amount[tr_type_code] = cumulative_amounts[type_key]
            value = group_amount[tr_type_code]
            pretty = base_utils.prettify_compact(group_amount[tr_type_code])

            sum_by_date[date_key][tr_type] = value
            sum_by_date[date_key][tr_type + '_Pretty'] = pretty

    return mark_safe(json.dumps(sum_by_date.values(), cls=JSONEncoder))
