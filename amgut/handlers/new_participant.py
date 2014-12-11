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
        deceased_parent = self.get_argument("deceased_parent", None)
        participant_name = self.get_argument("participant_name")
        participant_email = self.get_argument("participant_email")
        is_juvenile = self.get_argument("is_juvenile", 'off')
        parent_1_name = self.get_argument("parent_1_name", None)
        parent_2_name = self.get_argument("parent_2_name", None)

        ag_login_id = ag_data.get_user_for_kit(self.current_user)
        kit_email = ag_data.get_user_info(self.current_user)['email']

        # Check if the participant is on the exceptions list
        is_exception = (
            participant_name
            in ag_data.getParticipantExceptions(ag_login_id))

        # If the participant already exists, stop them outright
        if ag_data.check_if_consent_exists(ag_login_id, participant_name):
            errmsg = url_escape(tl['PARTICIPANT_EXISTS'] % participant_name)
            self.redirect(media_locale['SITEBASE'] + "/authed/portal/?errmsg=%s" % errmsg)
            return

        if is_juvenile == 'off' and is_exception:
            errmsg = url_escape(tl["JUVENILE_CONSENT_EXPECTED"] %
                                participant_name)
            self.redirect(media_locale['SITEBASE'] + "/authed/portal/?errmsg=%s" % errmsg)
            return

        if is_juvenile == 'on':
            # If they aren't already an exception, we need to verify them
            if not is_exception:
                alert_message = tl['MINOR_PARENTAL_BODY']

                subject = ("AGJUVENILE: %s (ag_login_id: %s) is a child"
                           % (participant_name, ag_login_id))

                message = MESSAGE_TEMPLATE % (participant_name,
                                              parent_1_name, parent_2_name,
                                              deceased_parent,
                                              self.current_user, kit_email)

                try:
                    send_email(message, subject, sender=kit_email)
                    alert_message = tl['MESSAGE_SENT']
                except:
                    alert_message = media_locale['EMAIL_ERROR']

                self.redirect(media_locale['SITEBASE'] + "/authed/portal/?errmsg=%s" % alert_message)
                return

        human_survey_id = binascii.hexlify(os.urandom(8))

        consent= {'participant_name': participant_name,
                  'participant_email': participant_email,
                  'parent_1_name': parent_1_name,
                  'parent_2_name': parent_2_name,
                  'is_juvenile': True if is_juvenile == 'on' else False,
                  'deceased_parent': deceased_parent,
                  'login_id': ag_login_id,
                  'survey_id': human_survey_id}

        redis.hset(human_survey_id, 'consent', dumps(consent))
        redis.expire(human_survey_id, 86400)

        self.set_secure_cookie('human_survey_id', human_survey_id)
        self.redirect(media_locale['SITEBASE'] + "/authed/survey_main/")
