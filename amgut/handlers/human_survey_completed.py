import logging

from tornado.web import authenticated

from amgut.lib.util import external_surveys
from amgut.handlers.base_handlers import BaseHandler
from amgut import media_locale, text_locale
from amgut.lib.mail import send_email
from amgut.connections import ag_data


def build_consent_form(consent_info):
    tl = text_locale['new_participant.html']
    # email out the consent form
    if consent_info['age_range'] == '0-6':
        message = ("%s<p>%s: %s</p><p>%s: %s</p><p>%s: %s</p>"
                   "<p>%s: %s</p><p>%s: %s</p><p>%s: %s</p>") %\
            (tl['CONSENT_YOUR_CHILD'],
             tl['PARTICIPANT_NAME'], consent_info['participant_name'],
             tl['PARTICIPANT_EMAIL'], consent_info['participant_email'],
             tl['PARTICIPANT_PARENT_1'], consent_info['parent_1_name'],
             tl['PARTICIPANT_PARENT_2'], consent_info['parent_2_name'],
             tl['PARTICIPANT_DECEASED_PARENTS'],
             consent_info['deceased_parent'],
             tl['DATE_SIGNED'], str(consent_info['date_signed']))

    elif consent_info['age_range'] == '7-12':
        message = ("%s<p>%s: %s</p><p>%s: %s</p><p>%s: %s</p>"
                   "%s<p>%s: %s</p><p>%s: %s</p><p>%s: %s</p>"
                   "<p>%s: %s</p>") %\
            (tl['ASSENT_7_12'],
             tl['PARTICIPANT_NAME'], consent_info['participant_name'],
             tl['PARTICIPANT_EMAIL'], consent_info['participant_email'],
             tl['OBTAINER_NAME'], consent_info['assent_obtainer'],
             tl['CONSENT_YOUR_CHILD'],
             tl['PARTICIPANT_PARENT_1'], consent_info['parent_1_name'],
             tl['PARTICIPANT_PARENT_2'], consent_info['parent_2_name'],
             tl['PARTICIPANT_DECEASED_PARENTS'],
             consent_info['deceased_parent'],
             tl['DATE_SIGNED'], str(consent_info['date_signed']))

    elif consent_info['age_range'] == '13-17':
        message = ("%s<p>%s: %s</p><p>%s: %s</p>"
                   "%s<p>%s: %s</p><p>%s: %s</p><p>%s: %s</p>"
                   "<p>%s: %s</p>") %\
            (tl['ASSENT_13_17'],
             tl['PARTICIPANT_NAME'], consent_info['participant_name'],
             tl['PARTICIPANT_EMAIL'], consent_info['participant_email'],
             tl['CONSENT_YOUR_CHILD'],
             tl['PARTICIPANT_PARENT_1'], consent_info['parent_1_name'],
             tl['PARTICIPANT_PARENT_2'], consent_info['parent_2_name'],
             tl['PARTICIPANT_DECEASED_PARENTS'],
             consent_info['deceased_parent'],
             tl['DATE_SIGNED'], str(consent_info['date_signed']))

    elif consent_info['age_range'] == '18-plus':
        message = "%s<p>%s: %s</p><p>%s: %s</p><p>%s: %s</p>" %\
            (tl['CONSENT_18'],
             tl['PARTICIPANT_NAME'], consent_info['participant_name'],
             tl['PARTICIPANT_EMAIL'], consent_info['participant_email'],
             tl['DATE_SIGNED'], str(consent_info['date_signed']))

    else:
        # old consent so no idea of age range and text, only juv/non-juv
        raise NotImplementedError("Old consent, no text available")
    return message


class HumanSurveyCompletedHandler(BaseHandler):
    @authenticated
    def get(self):
        human_survey_id = self.get_secure_cookie('completed_survey_id')

        if human_survey_id is None:
            self.clear_cookie('completed_survey_id')
            self.redirect(media_locale['SITEBASE'] + '/authed/portal/')

        else:
            surveys = [f(human_survey_id) for f in external_surveys]

            self.render('human_survey_completed.html', skid=self.current_user,
                        surveys=surveys)
            consent_info = ag_data.getConsent(human_survey_id)
            message = build_consent_form(consent_info)

            try:
                send_email(message, 'American Gut - Signed Consent Form(s)',
                           recipient=consent_info['participant_email'])
            except:
                logging.exception('Error sending signed consent form for '
                                  'survey ID: %s to email: %s' %
                                  (human_survey_id,
                                   consent_info['participant_email']))

    @authenticated
    def post(self):
        self.clear_cookie('completed_survey_id')
        self.redirect(media_locale['SITEBASE'] + '/authed/portal/')
