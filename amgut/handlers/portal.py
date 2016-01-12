from tornado.web import authenticated

from amgut import media_locale, text_locale
from amgut.lib.mail import send_email
from amgut.handlers.base_handlers import BaseHandler
from amgut.connections import ag_data


class PortalHandler(BaseHandler):
    @authenticated
    def get(self):
        errmsg = self.get_argument('errmsg', "")
        kit_id = self.current_user

        user_info = ag_data.get_user_info(kit_id)

        if not user_info:
            self.redirect(media_locale['SITEBASE'] + '/auth/logout/')
            return

        user_name = user_info['name']

        kit_details = ag_data.getAGKitDetails(kit_id)
        kit_verified = True if kit_details['kit_verified'] == 'y' else False

        results = ag_data.get_barcode_results(kit_id)
        has_results = len(results) != 0

        barcodes = ag_data.getBarcodesByKit(kit_id)

        kit_ver_error = False
        verification_textbox = ''
        unconsented = ag_data.get_nonconsented_scanned_barcodes(kit_id)

        self.render("portal.html", skid=kit_id, user_name=user_name,
                    errmsg=errmsg, kit_verified=kit_verified,
                    has_results=has_results, results=results,
                    barcodes=barcodes, kit_ver_error=kit_ver_error,
                    verification_textbox=verification_textbox,
                    unconsented=unconsented)

    @authenticated
    def post(self):
        kit_id = self.current_user
        errmsg = self.get_argument('errmsg', "")
        user_code = self.get_argument('user_verification_code', "")
        kit_details = ag_data.getAGKitDetails(kit_id)
        barcodes = ag_data.getBarcodesByKit(kit_id)
        user_info = ag_data.get_user_info(kit_id)
        user_name = user_info['name']
        results = ag_data.get_barcode_results(kit_id)
        has_results = len(results) != 0

        kit_verified = True if kit_details['kit_verified'] == 'y' else False

        if not kit_verified and user_code == "":
            # Resend kit verification code
            tl = text_locale['handlers']
            subject = tl['AUTH_SUBJECT']
            addendum = ''
            if self.current_user.startswith('PGP_'):
                addendum = tl['AUTH_REGISTER_PGP']

            body = tl['AUTH_REGISTER_BODY'].format(
                kit_details['kit_verification_code'], addendum)

            kit_ver_error = False
            verification_textbox = ''
            try:
                send_email(body, subject, recipient=user_info['email'],
                           sender=media_locale['HELP_EMAIL'])
            except:
                errmsg = media_locale['EMAIL_ERROR']
        else:
            # Verify the given kit verification code
            if kit_details['kit_verification_code'] == user_code:
                ag_data.verifyKit(kit_id)
                kit_ver_error = False
                verification_textbox = ''
            else:
                kit_ver_error = True
                verification_textbox = ' highlight'

        self.render("portal.html", skid=kit_id, user_name=user_name,
                    errmsg=errmsg, kit_verified=kit_verified,
                    has_results=has_results, results=results,
                    barcodes=barcodes,
                    verification_textbox=verification_textbox,
                    kit_ver_error=kit_ver_error)
