''' Module for sharing common text values throughout openly

Allows overwriting for individual projects by specifying in the settings:
COMMON_TEXT_OVERRIDE = 'myproject.my_common_text_module'

Which should be a python path to an importable python module which defines individual
attributes to be used instead of base openly strings, just like ./common_text.py in this module
Only override the strings you need to change, if not defined in the override module
the string is read from the openly ./common_text.py in this module
'''
from django.conf import settings
from . import common_text
from importlib import import_module

from typing import Sequence, Dict

common_text_module = None
common_text_module_path = getattr(settings, 'COMMON_TEXT_OVERRIDE', None)
if common_text_module_path:
    common_text_module = import_module(common_text_module_path)


def get_dict(*args: Sequence[str], lazy: bool = False) -> Dict[str, str]:
    ''' returns a dict containing values for all the strings passed in args'''
    return {f'{key}': get(f'{key}', lazy=lazy) for key in args}


def get(key: str, lazy: bool = False) -> str:
    ''' returns the value for given key forcing to string unless lazy is True '''
    key_as_str = '%s' % (key,)
    if common_text_module and hasattr(common_text_module, key_as_str):
        value = getattr(common_text_module, key_as_str)
    else:
        value = getattr(common_text, key_as_str)
    return value if lazy else str(value)
