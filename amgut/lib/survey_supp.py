import re
from collections import defaultdict

from future.utils import viewitems

from amgut import text_locale
from amgut.lib.data_access.survey import Survey

primary_human_survey = Survey(1)
