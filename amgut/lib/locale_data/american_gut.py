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

# Actual text locale
text_locale = {
    'FAQ.html': _FAQ,
    'help_request.html': _HELP_REQUEST
    }

# Any media specific localizations
media_locale = {'logo': '/static/img/ag_logo.jpg'}
