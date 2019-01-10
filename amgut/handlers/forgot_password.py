from string import ascii_letters, digits
from urllib.parse import quote
from random import choice

from amgut.lib.mail import send_email
from amgut.handlers.base_handlers import BaseHandler
from amgut.connections import ag_data
from amgut import text_locale


class ForgotPasswordHandler(BaseHandler):
    def get(self):
        email = self.get_argument('email', None)
        kitid = self.get_argument('kitid', None)
        kit_counts = ag_data.getMapMarkers()
        self.render('forgot_password.html', email=email, kitid=kitid,
                    result=None, messaage='',
                    kit_counts=kit_counts, loginerror='')

    def post(self):
        email = self.get_argument('email', None)
        kitid = self.get_argument('kitid', None)
        self.create_passcode_and_send_email(email, kitid)

    def create_passcode_and_send_email(self, email, kit_id):
        kitids = ag_data.getAGKitIDsByEmail(email)
        kit_counts = ag_data.getMapMarkers()
        tl = text_locale['handlers']
        # if the kit id matches the email generate and send an email
        if kit_id in kitids:
            alphabet = letters + digits
            new_act_code = ''.join([choice(alphabet) for i in range(20)])
            # add new pass to the database
            ag_data.ag_set_pass_change_code(email, kit_id, new_act_code)
            MESSAGE = (tl['RESET_PASS_BODY'] % (kit_id, quote(email), kit_id,
                                                quote(new_act_code)))

            # send the user an email and tell them to change their password
            try:
                send_email(MESSAGE, tl['CHANGE_PASS_SUBJECT'], email)
                self.render('forgot_password.html', email='', kitid='',
                            result=1, message='',
                            kit_counts=kit_counts, loginerror='')
            except BaseException:
                self.render('forgot_password.html', email='', kitid='',
                            result=2, message=MESSAGE,
                            kit_counts=kit_counts, loginerror='')

        else:
            self.render('forgot_password.html', email='', kitid='',
                        result=3, message='',
                        kit_counts=kit_counts, loginerror='')
