#!/usr/bin/env python
# coding: utf-8

# In[1]:

'''
Import data from an IATI XML file to an AIMS model
Prerequisites:
python3 -m pip install requests xmltodict
'''

import functools
import xmltodict
import requests

# Codelist sites: from reference or github
# CODELIST_URL = 'http://reference.iatistandard.org/202/codelists/downloads/clv3/xml/'
CODELIST_URL = 'https://raw.githubusercontent.com/IATI/IATI-Codelists-NonEmbedded/master/xml/'


def parse_narrative(thing: dict, narrative_field: str) -> str:
    '''
    A Narrative might be a string or a list or none
    When it is a list the first element is usually a simple string; the second element is
    a DefaultDict of translations

    Returns a string or None
    '''
    narrative = thing.get(narrative_field).get('narrative')
    if narrative is None:
        return None
    elif isinstance(narrative, list):
        return narrative[0]
    elif isinstance(narrative, str):
        return narrative
    raise TypeError('unhandled narrative type')


def parse_attribute_equals(thing: dict, attribute: str, value: str) -> bool:
    '''
    Compare an 'attribute' to a given value
    '''
    return thing.get('@%s' % (attribute,)) == value


@functools.lru_cache(maxsize=128)
def xml_dict(filename: str = 'Sector.xml') -> dict:
    '''
    Returns XML parsed as Python objects
    '''
    file = requests.get(CODELIST_URL + filename)
    data = file.text
    assert file.status_code == 200, 'Request did not return a 200'
    file.close()
    return xmltodict.parse(data)
