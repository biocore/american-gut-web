from tornado.web import authenticated

from amgut.handlers.base_handlers import BaseHandler


class AddSampleOverviewHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render("add_sample_overview.html", skid=self.current_user)
