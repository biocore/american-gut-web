from tornado.web import authenticated

from amgut.lib.vioscreen import decode_key
from amgut.connections import ag_data
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
        ag_data.updateVioscreenStatus(vio_info["username"],
                                      int(vio_info["status"]))

        self.redirect(media_locale['SITEBASE'] + '/authed/portal/')
