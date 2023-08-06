'''
Functions which can be used in
manager classes for annotation purposes
This is intended as a more general toolbox than the 'aggragations' module
and to not require model imports, to prevent circular imports
'''
import logging
import datetime
from django.db.models import Case, When, F, Q

logger = logging.getLogger(__name__)


def today(delta_days: int = 0) -> datetime.date:
    '''
    This function does exactly what it says on the box
    '''
    return datetime.datetime.today().date() + datetime.timedelta(days=delta_days)


def replace_future_dates(field_name: str = 'value_date', for_date: datetime.date = None):
    '''
    Replaces a "value_date" field with a reasonable past-date default when it is a date from the future
    >>> from aims.annotations import today, replace_future_dates
    >>> for delta in range(-7,7):
    >>>     replace_future_dates(for_date = today(delta))
    aims.annotations:DEBUG Today's date: 2018-10-11; Effective date for values: 2018-10-08
    ...
    aims.annotations:DEBUG Today's date: 2018-10-16; Effective date for values: 2018-10-15
    ...
    aims.annotations:DEBUG Today's date: 2018-10-22; Effective date for values: 2018-10-15
    aims.annotations:DEBUG Today's date: 2018-10-23; Effective date for values: 2018-10-22
    aims.annotations:DEBUG Today's date: 2018-10-24; Effective date for values: 2018-10-22
    '''
    def get_effective_date(for_date: datetime.date) -> datetime.date:
        '''
        Return the "effective date" for the first day of the previous week
        For currency exchange rate calculations, this ensures any 'future' values are a
        reasonable approximation without updating too frequently
        '''
        past_date = for_date - datetime.timedelta(days=1)
        effective_date = past_date - datetime.timedelta(days=past_date.weekday())
        logger.debug("Today's date: %s; Effective date for values: %s", for_date, effective_date)
        return effective_date

    date = for_date or today()
    return Case(When(**{'%s__lt' % (field_name, ): date}, then=F(field_name)), default=get_effective_date(date))


def future_dates(field_name: str = 'value_date'):
    '''
    Return a filter object with the field_name parameter set to dates after today
    '''
    return Q(**{'{}__gte'.format(field_name): today()})
