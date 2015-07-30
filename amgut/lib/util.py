# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from json import loads, dumps
from collections import defaultdict

from future.utils import viewitems
from tornado.escape import url_escape
from wtforms import Form

from amgut import media_locale, text_locale
from amgut.connections import ag_data, redis
from amgut.lib.config_manager import AMGUT_CONFIG
from amgut.lib.vioscreen import encrypt_key
from amgut.lib.data_access.env_management import (
    create_database, build_and_initialize, make_settings_table, patch_db,
    populate_test_db, drop_schema)


def reset_test_database(wrapped_fn):
    """Decorator that drops the public schema, rebuilds and repopulates the
    schema with test data, then executes wrapped_fn
    """

    def decorated_wrapped_fn(*args, **kwargs):
        drop_schema()
        build_and_initialize()
        make_settings_table()
        patch_db()
        populate_test_db()

        return wrapped_fn(*args, **kwargs)

    return decorated_wrapped_fn


def ag_test_checker():
    """Decorator that allows the execution of all methods in a test class only
    and only if the AG site is set up to work in a test environment

    Raises
    ------
    RuntimeError
        If the AG site is set up to work in a production environment
    """
    def class_modifier(cls):
        # First, we check that we are not in a production environment
        if not AMGUT_CONFIG.test_environment \
                or AMGUT_CONFIG.database != "ag_test":
            raise RuntimeError("Working in a production environment. Not "
                               "executing the tests to keep the production "
                               "database safe.")

        # Now, we decorate the setup and teardown functions
        class DecoratedClass(cls):
            def setUp(self):
                super(DecoratedClass, self).setUp()

            @reset_test_database
            def tearDown(self):
                super(DecoratedClass, self).tearDown()
        return DecoratedClass
    return class_modifier


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

    The top-level attributes of the generated class correspond to the question_ids from
    amgut.lib.human_survey_supp structures

    Select fields are generated for questions that require a single response, and sets
    of checkboxes for questions that can have multiple responses
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
    user_info = ag_data.get_person_info(survey_id)
    url = ("https://vioscreen.com/remotelogin.aspx?Key=%s&RegCode=KLUCB" %
           url_escape(encrypt_key(survey_id, user_info)))
    return embedded_text % url


def survey_asd(survey_id):
    """Return a formatted text block and URL for the external survey"""
    tl = text_locale['human_survey_completed.html']
    url = media_locale['SURVEY_ASD_URL'] % {'survey_id': survey_id}
    embedded_text = tl['SURVEY_ASD']
    return embedded_text % url


external_surveys = (survey_vioscreen, survey_asd)
