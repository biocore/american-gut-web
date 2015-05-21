from tornado.web import authenticated, HTTPError

from os.path import join

from .base_handlers import BaseHandler
from amgut import AMGUT_CONFIG
from amgut.connections import ag_data


# {filetype from get: (local path, file suffix)}
FILETYPES = {'taxa': ('taxa-summaries', '.txt'),
             'result-pdf': ('pdfs', '.pdf')}


class DownloadHandler(BaseHandler):
    @authenticated
    def get(self, barcode, filetype):
        # Check access to file
        has_access = ag_data.check_access(self.current_user, barcode)

        if not has_access:
            raise HTTPError(403, "Access forbidden")

        if filetype not in FILETYPES:
            raise HTTPError(500, "Unrecognized filetype")

        filetype_path, filetype_suffix = FILETYPES[filetype]
        basepath = join(AMGUT_CONFIG.base_data_dir, filetype_path)
        fname = barcode + filetype_suffix
        fullpath = join(basepath, fname)

        # If we don't have nginx, write a file that indicates this
        self.write("This installation of AG was not equipped with nginx, "
                   "so it is incapable of serving files. The file you "
                   "attempted to download is located at %s" % fullpath)

        self.set_header('Content-Description', 'File Transfer')
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Transfer-Encoding', 'binary')
        self.set_header('Expires',  '0')
        self.set_header('Cache-Control',  'no-cache')
        self.set_header('X-Accel-Redirect', '/protected/' + fullpath)
        self.set_header('Content-Disposition',
                        'attachment; filename=%s' % fname)

        self.finish()
