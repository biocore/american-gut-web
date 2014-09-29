from amgut.handlers.base_handlers import BaseHandler


class FAQHandler(BaseHandler):
    page = 'FAQ.html'

    def get(self):
        self.render(self.page, loginerror='')
