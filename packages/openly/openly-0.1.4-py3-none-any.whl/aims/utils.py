from decimal import Decimal
import logging
import time
import re
from collections import defaultdict

from django.db import connection
from django.utils.safestring import mark_safe
from rest_framework import renderers
from hashlib import md5

logger = logging.getLogger(__name__)


def str_to_int(instring: str) -> int:
    instring = '%s' % (instring)
    return int(md5(instring.encode()).hexdigest(), base=16) % 10000000


class AdvisoryLock():
    '''
    This context manager ensures that an "advisory lock" is available and taken out before
    running code. This is important in a multiprocess / multithread environment
    where multiple long running queries may be altering rows at the same time.
    '''

    def __init__(self, lock_name: str = 'my-lock', wait_timeout=0.1, retry_limit=120, timeout_geometric=1.1):
        self.lock_no = str_to_int(lock_name)
        self.wait_timeout = wait_timeout
        self.retry_limit = retry_limit
        self.timeout_geometric = timeout_geometric

    def __enter__(self):
        unlocked = False
        wait_timeout = self.wait_timeout
        total_time = 0
        retries = 0

        with connection.cursor() as c:
            while not unlocked and retries < self.retry_limit:
                c.execute('SELECT pg_try_advisory_lock(%s);', (self.lock_no,))
                unlocked = c.fetchone()[0]
                if not unlocked:
                    time.sleep(wait_timeout)
                    retries += 1
                    wait_timeout = wait_timeout * self.timeout_geometric  # Add 100ms each time
                    total_time += wait_timeout

        if retries > 0:
            logger.debug('Lock %s acquired, try %s at %s seconds', self.lock_no, retries, total_time)
        if retries > self.retry_limit * 0.75:
            logger.warning('Lock close to timing out. maybe increase the lock retries or rethink your use of this lock')
        if retries >= self.retry_limit:
            logger.error('Lock timed out. Lock may not have been released')
            raise AssertionError('Timed out waiting for advisory lock release. HINT: Run `SELECT pg_advisory_unlock(%s);`' % self.lock_no)

    def __exit__(self, *args):
        with connection.cursor() as c:
            # We never want to leave it locked: on exit, unlock it
            c.execute('SELECT pg_advisory_unlock(%s);', (self.lock_no,))
        logger.debug('Lock released')


def dictify_tuple_list(tuple_list):
    """ Given a list of tuples ((t0, t1, t2, ...), ...) generate a dict of lists with entries
    [t1, t2, ...] sharing the same first element t0, using t0 as the key.
    """
    d = defaultdict(lambda: [])
    for tuple_ in tuple_list:
        tuple_ = tuple([tuple_element if tuple_element is not None else '' for tuple_element in tuple_])
        if tuple_[0] in d:
            d[tuple_[0]].append(tuple_[1:])
        else:
            d[tuple_[0]] = [tuple_[1:]]
    return d


def clean_percentages(percentages, precision=None):
    ''' Cleans a list of percentages so their total sum is 100.0 where the list may contain
    non-negative numbers and None values indicating currently unset percentages. The list is
    first checked for any unset percentages and if none are present then the list values are
    scaled so their sum is 100. If there are unset values then the sum of set values is
    calculated. If the sum is less than 100 then the remaining percentage is split evenly
    among unset percentages. Otherwise the set values are scaled down so their sum is 100
    and unset percentages are set to 0.
    '''

    assert len([x for x in percentages if x is not None and x < 0]) == 0

    if None not in percentages:
        # If all percentages are numbers scale all percentages such that their sum is 100.0
        cur_sum = sum(percentages)
        if cur_sum == 0.0:
            new_percentages = [(100.0 / len(percentages)) for i in range(len(percentages))]
        else:
            scale = 100.0 / cur_sum
            new_percentages = [p * scale for p in percentages]
    else:
        # If some percentages are not set divide the remaining percentage among them evenly
        # if the current total percentage is less than 100.0, otherwise set them to 0.0 and
        # scale the other percentages so their sum is 100.0
        cur_sum = sum([x for x in percentages if x is not None])
        if cur_sum < 100.0:
            rem_sum = 100.0 - cur_sum
            num_unset = percentages.count(None)
            new_percentages = [x if x is not None else (rem_sum / num_unset) for x in percentages]
        else:
            scale = 100.0 / cur_sum
            new_percentages = [x * scale if x is not None else 0.0 for x in percentages]

    # If given account for rounding errors due to lack of precision
    if precision is not None:
        new_percentages = [round(p, precision) for p in new_percentages]
        rounding_error = 100 - sum(new_percentages)
        for i in range(len(new_percentages)):
            if new_percentages[i] > 0 and new_percentages[i] + rounding_error > 0:
                new_percentages[i] += rounding_error
                break

    return new_percentages


def render(data):
    '''
    Return a safely rendered, utf-8 string representation of data
    This is intended to provide a way to reliably feed JSON into templates
    which can otherwise be troublesome due to invalid characters, forgetting mark_safe,
    decimals etc. JSON.parse('{str}') should always work with output from this.
    '''
    return mark_safe(renderers.JSONRenderer().render(data).decode('utf-8'))


def date_to_financial_year(date):
    """ From an iso date, return the corresponding financial year.

    The financial year starts in October, and ends in September in Myanmar.
    See query_builder.js > get_financial_year for the JS equivalent
    Example: 2019-10-01 -> 'FY2019-2020'
             2020-02-01 -> 'FY2019-2020'
    """
    if not date:
        return None
    matches = re.match(r'(\d\d\d\d)-(\d\d)', date)
    year = matches.group(1)
    month = matches.group(2)
    if int(month) <= 9:
        return 'FY{}-{}'.format(int(year) - 1, year)
    else:
        return 'FY{}-{}'.format(year, int(year) + 1)


def get_rounded_budget(raw_budget, currency='$'):
    """ From a raw budget in USD, return a budget in rounded kilo/millions/billions of USD.

    10,500,200 -> $ 10M
    45,700,200 -> $ 45M
    """
    if not raw_budget:
        # None or 0
        return currency + ' -'
    if raw_budget < 1000000:
        return '{} {:.0f}K'.format(currency, raw_budget / 1000)
    if raw_budget >= 1000000000:
        return '{} {:.2f}B'.format(currency, raw_budget / 1000000000)

    rounded_budget = round(raw_budget / Decimal(1000000.0))
    return '{} {}M'.format(currency, rounded_budget)
