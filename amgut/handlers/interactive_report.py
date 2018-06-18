import os
from functools import partial

from tornado.web import authenticated

from amgut.lib.config_manager import AMGUT_CONFIG
from amgut.connections import ag_data
from amgut.handlers.base_handlers import BaseHandler
from amgut import media_locale, text_locale


class InteractiveReportHandler(BaseHandler):
    @authenticated
    def get(self, barcode):
        #barcode = self.get_argument('barcode', None)
        print(barcode)
        if barcode is None:
            self.redirect(media_locale['SITEBASE'] + '/authed/portal/')
            return

        self.render('interactive_report.html', skid=self.current_user,
                    barcode=barcode)
