from tornado.web import authenticated

from amgut.handlers.base_handlers import BaseHandler


class SurveyMainHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render("survey_main.html", skid=self.current_user)
