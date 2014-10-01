from urllib import unquote
from tornado.web import authenticated

from amgut.handlers.base_handlers import BaseHandler
from amgut.util import AG_DATA_ACCESS
from amgut.lib.mail import send_email
from amgut.lib.locale_data.american_gut import media_locale


class ChangePasswordHandler(BaseHandler):
    @authenticated
    def get(self):
        user_info = AG_DATA_ACCESS.get_user_info(self.current_user)
        self.render('change_password.html', email=user_info['email'],
                    skid=self.current_user, new_password=None,
                    confirm_password=None, result='valid', message=None)

    @authenticated
    def post(self):
        email = self.get_argument('email', None)
        if email is not None:
            email = unquote(email)
        new_password = self.get_argument('new_password', None)
        confirm_password = self.get_argument('confirm_password', None)
        self.reset_pass_and_email(new_password, confirm_password, email,
                                  self.current_user)

    def reset_pass_and_email(self, new_password, confirm_password, email,
                             supplied_kit_id):
        AG_DATA_ACCESS.ag_update_kit_password(supplied_kit_id, new_password)
        MESSAGE = ('This is a courtesy email to confirm that you have '
                   'changed your password for your kit with ID %s. '
                   'If you did not request this change, please email us '
                   'immediately at %s.'
                   % (supplied_kit_id, media_locale['HELP_EMAIL']))
        try:
            send_email(MESSAGE, 'American Gut Password Reset', email)
            self.render('change_password.html', email='',
                        skid=self.current_user,
                        new_password='', confirm_password='', result=4,
                        message='')
        except:
            self.render('change_password.html', email='',
                        skid=self.current_user,
                        new_password='', confirm_password='', result=5,
                        message='')
