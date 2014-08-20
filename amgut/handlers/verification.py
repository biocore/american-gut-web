from tornado.web import authenticated

from amgut.handlers.base_handlers import BaseHandler


class VerificationHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render("verification.html", skid=self.current_user)
