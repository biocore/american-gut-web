import binascii
import os
from json import dumps

from tornado.web import authenticated
from tornado.escape import url_escape

from amgut import media_locale, text_locale
from amgut.handlers.base_handlers import BaseHandler
from amgut.connections import ag_data, redis
from amgut.lib.mail import send_email


MESSAGE_TEMPLATE = """Contact: %s
        --------------------------------------------------------------------------------
        Message:
        This participant is a child, the person filling out the survey for them
        needs to provide proof of consent. Email them for proof.

        Parent/Guardian 1: %s
        Parent/Guardian 2: %s
        Deceased: %s
        Kit id: %s
        Email: %s
        --------------------------------------------------------------------------------
"""


class NewParticipantHandler(BaseHandler):
    """"""
    @authenticated
    def get(self):
        self.render("new_participant.html", skid=self.current_user)

    @authenticated
    def post(self):
        tl = text_locale['handlers']
        participant_name = self.get_argument("participant_name")
        participant_email = self.get_argument("participant_email")
        age_range = self.get_argument("age_range")
        parent_1_name = self.get_argument("parent_1_name", None)
        parent_2_name = self.get_argument("parent_2_name", None)
        obtainer_name = self.get_argument("obtainer_name", None)
        deceased_parent = self.get_argument("deceased_parent", None)

        ag_login_id = ag_data.get_user_for_kit(self.current_user)

        # If the participant already exists, stop them outright
        if ag_data.check_if_consent_exists(ag_login_id, participant_name):
            errmsg = url_escape(tl['PARTICIPANT_EXISTS'] % participant_name)
            self.redirect(media_locale['SITEBASE'] + "/authed/portal/?errmsg=%s" % errmsg)
            return

        human_survey_id = binascii.hexlify(os.urandom(8))

        consent= {'participant_name': participant_name,
                  'participant_email': participant_email,
                  'parent_1_name': parent_1_name,
                  'parent_2_name': parent_2_name,
                  'is_juvenile': True if age_range != '18-plus' else False,
                  'deceased_parent': deceased_parent,
                  'obtainer_name': obtainer_name,
                  'age_range': age_range,
                  'login_id': ag_login_id,
                  'survey_id': human_survey_id}

        redis.hset(human_survey_id, 'consent', dumps(consent))
        redis.expire(human_survey_id, 86400)

        self.set_secure_cookie('human_survey_id', human_survey_id)
        self.redirect(media_locale['SITEBASE'] + "/authed/survey_main/")
