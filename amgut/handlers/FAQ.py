from amgut import media_locale
from amgut.handlers.base_handlers import BaseHandler


class FAQHandler(BaseHandler):
    def get(self):
        self.render('FAQ.html', media_locale=media_locale, loginerror='')
