from tornado.web import authenticated


from amgut.handlers.base_handlers import BaseHandler


class KitIndexHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render("authed_index.html", skid=self.current_user)
