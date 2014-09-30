from urllib import unquote

from amgut.handlers.base_handlers import BaseHandler
from amgut.util import AG_DATA_ACCESS
from amgut.lib.mail import send_email


class ChangePasswordHandler(BaseHandler):
    def get(self):
        latlongs = AG_DATA_ACCESS.getMapMarkers()
        user_info = AG_DATA_ACCESS.get_user_info(self.current_user)
        self.render('change_pass_verify.html', email=user_info['email'],
                    kitid=self.current_user, passcode='', new_password=None,
                    confirm_password=None, result='valid', message=None,
                    latlongs_db=latlongs, loginerror='')

    def post(self):
        email = self.get_argument('email', None)
        kit_id = self.get_argument('kitid', None)
        if email is not None:
            email = unquote(email)
        new_password = self.get_argument('new_password', None)
        confirm_password = self.get_argument('confirm_password', None)
        self.reset_pass_and_email(new_password, confirm_password, email,
                                  kit_id)

    def reset_pass_and_email(self, new_password, confirm_password, email,
                             supplied_kit_id):
        AG_DATA_ACCESS.ag_update_kit_password(supplied_kit_id, new_password)
        latlongs = AG_DATA_ACCESS.getMapMarkers()
        MESSAGE = ('This is a courtesy email to confirm that you have '
                   'changed your password for your kit with ID %s. '
                   'If you did not request this change, please email us '
                   'immediately at info@americangut.org.' % supplied_kit_id)
        try:
            send_email(MESSAGE, 'American Gut Password Reset', email)
            self.render('change_pass_verify.html', email='', kitid='',
                        passocde='', new_password='',
                        confirm_password='', result=4, message='',
                        latlongs_db=latlongs, loginerror='')
        except:
            self.render('change_pass_verify.html', email='', kitid='',
                        passocde='', new_password='',
                        confirm_password='', result=5, message='',
                        latlongs_db=latlongs, loginerror='')
