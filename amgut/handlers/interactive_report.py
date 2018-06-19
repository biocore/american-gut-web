from tornado.web import authenticated

from amgut.connections import ag_data
from amgut.handlers.base_handlers import BaseHandler

class InteractiveReportHandler(BaseHandler):
    @authenticated
    def get(self, barcode):
        if barcode is None:
            self.redirect(media_locale['SITEBASE'] + '/authed/portal/')
            return

        has_access = ag_data.check_access(self.current_user, barcode)
        if not has_access:
            self.set_status(403)
            self.render("403.html", skid=self.current_user)
            return

        self.render('interactive_report.html', skid=self.current_user,
                    barcode=barcode)
