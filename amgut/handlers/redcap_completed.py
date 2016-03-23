from tornado.web import authenticated

from amgut import media_locale
from amgut.handlers.base_handlers import BaseHandler
from amgut.lib.data_access.redcap import log_complete


class RedcapCompletedHandler(BaseHandler):
    @authenticated
    def get(self):
        record_id = self.get_argument('record_id')
        instrument = self.get_argument('instrument')
        survey_id = self.get_argument('survey_id')
        log_complete(record_id, instrument, survey_id)
        if "human" in instrument:
            self.redirect(media_locale['SITEBASE'] +
                          '/authed/human_survey_completed/')
        else:
            self.redirect('/authed/portal/')
