from tornado.web import authenticated

from amgut.handlers.base_handlers import BaseHandler


class AddendumHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render("addendum.html", skid=self.current_user)
