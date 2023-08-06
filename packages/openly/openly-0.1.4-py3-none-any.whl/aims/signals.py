import importlib
from typing import Any, Iterable, Union  # noqa: F401
import uuid
import logging
import warnings

from django.contrib.sessions.models import Session
from django.db import IntegrityError
from django.db import models
from django.db.models.base import ModelBase
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from haystack.signals import BaseSignalProcessor
from kombu.exceptions import OperationalError
from sentry_sdk import capture_exception

from aims import models as aims
from aims.utils import AdvisoryLock

from .tasks import update_object_index, get_index_identity, get_instance_identity

logger = logging.getLogger(__name__)


class QueuedSignalProcessor(BaseSignalProcessor):
    """
    When an indexed model is saved, enqueue a task that will update the index.
    This processor is iati-aware: when saving a iati model, the related aims model search index is updated.
    """

    def setup(self):
        post_save.connect(self.handle_save)
        post_delete.connect(self.handle_delete)

    def teardown(self):
        post_save.disconnect(self.handle_save)
        post_delete.disconnect(self.handle_delete)

    def handle_save(self, sender: ModelBase, instance: Session, **kwargs: Any):
        if getattr(settings, 'NO_INDEX_UPDATE', False):
            return
        try:
            importlib.import_module("haystack")
        except:
            logger.info("Haystack was not installed, returning")
            return
        # special handling to ensure we process organisations related to an activity
        if sender is aims.Activity and instance.reporting_organisation is not None:
            if aims.Partner.objects.filter(pk=instance.reporting_organisation.pk).exists():
                self.enqueue_update_index(aims.Partner, aims.Partner.objects.get(pk=instance.reporting_organisation.pk), **kwargs)
        if sender is aims.Activity:
            for apo in instance.participating_organisations.distinct('organisation_id'):
                if aims.Partner.objects.filter(pk=apo.organisation_id).exists():
                    self.enqueue_update_index(aims.Partner, aims.Partner.objects.get(pk=apo.organisation_id), **kwargs)

        # update index for the current class, if it exists
        self.enqueue_update_index(sender, instance, **kwargs)

    def enqueue_update_index(self, sender: Union[ModelBase, Session], instance: Session, **kwargs: Any) -> Union[bool, Any]:
        """
        Like BaseSignalProcessor.handle_save, but
        tries to enqueue the update instead of doing it synchronously.
        """
        from haystack.exceptions import NotHandled
        # most likely backend_names == ['default']
        backend_names = self.connection_router.for_write(instance=instance)  # type: Iterable[str]
        sender_identity = get_instance_identity(sender, instance)
        no_delay = getattr(settings, 'NO_INDEX_DELAY', False)  # type: bool

        # Go through each of the index backends (usually, Whoosh / Haystack languages)
        # and update the index value
        for backend_name in backend_names:

            try:
                index = self.connections[backend_name].get_unified_index().get_index(sender)
            except NotHandled:
                # This means there is no index for that model.
                # Usually we index Activity, Organisation models.
                return

            # For asycnronous calls passing class instances is a terrible idea
            # Dehydrate them to strings instead
            index_identity = get_index_identity(index)

            if no_delay:
                return update_object_index(index_identity, sender_identity, backend_name)  # type:ignore

            # Asyncronously hand the task off to celery
            # Note that this may result in long delay if you have no celery worker or
            # rabbitmq database or very very long delay if you don't have
            # celery correctly configured
            try:
                return update_object_index.delay(index_identity, sender_identity, backend_name)  # type:ignore
            except OperationalError as E:
                if settings.DEBUG:
                    # A dev env maybe encountered a problem with celery.
                    # Developer should fix this and we raise it for them.
                    logger.error(
                        'You have encountered an error with the messaging backend. rabbitmq might not be listening.'
                        + ' Run a rabbitmq server or add to settings `NO_INDEX_DELAY = true`'
                        + ' https://github.com/catalpainternational/openly/#troubleshooting'
                    )
                    raise

                # A production server has probably encountered a problem with celery. This is ugly. We
                # don't want to raise it here because this is only for indexing, but sentry ought to know about it.
                capture_exception(E)
                try:
                    return update_object_index(index_identity, sender_identity, backend_name)  # type:ignore
                except Exception as E:
                    # The problem may not be with celery but some other part of our indexing
                    # setup (on dev server). Developer wants to know about this too.
                    # This is non fatal for the user and they won't see a 500 on the activity editor
                    # as we capture_exception() on it.
                    capture_exception(E)

    def handle_delete(self, sender: ModelBase, instance: Session, **kwargs: Any):
        """
        Delete an instance from all indexes
        Unlike 'enqueue' above this is always syncronous
        """
        try:
            importlib.import_module("haystack")
        except:
            logger.info("Haystack was not installed, returning")
            return
        from haystack.exceptions import NotHandled
        backend_names = self.connection_router.for_write(instance=instance)  # type: Iterable[str]
        if getattr(settings, 'NO_INDEX_UPDATE', False):
            return
        for backend_name in backend_names:
            try:
                index = self.connections[backend_name].get_unified_index().get_index(sender)
            except NotHandled:
                return

            try:
                index.remove_object(instance, using=backend_name)
            except Exception as E:
                logger.critical('An index removal failed on: %s', sender, exc_info=True)
                warnings.warn(F"{E}")


FinancialModel = Union[aims.CurrencyExchangeRate, aims.Transaction, aims.Budget, aims.Activity]


@receiver(post_save)
def update_activity_financials(sender: FinancialModel, instance: Session, **kwargs: Any):

    if sender in [aims.CurrencyExchangeRate]:
        logger.debug('Signal triggered TransactionExchangeRate and BudgetExchangeRate table match_currency_rates()')
        aims.TransactionExchangeRate.objects.match_currency_rates()
        aims.BudgetExchangeRate.objects.match_currency_rates()
        with AdvisoryLock('transaction'):
            aims.Transaction.objects.update_usd_value()
        with AdvisoryLock('budget'):
            aims.Budget.objects.update_usd_value()

    # We may have changed the transaction currency, in which case our TransactionExchangeRate is stuffed
    if sender in [aims.Transaction]:
        logger.debug('Transaction currency altered. Refreshing TransactionExchangeRates')
        aims.TransactionExchangeRate.objects.match_currency_rates()
        with AdvisoryLock('transaction'):
            aims.Transaction.objects.update_usd_value()

    # We may have changed the budget currency, in which case our BudgetExchangeRate is stuffed
    if sender in [aims.Budget]:
        logger.debug('Budget currency altered. Refreshing BudgetExchangeRate')
        aims.BudgetExchangeRate.objects.match_currency_rates()
        with AdvisoryLock('budget'):
            aims.Budget.objects.update_usd_value()

    if sender in [aims.Transaction, aims.CurrencyExchangeRate, aims.Activity]:
        logger.debug('Signal-triggered CommitmentTotal.finance_annotate()')
        # Update the commtitment totals table on saving of a Transaction / Exchange Rate
        # Activity is also included here to prevent a RelatedObjectError when an activity is saved
        try:
            if sender == aims.Transaction:
                aims.CommitmentTotal.finance_annotate(activity_id=instance.activity.id)
            elif sender == aims.Activity:
                aims.CommitmentTotal.finance_annotate(activity_id=instance.id)
            elif sender == aims.CurrencyExchangeRate:
                aims.CommitmentTotal.finance_annotate()
        except (aims.CommitmentTotal.DoesNotExist, aims.Activity.DoesNotExist):
            logger.warning('Unexpected error: Aims CommitmentTotal or Activity did not exist')


@receiver(post_delete)
def update_activity_financials_on_transaction_delete(sender: aims.Transaction, instance: models.Model, **kwargs: Any):
    if sender in [aims.Transaction]:
        logger.debug('Transaction delete signal-triggered CommitmentTotal.finance_annotate()')
        # If I'm the only commitment in this Activity, set the commitment total values to zero
        try:
            if not hasattr(instance, 'activity') or not instance.activity:
                return
        except (aims.Activity.DoesNotExist, KeyError):
            return
        if instance.activity.transaction_set.filter(transaction_type='C').count() == 0:
            try:
                ct = aims.CommitmentTotal.objects.get(activity=instance.activity)
                ct.currency_id = 'USD'
                ct.value = 0
                ct.usd_value = 0
                ct.save()
            except aims.CommitmentTotal.DoesNotExist:
                logger.warning('Unexpected error: Aims CommitmentTotal did not exist')
            except IntegrityError:
                # This happens when the Activity is hard deleted, seems like it is a race condition
                pass
        try:
            aims.CommitmentTotal.finance_annotate(activity_id=instance.activity.id)
        except (aims.CommitmentTotal.DoesNotExist, aims.Activity.DoesNotExist):
            logger.warning('Unexpected error: Aims CommitmentTotal or Activity did not exist')


@receiver(post_save)
def set_transaction_provider_organisation_to_activity_funding_organisation(sender: aims.Transaction, instance: Session, **kwargs: Any):
    """ A provider organisation for a transaction should be added to the activity funding organisations. """
    if sender != aims.Transaction:
        return
    if sender.provider_organisation_id is None:
        return

    try:
        aims.ActivityParticipatingOrganisation.objects.get_or_create(
            organisation_id=instance.provider_organisation_id,
            activity_id=instance.activity_id,
            role_id='Funding'
        )
    except IntegrityError:
        pass


@receiver(post_save)
def save_iati_data_in_aims(sender: ModelBase, instance: Session, **kwargs: Any):

    if len(sender.__subclasses__()) > 0:
        for subclass in sender.__subclasses__():
            if hasattr(subclass, 'remote_data'):
                if isinstance(subclass.objects, aims.AIMSManager):
                    exists = subclass.objects.all_openly_statuses().filter(remote_data_id=instance.pk).exists()
                else:
                    exists = subclass.objects.filter(remote_data_id=instance.pk).exists()

                if not exists:
                    new_row = subclass()
                    new_row.pk = instance.pk
                    new_row.__dict__.update(instance.__dict__)
                    new_row.date_created = timezone.now()
                    new_row.save()


@receiver(pre_save)
def activity_pre_save(sender: ModelBase, instance: aims.Activity, **kwargs: Any):
    if sender != aims.Activity:
        return

    instance.completion = instance.completion_percentage / 100


@receiver(pre_save)
def set_activity_id_import(sender: ModelBase, instance: Session, **kwargs: Any):
    if sender != aims.Activity:
        return

    # exit out when laoding fixtures
    if kwargs['raw']:
        return

    def get_unused_uuid() -> str:
        exists = True
        while exists:
            new_pk = str(uuid.uuid1())
            exists = aims.Activity.objects.filter(pk=new_pk).exists()
        return new_pk

    if instance._state.adding and not instance.id:
        instance.id = get_unused_uuid()


@receiver(post_save)
def set_document_url_on_upload(sender: ModelBase, instance: Session, **kwargs: Any):
    if sender != aims.DocumentUpload:
        return
    link = instance.documentlink
    try:
        link.url = instance.doc.url
    except ValueError:
        return
    link.save()


@receiver(post_save)
def set_activity_vocabulary_id(sender: ModelBase, instance: Session, **kwargs: Any):
    """
    Openly issue 1806
    vocabulary_id is not being adjusted on sector save
    Switches DAC-3 to DAC-5 and vv.
    """
    if sender != aims.ActivitySector:
        return

    vocab_id = instance.vocabulary_id  # type: str
    sector_id = instance.sector_id  # type: int
    if vocab_id == 'DAC-3' and sector_id > 1000:
        instance.vocabulary_id = 'DAC-5'
        instance.save()
    # This should never happen, included for completeness and testing
    if vocab_id == 'DAC-5' and sector_id < 1000:
        instance.vocabulary_id = 'DAC-3'
        instance.save()


@receiver(post_save)
def trigger_location_simplesync(sender: ModelBase, instance: Session, **kwargs: Any) -> None:
    '''
    Sync the 'adm_code' and 'area_id' fields to give
    non-simple-locations projects some awareness of simple-locations
    '''
    if sender == aims.Location and not getattr(settings, 'USE_SIMPLE_LOCATIONS', False):
        aims.Location.objects.sync_simple()
