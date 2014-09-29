#!/usr/bin/env python
from __future__ import division

# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Project Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------


# Template specific dicts
_FAQ = {'FAQ_0_WHAT_IS_A_GUT': 'asdasdasd'}
_HELP_REQUEST = {
    'CONTACT_HEADER': "Contact the American Gut",
    'RESPONSE_TIMING': "We will send a response to the email address you supply within 24 hours.",
    'FIRST_NAME': "First name",
    'LAST_NAME': "Last name",
    'EMAIL_ADDRESS': "Email address",
    'PROBLEM_PROMPT': "Enter information related to your problem"
}
_DB_ERROR = {
    'HEADER': 'Oops! There seems to be a database error.',
    'MESSAGE': 'Please help us to debug by emailing us at <a href="mailto:%(help_email)s">%(help_email)s</a> and tell us exactly what happend before you got this error.',
    'SIGNOFF': 'Thanks, <br /> The American Gut Team'
}

# Actual text locale
text_locale = {
    'FAQ.html': _FAQ,
    'help_request.html': _HELP_REQUEST,
    'db_error.html': _DB_ERROR
    }

# Any media specific localizations
media_locale = {'logo': '/static/img/ag_logo.jpg'}
