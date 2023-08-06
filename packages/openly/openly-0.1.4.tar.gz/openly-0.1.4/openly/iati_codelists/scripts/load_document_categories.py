#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xml.etree.ElementTree as ET
import urllib3
from django.apps import apps
import logging
logger = logging.getLogger(__name__)

# For debugging purposes, you may want to add this to settings.py as LOGGING['loggers']['iati_codelists']
# { 'handlers': ['console'], 'level': 'DEBUG','propagate': True, },

# In[2]:


ns = {'xml': 'http://www.w3.org/XML/1998/namespace', }
language_field = '{%s}lang' % (ns['xml'])
default_language = 'en'


# In[3]:


def codelist_url(codelist_name: str) -> str:
    root = 'http://reference.iatistandard.org/203/codelists/downloads/clv3/xml/'
    return '%s%s.xml' % (root, codelist_name)


# In[4]:


def get(url: str) -> str:
    logger.info('Fetching %s' % (url,))
    try:
        http = urllib3.PoolManager()
        r = http.request('GET', url)
        assert r.status == 200
    except Exception as e:
        logger.error(e, exc_info=True)
        raise
    return r.data


# In[8]:


def documentcategorycategories():
    logger.info('Fetching codelist')
    content = get(codelist_url('DocumentCategory-category'))
    root = ET.fromstring(content)
    item_root = root.find('codelist-items')
    items = item_root.findall('codelist-item')
    logger.info('Loading codelist items')

    categories = []
    try:
        for i in items:
            item = {}
            for n in i.findall('./name/narrative', ns):
                lang = n.attrib.get(language_field, default_language)
                item['name_%s' % (lang,)] = n.text

            for n in i.findall('./name/description', ns):
                lang = n.attrib.get(language_field, default_language)
                item['description_%s' % (lang,)] = n.text

            item['code'] = i.find('./code').text
            item['name'] = item.pop('name_en')
            categories.append(item)

            # Do an update/create
            model = apps.get_model('aims', 'DocumentCategoryCategory')
            model.objects.get_or_create(pk=item['code'], defaults=item)[0]
            model.objects.filter(pk=item['code']).update(**item)
    except Exception as e:
        logger.error(e, exc_info=True)
        raise
    return categories


# In[9]:


def document_categories():
    logger.info('Fetching DocumentCategory codelist')
    try:
        content = get(codelist_url('DocumentCategory'))
        root = ET.fromstring(content)
        item_root = root.find('codelist-items')
        items = item_root.findall('codelist-item')
    except Exception as e:
        logger.error(e, exc_info=True)
        raise

    logger.info('Loading items')

    categories = []
    try:
        for i in items:
            item = {}
            for n in i.findall('./name/narrative', ns):
                lang = n.attrib.get(language_field, default_language)
                item['name_%s' % (lang,)] = n.text

            for n in i.findall('./name/description', ns):
                lang = n.attrib.get(language_field, default_language)
                item['description_%s' % (lang,)] = n.text

            item['code'] = i.find('./code').text
            item['category_id'] = i.find('./category').text

            item.pop('name_fr')
            item.pop('description_fr', '')
            categories.append(item)

            # Do an update/create
            model = apps.get_model('aims', 'DocumentCategory')
            model.objects.get_or_create(pk=item['code'], defaults=item)[0]
            model.objects.filter(pk=item['code']).update(**item)
    except Exception as e:
        logger.error(e, exc_info=True)
        raise
    return categories


# In[10]:


def run():
    documentcategorycategories()
    document_categories()
