# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from json import loads
from os.path import abspath, join, dirname
from functools import partial

from future.utils import viewitems
from psycopg2 import connect

from amgut import r_server, media_locale, text_locale
from amgut.lib.human_survey_supp import question_type, supplemental_map
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


def store_survey(human_survey_id):
    """Store the survey"""
    class response_director(object):
        def __init__(self):
            self._single = {}
            self._multiple = {}
            self._text = {}

            self._setters = {'SINGLE': self._single_store,
                             'MULTIPLE': self._multiple_store,
                             'TEXT': self._text_store}

        def __setitem__(self, key, value):
            self._setters[question_type[key]](key, value)

        def _single_store(self, key, value):
            self._single[key] = value

        def _multiple_store(self, key, value):
            self._multiple[key] = value

        def _text_store(self, key, value):
            self._text[key] = value

    data = r_server.hgetall(human_survey_id)
    to_store = response_director()

    for page in data:
        page_data = loads(data[page])
        questions = page_data['questions']
        supplemental = page_data['supplemental']

        for quest, resps in viewitems(questions):
            resps = set([int(i) for i in resps])

            if quest in supplemental_map:
                indices, supp_key = supplemental_map[quest]

                if set(indices).intersection(resps):
                    to_store[supp_key] = supplemental[supp_key]
                else:
                    to_store[supp_key] = None

            to_store[quest] = resps

    # TODO: serialize and dump into the database


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
