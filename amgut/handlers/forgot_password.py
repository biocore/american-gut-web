from string import letters, digits
from urllib import quote
from random import choice

from amgut.lib.mail import send_email
from amgut.handlers.base_handlers import BaseHandler
from amgut.util import AG_DATA_ACCESS
from amgut import text_locale


class ForgotPasswordHandler(BaseHandler):
    def get(self):
        email = self.get_argument('email', None)
        kitid = self.get_argument('kitid', None)
        latlongs = AG_DATA_ACCESS.getMapMarkers()
        self.render('forgot_password.html', email=email, kitid=kitid,
                    result=None, messaage='',
                    latlongs_db=latlongs, loginerror='')

    def post(self):
        email = self.get_argument('email', None)
        kitid = self.get_argument('kitid', None)
        self.create_passcode_and_send_email(email, kitid)

    def create_passcode_and_send_email(self, email, kit_id):
        kitids = AG_DATA_ACCESS.getAGKitIDsByEmail(email)
        latlongs = AG_DATA_ACCESS.getMapMarkers()
        tl = text_locale['handlers']
        #if the kit id matches the email generate and send an email
        if kit_id in kitids:
            alphabet = letters + digits
            new_act_code = ''.join([choice(alphabet) for i in range(20)])
            # add new pass to the database
            AG_DATA_ACCESS.ag_set_pass_change_code(email, kit_id, new_act_code)
            MESSAGE = (tl['RESET_PASS_BODY'] % (kit_id, quote(email), kit_id,
                                                quote(new_act_code)))

            #send the user an email and tell them to change their password
            try:
                    send_email(MESSAGE, tl['CHANGE_PASS_SUBJECT'], email)
                    self.render('forgot_password.html', email='', kitid='',
                                result=1, message='',
                                latlongs_db=latlongs, loginerror='')
            except:
                    self.render('forgot_password.html', email='', kitid='',
                                result=2, message=MESSAGE,
                                latlongs_db=latlongs, loginerror='')

        else:
            self.render('forgot_password.html', email='', kitid='',
                        result=3, message='',
                        latlongs_db=latlongs, loginerror='')
