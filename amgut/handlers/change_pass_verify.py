from urllib import unquote

from amgut.lib.mail import send_email
from amgut.handlers.base_handlers import BaseHandler
from amgut.util import AG_DATA_ACCESS
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
        latlongs = AG_DATA_ACCESS.getMapMarkers()
        self.render('change_pass_verify.html', email=email, kitid=kitid,
                    passcode=passcode, new_password=new_password,
                    confirm_password=confirm_password,
                    result=result, message=None, latlongs_db=latlongs,
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
        return AG_DATA_ACCESS.ag_verify_kit_password_change_code(email, kitid,
                                                                 passcode)

    def reset_pass_and_email(self, new_password, confirm_password, email,
                             supplied_kit_id):
        AG_DATA_ACCESS.ag_update_kit_password(supplied_kit_id, new_password)
        latlongs = AG_DATA_ACCESS.getMapMarkers()
        tl = text_locale['handlers']
        MESSAGE = tl['CHANGE_PASS_BODY'] % supplied_kit_id
        try:
            send_email(MESSAGE, tl['CHANGE_PASS_SUBJECT'], email)
            self.render('change_pass_verify.html', email='', kitid='',
                        passocde='', new_password='',
                        confirm_password='', result=4, message='',
                        latlongs_db=latlongs, loginerror='')
        except:
            self.render('change_pass_verify.html', email='', kitid='',
                        passocde='', new_password='',
                        confirm_password='', result=5, message='',
                        latlongs_db=latlongs, loginerror='')
