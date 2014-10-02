from tornado.web import authenticated

from amgut.lib.mail import send_email
from amgut.handlers.base_handlers import BaseHandler
from amgut import media_locale


class HelpRequestHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render('help_request.html', skid=self.current_user, result='')

    @authenticated
    def post(self):
        email_address = self.get_argument('email_address')
        skid = self.current_user[-2:]  # last two letters of kit id
        first_name = self.get_argument('first_name')
        last_name = self.get_argument('last_name')
        message = self.get_argument('message_body')

        if email_address:
            SUBJECT = """AGHELP: %s %s %s""" % (first_name, last_name, skid)

            MESSAGE = """Contact: %s %s
            Reply to: %s
            --------------------------------------------------------------------------------
            Message:
            %s
            --------------------------------------------------------------------------------
            """ % (first_name, last_name, email_address, message)

            try:
                send_email(MESSAGE, SUBJECT, sender=email_address)
                result = media_locale["EMAIL_SENT"]
            except:
                result = media_locale['EMAIL_ERROR']

            self.render('help_request.html', skid=self.current_user,
                        result=result)
