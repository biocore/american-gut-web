from tornado.web import authenticated

from amgut.lib.util import external_surveys
from amgut.handlers.base_handlers import BaseHandler


class HumanSurveyCompletedHandler(BaseHandler):
    @authenticated
    def post(self):
        human_survey_id = self.get_secure_cookie('human_survey_id')
        go_home = self.get_argument('go_home', None)

        if human_survey_id is None or go_home is not None:
            self.clear_cookie('human_survey_id')
            self.redirect('/authed/portal/')

        else:
            surveys = [f(human_survey_id) for name, f in external_surveys]

            self.render('human_survey_completed.html', skid=self.current_user,
                        surveys=surveys)
