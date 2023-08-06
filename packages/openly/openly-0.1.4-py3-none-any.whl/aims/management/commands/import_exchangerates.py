import logging
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from aims import models as aims
from django.db.models import Count

REQUESTS = 3

logger = logging.getLogger('rates')
logger.setLevel(logging.DEBUG)
base_currency = 'USD'


def exchangerates():
    """
    This is run as a periodic task
    :return:
    """
    fixmissing()


def drop_unused_rates():
    '''
    Remove rates which are no longer referenced by any transaction or budget
    '''
    currency_exchange_rates = aims.CurrencyExchangeRates.objects.annotate(
        Count('transactionexchangerate'),
        Count('budgetexchangerate')).filter(
            transactionexchangerate__count=0,
            budgetexchangerate__count=0).count()
    for i in currency_exchange_rates:
        try:
            i.delete()
        except IntegrityError:
            pass


def fixmissing(limit=REQUESTS):
    for model in [aims.TransactionExchangeRate, aims.BudgetExchangeRate]:
        model.objects.fetch_currency_rates(limit=int(limit))
        model.objects.match_currency_rates()

    for model in [aims.Transaction, aims.Budget]:
        model.objects.update_usd_value()


class Command(BaseCommand):
    help = 'Imports exchange rates for Transactions which have missing data'

    def add_arguments(self, parser):
        parser.add_argument('--requests', default=REQUESTS, help='The number of requests to make')

    def handle(self, *args, **options):
        fixmissing(limit=int(options.get('requests', REQUESTS)))
        # drop_unused_rates()
