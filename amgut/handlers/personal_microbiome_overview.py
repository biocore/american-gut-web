from tornado.web import authenticated

from amgut.handlers.base_handlers import BaseHandler


class PersonalMicrobiomeOverviewHandler(BaseHandler):
    """"""
    @authenticated
    def get(self):
        participant_name = self.get_argument('participant_name')
        self.render("personal_microbiome_overview.html",
                    skid=self.current_user,
                    participant_name=participant_name)
