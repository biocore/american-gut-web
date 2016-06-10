# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
import posixpath
import urlparse

from json import loads, dumps
from collections import defaultdict

from future.utils import viewitems
from tornado.escape import url_escape
from wtforms import Form

from amgut import media_locale, text_locale
from amgut.lib.data_access.sql_connection import TRN
from amgut.connections import redis
from amgut.lib.vioscreen import encrypt_key


class PartitionResponse(object):
    """Partition responses based on the response type

    Splits up the responses based on whether the response can or cannot be
    associated with a foreign key in the database.
    """
    def __init__(self, question_types):
        self.with_fk = {}
        self.without_fk = {}
        self._question_types = question_types
        self._dmap = {'SINGLE': self.with_fk,
                      'MULTIPLE': self.with_fk,
                      'TEXT': self.without_fk,
                      'STRING': self.without_fk}

    def __setitem__(self, qid, value):
        d = self._dmap[self._question_types[qid]]
        self._store(d, qid, value)

    def _store(self, d, qid, value):
        d[qid] = value


def make_survey_class(group, survey_type):
    """Creates a form class for a group of questions

    The top-level attributes of the generated class correspond to the
    question_ids from amgut.lib.human_survey_supp structures

    Select fields are generated for questions that require a single response,
    and sets of checkboxes for questions that can have multiple responses
    """
    attrs = {}
    prompts = {}
    triggers = defaultdict(list)
    triggered = defaultdict(list)

    for q in group.questions:
        for eid, element in zip(q.interface_element_ids, q.interface_elements):
            attrs[eid] = element
            prompts[eid] = q.question

            if q.triggers:
                for triggered_id, triggering_responses in q.triggers.items():
                    triggers[eid].extend(triggering_responses)
                    triggered[eid].extend(group.id_to_eid[triggered_id])

    attrs['prompts'] = prompts
    attrs['triggers'] = triggers
    attrs['triggered'] = triggered
    attrs['supplemental_eids'] = group.supplemental_eids

    return type(survey_type, (Form,), attrs)


def store_survey(survey, survey_id):
    """Store the survey

    Parameters
    ----------
    survey : amgut.lib.data_access.survey.Survey
        The corresponding survey
    survey_id : str
        The corresponding survey ID to retreive from redis
    """
    def get_survey_question_id(key):
        return int(key.split('_')[-2])

    data = redis.hgetall(survey_id)
    to_store = PartitionResponse(survey.question_types)
    consent_details = loads(data.pop('consent'))

    if 'existing' in data:
        data.pop('existing')

    for page in data:
        page_data = loads(data[page])
        questions = page_data['questions']

        for quest, resps in viewitems(questions):
            qid = get_survey_question_id(quest)
            qtype = survey.question_types[qid]

            if resps is None:
                resps = {-1}  # unspecified multiple choice
            elif qtype in ['SINGLE', 'MULTIPLE']:
                resps = set([int(i) for i in resps])
            else:
                pass

            to_store[qid] = resps

    with_fk_inserts = []
    for qid, indices in viewitems(to_store.with_fk):
        question = survey.questions[qid]

        for idx in indices:
            resp = question.responses[idx] if idx != -1 else survey.unspecified
            with_fk_inserts.append((survey_id, qid, resp))

    without_fk_inserts = [(survey_id, qid, dumps(v))
                          for qid, v in viewitems(to_store.without_fk)]

    survey.store_survey(consent_details, with_fk_inserts, without_fk_inserts)


def survey_vioscreen(survey_id):
    """Return a formatted text block and URL for the external survey"""
    tl = text_locale['human_survey_completed.html']
    embedded_text = tl['SURVEY_VIOSCREEN']
    url = ("https://vioscreen.com/remotelogin.aspx?Key=%s&RegCode=KLUCB" %
           url_escape(encrypt_key(survey_id)))
    return embedded_text % url


def survey_asd(survey_id):
    """Return a formatted text block and URL for the external survey"""
    tl = text_locale['human_survey_completed.html']
    url = media_locale['SURVEY_ASD_URL'] % {'survey_id': survey_id}
    embedded_text = tl['SURVEY_ASD']
    return embedded_text % url


external_surveys = (survey_vioscreen,)  # survey_asd)


def rollback(f):
    """Decorator for test functions to rollback on complete."""
    def inner(*args, **kwargs):
        with TRN:
            f(*args, **kwargs)
            TRN.rollback()


def basejoin(base, url):
    """
    Add the specified relative URL to the supplied base URL.

    >>> tests = [
    ...     ('https://abc.xyz',    'd/e'),
    ...     ('https://abc.xyz/',   'd/e'),
    ...     ('https://abc.xyz',    '/d/e'),
    ...     ('https://abc.xyz/',   '/d/e'),
    ...
    ...     ('https://abc.xyz',    '/d/e?a=b'),
    ...     ('https://abc.xyz/',   '/d/e?a=b'),
    ...
    ...     ('https://abc.xyz',    'd/e/'),
    ...     ('https://abc.xyz/',   'd/e/'),
    ...     ('https://abc.xyz',    '/d/e/'),
    ...     ('https://abc.xyz/',   '/d/e/'),
    ...
    ...     ('https://abc.xyz',    'd/e/?a=b'),
    ...     ('https://abc.xyz/',   'd/e/?a=b'),
    ...
    ...     ('https://abc.xyz/f',  'd/e/'),
    ...     ('https://abc.xyz/f/', 'd/e/'),
    ...     ('https://abc.xyz/f',  '/d/e/'),
    ...     ('https://abc.xyz/f/', '/d/e/'),
    ...
    ...     ('https://abc.xyz/f',  './e/'),
    ...     ('https://abc.xyz/f/', './e/'),
    ...
    ...     ('https://abc.xyz/f',  '../e/'),
    ...     ('https://abc.xyz/f/', '../e/'),
    ...
    ...     ('https://abc.xyz/f',  'd/../e/'),
    ...     ('https://abc.xyz/f/', 'd/../e/'),
    ...     ('https://abc.xyz/f',  '/d/../e/'),
    ...     ('https://abc.xyz/f/', '/d/../e/'),
    ... ]
    >>> for result in [basejoin(a, b) for a, b in tests]:
    ...     print result
    https://abc.xyz/d/e
    https://abc.xyz/d/e
    https://abc.xyz/d/e
    https://abc.xyz/d/e
    https://abc.xyz/d/e?a=b
    https://abc.xyz/d/e?a=b
    https://abc.xyz/d/e/
    https://abc.xyz/d/e/
    https://abc.xyz/d/e/
    https://abc.xyz/d/e/
    https://abc.xyz/d/e/?a=b
    https://abc.xyz/d/e/?a=b
    https://abc.xyz/f/d/e/
    https://abc.xyz/f/d/e/
    https://abc.xyz/f/d/e/
    https://abc.xyz/f/d/e/
    https://abc.xyz/f/e/
    https://abc.xyz/f/e/
    https://abc.xyz/f/e/
    https://abc.xyz/f/e/
    https://abc.xyz/f/e/
    https://abc.xyz/f/e/
    https://abc.xyz/f/e/
    https://abc.xyz/f/e/
    """
    # The base URL is authoritative: a URL like '../' should not remove
    # portions of the base URL.
    if not base.endswith('/'):
        base += '/'

    # Handle internal compactions, e.g. "./e/../d/" becomes "./d/"
    normalized_url = posixpath.normpath(url)

    # Ditto authoritativeness.
    if normalized_url.startswith('..'):
        normalized_url = normalized_url[2:]

    # Ditto authoritativeness.
    if normalized_url.startswith('/'):
        normalized_url = '.' + normalized_url

    # normpath removes an ending slash, add it back if necessary
    if url.endswith('/') and not normalized_url.endswith('/'):
        normalized_url += '/'

    join = urlparse.urljoin(base, normalized_url)
    joined_url = urlparse.urlparse(join)

    return urlparse.urlunparse((joined_url.scheme,
                                joined_url.netloc,
                                joined_url.path,
                                joined_url.params,
                                joined_url.query,
                                joined_url.fragment))


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True, optionflags=(doctest.NORMALIZE_WHITESPACE |
                                               doctest.REPORT_NDIFF))
