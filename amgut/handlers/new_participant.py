from tornado.web import authenticated
from tornado.escape import url_escape

from amgut import media_locale, text_locale
from amgut.handlers.base_handlers import BaseHandler
from amgut.connections import ag_data
from amgut.lib.data_access.redcap import get_survey_url


class NewParticipantHandler(BaseHandler):
    """"""
    @authenticated
    def get(self):
        self.render("new_participant.html", skid=self.current_user, message='',
                    default_lang=media_locale['DEFAULT_LANGUAGE'])

    @authenticated
    def post(self):
        tl = text_locale['handlers']
        participant_name = self.get_argument("participant_name").strip()
        participant_email = self.get_argument("participant_email").strip()
        age_range = self.get_argument("age_range")
        parent_1_name = self.get_argument("parent_1_name", None)
        parent_2_name = self.get_argument("parent_2_name", None)
        obtainer_name = self.get_argument("obtainer_name", None)
        deceased_parent = self.get_argument("deceased_parent", 'No')
        language = self.get_argument('language')
        sitebase = media_locale['SITEBASE']

        if not participant_name or not participant_email:
            self.render("new_participant.html", skid=self.current_user,
                        message=tl['MISSING_NAME_EMAIL'])
            return

        ag_login_id = ag_data.get_user_for_kit(self.current_user)

        # If the participant already exists, stop them outright
        if ag_data.check_if_consent_exists(ag_login_id, participant_name):
            errmsg = url_escape(tl['PARTICIPANT_EXISTS'] % participant_name)
            url = sitebase + "/authed/portal/?errmsg=%s" % errmsg
            self.redirect(url)
            return

        consent = {'participant_name': participant_name,
                   'participant_email': participant_email,
                   'parent_1_name': parent_1_name,
                   'parent_2_name': parent_2_name,
                   'is_juvenile': True if age_range != '18-plus' else False,
                   'deceased_parent': deceased_parent,
                   'obtainer_name': obtainer_name,
                   'age_range': age_range,
                   'login_id': ag_login_id,
                   'language': language}

        # Save consent info and redirect to redcap
        record_id = ag_data.store_consent(consent)
        url = get_survey_url(record_id, instrument='ag_human_' + language)
        self.redirect(url)
