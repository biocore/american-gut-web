from amgut.handlers.base_handlers import BaseHandler


class InternationalHandler(BaseHandler):
    def get(self):
        language = self.get_argument('lan', 'en')
        self.render("international.html", language=language, loginerror="")
