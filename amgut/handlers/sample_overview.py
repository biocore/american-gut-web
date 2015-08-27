import os
import json

from tornado.web import authenticated
import requests

from amgut.lib.config_manager import AMGUT_CONFIG
from amgut.connections import ag_data
from amgut.handlers.base_handlers import BaseHandler
from amgut import media_locale


def _format_data_path(base, dir, barcode, ext):
    return os.path.join(base, dir, '.'.join([barcode, ext]))


class SampleOverviewHandler(BaseHandler):
    def _sample_overview_renderer(self):
        barcode = self.get_argument('barcode', None)
        if barcode is None:
            self.redirect(media_locale['SITEBASE'] + '/authed/portal/')
            return

        has_access = ag_data.check_access(self.current_user, barcode)
        if not has_access:
            self.set_status(403)
            self.render("403.html", skid=self.current_user)
            return

        sample_data = ag_data.getAGBarcodeDetails(barcode)

        if not sample_data:
            self.set_status(404)
            self.render("404.html", skid=self.current_user)
            return

        fs_base = AMGUT_CONFIG.base_data_dir
        web_base = "%s/results" % media_locale['SITEBASE']

        fs_barcode_pdf = _format_data_path(fs_base, 'pdfs', barcode, 'pdf')
        fs_barcode_txt = _format_data_path(fs_base, 'taxa-summaries', barcode,
                                        'txt')
        web_barcode_pdf = _format_data_path(web_base, 'pdfs', barcode, 'pdf')
        web_barcode_txt = _format_data_path(web_base, 'taxa-summaries',
                                            barcode, 'txt')

        if not os.path.exists(fs_barcode_pdf):
            web_barcode_pdf = None
        if not os.path.exists(fs_barcode_txt):
            web_barcode_txt = None

        req = requests.get('http://api.microbio.me/americangut/1/sample/%s' % barcode)
        if req.status_code == 200 and req.content != "(null)":
            bc_with_suf = json.loads(req.content)[0]
            biomv1_url = 'http://api.microbio.me/americangut/1/otu/%s/json' % bc_with_suf
            classic_url = 'http://api.microbio.me/americangut/1/otu/%s/txt' % bc_with_suf

            seq_req = requests.get('http://api.microbio.me/americangut/1/sequence/%s' % bc_with_suf)
            if seq_req.status_code == 200:
                sequence_url = json.loads(seq_req.content)[0]['fastq_url']
            else:
                sequence_url = None
        else:
            sequence_url = None
            biomv1_url = None
            classic_url = None
            sequence_url = None

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
                    barcode_pdf=web_barcode_pdf, barcode_txt=web_barcode_txt,
                    bgcolor=bgcolor, status=status, barcode=barcode,
                    sample_origin=sample_origin, sample_date=sample_date,
                    sample_time=sample_time, notes=notes,
                    sequence_url=sequence_url, biomv1_url=biomv1_url,
                    classic_url=classic_url)

    @authenticated
    def get(self):
        self._sample_overview_renderer()

    @authenticated
    def post(self):
        bc_to_remove = self.get_argument("remove", None)
        if bc_to_remove:
            ag_login_id = ag_data.get_user_for_kit(self.current_user)
            ag_data.deleteSample(bc_to_remove, ag_login_id)
            self.redirect(media_locale['SITEBASE'] + "/authed/portal/")
            return

        self._sample_overview_renderer()
