from .load_document_categories import get, codelist_url
import xml.etree.ElementTree as ET
from django.apps import apps
import logging
logger = logging.getLogger(__name__)


def run():
    try:
        logger.info('Fetching codelist')
        content = get(codelist_url('FileFormat'))
        root = ET.fromstring(content)
        item_root = root.find('codelist-items')
        items = item_root.findall('codelist-item')
        logger.info('Loading codelist items')
    except Exception as e:
        logger.error(e, exc_info=True)
        raise

    categories = []
    try:
        for i in items:
            item = {
                'code': i.find('./code').text,
                'name': i.find('./code').text
            }

            # Do an update/create
            model = apps.get_model('aims', 'FileFormat')
            model.objects.get_or_create(pk=item['code'], defaults=item)[0]
            model.objects.filter(pk=item['code']).update(**item)
    except Exception as e:
        logger.error(e, exc_info=True)
        raise
    return categories
