from tornado.web import authenticated

from amgut.handlers.base_handlers import BaseHandler
from amgut.util import AG_DATA_ACCESS


class PortalHandler(BaseHandler):
    @authenticated
    def get(self):
        errmsg = self.get_argument('errmsg', "")

        user_info = AG_DATA_ACCESS.get_user_info(self.current_user)
        user_name = user_info['name']

        kit_details = AG_DATA_ACCESS.getAGKitDetails(self.current_user)
        kit_verified = kit_details['kit_verified']

        results = AG_DATA_ACCESS.get_barcode_results(self.current_user)
        has_results = len(results) != 0

        self.render("portal.html", skid=self.current_user, user_name=user_name,
                    errmsg=errmsg, kit_verified=kit_verified,
                    has_results=has_results)
