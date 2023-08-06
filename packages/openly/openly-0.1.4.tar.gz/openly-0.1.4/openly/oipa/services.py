import warnings
import requests
from collections import defaultdict
from datetime import datetime, date, timedelta
from django.conf import settings
from django.utils import timezone
from aims.models import Activity, AidType, Budget, BudgetStatus, BudgetType, Currency, DisbursementChannel, FinanceType, FlowType, TiedStatus, Transaction, TransactionType
from .models import OipaActivityLink, OipaSyncRecord
from . import serializers as oipa_serializers
from json.decoder import JSONDecodeError
from sentry_sdk import capture_exception
from typing import Any, Dict, Tuple
from aims.oipa_serializers.changes import v201_to_v105
from .response_cache import cached_get
from aims.utils import AdvisoryLock
import logging
logger = logging.getLogger(__name__)


def get_syncs(activity_id):
    # filter out sync records with 0's for all fields, as there are no changes.
    syncs = OipaSyncRecord.objects \
        .filter(activity_id=activity_id) \
        .exclude(b_added=0, c_added=0, of_added=0, if_added=0) \
        .all()
    return oipa_serializers.OipaSyncRecordSerializer(syncs, many=True).data


def clear_sync_history(activity_id):
    # delete all sync records for a given activity
    OipaSyncRecord.objects \
        .filter(activity_id=activity_id) \
        .delete()


def safeget(dct, *keys):

    # There are a number of different errors which may be raised in fetching data from a JSON structure
    # Key, Index, Type

    for key in keys:
        try:
            if not dct:
                logger.debug('Empty: %s', ','.join(str(k) for k in keys), exc_info=True)
                return None
            dct = dct[key]
        except TypeError:
            if isinstance(dct, list) and not isinstance(key, int):
                # Indicating an unexpected string as list index
                raise
            logger.debug('TypeError retrieving path: %s', ','.join(str(k) for k in keys), exc_info=True)
        except (KeyError, IndexError):
            logger.debug('Error retrieving path: %s', ','.join(str(k) for k in keys), exc_info=True)
    return dct


def oipa_activity_handler(response: requests.models.Response) -> Dict:
    '''
    Handle a request returned from the OIPA server

    Returns a formatted dict of the response
    or raises an appropriate HTTPError, JSONDecodeError, KeyError
    '''
    try:
        response.raise_for_status()  # Abort with appropriate error status if the response code is not a 200

    except requests.exceptions.HTTPError:
        logger.error('OIPA server returned an %s error code', response.status_code)
        raise

    try:
        data = response.json()
        narratives = safeget(data, "title", "narratives")
        return {
            'iati_id': data['iati_identifier'],
            'oipa_id': data['id'],
            'title': safeget(narratives, 0, "text") if narratives else None,
            'currency': safeget(data, "default_currency", "code"),
            'last_updated_datetime': data["last_updated_datetime"],
            'reporting_org': safeget(data, "reporting_organisation", "narratives", 0, "text"),
            'status': safeget(data, "activity_status", "name"),
        }
    except JSONDecodeError:
        logger.error('OIPA server returned a non JSON response')
        raise

    except KeyError:
        logger.error('OIPA server returned an unexpected response format')
        raise


def transactions_template():
    return defaultdict(lambda: dict([("data", list()), ("count", 0)]))


def oipa_transactions_handler(response: requests.models.Response, transactions: dict = None) -> Tuple[Dict, bool]:
    '''
    Handle a response from OIPA transactions
    The second return parameter is whether further results exist in which case you probably want
    to imcrement the page count
    '''

    transactions = transactions or transactions_template()
    try:
        response.raise_for_status()  # Abort with appropriate error status if the response code is not a 200
    except requests.exceptions.HTTPError:
        logger.error('OIPA server returned an %s error code', response.status_code)
        raise

    openly_codes = v201_to_v105['TransactionType']
    try:
        data = response.json()
    except JSONDecodeError:
        logger.error('OIPA server returned a non JSON response')
        raise

    if 'results' not in data:
        raise KeyError('No results key in transaction JSON')

    for t in data['results']:
        if float(t["value"]) < 0:
            continue
        # Convert the newer numeric code type to the legacy, alphabetic code in openly
        openly_trans_code = openly_codes[t["transaction_type"]["code"]]
        if openly_trans_code not in ["C", "D", "E", "IF"]:
            continue
        if openly_trans_code in ["D", "E"]:
            # Consolidate Disbursement and Expenditure codes
            trans_code = "OF"
        else:
            trans_code = openly_trans_code
        transactions[trans_code]['count'] += 1
        transactions[trans_code]['data'].append({
            "transaction_type": trans_code,
            "transaction_code_orig": openly_trans_code,
            "transaction_date": safeget(t, "transaction_date"),
            "value": safeget(t, "value"),
            "value_date": safeget(t, "value_date"),
            "description": safeget(t, "description", "narratives", 0, 'text') if safeget(t, "description", "narratives") else None,
            "currency": safeget(t, 'currency', 'code'),
            "provider_organisation": safeget(t, 'provider_organisation'),
            "receiver_organisation": safeget(t, 'receiver_organisation'),
            "disbursement_channel": safeget(t, 'disbursement_channel'),
            "flow_type": safeget(t, 'flow_type', 'code'),
            "finance_type": int(safeget(t, 'finance_type', 'code')) if 'finance_type' in t and safeget(t, 'finance_type', 'code') else None,
            "aid_type": safeget(t, 'aid_type', 'code'),
            "tied_status": safeget(t, 'tied_status', 'code')
        })
    if data['next']:
        return transactions, True
    return transactions, False


def oipa_budgets_handler(response: requests.Response, quarterly: bool = True) -> Dict:
    '''
    Parses the response from OIPA to extract budgets
    '''
    def get_qrt(dt):
        if dt.month < 4:
            return 1
        else:
            return (dt.month - 1) // 3 + 1

    def rollup_to_quarterly_budgets(budgets):
        # calculate the quarter start end dates and assign to each budget
        for b in budgets['data']:
            period_start = datetime.strptime(b['period_start'], '%Y-%m-%d').date()
            period_start_qrt = get_qrt(period_start)
            period_end = datetime.strptime(b['period_end'], '%Y-%m-%d').date()
            period_end_qrt = get_qrt(period_end)

            b['period_start'] = date(
                period_start.year,
                int((period_start_qrt - 1) * 3) + 1,
                1
            )
            period_end_divmod = divmod(period_end_qrt, 4)
            period_end_plus_one_day = date(
                int(period_end.year + period_end_divmod[0]),
                int(period_end_divmod[1] * 3) + 1,
                1
            )
            b['period_end'] = period_end_plus_one_day - timedelta(1)

        return budgets

    try:
        response.raise_for_status()  # Abort with appropriate error status if the response code is not a 200
    except requests.exceptions.HTTPError:
        logger.error('OIPA server returned an %s error code', response.status_code)
        raise

    try:
        data = response.json()
    except JSONDecodeError:
        logger.error('OIPA server returned a non JSON response')
        raise

    try:
        budgets = {
            "data": [{
                "activity": data["iati_identifier"],
                "type": b["type"]["code"],
                "status": b["status"]["code"],
                "value": b["value"]["value"],
                "value_date": b["value"]["date"],
                "currency": b["value"]["currency"]['code'],
                "period_start": b["period_start"],
                "period_end": b["period_end"],
            } for b in data['budgets'] if (b["value"]["value"] or 0) > 0],
            "count": len(data['budgets'])
        }
    except KeyError:
        logger.error('Key Error on retrieving OIPA budgets')
        return {"data": [], "count": 0}

    if quarterly:
        return rollup_to_quarterly_budgets(budgets)
    return budgets


class IatiIntegrityError(Exception):
    ''' IATI Integrity Exception - To be thrown by the OIPA data validator class
        if / when it is deemed that OIPA data does not pass our import checks.
    '''

    def __init__(self, message=None):
        if message:
            super().__init__(message)
        else:
            super().__init__('IATI data is missing key fields and AIMS Activity has no defaults set.')

    def __str__(self):
        return self.message


class OipaRecords():
    '''
    Retrieve IATI records from an OIPA server for an
    activity or an activity's transactions
    '''

    def __repr__(self):
        return 'Oipa Records - %s, - %s' % (self.oipa_url, self.iati_id)

    def __init__(self, iati_id: str, oipa_url=False, **kwargs):
        '''
        A nice example ID is GB-1-203400-103
        >>> ors = OipaRecords('GB-1-203400-103')
        >>> ors.get_activity()
        >>> ors.get_transactions()
        '''
        assert iati_id and iati_id != 'null'
        self.iati_id = str(iati_id)
        self.oipa_url = kwargs.get('oipa_url', getattr(settings, 'OIPA_SERVER_URL', 'https://www.oipa.nl'))

    @property
    def _json(self):
        '''
        Fetch the 'internal' OIPA ID
        This ought to be more reliable than the IATI ID
        which may contain URL-confusing characters
        '''
        extra_params = {
            'q': self.iati_id,
            'q_lookup': 'exact',
            'q_fields': 'iati_identifier'
        }
        url = '{}/api/activities/'.format(self.oipa_url)

        # Returns a cached response if present else make a call to OIPA server
        response = cached_get(url=url, extra_params=extra_params)
        response.raise_for_status()

        # Extract the response from the JSON. Expect one match; raise if 0 or > 1 results.
        try:
            rjson = response.json()

            if len(rjson['results']) == 0:
                # This is of questionable value - a 'last-ditch' effort to try again
                logger.warning('Received No IATI matches for %s. Retry with startswith ID', self.iati_id)
                extra_params['q_lookup'] = 'startswith'
                response = cached_get(url=url, extra_params=extra_params)
                response.raise_for_status()
                rjson = response.json()
            assert len(rjson['results']) == 1
            return rjson
        except JSONDecodeError:
            logger.error('OIPA server returned a non JSON response')
            raise
        except (KeyError, AssertionError):
            raise AssertionError('Expected a JSON response with one "result" from %s- got %s' % (response.url, response.json()))

    @property
    def _result(self):
        '''
        Return the first result from an OIPA search for activity ID
        '''
        return self._json['results'][0]

    @property
    def _activity_url(self):
        '''
        Return the first result URL from an OIPA search for activity ID
        '''
        return self._json['results'][0]['url']

    @property
    def activity(self) -> Dict[str, Any]:
        '''
        Call the OIPA server URL to fetch OIPA records
        Returns a formatted dict of the response
        or raises a TimeOut or SSLErrors
        '''
        return oipa_activity_handler(cached_get(self._activity_url))

    @property
    def transactions(self) -> Dict[str, Any]:
        '''
        Retrieve Transactions for an IATI activity
        '''

        url = self._result['transactions']
        # Initially no transactions - this is set in the handler
        page = 1
        transactions = None
        next_page = True

        while next_page:
            try:
                response = cached_get(url, {'page': str(page)})
                transactions, next_page = oipa_transactions_handler(response, transactions)
            except requests.exceptions.HTTPError:
                # This may turn out to be a little too verbose as an activity with no transactions
                # seems to return a 404 from the API
                capture_exception()
                break
            if next_page:
                page += 1
        return transactions or transactions_template()

    @property
    def budgets(self):
        response = cached_get(self._activity_url)
        try:
            response.raise_for_status()
            return oipa_budgets_handler(response)
        except requests.exceptions.HTTPError:
            # This may turn out to be a little too verbose as an activity with no transactions
            # seems to return a 404 from the API
            capture_exception()
            return


class ActivityLink():

    def __init__(self, activity_id):
        self.activity_id = activity_id
        try:
            self.link = OipaActivityLink.objects.filter(activity_id=activity_id).get()
        except OipaActivityLink.DoesNotExist:
            self.link = None

    def get_link(self):
        return self.link

    def update_link(self, linked_fields):
        if self.link:
            self.link.oipa_fields = linked_fields
            self.link.save()
        else:
            self.link = OipaActivityLink.objects.create(**{
                'activity_id': self.activity_id,
                'oipa_fields': linked_fields
            })
        # remove all sync history records
        clear_sync_history(self.link.activity_id)
        return self.link

    def clear_link(self):
        if self.link:
            self.link.oipa_fields = []
            self.link.save()
        else:
            # if link does not exist, create a placeholder with sync OFF and empty fields
            self.link = OipaActivityLink.objects.create(**{
                'activity_id': self.activity_id,
                'oipa_fields': []
            })
        # remove all sync history records
        clear_sync_history(self.link.activity_id)
        return oipa_serializers.OipaActivityLinkSerializer(self.link).data

    def delete_link(self):
        if self.link:
            try:
                # remove all sync history records
                clear_sync_history(self.link.activity_id)
                aims_activity = Activity.objects.get(id=self.link.activity_id)
                self.link.delete()
                aims_activity.iati_identifier = None
                aims_activity.save()
                return True
            except Exception as E:
                warnings.warn(F'Unhandled legacy exception: {E}')
                return False
        else:
            return False


class OipaValidator():
    def __init__(self, activity):
        self.activity = activity
        self.setup_defaults()
        self.link = ActivityLink(activity.id).get_link()
        # set all validation results for the transaction types and budgets to FALSE
        self.results = {
            'B': {'verdict': False, 'evidence': []},
            'OF': {'verdict': False, 'evidence': []},
            'C': {'verdict': False, 'evidence': []},
            'IF': {'verdict': False, 'evidence': []}
        }
        self.clean_records = {}

    def lookup_openly_attribute(self, source, field, key, attr_name=None, default_val=None):
        try:
            attr = next((item for item in source if item.code == key), default_val)
            if attr:
                return attr
            else:
                self.log_evidence(field, "Error field data - %s" % attr_name)
        except TypeError:
            self.log_evidence(field, "Error field data - %s" % attr_name)

    def log_evidence(self, field, msg):
        self.results[field]['evidence'].append(msg)

    def finalize_verdict(self, field):
        f = self.results[field]
        # check that we have evidence to condem a transaction type
        if len(f['evidence']) > 0:
            # condense duplicate evidence points into one
            f['evidence'] = list(set(f['evidence']))
            # set verdict to False (dirty / invalid data)
            f['verdict'] = False
        else:
            # we have no evidence, so make sure verdict is True (clean)
            f['verdict'] = True

    def setup_defaults(self):
        self.openly_transaction_types = TransactionType.objects.all()
        self.openly_aid_types = AidType.objects.all()
        self.openly_finance_types = FinanceType.objects.all()
        self.openly_flow_types = FlowType.objects.all()
        self.openly_tied_statuses = TiedStatus.objects.all()
        self.openly_currencies = Currency.objects.all()
        self.openly_disbursement_channels = DisbursementChannel.objects.all()
        self.openly_budget_statuses = BudgetStatus.objects.all()
        self.openly_budget_types = BudgetType.objects.all()

    def validate_transactions(self, oipa_records):
        for field in ['C', 'OF', 'IF']:
            self.clean_records[field] = []
            if oipa_records != []:
                for r in oipa_records[field]['data']:
                    try:
                        # validate a record
                        r['activity'] = self.activity
                        # convert strings to datetime
                        r['transaction_date'] = datetime.strptime(r['transaction_date'], '%Y-%m-%d').date()
                        r['value_date'] = datetime.strptime(r['value_date'], '%Y-%m-%d').date()
                        # assign correct openly objects for various codes/statuses
                        r['transaction_type'] = self.lookup_openly_attribute(self.openly_transaction_types, field, r["transaction_code_orig"], "trans code")
                        # Now that we've assigned the correct Openly code we can get rid of the original OIPA code
                        r.pop("transaction_code_orig")
                        r['aid_type'] = self.lookup_openly_attribute(self.openly_aid_types, field, r['aid_type'], "aid type", self.activity.default_aid_type)
                        r['finance_type'] = self.lookup_openly_attribute(self.openly_finance_types, field, r['finance_type'], "finance type", self.activity.default_finance_type)
                        if r.get('flow_type', None):
                            r['flow_type'] = self.lookup_openly_attribute(self.openly_flow_types, field, int(r['flow_type']), "flow type", self.activity.default_flow_type)
                        if r.get('tied_status', None):
                            r['tied_status'] = self.lookup_openly_attribute(self.openly_tied_statuses, field, int(r['tied_status']), "tied status", self.activity.default_tied_status)
                        if r.get('currency', None):
                            r['currency'] = self.lookup_openly_attribute(self.openly_currencies, field, r['currency'], "currency", self.activity.default_currency)
                        if r['disbursement_channel']:
                            r['disbursement_channel'] = self.lookup_openly_attribute(self.openly_disbursement_channels, field, int(r['disbursement_channel']['code']), "disburse channel", "")
                        # Mapping IATI Orgs to Mohing Orgs (receiver)
                        if len(self.activity.implementing_partners_list) >= 1:
                            r['receiver_organisation'] = self.activity.implementing_partners_list[0]
                        else:
                            self.log_evidence(field, "No implementing organisation(s) setup.")
                            break
                        # Mapping IATI Orgs to Mohing Orgs (provider)
                        if self.activity.reporting_organisation.type:
                            r['provider_organisation'] = self.activity.reporting_organisation
                        else:
                            self.log_evidence(field, "No reporting organisation(s) setup.")
                            break
                    except (IatiIntegrityError, ValueError) as err:
                        self.log_evidence(field, str(err))
                    else:
                        self.clean_records[field].append(Transaction(**r))
                # check to see if the field passed
                self.finalize_verdict(field)
                if not self.results[field]['verdict']:
                    # Encountered errors. Block syncing.
                    self.handle_bad_data(field)

    def validate_budgets(self, oipa_records):
        self.clean_records['B'] = []
        type_one = defaultdict(list)  # original type
        type_two = defaultdict(list)  # revised type
        for r in oipa_records:
            period = r['period_start']
            if int(r['type']) == 2:
                type_two[period].append(r)
            else:
                type_one[period].append(r)

        for period in type_one.keys():
            try:
                # if period in type two, remove it. We will take orig over revised.
                if period in type_two.keys():
                    type_two.pop(period, None)
                # append a rolled up quarter budget
                rolled_up_budgets = self.rollup_budgets_for_quarter(type_one[period])
                self.clean_records['B'].append(self.prep_budget(rolled_up_budgets))
            except (IatiIntegrityError, ValueError):
                self.log_evidence('B', 'Required fields are missing.')

        # any remaining type 2 budgets should be pushed in now
        for period in type_two.keys():
            try:
                # append a rolled up quarter budget
                rolled_up_budgets = self.rollup_budgets_for_quarter(type_two[period])
                self.clean_records['B'].append(self.prep_budget(rolled_up_budgets))
            except (IatiIntegrityError, ValueError):
                self.log_evidence('B', 'Required fields are missing.')

        # check to see if the field passed
        self.finalize_verdict('B')
        if not self.results['B']['verdict']:
            # Enconutered errors. Block syncing.
            self.handle_bad_data('B')

    def rollup_budgets_for_quarter(self, budgets):
        rolled_up_budget = budgets[0]  # use any budget for a stating point
        rolled_up_budget['value'] = sum([b['value'] for b in budgets])
        return rolled_up_budget

    def prep_budget(self, r):
        r['activity'] = self.activity
        # convert strings to datetime
        r['period_start'] = r['period_start']
        r['period_end'] = r['period_end']
        # assign correct openly objects for various codes/statuses
        r['type'] = self.lookup_openly_attribute(self.openly_budget_types, 'B', int(r['type']))
        r['status'] = self.lookup_openly_attribute(self.openly_budget_statuses, 'B', int(r['status']))
        r['currency'] = self.lookup_openly_attribute(self.openly_currencies, 'B', r['currency'], self.activity.default_currency)
        return Budget(**r)

    def handle_bad_data(self, field):
        # IATI Activity data should NOT be syncronized!
        if self.link and field in self.link.oipa_fields:
            # Break Sync Link for affected Activity Budgets / Transaction Field
            self.link.oipa_fields.remove(field)
            # Save revised link record
            self.link.save()


class OipaSync():

    def initialize_counter(self, oipa_records, openly_records, initial_sync):
        oipa_rec_count = len(oipa_records)
        # We set Openly record count to zero if it's the initial sync (or an update of the sync link)
        # allows for the calculation of records added vs updated. This calculation choice,
        # while slightly convoluted, was chosen because we cannot reliably match up new/old records.
        # Since we wll delete and re-populate the various transaction types with each sync it's important
        # know how many records existed prior to sync and work from that to get back to new records added
        # (for NOT initital syncs). Initial syncs can use a simple count of records added.
        if initial_sync:
            openly_rec_count = 0
        else:
            openly_rec_count = len(openly_records)

        results = {
            'deleted': openly_rec_count - oipa_rec_count if oipa_rec_count < openly_rec_count else 0,
            'added': oipa_rec_count - openly_rec_count if openly_rec_count < oipa_rec_count else 0,
            'updated': 0
        }
        return results

    def sync_activity(self, activity_link, initial_sync=False):
        aims_activity = Activity.objects.all_openly_statuses().filter(id=activity_link.activity_id).get()
        logger.debug("~~~ Starting Activity Sync | %s(OIPA) | %s(MOHINGA) ~~~" % (aims_activity.iati_identifier, aims_activity.id))
        # Fetch and validate data from OIPA before attempting sync
        oipa_validator = OipaValidator(aims_activity)
        assert aims_activity.iati_identifier

        # This part, fetching transactions, may timeout
        oipa_validator.validate_transactions(OipaRecords(aims_activity.iati_identifier).transactions)
        temp_budgets = OipaRecords(aims_activity.iati_identifier).budgets

        if temp_budgets:
            oipa_validator.validate_budgets(temp_budgets['data'])
        else:
            oipa_validator.validate_budgets([])

        logger.debug("Oipa Linked Fields: " + str(activity_link.oipa_fields))
        logger.debug("Oipa Validator Results: " + str(oipa_validator.results))

        updates = {}
        for field in activity_link.oipa_fields:
            if oipa_validator.results[field]:
                if field == "B":
                    oipa_records = oipa_validator.clean_records['B']
                    openly_records = Budget.objects.filter(activity=aims_activity).all()
                else:
                    try:
                        oipa_records = oipa_validator.clean_records[field]
                    except KeyError:
                        oipa_records = []
                    finally:
                        if field == "OF":
                            openly_records = Transaction.objects.filter(activity=aims_activity).filter(transaction_type_id__in=['D', 'E']).all()
                        else:
                            openly_records = Transaction.objects.filter(activity=aims_activity).filter(transaction_type_id=field).all()
                # sync records to the DB
                updates[field] = self.sync_db(aims_activity, field, oipa_records, openly_records, initial_sync)

        # if there were records added, we should update the activity date_modified
        if (sum([updates[field]['added'] for field in updates]) > 0):
            aims_activity.save()

        # build and save OipaSyncRecord for Activity
        sync_time = str(timezone.now())
        r = {"activity_id": aims_activity.id, "sync_datetime": sync_time}
        for f in updates:
            try:
                r[f.lower() + "_added"] = updates[f]['added']
            except KeyError:
                r[f.lower() + "_added"] = 0
        sync_record = OipaSyncRecord.objects.create(**r)
        sync_results = oipa_serializers.OipaSyncRecordSerializer(sync_record).data
        logger.debug("Activity Sync Record: " + str(sync_results))
        return sync_results

    def sync_db(self, activity, field, oipa_records, openly_records, initial_sync):
        # initialize sync results counter obj
        results = self.initialize_counter(oipa_records, openly_records, initial_sync)
        # delete all old budgets
        if field == "B":
            with AdvisoryLock('budget'):
                Budget.objects.filter(activity=activity).delete()

        # delete all transactions of target type
        elif field == "C":
            with AdvisoryLock('transaction'):
                Transaction.objects.filter(activity=activity).filter(transaction_type_id="C").delete()
        elif field == "OF":
            with AdvisoryLock('transaction'):
                Transaction.objects.filter(activity=activity).filter(transaction_type_id__in=['D', 'E']).delete()
        elif field == "IF":
            with AdvisoryLock('transaction'):
                Transaction.objects.filter(activity=activity).filter(transaction_type_id='IF').delete()

        # push in new records
        for r in oipa_records:
            r.save()
            results['updated'] += 1

        if field == "B":
            # split multiple quarters
            with AdvisoryLock('budget'):
                Budget.objects.split_multiple_quarters_budget(activity_id=activity.id, i_am_sure=True)

        return results
