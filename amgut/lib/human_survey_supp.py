import re
from collections import defaultdict
from future.utils import viewitems
from amgut import text_locale

# {idx: actual question} or {int: str}
question_map = {}

# {idx: possible choices} or {int: tuple}
responses_map = {}

# {idx: key of question} or {int: str}
key_map = {}

# {question group: idx} or {str: list of int}
question_group = defaultdict(list)

# the question group order according to the approved questionnaire
group_order = ['GENERAL_DIET', 'GENERAL', 'LIFESTYLE_HYGIENE', 'HEALTH',
               'DETAILED_DIET']

question_idx = re.compile('([0-9.]+)')
for text_key, values in viewitems(text_locale['human_survey.html']):
    if (text_key.startswith('SUPPLEMENT')
            or text_key.startswith('PERSONAL')
            or text_key.endswith('TITLE')):
        continue

    idx = float(question_idx.search(text_key).group(1))
    if text_key.endswith('CHOICES'):
        responses_map[idx] = values
    else:
        question_map[idx] = values
        key_map[idx] = text_key
        group = text_key.split('_QUESTION_', 1)[0]
        question_group[group].append(idx)

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
    'HEALTH_QUESTION_51.23':
        ((2, 3, 4,), 'SUPPLEMENTAL_OTHER_CONDITIONS'),  # triggered on Other
    }

# associates the question with its type, where SINGLE is a question with only
# a single response and MULTIPLE is a question that can have multiple
# responses.
question_type = {
    'GENERAL_DIET_QUESTION_0': 'SINGLE',
    'GENERAL_DIET_QUESTION_1': 'SINGLE',
    'GENERAL_DIET_QUESTION_2': 'SINGLE',
    'GENERAL_DIET_QUESTION_3': 'SINGLE',
    'GENERAL_DIET_QUESTION_4': 'SINGLE',
    'GENERAL_DIET_QUESTION_5': 'SINGLE',
    'GENERAL_DIET_QUESTION_6': 'SINGLE',
    'GENERAL_DIET_QUESTION_7': 'SINGLE',
    'GENERAL_DIET_QUESTION_8': 'MULTIPLE',
    'GENERAL_DIET_QUESTION_9': 'SINGLE',
    'GENERAL_DIET_QUESTION_10': 'SINGLE',
    'GENERAL_DIET_QUESTION_11': 'SINGLE',
    'GENERAL_DIET_QUESTION_12': 'SINGLE',
    'GENERAL_QUESTION_13': 'SINGLE',
    'GENERAL_QUESTION_14': 'SINGLE',
    'GENERAL_QUESTION_15': 'SINGLE',
    'GENERAL_QUESTION_16': 'SINGLE',
    'GENERAL_QUESTION_17': 'SINGLE',
    'GENERAL_QUESTION_18': 'SINGLE',
    'GENERAL_QUESTION_19': 'SINGLE',
    'GENERAL_QUESTION_20': 'SINGLE',
    'GENERAL_QUESTION_21': 'SINGLE',
    'GENERAL_QUESTION_22': 'SINGLE',
    'LIFESTYLE_HYGIENE_QUESTION_23': 'SINGLE',
    'LIFESTYLE_HYGIENE_QUESTION_24': 'SINGLE',
    'LIFESTYLE_HYGIENE_QUESTION_25': 'SINGLE',
    'LIFESTYLE_HYGIENE_QUESTION_26': 'SINGLE',
    'LIFESTYLE_HYGIENE_QUESTION_27': 'SINGLE',
    'LIFESTYLE_HYGIENE_QUESTION_28': 'SINGLE',
    'LIFESTYLE_HYGIENE_QUESTION_29': 'MULTIPLE',
    'LIFESTYLE_HYGIENE_QUESTION_30': 'SINGLE',
    'LIFESTYLE_HYGIENE_QUESTION_31': 'SINGLE',
    'LIFESTYLE_HYGIENE_QUESTION_32': 'SINGLE',
    'LIFESTYLE_HYGIENE_QUESTION_33': 'SINGLE',
    'LIFESTYLE_HYGIENE_QUESTION_34': 'SINGLE',
    'LIFESTYLE_HYGIENE_QUESTION_35': 'SINGLE',
    'HEALTH_QUESTION_36': 'SINGLE',
    'HEALTH_QUESTION_37': 'SINGLE',
    'HEALTH_QUESTION_38': 'SINGLE',
    'HEALTH_QUESTION_39': 'SINGLE',
    'HEALTH_QUESTION_40': 'SINGLE',
    'HEALTH_QUESTION_41': 'SINGLE',
    'HEALTH_QUESTION_42': 'SINGLE',
    'HEALTH_QUESTION_43': 'SINGLE',
    'HEALTH_QUESTION_44': 'SINGLE',
    'HEALTH_QUESTION_45': 'SINGLE',
    'HEALTH_QUESTION_46': 'SINGLE',
    'HEALTH_QUESTION_47': 'SINGLE',
    'HEALTH_QUESTION_48': 'SINGLE',
    'HEALTH_QUESTION_49': 'SINGLE',
    'HEALTH_QUESTION_50': 'SINGLE',
    'HEALTH_QUESTION_51.03': 'SINGLE',
    'HEALTH_QUESTION_51.04': 'SINGLE',
    'HEALTH_QUESTION_51.05': 'SINGLE',
    'HEALTH_QUESTION_51.06': 'SINGLE',
    'HEALTH_QUESTION_51.07': 'SINGLE',
    'HEALTH_QUESTION_51.08': 'SINGLE',
    'HEALTH_QUESTION_51.09': 'SINGLE',
    'HEALTH_QUESTION_51.10': 'SINGLE',
    'HEALTH_QUESTION_51.11': 'SINGLE',
    'HEALTH_QUESTION_51.12': 'SINGLE',
    'HEALTH_QUESTION_51.13': 'SINGLE',
    'HEALTH_QUESTION_51.14': 'SINGLE',
    'HEALTH_QUESTION_51.15': 'SINGLE',
    'HEALTH_QUESTION_51.16': 'SINGLE',
    'HEALTH_QUESTION_51.17': 'SINGLE',
    'HEALTH_QUESTION_51.18': 'SINGLE',
    'HEALTH_QUESTION_51.19': 'SINGLE',
    'HEALTH_QUESTION_51.20': 'SINGLE',
    'HEALTH_QUESTION_51.21': 'SINGLE',
    'HEALTH_QUESTION_51.22': 'SINGLE',
    'HEALTH_QUESTION_51.23': 'SINGLE',
    'HEALTH_QUESTION_53': 'SINGLE',
    'HEALTH_QUESTION_54': 'SINGLE',
    'HEALTH_QUESTION_55': 'MULTIPLE',
    'DETAILED_DIET_QUESTION_56': 'SINGLE',
    'DETAILED_DIET_QUESTION_57': 'SINGLE',
    'DETAILED_DIET_QUESTION_58': 'SINGLE',
    'DETAILED_DIET_QUESTION_59': 'SINGLE',
    'DETAILED_DIET_QUESTION_60': 'SINGLE',
    'DETAILED_DIET_QUESTION_61': 'SINGLE',
    'DETAILED_DIET_QUESTION_62': 'SINGLE',
    'DETAILED_DIET_QUESTION_63': 'SINGLE',
    'DETAILED_DIET_QUESTION_64': 'SINGLE',
    'DETAILED_DIET_QUESTION_65': 'SINGLE',
    'DETAILED_DIET_QUESTION_66': 'SINGLE',
    'DETAILED_DIET_QUESTION_67': 'SINGLE',
    'DETAILED_DIET_QUESTION_68': 'SINGLE',
    'DETAILED_DIET_QUESTION_69': 'SINGLE',
    'DETAILED_DIET_QUESTION_70': 'SINGLE',
    'DETAILED_DIET_QUESTION_71': 'SINGLE',
    'DETAILED_DIET_QUESTION_72': 'SINGLE',
    'DETAILED_DIET_QUESTION_73': 'SINGLE',
    'DETAILED_DIET_QUESTION_74': 'SINGLE',
    'DETAILED_DIET_QUESTION_75': 'SINGLE',
    'DETAILED_DIET_QUESTION_76': 'SINGLE',
    'DETAILED_DIET_QUESTION_77': 'SINGLE'}
