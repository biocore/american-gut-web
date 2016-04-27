from tornado.web import authenticated

from amgut.lib.util import external_surveys
from amgut.handlers.base_handlers import BaseHandler
from amgut import media_locale
from amgut.lib.data_access.redcap import log_complete


class HumanSurveyCompletedHandler(BaseHandler):
    @authenticated
    def get(self):
        human_survey_id = self.get_argument('survey_id')
        record_id = self.get_argument('record_id')
        instrument = self.get_argument('instrument')
        event = self.get_argument('event')
        log_complete(record_id, instrument, event)

        surveys = [f(human_survey_id) for f in external_surveys]

        self.render('human_survey_completed.html', skid=self.current_user,
                    surveys=surveys)

    @authenticated
    def post(self):
        self.clear_cookie('completed_survey_id')
        self.redirect(media_locale['SITEBASE'] + '/authed/portal/')
