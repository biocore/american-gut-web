from tornado.web import authenticated

from amgut.lib.util import external_surveys
from amgut.handlers.base_handlers import BaseHandler
from amgut import media_locale


class HumanSurveyCompletedHandler(BaseHandler):
    @authenticated
    def get(self):
        human_survey_id = self.get_secure_cookie('completed_survey_id')

        if human_survey_id is None:
            self.clear_cookie('completed_survey_id')
            self.redirect(media_locale['SITEBASE'] + '/authed/portal/')

        else:
            surveys = [f(human_survey_id) for f in external_surveys]

            self.render('human_survey_completed.html', skid=self.current_user,
                        surveys=surveys)

    @authenticated
    def post(self):
        self.clear_cookie('completed_survey_id')
        self.redirect(media_locale['SITEBASE'] + '/authed/portal/')
