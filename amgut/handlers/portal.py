from tornado.web import authenticated

from amgut.handlers.base_handlers import BaseHandler
from amgut.util import AG_DATA_ACCESS


class PortalHandler(BaseHandler):
    @authenticated
    def get(self):
        errmsg = self.get_argument('errmsg', "")
        kit_id = self.current_user

        user_info = AG_DATA_ACCESS.get_user_info(kit_id)
        user_name = user_info['name']

        kit_details = AG_DATA_ACCESS.getAGKitDetails(kit_id)
        kit_verified = True if kit_details['kit_verified'] == 'y' else False

        results = AG_DATA_ACCESS.get_barcode_results(kit_id)
        has_results = len(results) != 0

        barcodes = AG_DATA_ACCESS.getBarcodesByKit(kit_id)

        kit_ver_error = False
        verification_textbox = ''

        self.render("portal.html", skid=kit_id, user_name=user_name,
                    errmsg=errmsg, kit_verified=kit_verified,
                    has_results=has_results, results=results,
                    barcodes=barcodes, kit_ver_error=kit_ver_error,
                    verification_textbox=verification_textbox)

    @authenticated
    def post(self):
        kit_id = self.current_user
        errmsg = self.get_argument('errmsg', "")
        user_code = self.get_argument('user_verification_code')
        kit_details = AG_DATA_ACCESS.getAGKitDetails(kit_id)
        barcodes = AG_DATA_ACCESS.getBarcodesByKit(kit_id)
        user_info = AG_DATA_ACCESS.get_user_info(kit_id)
        user_name = user_info['name']
        results = AG_DATA_ACCESS.get_barcode_results(kit_id)
        has_results = len(results) != 0

        kit_verified = True if kit_details['kit_verified'] == 'y' else False

        if kit_details['kit_verification_code'] == user_code:
            AG_DATA_ACCESS.verifyKit(kit_id)
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
