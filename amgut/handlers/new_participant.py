from tornado.web import authenticated

from amgut.handlers.base_handlers import BaseHandler
from amgut.util import AG_DATA_ACCESS


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
        kit_email = AG_DATA_ACCESS.TODO_SOMETHING(self.current_user)

        # Get the list of participants attached to that login id
        participants = AG_DATA_ACCESS.getHumanParticipants(ag_login_id)

        # Check if the participant is on the exceptions list
        is_exception = (
            participant_name
            in AG_DATA_ACCESS.getParticipantExceptions(ag_login_id))

        # If the participant already exists, stop them outright
        if participant_name in participants:
            self.render("portal.html", errmsg="Participant %s already exists!"
                                              % participant_name)

        if is_juvenile == 'off' and is_exception:
            self.render("portal.html", errmsg="We are expecting a survey from "
                                              "that juvenile user (%s)"
                                              % participant_name)

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

                message = ("""Contact: %s
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
        """ % (participant_name, juvenile_age, parent_1_name, parent_2_name,
               deceased_parent, self.current_user, kit_email))
