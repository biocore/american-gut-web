from amgut.lib.mail import send_email
from amgut.handlers.base_handlers import BaseHandler
from amgut.util import AG_DATA_ACCESS
from amgut import text_locale



class KitIDHandler(BaseHandler):
    def get(self):
        self.render('retrieve_kitid.html', message='', output='form',
                    loginerror='')

    def post(self):
        email = self.get_argument('email')
        tl = text_locale['handlers']
        if email:
            kitids = AG_DATA_ACCESS.getAGKitIDsByEmail(email)
        try:
            if len(kitids) > 0:
                MESSAGE = tl['KIT_IDS_BODY'] % ", ".join(kitids)
                try:
                    send_email(MESSAGE, tl['KIT_IDS_SUBJECT'], email)
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
