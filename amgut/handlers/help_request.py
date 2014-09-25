from amgut import text_locale, media_locale
from amgut.lib.mail import send_email
from amgut.handlers.base_handlers import BaseHandler


class HelpRequestHandler(BaseHandler):
    def get(self):
        page = 'help_request.html'
        self.render(page, skid=self.current_user, result='',
                    text_locale=text_locale[page],
                    media_locale=media_locale[page])

    def post(self):
        page = 'help_request.html'
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
                result = 'Your message has been sent. We will reply shortly'
            except:
                result = ("There was a problem sending your email. Please "
                          "contact us directly at "
                          "<a href='mailto:info@americangut.org'>info@americangut.org</a>")

            self.render(page, skid=self.current_user, result=result,
                        text_locale=text_locale[page],
                        media_locale=media_locale[page])
