import logging

from django.conf import settings
from django.core.exceptions import ValidationError

from aims.oipa_serializers.serializers import (
    ActivityDeserializer, IATISourceRefSerializer, OrganisationDeserializer, TransactionDeserializer,
)

from .api_list_iterator import APIListIterator
oipa_server_url = getattr(settings, 'OIPA_SERVER_URL', 'https://www.oipa.nl')
logger = logging.getLogger(__file__)


class OipaSyncer(object):

    def __init__(self, reporting_organisations=None, activities=None, since=None, xml=None):
        self.params = {
            'format': 'json'
        }

        if reporting_organisations is not None:
            self.params['reporting_organisation'] = ','.join(reporting_organisations)
        if activities is not None:
            self.params['activities'] = ','.join(activities)
        if since is not None:
            self.params['last_updated_datetime_gte'] = since
        if xml is not None:
            self.params['xml_source_ref'] = xml

    def sync(self):
        url = oipa_server_url + '/api/activities'
        activities_iter = APIListIterator(url, params=self.params)
        for activity in activities_iter:
            activity_serializer = ActivityDeserializer(data=activity, partial=True)
            try:
                if activity_serializer.is_valid():
                    activity_model = activity_serializer.save()
                    activity_model.clean_location_percentages()
                    activity_model.clean_activity_sector_percentages()
                    logger.info('Saved {}'.format(activity_model))
                    if 'transactions' in activity:
                        transactions_url = activity.pop('transactions')
                        transactions_iter = APIListIterator(transactions_url,
                                                            params={'format': 'json'})
                        for transaction in transactions_iter:
                            transaction['activity']['id'] = activity_model.id
                            transaction_serializer = TransactionDeserializer(data=transaction,
                                                                             partial=True)
                            if transaction_serializer.is_valid():
                                transaction_model = transaction_serializer.save()
                                logger.info(transaction_model)
                            else:
                                logger.warning('TRANSACTION ERRORS: ', transaction_serializer.errors)
                else:
                    logger.warning('ACTIVITY_ERRORS: ', activity_serializer.errors)
            except ValidationError as e:
                logger.warning(e)


class IATISourceSyncer(object):
    def __init__(self, oipa=False):
        self.url = (oipa or oipa_server_url) + '/api/datasets'

        self.params = {
            'is_parsed': 'true',
            'format': 'json'
        }

    def sync(self):
        model_iter = APIListIterator(self.url, params=self.params)
        for model in model_iter:
            serializer = IATISourceRefSerializer(data=model, partial=True)
            try:
                if serializer.is_valid():
                    model = serializer.save()
                    logger.info('Saved {}'.format(model))
                else:
                    logger.warning('ERRORS: ', serializer.errors)
            except ValidationError as e:
                logger.warning(e)


class IATIOrganisationSyncer(object):
    def __init__(self, oipa=False):
        self.url = (oipa or oipa_server_url) + '/api/organisations'

        self.params = {
            'is_parsed': 'true',
            'format': 'json'
        }

    def sync(self):
        model_iter = APIListIterator(self.url, params=self.params)
        for model in model_iter:
            serializer = OrganisationDeserializer(data=model, partial=True)
            try:
                if serializer.is_valid():
                    model = serializer.save()
                    logger.info('Saved {}'.format(model))
                else:
                    logger.warning('ERRORS: ', serializer.errors)
            except ValidationError as e:
                logger.warning(e)
