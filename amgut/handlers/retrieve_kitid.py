from amgut.lib.mail import send_email
from amgut.handlers.base_handlers import BaseHandler
from amgut.connections import ag_data
from amgut import text_locale


class KitIDHandler(BaseHandler):
    def get(self):
        kit_counts = ag_data.getMapMarkers()
        self.render('retrieve_kitid.html', message='', output='form',
                    loginerror='', kit_counts=kit_counts)

    def post(self):
        kit_counts = ag_data.getMapMarkers()
        email = self.get_argument('email')
        tl = text_locale['handlers']
        if email:
            kitids = ag_data.getAGKitIDsByEmail(email)
        try:
            if len(kitids) > 0:
                MESSAGE = tl['KIT_IDS_BODY'] % ", ".join(kitids)
                try:
                    send_email(MESSAGE, tl['KIT_IDS_SUBJECT'], email)
                    self.render('retrieve_kitid.html', message='',
                                output='success', loginerror='',
                                kit_counts=kit_counts)
                except BaseException:
                    self.render('retrieve_kitid.html', message=MESSAGE,
                                output='noemail', loginerror='',
                                kit_counts=kit_counts)
            else:
                self.render('retrieve_kitid.html', message='nokit',
                            output='form', loginerror='',
                            kit_counts=kit_counts)

        except BaseException:
            self.render('retrieve_kitid.html', message='', output='exception',
                        loginerror='', kit_counts=kit_counts)
