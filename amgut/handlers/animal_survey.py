import binascii
import os

from tornado.web import authenticated
from tornado.escape import url_escape
from tornado.websocket import WebSocketHandler
import tornado.gen as gen

from amgut.handlers.util import as_transaction
from amgut.handlers.base_handlers import BaseHandler
from amgut.connections import ag_data
from amgut import text_locale, media_locale
from amgut.lib.config_manager import AMGUT_CONFIG
from amgut.lib.data_access.redcap import get_survey_url, create_record


class AnimalSurveyHandler(BaseHandler):
    @authenticated
    def get(self):
        skid = self.current_user
        self.render('animal_survey.html', skid=skid,
                    default_lang=media_locale['DEFAULT_LANGUAGE'])

    @authenticated
    @as_transaction
    @gen.coroutine
    def post(self):
        skid = self.current_user
        tl = text_locale['handlers']
        ag_login_id = ag_data.get_user_for_kit(skid)
        ag_login_info = ag_data.get_login_info(ag_login_id)[0]

        participant_name = self.get_argument('name')
        language = self.get_argument('language')

        # If the participant already exists, stop them outright
        if ag_data.check_if_consent_exists(ag_login_id, participant_name):
            errmsg = url_escape(tl['PARTICIPANT_EXISTS'] % participant_name)
            url = AMGUT_CONFIG.sitebase + "/authed/portal/?errmsg=%s" % errmsg
            self.redirect(url)
            return

        consent = {
            'login_id': ag_login_id,
            'participant_name': participant_name,
            'participant_email': ag_login_info['email'],
            'assent_obtainer': 'ANIMAL_SURVEY',
            'parent_1_name': 'ANIMAL_SURVEY',
            'parent_2_name': 'ANIMAL_SURVEY',
            'is_juvenile': True,
            'deceased_parent': False,
            'obtainer_name': 'ANIMAL_SURVEY',
            'age_range': 'ANIMAL_SURVEY',
            'language': language,
            'type': 'animal'
        }

        # Save consent info and redirect to redcap
        instrument = 'ag-animal-' + language
        record_id = ag_data.store_consent(consent)
        yield create_record(record_id, consent['login_id'],
                            consent['participant_name'])
        survey_id = binascii.hexlify(os.urandom(8))
        url = yield get_survey_url(record_id, instrument=instrument)
        url = "%s&survey_id=%s&portal=%s" % (url, survey_id,
                                             AMGUT_CONFIG.sitebase)
        self.redirect(url)


class CheckParticipantName(WebSocketHandler, BaseHandler):
    @authenticated
    def on_message(self, msg):
        tl = text_locale['handlers']
        skid = self.current_user
        participant_name = msg

        ag_login_id = ag_data.get_user_for_kit(skid)
        human_participants = ag_data.getHumanParticipants(ag_login_id)
        animal_participants = ag_data.getAnimalParticipants(ag_login_id)

        if participant_name in (human_participants + animal_participants):
            # if the participant already exists in the system, fail nicely
            output_message = (tl['PARTICIPANT_EXISTS'] % participant_name)
        else:
            # otherwise, success!
            output_message = 'success'

        self.write_message(output_message)
