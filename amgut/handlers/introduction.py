from amgut.handlers.base_handlers import BaseHandler


class IntroductionHandler(BaseHandler):
    page = 'introduction.html'

    def get(self):
        self.render(self.page, loginerror='')
