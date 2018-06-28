from tornado.web import authenticated
from tornado.web import HTTPError
from tornado.escape import url_escape
from amgut.lib.vioscreen import encrypt_key

from amgut.handlers.base_handlers import BaseHandler
from amgut.connections import ag_data
from amgut import media_locale, text_locale


class ParticipantOverviewHandler(BaseHandler):
    @authenticated
    def post(self, participant_name):
        text = text_locale['participant_overview.html']
        participant_name = participant_name.strip('/')  # for nginx
        skid = self.current_user
        ag_login_id = ag_data.get_user_for_kit(skid)
        barcodes = ag_data.getParticipantSamples(ag_login_id, participant_name)
        if barcodes:
            ebi_submitted = any(ag_data.is_deposited_ebi(b['barcode'])
                                for b in barcodes)
        else:
            ebi_submitted = False

        # Check if we have to remove the participant
        participant_to_remove = self.get_argument("remove", None)
        if participant_to_remove and not ebi_submitted:
            barcodes = ag_data.getParticipantSamples(
                ag_login_id, participant_to_remove)
            # Remove all the samples attached to the participant
            for bc in barcodes:
                ag_data.deleteSample(bc['barcode'], ag_login_id)
            # Remove the participant
            ag_data.deleteAGParticipantSurvey(
                ag_login_id, participant_to_remove)
            # Redirect to portal
            self.redirect(media_locale['SITEBASE'] + "/authed/portal/")
            return

        participant_type = self.get_argument('participant_type')
        internal_surveys = ag_data.get_participants_surveys(ag_login_id,
                                                            participant_name)
        vioscreens = []
        
        if internal_surveys is None:
            raise HTTPError(404, "Could not retrieve survey details for "
                            "participant '%s'" % participant_name)
        else:
            for survey_group, survey_id, survey_name in internal_surveys:
                if survey_group == -1:
                    # Magic number 3 is the vioscreen code for complete survey
                    status = ag_data.get_vioscreen_status(survey_id)
                    url = (("https://vioscreen.com/remotelogin.aspx?Key=%s"
                            "&RegCode=KLUCB") %
                           url_escape(encrypt_key(survey_id)))
                    if status is not None and status != 3:
                        vioscreens.append(text['VIOSCREEN_CONTINUE'] % url)
                    elif status is not None:
                        vioscreens.append(text['VIOSCREEN_COMPLETE'])
                    else:
                        vioscreens.append(text['VIOSCREEN_START'] % url)

        # Get the list of samples for this participant
        samples = ag_data.getParticipantSamples(ag_login_id,
                                                participant_name)

        self.render('participant_overview.html', skid=skid,
                    participant_name=participant_name,
                    internal_surveys=internal_surveys,
                    participant_type=participant_type, samples=samples,
                    vioscreens=vioscreens, ebi_submitted=ebi_submitted)

    @authenticated
    def get(self, *args, **kwargs):
        self.redirect(media_locale['SITEBASE'] + '/authed/portal/')
