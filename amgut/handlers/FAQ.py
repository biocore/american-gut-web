from amgut.handlers.base_handlers import BaseHandler
from amgut import text_locale, media_locale


class FAQHandler(BaseHandler):
    page = 'FAQ.html'

    def get(self):
        self.render(self.page, loginerror='', media_locale=media_locale,
                    text_locale=text_locale[self.page])
