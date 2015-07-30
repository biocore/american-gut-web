from tornado.web import authenticated, HTTPError

from os.path import join, exists

from .base_handlers import BaseHandler
from amgut import AMGUT_CONFIG
from amgut.connections import ag_data


# {filetype from get: (local path, file suffix)}
FILETYPES = {'taxa': ('taxa-summaries', '.txt'),
             'result-pdf': ('pdfs', '.pdf')}


class DownloadHandler(BaseHandler):
    @authenticated
    def get(self, *args, **kwargs):
        barcode = self.get_argument('barcode', None)
        filetype = self.get_argument('filetype', None)

        if barcode is None or filetype is None:
            raise HTTPError(400, "Incorrectly formed GET request")

        # Check access to file
        has_access = ag_data.check_access(self.current_user, barcode)

        if not has_access:
            self.set_status(403)
            self.render("403.html", skid=self.current_user)
            return

        if filetype not in FILETYPES:
            raise HTTPError(400, "Unrecognized filetype")

        filetype_path, filetype_suffix = FILETYPES[filetype]
        fname = barcode + filetype_suffix
        fullpath = join(filetype_path, fname)

        if not exists(join(AMGUT_CONFIG.base_data_dir, fullpath)):
            raise HTTPError(400, "File %s is not available" % fullpath)

        self.set_header('Content-Description', 'File Transfer')
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Transfer-Encoding', 'binary')
        self.set_header('Expires', '0')
        self.set_header('Cache-Control', 'no-cache')
        self.set_header('X-Accel-Redirect', '/protected/' + fullpath)
        self.set_header('Content-Disposition',
                        'attachment; filename=%s' % fname)

        self.finish()
