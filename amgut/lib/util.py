# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from json import loads, dumps
from os.path import abspath, join, dirname
from functools import partial

from future.utils import viewitems
from psycopg2 import connect

from amgut import r_server, media_locale, text_locale, db_conn
from amgut.lib.config_manager import AMGUT_CONFIG

get_db_file = partial(join, join(dirname(dirname(abspath(__file__))), 'db'))
LAYOUT_FP = get_db_file('ag.sql')
INITIALIZE_FP = get_db_file('initialize.sql')
POPULATE_FP = get_db_file('populate_test.sql')


def reset_test_database(wrapped_fn):
    """Decorator that drops the public schema, rebuilds and repopulates the
    schema with test data, then executes wrapped_fn
    """

    def decorated_wrapped_fn(*args, **kwargs):
        conn = connect(user=AMGUT_CONFIG.user, password=AMGUT_CONFIG.password,
                       host=AMGUT_CONFIG.host, port=AMGUT_CONFIG.port,
                       database=AMGUT_CONFIG.database)
        cur = conn.cursor()
        # Drop the schema
        # cur.execute("DROP SCHEMA public CASCADE")

        # Create the public schema
        # cur.execute("CREATE SCHEMA public")

        # Build the SQL layout
        # with open(LAYOUT_FP, 'U') as f:
        #     cur.execute(f.read())

        # Initialize the test db
        # with open(INITIALIZE_FP) as f:
        #     cur.execute(f.read)

        # Populate the test db
        # with open(POPULATE_FP) as f:
        #     cur.execute(f.read)

        conn.commit()
        cur.close()
        conn.close()

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

    data = r_server.hgetall(survey_id)
    to_store = PartitionResponse(survey.question_types)
    consent_details = loads(data.pop('consent'))

    for page in data:
        page_data = loads(data[page])
        questions = page_data['questions']
        #supplemental = page_data['supplemental']

        for quest, resps in viewitems(questions):
            qid = get_survey_question_id(quest)
            qtype = survey.question_types[qid]

            if resps is None:
                resps = {-1} # unspecified multiple choice
            elif qtype in ['SINGLE', 'MULTIPLE']:
                resps = set([int(i) for i in resps])
            else:
                pass

            #if qtype in ['SINGLE', 'MULTIPLE'] and quest in supplemental_map:
            #    indices, supp_key = supplemental_map[quest]
#
 #               if set(indices).intersection(resps):
  #                  to_store[supp_qid] = supplemental[supp_qid]
   #             else:
    #                to_store[supp_qid] = None

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
    url = media_locale['SURVEY_VIOSCREEN_URL'] % {'survey_id': survey_id}
    embedded_text = tl['SURVEY_VIOSCREEN']
    return embedded_text % url


def survey_asd(survey_id):
    """Return a formatted text block and URL for the external survey"""
    tl = text_locale['human_survey_completed.html']
    url = media_locale['SURVEY_ASD_URL'] % {'survey_id': survey_id}
    embedded_text = tl['SURVEY_ASD']
    return embedded_text % url


# external_surveys = (survey_vioscreen, survey_asd)
external_surveys = (survey_asd, )
