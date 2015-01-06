from tornado.web import authenticated
from tornado.web import HTTPError

from amgut.handlers.base_handlers import BaseHandler
from amgut.connections import ag_data
from amgut import media_locale


class ParticipantOverviewHandler(BaseHandler):
    @authenticated
    def post(self, participant_name):
        participant_name = participant_name.strip('/')  # for nginx
        skid = self.current_user
        ag_login_id = ag_data.get_user_for_kit(skid)

        # Check if we have to remove the participant
        participant_to_remove = self.get_argument("remove", None)
        if participant_to_remove:
            barcodes = ag_data.getParticipantSamples(
                ag_login_id, participant_to_remove)
            # Remove all the samples attached to the participant
            for bc in barcodes:
                ag_data.deleteSample(bc['barcode'], ag_login_id)
            # Remove the participant
            ag_data.deleteAGParticipant(
                ag_login_id, participant_to_remove)
            # Redirect to portal
            self.redirect(media_locale['SITEBASE'] + "/authed/portal/")
            return

        participant_type = self.get_argument('participant_type')
        survey_id = ag_data.get_survey_id(ag_login_id, participant_name)

        if survey_id is None:
            raise HTTPError(404, "Could not retrieve survey details for "
                            "participant '%s'" % participant_name)

        # Get the list of samples for this participant
        samples = ag_data.getParticipantSamples(ag_login_id,
                                                participant_name)

        self.render('participant_overview.html', skid=skid,
                    participant_name=participant_name, survey_id=survey_id,
                    participant_type=participant_type, samples=samples)
