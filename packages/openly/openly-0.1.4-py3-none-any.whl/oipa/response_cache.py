import requests
from django.core.cache import cache
import logging


logger = logging.getLogger(__name__)

RESPONSE_TIMEOUT = 20
CACHE_TIMEOUT = 60 * 60


def cache_key(url, extra_params: dict):
    '''
    Provide a cache key for response caching
    '''
    params = {'url': url}
    if extra_params:
        params.update(extra_params)

    key = hash(tuple(frozenset(sorted(params.items()))))
    return key


def cached_get(url: str, extra_params: dict = None, response_timeout=RESPONSE_TIMEOUT, cache_timeout=CACHE_TIMEOUT) -> requests.Response:
    '''
    Provide a wrapper for 'requests.get' for consistent handling of
    exceptions and cache handling
    '''

    params = {'format': 'json'}
    # Make sure we get fresh fresh data (if we're making the request; otherwise, store by cache_timeout)
    headers = {'cache_timeout': '-1', 'Cache-Control': "no-cache, no-store, must-revalidate", "max-age": "0"}

    if extra_params:
        params.update(extra_params)

    key = cache_key(url, extra_params)

    response = cache.get(key)
    if response:
        logger.debug('Cached response returned @ %s (%s)', url, str(params))
        return response

    try:
        logger.debug('Fetch response @ %s (%s)', url, str(params))
        response = requests.get(url, params=params, headers=headers, timeout=response_timeout)
    except requests.exceptions.ConnectTimeout:
        logger.error('Server timed out')
        raise

    except requests.exceptions.SSLError:
        logger.error('Server threw an error on the SSL cert')
        raise

    cache.set(key, response, cache_timeout)
    logger.debug('Cache set @ %s (%s)', url, str(params))
    logger.debug('Cache set @ %s', key)
    return cache.get(key)
