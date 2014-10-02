import os

from tornado.web import authenticated

from amgut.lib.config_manager import AMGUT_CONFIG
from amgut.util import AG_DATA_ACCESS
from amgut.handlers.base_handlers import BaseHandler
from amgut import media_locale


def _format_data_path(dir, barcode, ext):
    return os.path.join(AMGUT_CONFIG.base_data_dir, dir,
                        '.'.join([barcode, ext]))


class SampleOverviewHandler(BaseHandler):

    def _sample_overview_renderer(self):
        barcode = self.get_argument('barcode')

        sample_data = AG_DATA_ACCESS.getAGBarcodeDetails(barcode)

        barcode_pdf = _format_data_path('pdfs', barcode, 'pdf')
        barcode_txt = _format_data_path('taxa-summaries', barcode, 'txt')

        if not os.path.exists(barcode_pdf):
            barcode_pdf = None
        if not os.path.exists(barcode_txt):
            barcode_txt = None

        sample_time = sample_data['sample_time']
        sample_date = sample_data['sample_date']

        status = sample_data['status']
        if status is None:
            bgcolor = '#FFF'
            status = 'Submitted'
        elif status == 'Received':
            bgcolor = '#AFA'
        else:
            bgcolor = '#FFF'

        sample_origin = sample_data['site_sampled']
        if sample_origin is None:
            sample_origin = sample_data['environment_sampled']

        notes = sample_data['notes']
        if notes is None:
            notes = ''

        self.render('sample_overview.html', skid=self.current_user,
                    barcode_pdf=barcode_pdf, barcode_txt=barcode_txt,
                    bgcolor=bgcolor, status=status, barcode=barcode,
                    sample_origin=sample_origin, sample_date=sample_date,
                    sample_time=sample_time, notes=notes)

    @authenticated
    def get(self):
        self._sample_overview_renderer()

    @authenticated
    def post(self):
        bc_to_remove = self.get_argument("remove", None)
        if bc_to_remove:
            ag_login_id = AG_DATA_ACCESS.get_user_for_kit(self.current_user)
            AG_DATA_ACCESS.deleteSample(bc_to_remove, ag_login_id)
            self.redirect(media_locale['SITEBASE'] + "/authed/portal/")

        self._sample_overview_renderer()
