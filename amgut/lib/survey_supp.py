import re
from future.utils import viewitems
from amgut import text_locale

question_map = {}  # {idx: actual question} or {int: str}
responses_map = {}  # {idx: possible choices} or {int: tuple}
key_map = {}  # {idx: key of question} or {int: str}
question_group = {}  # {idx: question group} or {int : str}

question_idx = re.compile('([0-9]+)')
for text_key, values in viewitems(text_locale['human_survey.html']):
    if text_key.startswith('SUPPLEMENT') or text_key.startswith('PERSONAL'):
        continue

    idx = int(question_idx.search(text_key).group(1))
    if text_key.endswith('CHOICES'):
        responses_map[idx] = values
    else:
        question_map[idx] = values
        key_map[idx] = text_key
        group = text_key.split('_QUESTION_', 1)[0]
        question_group[idx] = group

# some responses trigger supplemental questions. This structure provides an
# association between the question, what responses trigger, and what ID is
# to be triggered if that response is made

# the responses are all indices, where 0 corresponses to _NO_RESPONSE
supplemental_map = {
    'GENERAL_DIET_QUESTION_5':
        ((1,), 'SUPPLEMENTAL_MEDICATION'),  # triggered on Yes
    'GENERAL_DIET_QUESTION_11':
        ((1,), 'SUPPLEMENTAL_DIET'),  # triggered on Yes
    'GENERAL_QUESTION_13':
        ((5,), 'SUPPLEMENTAL_RICE'),  # triggered on Other
    'GENERAL_QUESTION_15':
        ((1, 2, 3), 'SUPPLEMENTAL_TRAVEL'),  # triggered on Month, 3 months, 6 months
    'GENERAL_QUESTION_17':
        ((1,), 'SUPPLEMENTAL_RELATIONSHIP'),  # triggered on Yes
    'GENERAL_QUESTION_19':
        ((1,), 'SUPPLEMENTAL_PETS'),  # triggered on Yes
    'GENERAL_QUESTION_20':
        ((1,), 'SUPPLEMENTAL_PETS'),  # triggered on Yes
    'HEALTH_QUESTION_38':
        ((1, 2), 'SUPPLEMENTAL_ANTIBIOTICS'),  # triggered on Week, Month
    'HEALTH_QUESTION_41':
        ((1,), 'SUPPLEMENTAL_PREGNANCY'),  # triggered on Yes
    'HEALTH_QUESTION_48':
        ((1,), 'SUPPLEMENTAL_MEDICATION'),  # triggered on Yes
    'HEALTH_QUESTION_51':
        ((23,), 'SUPPLEMENTAL_OTHER_CONDITIONS'),  # triggered on Other
    }

