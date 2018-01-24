#!/usr/bin/env python
# encoding: utf-8
from django.conf import settings
from .utils import logger, cache


def seo_processor(requests):
    key = 'seo_processor'
    value = cache.get(key)
    if value:
        logger.info('get processor cache.')
        return value
    else:

        logger.info('set processor cache.')
        value = {
            'SITE_URL' : settings.SITE_URL,
            'SITE_NAME': settings.SITE_NAME,
            'SITE_KEYWORDS': settings.SITE_SEO_KEYWORDS,
            'SITE_BASE_URL': requests.scheme + '://' + requests.get_host() + '/',

        }
        cache.set(key, value, 60 * 60 * 10)
        return value
