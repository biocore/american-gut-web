#!/usr/bin/env python
from __future__ import division

# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Project Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

import importlib

from amgut.lib.config_manager import AMGUT_CONFIG
from amgut.lib.locale_data import media_locale
from redis import Redis

r_server = Redis(host=AMGUT_CONFIG.redis_host,
                 port=AMGUT_CONFIG.redis_port,
                 db=AMGUT_CONFIG.redis_db_id)

current_locale_module = '.'.join(['amgut.lib.locale_data',
                                  AMGUT_CONFIG.locale])

try:
    current_locale = importlib.import_module(current_locale_module)
except ImportError:
    raise ImportError("Cannot import locale! %s" % current_locale_module)

text_locale = current_locale.text_locale
media_locale.update(current_locale.media_locale)

__all__ = ['r_server', 'text_locale', 'media_locale', 'AMGUT_CONFIG']
