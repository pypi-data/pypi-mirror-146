import warnings
from celery import shared_task
from django.core.management import call_command
from django.db import models

from .management.commands.import_exchangerates import exchangerates
import logging
import importlib
from django.apps import apps

from typing import Any, Tuple, Union
from django.contrib.sessions.models import Session

logger = logging.getLogger(__name__)


IndexIdentity = Tuple[str, str]
Identity = Tuple[str, str, Union[str, int]]


def get_instance_identity(sender: Any, instance: Session) -> Tuple[str, str, Union[str, int]]:
    return (
        sender._meta.app_label,
        sender._meta.model_name,
        instance.pk
    )


def get_index_identity(index: Any) -> Tuple[str, str]:
    return (
        index.__class__.__module__,
        index.__class__.__name__
    )


def get_index(index_identity: Identity):
    '''
    Unpacking index identity from tuple of class_name, mod_name
    '''
    module_name, class_name = index_identity[0], index_identity[1]
    search_module = importlib.import_module(module_name)
    index_class = getattr(search_module, class_name)
    return index_class()


def get_instance(sender_identity: Identity) -> Union[models.Model, None]:
    '''
    Unpacking the sender model instance from tuple of app, model_name, and pk
    '''
    app_label, model_name, model_pk = sender_identity
    model = apps.get_model(app_label, model_name)
    try:
        instance = model.objects.get(pk=model_pk)
    except model.DoesNotExist:
        return None
    return instance


@shared_task
def update_index():
    call_command('rebuild_index', '--noinput')


@shared_task
def update_object_index(index_identity: Identity, sender_identity: Identity, backend: Any):

    try:
        instance = get_instance(sender_identity)
        index = get_index(index_identity)
        if not instance:
            logger.debug('No instance to update')
            return
        logger.debug('Index update triggered for %s', instance)
        try:
            index.update_object(instance, using=backend)
        except instance.__class__.DoesNotExist:
            logger.debug('Object not found for %s', instance)
            return False
        except ValueError:
            logger.warning('A ValueError indicates you may have pickles from an incompatible version of Python', exc_info=True)
        logger.debug('Index update returned for %s', instance)
    except Exception as E:
        logger.critical('An index update failed on: %s %s', index_identity, sender_identity, exc_info=True)
        warnings.warn(F'{E}')
        return False
    return True


@shared_task
def update_currency_rates():
    exchangerates()


@shared_task
def clear_blank_activities(*args, **kwargs):
    apps.get_model("aims", "Activity").objects.clear_blank_activities()
