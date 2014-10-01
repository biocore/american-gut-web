from tornado.web import authenticated

from amgut.handlers.base_handlers import BaseHandler
from amgut.util import AG_DATA_ACCESS
from amgut.lib.mail import send_email
from amgut.lib.locale_data.american_gut import media_locale


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
            errmsg = "Participant %s already exists!" % participant_name
            self.redirect("/authed/portal/?errmsg=%s" % errmsg)

        if is_juvenile == 'off' and is_exception:
            errmsg = ("We are expecting a survey from that juvenile user (%s)"
                      % participant_name)
            self.redirect("/authed/portal/?errmsg=%s" % errmsg)

        if is_juvenile == 'on':
            # If they aren't already an exception, we need to verify them
            if not is_exception:
                juvenile_age = self.get_argument("juvenile_age")
                parent_1_name = self.get_argument("parent_1_name")
                parent_2_name = self.get_argument("parent_2_name")

                alert_message = ("Thank you for your interest in this study. "
                                 "Because of your status as a minor, we will "
                                 "contact you within 24 hours to verify "
                                 "parent/guardian consent.")

                subject = ("AGJUVENILE: %s (ag_login_id: %s) is a child"
                           % (participant_name, ag_login_id))

                message = MESSAGE_TEMPLATE % (participant_name, juvenile_age,
                                              parent_1_name, parent_2_name,
                                              deceased_parent,
                                              self.current_user, kit_email)

                try:
                    send_email(message, subject, sender=kit_email)
                    alert_message = ("Your message has been sent."
                                     " We will reply shortly")
                except:
                    alert_message = ("There was a problem sending your email."
                                     " Please contact us directly at "
                                     "<a href='mailto:%(help_email)s'>"
                                     "%(help_email)s</a>" %
                                     {'help_email': media_locale['HELP_EMAIL']})

                self.redirect("/authed/portal/?errmsg=%s" % alert_message)

        self.redirect("/authed/survey_main/")
