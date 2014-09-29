from amgut import media_locale
from amgut.handlers.base_handlers import BaseHandler


class ConstructionHandler(BaseHandler):
    def get(self):
        self.render("construction.html", loginerror="",
                    media_locale=media_locale)
