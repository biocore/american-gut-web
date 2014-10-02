from tornado.web import authenticated

from amgut.handlers.base_handlers import BaseHandler
from amgut.util import AG_DATA_ACCESS
from amgut.lib.mail import send_email
from amgut import media_locale, text_locale


MESSAGE_TEMPLATE = """Contact: %s
        --------------------------------------------------------------------------------
        Message:
        This participant is a child, the person filling out the survey for them
        needs to provide proof of consent. Email them for proof.

        Juvenile age: %s
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
        is_juvenile = self.get_argument("is_juvenile", 'off')

        ag_login_id = AG_DATA_ACCESS.get_user_for_kit(self.current_user)
        kit_email = AG_DATA_ACCESS.get_user_info(self.current_user)['email']

        # Get the list of participants attached to that login id
        participants = AG_DATA_ACCESS.getHumanParticipants(ag_login_id)

        # Check if the participant is on the exceptions list
        is_exception = (
            participant_name
            in AG_DATA_ACCESS.getParticipantExceptions(ag_login_id))

        # If the participant already exists, stop them outright
        if participant_name in participants:
            errmsg = tl['PARTICIPANT_EXISTS'] % participant_name
            self.redirect(media_locale['SITEBASE'] + "/authed/portal/?errmsg=%s" % errmsg)

        if is_juvenile == 'off' and is_exception:
            errmsg = ("We are expecting a survey from that juvenile user (%s)"
                      % participant_name)
            self.redirect(media_locale['SITEBASE'] + "/authed/portal/?errmsg=%s" % errmsg)

        if is_juvenile == 'on':
            # If they aren't already an exception, we need to verify them
            if not is_exception:
                juvenile_age = self.get_argument("juvenile_age")
                parent_1_name = self.get_argument("parent_1_name")
                parent_2_name = self.get_argument("parent_2_name")

                alert_message = tl['MINOR_PARENTAL_BODY']

                subject = ("AGJUVENILE: %s (ag_login_id: %s) is a child"
                           % (participant_name, ag_login_id))

                message = MESSAGE_TEMPLATE % (participant_name, juvenile_age,
                                              parent_1_name, parent_2_name,
                                              deceased_parent,
                                              self.current_user, kit_email)

                try:
                    send_email(message, subject, sender=kit_email)
                    alert_message = tl['MESSAGE_SENT']
                except:
                    alert_message = media_locale['EMAIL_ERROR']

                self.redirect(media_locale['SITEBASE'] + "/authed/portal/?errmsg=%s" % alert_message)

        self.redirect(media_locale['SITEBASE'] + "/authed/survey_main/")
