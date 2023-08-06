# pylint: disable=W0221,W0223
import logging

from django.conf import settings
from django.utils import translation
from haystack import connections
from haystack.backends.whoosh_backend import WhooshEngine, WhooshSearchBackend, WhooshSearchQuery
from haystack.constants import DEFAULT_ALIAS


logger = logging.getLogger(__file__)


""" Extend Whoosh to provide support for multilingual fields.

This code is mostly taken from this blog post:
http://anthony-tresontani.github.io/Django/2012/09/20/multilingual-search/
"""


def get_using(language: str, alias: str = DEFAULT_ALIAS):
    """ Return the name of the backend for a given language. """
    new_using = alias + "_" + language
    using = new_using if new_using in settings.HAYSTACK_CONNECTIONS else alias
    return using


class MultilingualWhooshBackend(WhooshSearchBackend):
    def update(self, index, iterable, commit: bool = True, multilingual: bool = True):
        if multilingual:
            # if the language hasn't been set then use the default language
            initial_language = translation.get_language()
            if initial_language is None:
                initial_language = settings.LANGUAGE_CODE
            try:
                # retrieve unique backend name for each language and set translated
                # search indexes
                backends = set()
                for language, __ in settings.LANGUAGES:
                    using = get_using(language, alias=self.connection_alias)
                    # Ensure each backend is called only once
                    if using in backends:
                        continue
                    else:
                        backends.add(using)
                    translation.activate(language)
                    backend = connections[using].get_backend()
                    backend.update(index, iterable, commit, multilingual=False)
            finally:
                # Always revert back to language from caller's context
                translation.activate(initial_language)
        else:
            super(MultilingualWhooshBackend, self).update(index, iterable, commit)


class MultilingualWhooshQuery(WhooshSearchQuery):
    def __init__(self, using: str = DEFAULT_ALIAS):
        # if the language hasn't been set then use the default language
        language = translation.get_language()
        if language is None:
            language = settings.LANGUAGE_CODE
        using = get_using(language)
        super(MultilingualWhooshQuery, self).__init__(using)


class MultilingualWhooshEngine(WhooshEngine):
    backend = MultilingualWhooshBackend
    query = MultilingualWhooshQuery
