#!/usr/bin/env python
from __future__ import division

# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Project Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------


# Any media specific localizations
media_locale = {'LOGO': '/static/img/british_gut_logo.jpg',
                'PROJECT_TITLE': 'British Gut Project'}

_FAQ = {}
_TAXA_SUMMARY = {}
_HELP_REQUEST = {}
_DB_ERROR = {}
_404 = {}
_PARTICIPANT_OVERVIEW = {}
_ADD_SAMPLE_OVERIVIEW = {}
_SAMPLE_OVERVIEW = {}
_NEW_PARTICIPANT_OVERVIEW = {}
_INTERNATIONAL = {}
_NEW_PARTICIPANT = {}
_MAP = {}
_FORGOT_PASSWORD = {}
_ERROR = {}
_RETREIVE_KITID = {}
_ADD_SAMPLE = {}
_REGISTER_USER = {}
_ADDENDUM = {}
_PORTAL = {}
_CHANGE_PASS_VERIFY = {}
_SURVEY_MAIN = {}

# Actual text locale
text_locale = {
    '404.html': _404,
    'FAQ.html': _FAQ,
    'new_participant_overview.html': _NEW_PARTICIPANT_OVERVIEW,
    'addendum.html': _ADDENDUM,
    'portal.html': _PORTAL,
    'db_error.html': _DB_ERROR,
    'retrieve_kitid.html': _RETREIVE_KITID,
    'add_sample.html': _ADD_SAMPLE,
    'error.html': _ERROR,
    'forgot_password.html': _FORGOT_PASSWORD,
    'help_request.html': _HELP_REQUEST,
    'new_participant.html': _NEW_PARTICIPANT,
    'international.html': _INTERNATIONAL,
    'add_sample_overview.html': _ADD_SAMPLE_OVERIVIEW,
    'participant_overview.html': _PARTICIPANT_OVERVIEW,
    'sample_overview.html': _SAMPLE_OVERVIEW,
    'taxa_summary.html': _TAXA_SUMMARY,
    'map.html': _MAP,
    'register_user.html': _REGISTER_USER,
    'chage_pass_verify.html': _CHANGE_PASS_VERIFY,
    'survey_main.html': _SURVEY_MAIN
}
