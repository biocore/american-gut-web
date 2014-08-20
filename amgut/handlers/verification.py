from tornado.web import authenticated

from amgut.util import AG_DATA_ACCESS
from amgut.handlers.base_handlers import BaseHandler


class VerificationHandler(BaseHandler):
    @authenticated
    def get(self):
        kit_id = self.current_user
        kit_details = AG_DATA_ACCESS.getAGKitDetails(kit_id)
        barcodes = AG_DATA_ACCESS.getBarcodesByKit(kit_id)
        message = ''
        verification_textbox = ''

        if kit_details['kit_verified'] == 'y':
            kit_verified = True
        else:
            kit_verified = False

        self.render("verification.html", skid=self.current_user,
                    kit_verified=kit_verified, barcodes=barcodes,
                    message=message, verification_textbox=verification_textbox)

    @authenticated
    def post(self):
        kit_id = self.current_user
        user_code = self.get_argument('user_verification_code')
        kit_details = AG_DATA_ACCESS.getAGKitDetails(kit_id)
        barcodes = AG_DATA_ACCESS.getBarcodesByKit(kit_id)

        if kit_details['kit_verified'] == 'y':
            kit_verified = True
        else:
            kit_verified = False

        if kit_details['kit_verification_code'] == user_code:
            AG_DATA_ACCESS.verifyKit(kit_id)
            message = 'Kit %s successfully verified!' % kit_id
            verification_textbox = ''
        else:
            message = ('The kit verification code you entered does not match '
                       'our records. Please double-check the code you '
                       'entered. If you continue to experience difficulties, '
                       'please <a href=/authed/help_request/>contact us</a>.')
            verification_textbox = ' highlight'

        self.render("verification.html", skid=self.current_user,
                    kit_verified=kit_verified, barcodes=barcodes,
                    verification_textbox=verification_textbox, message=message)
