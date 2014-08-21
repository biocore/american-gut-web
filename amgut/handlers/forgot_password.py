from string import letters, digits
from urllib import quote, unquote
from random import choice

from amgut.lib.mail import send_email
from amgut.handlers.base_handlers import BaseHandler
from amgut.util import AG_DATA_ACCESS


class ForgotPasswordHandler(BaseHandler):
    def get(self):
        email = self.get_argument('email', None)
        kitid = self.get_argument('kitid', None)
        passcode = self.get_argument('passcode', None)
        self.render('forgot_password.html', email=email, kitid=kitid,
                    passcode=passcode, result='new', messaage='',
                    latlongs_db='', loginerror='')

    def post(self):
        email = self.get_argument('email', None)
        kitid = self.get_argument('kitid', None)
        passcode = self.get_argument('passcode', None)
        new_password = self.get_argument('new_password', None)
        confirm_password = self.get_arguemnt('confirm_password', None)

        self.render('forgot_password.html', email=email, kitid=kitid,
                    passcode=passcode, new_password=new_password,
                    confirm_password=confirm_password, result=None,
                    message='', latlongs_db='', loginerror='')

    def create_passcode_and_send_email(self, email, kit_id):
        kitids = AG_DATA_ACCESS.getAGKitbyEmail(email)
        #if the kit id matches the email generate and send an email
        if kit_id in kitids:
            alphabet = letters + digits
            new_act_code = ''.join([choice(alphabet) for i in range(20)])
            # add new pass to the database
            AG_DATA_ACCESS.ag_set_pass_change_code(email, kit_id, new_act_code)

            MESSAGE = ('The password on American Gut Kit ID %s  has been reset'
                       ' please click the link below within two hours\n'
                       'http://microbio.me/americangut/forgot_password.psp?'
                       'email=%s;kit_id=%s;'
                       'passcode=%s' % (kit_id,
                                        quote(email),
                                        kit_id,
                                        quote(new_act_code)))

            #send the user an email and tell them to change their password
            try:
                    send_email(MESSAGE, 'American Gut Password Reset', email)
                    self.render('forgot_password.html', email='', kitid='',
                                passocde='', new_password='',
                                confirm_password='', result=1, message='',
                                loginerror='')
            except:
                    self.render('forgot_password.html', email='', kitid='',
                                passocde='', new_password='',
                                confirm_password='', result=2, message=MESSAGE,
                                loginerror='')

        else:
            self.render('forgot_password.html', email='', kitid='',
                        passocde='', new_password='',
                        confirm_password='', result=3, message='',
                        loginerror='')
