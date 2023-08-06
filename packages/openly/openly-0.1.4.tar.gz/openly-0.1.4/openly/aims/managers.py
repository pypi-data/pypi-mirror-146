from django.apps import apps
from django.conf import settings
from django.db import models
from django.db import connection
from django.db.transaction import atomic
from django.db.models import OuterRef, Subquery, ExpressionWrapper, Case, When, Func
from datetime import date, timedelta
from .openly_roles import OPENLY_SECTOR_TYPE_IATI, OPENLY_SECTOR_TYPE_NATIONAL
from .utils import clean_percentages, AdvisoryLock
from django.db.models.expressions import RawSQL
from django.db.models import Q, F
from simple_locations.models import Area
from typing import List, Tuple
from .annotations import replace_future_dates, future_dates
from dataquality.aggregates import SumOverPartition  # Django 2.0 has a lot of this built-in
from django.db import transaction

import datetime
import logging
logger = logging.getLogger(__name__)


class RoundedDecimal(Func):
    """
    Rounds numbers to a 15.2 decimal
    """
    template = '(%(expressions)s)::Decimal (15,2) '
    output_field = models.DecimalField(max_digits=15, decimal_places=2)


class PercentageCleanerManager(models.Manager):
    ''' Manager base class for models containing a percentage field that should sum
    to 100 across some subset of the models.

    Subclasses should set the group_by_fields as a list of the string names of the fields
    across which models should be grouped such that their percentage field sums to 100 and
    percentage_field to to the string name of the field containing the percentage if
    different from 'percentage'
    '''
    group_by_fields = []
    percentage_field = 'percentage'
    precision = 2

    def clean_all_percentages(self):
        ''' Partition models by the group_by_field and then clean the percentages attached to
        each model in this partition
        '''
        for grouped_fields in self.values_list(*self.group_by_fields):
            self.clean_grouped_percentages(
                self.filter(
                    # Create a dict {field name: field_value} for field names in group_by_fields
                    # and values in the current group and then pass to filter as kwargs
                    **dict(zip(self.group_by_fields, grouped_fields))
                ).values_list(
                    'id', self.percentage_field
                )
            )

    def clean_grouped_percentages(self, model_percentages):
        ''' Expects a list of (model id, percentage) pairs and then cleans the associated
        models so that the sum of their percentage fields is 100

        '''
        model_ids, percentages = zip(*model_percentages)
        new_percentages = clean_percentages(
            [float(p) if p is not None else p for p in percentages], precision=self.precision
        )
        for model_id, percentage in zip(model_ids, new_percentages):
            model = self.get(pk=model_id)
            setattr(model, self.percentage_field, percentage)
            model.save()


class ActivitySectorManager(PercentageCleanerManager):
    group_by_fields = ['activity', 'vocabulary']


class LocationManager(PercentageCleanerManager):
    group_by_fields = ['activity']

    def sync_simple(self):
        '''
        Match up, wherever possible, SimpleLocation instances to adm_code
        This is a "bridge" between Mohinga-style "location.adm_code" and new-style "SimpleLocations"
        which should provide consistency between our instances until the day comes when we can drop
        "old-style" locations

        Call me with
        >>> Location.objects.sync_simple()
        I should be very cheap and recursion-safe so feel free to use me in a signal
        '''
        if getattr(settings, 'USE_SIMPLE_LOCATIONS', False):
            logger.warning('This is only supposed to be run on OLD style locations')
            return

        # The 'adm_code' is set on saving an old style location
        # This should ensure that Locations always have a relevant SimpleLocation.Area object attached
        # Set up a SubQuery object which will join Location to Area
        sq = Area.objects.filter(code=OuterRef('adm_code')).values('pk')
        locations = self.get_queryset().annotate(new_area_id=Subquery(sq))

        # Nullify area where its code does not match the adm code
        self.get_queryset().exclude(area__code=F('adm_code')).exclude(area=None).update(area=None)
        # Do not update where it's already the same
        locations_to_update = locations.exclude(area_id=F('new_area_id'))
        # Assign the "new_area_id" as area_id to the Location object
        locations_to_update.update(area_id=F('new_area_id'))
        return


class ActivityManager(models.Manager):
    """ Financial calculations for activity """

    def commitments_only(self,):
        activities = self.get_queryset()
        return activities.filter(transaction__transaction_type_id='C')

    def annotate_dollars_category(self,):

        activities = self.commitments_only().annotate(
            dollars_category=SumOverPartition(F('transaction__usd_value'), F('id'), F('transaction__aid_type__category')),
            dollars_activity=SumOverPartition(F('transaction__usd_value'), F('id'))
        ).distinct(
            'transaction__aid_type__category', 'id'
        )
        return activities

    def annotate_percent_category(self,):
        activities = self.annotate_dollars_category().annotate(
            percent=Case(
                When(dollars_activity=0, then=0),
                default=F('dollars_category') / F('dollars_activity') * 100
            )
        )
        return activities

    def annotate_financetype_category(self,):

        activities = self.commitments_only().annotate(
            dollars_category=SumOverPartition(F('transaction__usd_value'), F('id'), F('transaction__finance_type__name')),
            dollars_activity=SumOverPartition(F('transaction__usd_value'), F('id'))
        ).distinct(
            'transaction__finance_type__category', 'id'
        )
        return activities

    def annotate_financetype_category_percent(self,):
        activities = self.annotate_financetype_category().annotate(
            percent=Case(
                When(dollars_activity=0, then=0),
                default=F('dollars_category') / F('dollars_activity') * 100
            )
        )
        return activities


class NationalSectorCategoryManager(models.Manager):
    """ Manager for all sectors which are local """

    def get_queryset(self,):
        return super(NationalSectorCategoryManager, self).get_queryset().filter(openly_type=OPENLY_SECTOR_TYPE_NATIONAL)


class IATISectorCategoryManager(models.Manager):
    """ Manager for all sectors which are local """

    def get_queryset(self,):
        return super(IATISectorCategoryManager, self).get_queryset().filter(openly_type=OPENLY_SECTOR_TYPE_IATI)


class NationalSectorManager(models.Manager):
    """ Manager for all sectors which are local """

    def get_queryset(self,):
        return super(NationalSectorManager, self).get_queryset().filter(category__openly_type=OPENLY_SECTOR_TYPE_NATIONAL)


class GovernmentOrganisationManager(models.Manager):
    ''' Manager encapsulating the logic distinguishing partner organisations. '''

    def get_queryset(self):
        # Government organisations are defined by their linked OrganisationType code
        return super(GovernmentOrganisationManager, self).get_queryset().exclude(name='').filter(type__code=10)


class LocalMinistryManager(models.Manager):
    ''' Manager encapsulating the logic distinguishing local ministries. '''

    def get_queryset(self):
        # Local Ministry organisations are defined by their linked OrganisationType code
        return super(LocalMinistryManager, self).get_queryset().exclude(name='').filter(type__code=100)


class PartnerOrganisationManager(models.Manager):
    ''' Manager encapsulating the logic distinguishing partner organisations. '''

    def get_queryset(self):
        # Partner organisations are featured around openly based sites, e.g. on the partner's
        # page and in search results. Generally an NGO is a partner if they have a user
        # attached, but additionally hide organisations with a non-existent or empty profile
        if getattr(settings, 'PARTNER_DEFINITION_FILTER', False):
            return super().get_queryset().filter(**getattr(settings, 'PARTNER_DEFINITION_FILTER')).distinct()
        if getattr(settings, 'PARTNER_DEFINITION_REPORTING_USERS', False):
            return super(PartnerOrganisationManager, self).get_queryset().filter(users__isnull=False, type__isnull=False, activity_reporting_organisation__isnull=False).exclude(profile__logo__exact='').distinct()
        else:
            return super(PartnerOrganisationManager, self).get_queryset().filter(users__isnull=False, type__isnull=False, profile__isnull=False).exclude(type__code=10).exclude(profile__logo__exact='').distinct()


class IATISectorManager(models.Manager):
    """ Manager for all sectors which are IATI """

    def get_queryset(self,):
        return super(IATISectorManager, self).get_queryset().filter(category__openly_type=OPENLY_SECTOR_TYPE_IATI)


class IATIDAC3SectorManager(IATISectorManager):
    """ Manager for all sectors which are from the DAC-5 set"""

    def get_queryset(self,):
        return super().get_queryset().filter(category__openly_type=OPENLY_SECTOR_TYPE_IATI, pk__lt=1000, pk__gt=1)


class IATIDAC5SectorManager(IATISectorManager):
    """ Manager for all sectors which are from the DAC-3 set """

    def get_queryset(self,):
        return super().get_queryset().filter(category__openly_type=OPENLY_SECTOR_TYPE_IATI, pk__gte=1000)


class USDValueFieldManager(models.Manager):
    # For Transactions and Budgets, add an "objects.update_usd_value" function

    def update_usd_value(self, **kwargs):
        """
        Update all of the usd_value fields in the budget or transaction table
        """
        objects = self.get_queryset()
        if 'filter' in kwargs:
            objects = objects.filter(**kwargs.get('filter'))
        # No need for a conversion if we are using the site currency
        objects.filter(currency_id='USD').exclude(usd_value=F('value')).update(usd_value=F('value'))

        # Django has a reference issue trying to use 'update' with the 'rate' field calculated here
        # hence the use of a Subquery
        subquery = objects.exclude(
            currency_id='USD'
        ).annotate(
            rate=F('{}exchangerate__exchangerate__rate'.format(self.model._meta.model_name)),
        ).annotate(
            dollars=ExpressionWrapper(F('rate') * F('value'), output_field=models.DecimalField(max_digits=15, decimal_places=2)),
        )

        no_rate_match = subquery.filter(rate__isnull=True, usd_value__isnull=False)
        logger.debug('%s missing rate matches', no_rate_match.count())

        with transaction.atomic():
            no_rate_match.update(usd_value=None)

        # The OuterRef here ensures that the correct reference is maintained
        subquery_dollars = subquery.filter(id=OuterRef('id')).values('dollars')
        objects = objects.annotate(dollars=Subquery(subquery_dollars, output_field=models.DecimalField(max_digits=15, decimal_places=2)))

        # Prevent updates where the difference is less than one cent, due to rounding differences
        # Prevent updates where the value is already null
        objects = objects.exclude(usd_value=RoundedDecimal('dollars'))
        objects = objects.exclude(dollars__isnull=True, usd_value__isnull=True)
        logger.debug('Updating %s transactions', objects.count())
        with transaction.atomic():
            objects.update(usd_value=F('dollars'))

    def effective_values_dates(self):
        objects = self.future.annotate(effective_value_date=replace_future_dates())
        return objects

    @property
    def future(self):
        return self.get_queryset().filter(future_dates())


class TransactionManager(USDValueFieldManager):
    '''
    Add an annotation for the effective date
    '''
    pass


class BudgetExchangeRateManager(models.Manager):

    def drop_invalid_matches(self):
        from aims.models import Budget
        # Delete from the database exchange rates where the budget date
        # no longer matches the exchange rate date or the budget currency
        # no longer matches the exchange rate currency
        mismatches = self.exclude(
            budget__value_date=F('exchangerate__date'),
            budget__currency=F('exchangerate__base_currency')
        )
        with AdvisoryLock('budget'):
            Budget.objects.filter(
                budgetexchangerate__in=mismatches
            ).update(usd_value=None)
            mismatches.delete()

    @atomic
    def match_currency_rates(self):
        """
        Rebuild the aims_budgetexchangerate table
        """

        self.drop_invalid_matches()
        with connection.cursor() as cur:
            cur.execute(
                '''
                INSERT INTO aims_budgetexchangerate (budget_id, exchangerate_id)
                SELECT budget.id AS budget_id, exchangerate.id AS exchangerate_id FROM
                    aims_budget budget,
                    aims_currency_exchange_rate exchangerate
                WHERE
                    budget.value_date =  exchangerate.date AND
                    exchangerate.base_currency_id = budget.currency_id AND
                    exchangerate.currency_id = 'USD' AND
                    budget.id NOT IN (SELECT budget_id FROM aims_budgetexchangerate)
                RETURNING budget_id;
                '''
            )
        return self

    def missing_currency_rates(self) -> List[Tuple[int, date, str]]:
        """
        Return the distinct date / currency pairs which are missing a conversion to USD
        """
        return [(b.budget_id, b.value_date, b.currency_id) for b in self.get_queryset().raw(
            '''
            SELECT DISTINCT ON(b.value_date, b.currency_id) b.id AS budget_id, value_date, b.currency_id FROM aims_budget b
            LEFT OUTER JOIN aims_currency_exchange_rate r
                ON b.value_date = r.date
                AND b.currency_id = r.base_currency_id
                AND r.currency_id = 'USD'
                WHERE b.currency_id != 'USD'
                AND r.rate IS NULL
                AND value_date IS NOT NULL
                AND value_date < now() - interval '30 days'
            '''
        )]

    def future_currency_rates(self) -> List[Tuple[int, datetime.date, str]]:
        '''
        Find 'future' transactions, and use the "sensible default" date as a currency exchange rate
        '''
        # 'from aims.models import Budget' would cause a circular import here
        model = apps.get_model('aims', 'Budget')
        rates = model.objects.effective_values_dates()
        # Exclude 'I already have an exchange rate'
        rates = rates.exclude(budgetexchangerate__exchangerate__date=F('effective_value_date'))
        # Exclude 'I'll never be valid'
        rates = rates.exclude(currency_id__isnull=True)
        # Now we should only have dates in the future, mogrified to be last Monday
        values = rates.values_list('pk', 'effective_value_date', 'currency_id')
        return list(values)

    def missing_and_future(self) -> List[Tuple[int, datetime.date, str]]:
        missing = self.missing_currency_rates()
        missing.extend(self.future_currency_rates())
        return missing

    def fetch_currency_rates(self, limit: int = 1):

        from aims.models import CurrencyExchangeRate

        self.drop_invalid_matches()
        # Run the CurrencyExchangeRate manager 'fetch' command
        # where there are currency/date matches missing from the database
        # and create the relevant CurrencyExchangeRate objects
        for budget_id, d, currency in self.missing_and_future()[:limit]:
            try:
                logger.debug('Creating BudgetExchangeRate %s for %s', currency, d)
                self.create(
                    budget_id=budget_id,
                    exchangerate=CurrencyExchangeRate.objects.fetch(d, currency).first()
                )
            except Exception as e:
                logger.error('%s' % e)
                continue
        return self


class TransactionExchangeRateManager(models.Manager):
    '''
    Manager to assist in settin exchange rates for transactions

    >>> TransactionExchangeRate.objects.drop_invalid_matches()
    aims.managers:DEBUG Set transaction usd_value to None; dropping TransactionExchangeRate for 0 invalid matches
    >>> TransactionExchangeRate.objects.match_currency_rates()  # Periodic task to 're-link' Transaction and CurrencyExchangeRate

    '''

    def drop_invalid_matches(self):
        from aims.models import Transaction
        # Delete from the database exchange rates where the transaction date
        # no longer matches the exchange rate date or the transaction currency
        # no longer matches the exchange rate currency
        mismatches = self.annotate(
            value_date=replace_future_dates(
                field_name='transaction__value_date'
            )
        ).exclude(
            value_date=F('exchangerate__date'),
            transaction__currency=F('exchangerate__base_currency')
        )
        logger.debug('Set transaction usd_value to None; dropping TransactionExchangeRate for %s invalid matches', mismatches.count())
        Transaction.objects.filter(transactionexchangerate__in=mismatches).update(usd_value=None)
        Transaction.objects.filter(transactionexchangerate__in=mismatches).filter(transactionexchangerate=None)

        mismatches.delete()

    @atomic
    def match_currency_rates(self, future=True):
        """
        Truncate and rebuild the aims_transactionexchangerate table
        """
        self.drop_invalid_matches()
        with connection.cursor() as cur:
            cur.execute(
                '''
                INSERT INTO aims_transactionexchangerate (transaction_id, exchangerate_id)
                SELECT transaction.id AS transaction_id, exchangerate.id AS exchangerate_id FROM
                    aims_transaction transaction,
                    aims_currency_exchange_rate exchangerate
                WHERE
                    transaction.value_date =  exchangerate.date AND
                    exchangerate.base_currency_id = transaction.currency_id AND
                    exchangerate.currency_id = 'USD' AND
                    transaction.id NOT IN (SELECT transaction_id FROM aims_transactionexchangerate)
                RETURNING transaction_id;
                '''
            )
        logger.debug('%s ExchangeRates', self.get_queryset().count())
        return self

    def missing_currency_rates(self) -> List[Tuple[int, datetime.date, str]]:
        """
        Return the distinct date / currency pairs which are missing a conversion to USD
        """
        missing_rates = [(b.transaction_id, b.value_date, b.currency_id) for b in self.get_queryset().raw(
            '''
            SELECT DISTINCT ON(b.value_date, b.currency_id) b.id AS transaction_id, value_date, b.currency_id FROM aims_transaction b
            LEFT OUTER JOIN aims_currency_exchange_rate r
                ON b.value_date = r.date
                AND b.currency_id = r.base_currency_id
                AND r.currency_id = 'USD'
                WHERE b.currency_id != 'USD'
                AND r.rate IS NULL
                AND value_date IS NOT NULL
                AND value_date < now() - interval '1 day'
            '''
        )]
        logger.debug('Missing currency rates: %s', len(missing_rates))
        return missing_rates

    def future_currency_rates(self) -> List[Tuple[int, datetime.date, str]]:
        '''
        Find 'future' transactions, and use the "sensible default" date as a currency exchange rate
        '''
        # 'from aims.models import Transaction' would cause a circular import here
        Transaction = apps.get_model('aims', 'Transaction')
        rates = Transaction.objects.effective_values_dates()
        # Exclude 'I already have an exchange rate'
        rates = rates.exclude(transactionexchangerate__exchangerate__date=F('effective_value_date'))
        # Exclude 'I'll never be valid'
        rates = rates.exclude(currency_id__isnull=True)
        # Now we should only have dates in the future, mogrified to be last Monday
        values = rates.values_list('pk', 'effective_value_date', 'currency_id')
        return list(values)

    def missing_and_future(self) -> List[Tuple[int, datetime.date, str]]:
        missing = self.missing_currency_rates()
        missing.extend(self.future_currency_rates())
        return missing

    def fetch_currency_rates(self, limit: int = 1, dry_run: bool = False):

        CurrencyExchangeRate = apps.get_model('aims', 'CurrencyExchangeRate')

        # Delete from the database exchange rates where the transaction date
        # no longer matches the exchange rate date or the transaction currency
        # no longer matches the exchange rate currency
        self.drop_invalid_matches()

        # Run the CurrencyExchangeRate manager 'fetch' command
        # where there are currency/date matches missing from the database
        # and create the relevant CurrencyExchangeRate objects

        for transaction_id, d, currency in self.missing_and_future():
            if dry_run:
                logger.debug('Fetch currency rates: date %s, currency %s, transaction %s', d, currency, transaction_id)
                continue
            exchangerate = CurrencyExchangeRate.objects.fetch(d, currency).first()
            logger.info('Fetch currency rates: %s %s', currency, exchangerate.rate)
            try:
                self.create(
                    transaction_id=transaction_id,
                    exchangerate=exchangerate
                )
            except Exception as e:
                logger.error('%s' % e)
                continue
        return self


class QuarterlyBudgetsManager(USDValueFieldManager):
    """
    Manager to assist in identifying roadblocks around quarterly budgets

    Provides
        Budget.objects.aligned_to_quarter() - return budgets which exactly match a single quarter
        Budget.objects.multiple_quarters_budget() - budget matches quarters but covers more than one quarter
        Budget.objects.not_aligned_to_quarter() - budget does not match quarters
        Budget.objects.exchange_rate_inconsistent() - budget currency != budget activity default currency

        'raw' methods:
        exchange_rate() - append the "exchange rate" field for the budget "value date"
    """

    def derived_date_properties(self):
        """
        Mark up with derived year, quarter, day fields
        """
        return dict(
            period_start_year=RawSQL('EXTRACT (year FROM period_start)', ''),
            period_start_day=RawSQL('EXTRACT (day FROM period_start)', ''),
            period_start_month=RawSQL('EXTRACT (month FROM period_start)', ''),
            period_start_quarter=RawSQL('EXTRACT (quarter FROM period_start)', ''),
            period_end_year=RawSQL('EXTRACT (year FROM period_end)', ''),
            period_end_day=RawSQL('EXTRACT (day FROM period_end)', ''),
            period_end_quarter=RawSQL('EXTRACT (quarter FROM period_end)', ''),
            period_end_month=RawSQL('EXTRACT (month FROM period_end)', ''),
            period_end_next_quarter=RawSQL('EXTRACT (quarter FROM period_end + interval \'1 day\')', '')
        )

    start_and_end_same_quarter = dict(
        period_start_quarter=F('period_end_quarter'),
        period_start_year=F('period_end_year'),
    )

    period_end_aligns_to_quarter = (
        Q(period_end_month=12, period_end_day=31) | Q(period_end_next_quarter=F('period_end_quarter') + 1)
    )

    period_start_aligns_to_quarter = dict(
        period_start_day=1,
        period_start_month__in=[1, 4, 7, 10]
    )

    def aligned_to_quarter(self):
        return self .get_queryset()\
            .annotate(**self.derived_date_properties())\
            .filter(**self.start_and_end_same_quarter)\
            .filter(self.period_end_aligns_to_quarter)\
            .filter(**self.period_start_aligns_to_quarter)\


    def multiple_quarters_budget(self, activity_id=None):
        """
        Budgets which cross multiple quarter boundaries but start and end on quarter boundaries nicely
        """
        budgets = self.get_queryset()\
            .annotate(**self.derived_date_properties())\
            .exclude(**self.start_and_end_same_quarter)\
            .filter(self.period_end_aligns_to_quarter)\
            .filter(**self.period_start_aligns_to_quarter)
        if activity_id:
            budgets = budgets.filter(activity_id=activity_id)
        return budgets

    def not_aligned_to_quarter(self):
        return self.get_queryset()\
            .annotate(**self.derived_date_properties())\
            .exclude(self.period_end_aligns_to_quarter & Q(**self.period_start_aligns_to_quarter))

    def exchange_rate(self):
        rawsql = '''
        SELECT DISTINCT ON (id) t.*, r.rate
        FROM aims_budget t
        LEFT OUTER JOIN aims_currency_exchange_rate r
            ON t.value_date = r.date
            AND t.currency_id = r.base_currency_id
            AND r.currency_id = 'USD'
        WHERE t.currency_id != 'USD';
        '''
        return self.raw(rawsql)

    def exchange_rate_inconsistent(self):
        return self .get_queryset()\
            .exclude(currency=F('activity__default_currency'))

    def exchange_rate_inconsistent_display(self):
        for b in self.exchange_rate_inconsistent():
            print("{}: {}{} @ {} = {} {}".format(b.activity_id, b.value, b.currency_id, b.value_date or b.period_start, b.activity.default_currency_id, b.currency_per_activity_default()))

    def split_multiple_quarters_budget(self, i_am_sure=False, activity_id=None):
        budgets = self.multiple_quarters_budget(activity_id)
        budgets = budgets.annotate(quarters=((F('period_end_year') - F('period_start_year')) * 4) + (F('period_end_quarter') - F('period_start_quarter')))
        budgets = budgets.annotate(value_per_quarter=F('value') / F('quarters'))
        deletable = []

        for budget in budgets:
            logger.info('{} {}'.format(budget.activity_id, budget.value))
            logger.info("{} - {}".format(budget.period_start, budget.period_end))
            for quarter in range(int(budget.quarters)):
                add_years, add_quarters = divmod(budget.period_start_quarter + quarter, 4)

                period_start = date(
                    int(budget.period_start_year + add_years),
                    int(add_quarters * 3) + 1,
                    1
                )

                next_quarter_add_years, next_quarter_add_quarters = divmod(budget.period_start_quarter + quarter + 1, 4)

                period_end_plus_one_day = date(
                    int(budget.period_start_year + next_quarter_add_years),
                    int(next_quarter_add_quarters * 3) + 1,
                    1
                )
                period_end = period_end_plus_one_day - timedelta(1)
                value_date = period_start
                value = round(budget.value_per_quarter, 2)

                new_budget = self.model(
                    activity=budget.activity,
                    period_start=period_start,
                    period_end=period_end,
                    value=value,
                    value_date=value_date,
                    currency=budget.currency
                )

                logger.info('\t{} - {} : {}'.format(new_budget.period_start, new_budget.period_end, new_budget.value))
                if i_am_sure:
                    new_budget.save()
            deletable.append(budget.pk)

        if i_am_sure:
            self.model.objects.filter(pk__in=deletable).delete()
        return budgets

    def make_aligned_to_quarters(self, i_am_sure=False, activity_id=None):
        budgets = self.not_aligned_to_quarter().filter(period_start__isnull=False, period_end__isnull=False)
        if activity_id:
            budgets = budgets.filter(activity_id=activity_id)

        for budget in budgets:
            period_start = date(
                int(budget.period_start_year),
                int((budget.period_start_quarter - 1) * 3) + 1,
                1
            )

            period_end_divmod = divmod(budget.period_end_quarter, 4)

            period_end_plus_one_day = date(
                int(budget.period_end_year + period_end_divmod[0]),
                int(period_end_divmod[1] * 3) + 1,
                1
            )

            period_end = period_end_plus_one_day - timedelta(1)

            print(budget.period_start, budget.period_end, '->', period_start, period_end)

            if i_am_sure:
                budget.period_start = period_start
                budget.period_end = period_end
                budget.save()
