#!/usr/bin/env python


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

current_locale_module = '.'.join(['amgut.lib.locale_data',
                                  AMGUT_CONFIG.locale])

try:
    current_locale = importlib.import_module(current_locale_module)
except ImportError:
    raise ImportError("Cannot import locale! %s" % current_locale_module)

text_locale = current_locale.text_locale
media_locale.update(current_locale.media_locale)

__all__ = ['text_locale', 'media_locale', 'AMGUT_CONFIG']
