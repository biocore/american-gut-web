from amgut.handlers.base_handlers import BaseHandler


class FAQHandler(BaseHandler):
    def get(self):
        self.render('FAQ.html', loginerror='')
