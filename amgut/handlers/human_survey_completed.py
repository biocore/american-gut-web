from tornado.web import authenticated

from amgut.lib.util import external_surveys
from amgut.handlers.base_handlers import BaseHandler
from amgut import media_locale
from amgut.connections import ag_data


class HumanSurveyCompletedHandler(BaseHandler):
    @authenticated
    def get(self):
        human_survey_id = self.get_secure_cookie('completed_survey_id')

        if human_survey_id is None:
            self.clear_cookie('completed_survey_id')
            self.redirect(media_locale['SITEBASE'] + '/authed/portal/')

        else:
            consent_info = ag_data.getConsent(human_survey_id)
            internal_surveys = ag_data.get_participants_surveys(
                consent_info['ag_login_id'], consent_info['participant_name'])
            surveys = [f(human_survey_id, consent_info, internal_surveys)
                       for f in external_surveys]

            self.render('human_survey_completed.html', skid=self.current_user,
                        surveys=surveys)

    @authenticated
    def post(self):
        self.clear_cookie('completed_survey_id')
        self.redirect(media_locale['SITEBASE'] + '/authed/portal/')
