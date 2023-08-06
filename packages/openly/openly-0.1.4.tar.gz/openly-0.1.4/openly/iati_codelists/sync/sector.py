'''
Syncronise sectors and categories
You probably want to run 'categories' first else you might have missing codes
'''

import logging
from django.apps import apps
from . import tools

logger = logging.getLogger(__name__)

# For debugging purposes, you may want to add this to settings.py as LOGGING['loggers']['iati_codelists.sync']
# { 'handlers': ['console'], 'level': 'DEBUG','propagate': True, },


def categories(save=False):
    '''
    Pull 'sectors' from the IATI XML and
    syncronise with our database content
    '''

    model = apps.get_model(app_label='aims', model_name='SectorCategory')
    items = tools.xml_dict(filename='SectorCategory.xml')

    for item in items['codelist']['codelist-items']['codelist-item']:

        code = item.get('code')

        try:
            instance = model.objects.get(pk=code)
        except model.DoesNotExist:
            instance = model()
            logger.info('Create sector Category %s', code)

        update_attributes = dict(
            code=code,
            description=tools.parse_narrative(item, 'description') or '',
            name=tools.parse_narrative(item, 'name') or '',
            withdrawn=tools.parse_attribute_equals(item, 'status', 'withdrawn'),
        )
        changes = False
        for attr, attr_value in update_attributes.items():
            if str(getattr(instance, attr)) != str(attr_value):
                logger.info('Sector Category %s %s changed', code, attr)
                logger.debug('%s', getattr(instance, attr))
                logger.debug('%s', attr_value)
                setattr(instance, attr, attr_value)
                changes = True
        if changes and save:
            instance.save()


def sectors(save=False):
    '''
    Pull 'sector categories' from the IATI XML and
    syncronise with our database content
    '''

    model = apps.get_model(app_label='aims', model_name='Sector')
    items = tools.xml_dict(filename='Sector.xml')

    for item in items['codelist']['codelist-items']['codelist-item']:

        code = item.get('code')

        try:
            instance = model.objects.get(pk=code)
        except model.DoesNotExist:
            instance = model()
            logger.info('Create sectos %s', code)

        update_attributes = dict(
            code=code,
            description=tools.parse_narrative(item, 'description') or '',
            name=tools.parse_narrative(item, 'name') or '',
            withdrawn=tools.parse_attribute_equals(item, 'status', 'withdrawn'),
            category_id=int(item.get('category'))
        )

        changes = False
        for attr, attr_value in update_attributes.items():
            if str(getattr(instance, attr)) != str(attr_value):
                changes = True
                logger.info('Sector %s %s changed', code, attr)
                logger.debug('%s', getattr(instance, attr))
                logger.debug('%s', attr_value)
                setattr(instance, attr, attr_value)
        if changes and save:
            instance.save()
