from amgut.handlers.base_handlers import BaseHandler


class ConstructionHandler(BaseHandler):
    def get(self):
        self.render("construction.html", loginerror="")
