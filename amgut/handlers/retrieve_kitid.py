from amgut.lib.mail import send_email
from amgut.handlers.base_handlers import BaseHandler
from amgut.util import AG_DATA_ACCESS


class KitIDHandler(BaseHandler):
    def get(self):
        self.render('retrieve_kitid.html', message='', output='form',
                    loginerror='')

    def post(self):
        email = self.get_argument('email')
        if email:
            kitids = AG_DATA_ACCESS.getAGKitIDsByEmail(email)
        try:
            if len(kitids) > 0:
                MESSAGE = ('Your American Gut Kit IDs are %s. You are '
                           'receiving this email because you requested your '
                           'Kit ID from the American Gut web page If you did '
                           'not request your Kit ID please email '
                           'info@americangut.org Thank you,\n The American '
                           'Gut Team\n' % ", ".join(kitids))
                try:
                    send_email(MESSAGE, 'American Gut Kit ID', email)
                    self.render('retrieve_kitid.html', message='',
                                output='success', loginerror='')
                except:
                    self.render('retrieve_kitid.html', message=MESSAGE,
                                output='noemail', loginerror='')
            else:
                self.render('retrieve_kitid.html', message='nokit',
                            output='form', loginerror='')

        except:
            self.render('retrieve_kitid.html', message='', output='exception',
                        loginerror='')
