from urllib import unquote

from amgut.lib.mail import send_email
from amgut.handlers.base_handlers import BaseHandler
from amgut.connections import ag_data
from amgut import text_locale


class ChangePassVerifyHandler(BaseHandler):

    def get(self):
        email = self.get_argument('email', None)
        if email is not None:
            email = unquote(email)
        kitid = self.get_argument('kitid', None)
        passcode = self.get_argument('passcode', None)
        new_password = self.get_argument('new_password', None)
        confirm_password = self.get_argument('confirm_password', None)

        if self.is_valid(email, kitid, passcode):
            result = 'valid'
        else:
            result = 'notvalid'
        kit_counts = ag_data.getMapMarkers()
        self.render('change_pass_verify.html', email=email, kitid=kitid,
                    passcode=passcode, new_password=new_password,
                    confirm_password=confirm_password,
                    result=result, message=None, kit_counts=kit_counts,
                    loginerror='')

    def post(self):
        email = self.get_argument('email', None)
        kit_id = self.get_argument('kitid', None)
        if email is not None:
            email = unquote(email)
        new_password = self.get_argument('new_password', None)
        confirm_password = self.get_argument('confirm_password', None)
        self.reset_pass_and_email(new_password, confirm_password, email,
                                  kit_id)

    def is_valid(self, email, kitid, passcode):
        return ag_data.ag_verify_kit_password_change_code(email, kitid,
                                                          passcode)

    def reset_pass_and_email(self, new_password, confirm_password, email,
                             supplied_kit_id):
        ag_data.ag_update_kit_password(supplied_kit_id, new_password)
        kit_counts = ag_data.getMapMarkers()
        tl = text_locale['handlers']
        MESSAGE = tl['CHANGE_PASS_BODY'] % supplied_kit_id
        try:
            send_email(MESSAGE, tl['CHANGE_PASS_SUBJECT'], email)
            self.render('change_pass_verify.html', email='', kitid='',
                        passocde='', new_password='',
                        confirm_password='', result=4, message='',
                        kit_counts=kit_counts, loginerror='')
        except:
            self.render('change_pass_verify.html', email='', kitid='',
                        passocde='', new_password='',
                        confirm_password='', result=5, message='',
                        kit_counts=kit_counts, loginerror='')
