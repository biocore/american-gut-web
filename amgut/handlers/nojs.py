from amgut.handlers.base_handlers import BaseHandler

class NoJSHandler(BaseHandler):
    def get(self):
        self.render('nojs.html')
