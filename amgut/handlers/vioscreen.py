from tornado.web import authenticated

from amgut.lib.vioscreen import decode_key
from amgut.util import AG_DATA_ACCESS
from amgut.handlers.base_handlers import BaseHandler
from amgut import media_locale


class VioscreenPassthroughHandler(BaseHandler):
    @authenticated
    def get(self):
        # get information out of  encrypted vioscreen url
        info = decode_key(self.get_argument('key'))
        vio_info = {}
        for keyval in info.split("&"):
            key, val = keyval.split("=")
            vio_info[key] = val

        # Add the status to the survey
        AG_DATA_ACCESS.updateVioscreenStatus(vio_info["username"],
                                             int(vio_info["status"]))

        self.redirect(media_locale['SITEBASE'] + '/authed/portal/')
