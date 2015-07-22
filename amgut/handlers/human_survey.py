from json import dumps, loads
import logging

from tornado.web import authenticated
from tornado.escape import url_escape

from amgut import media_locale, text_locale
from amgut.connections import ag_data, redis
from amgut.handlers.base_handlers import BaseHandler
from amgut.lib.util import store_survey, make_survey_class
from amgut.lib.survey_supp import primary_human_survey
from amgut.lib.mail import send_email


def build_consent_form(consent_info):
    tl = text_locale['new_participant.html']
    # build out the consent form
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


surveys = [make_survey_class(group, survey_type='HumanSurvey')
           for group in primary_human_survey.groups]


class HumanSurveyHandler(BaseHandler):
    @authenticated
    def post(self):
        # see if we're coming from an edit
        human_survey_id = self.get_argument('survey_id', None)
        page_number = int(self.get_argument('page_number'))

        if human_survey_id is None:
            # we came from consent
            human_survey_id = self.get_secure_cookie('human_survey_id')
            if human_survey_id is None:
                err_msg = url_escape("There was an unexpected error.")
                self.redirect(media_locale['SITEBASE'] + "/authed/portal/?errmsg=%s" % err_msg)
                return
        else:
            # we came from participant_overview
            consent = ag_data.getConsent(human_survey_id)
            self.set_secure_cookie('human_survey_id', human_survey_id)
            data = primary_human_survey.fetch_survey(human_survey_id)
            redis.hset(human_survey_id, 'consent', dumps(consent))
            redis.hset(human_survey_id, 'existing', dumps(data))
            redis.expire(human_survey_id, 86400)

        next_page_number = page_number + 1

        if page_number >= 0:
            form_data = surveys[page_number]()
            form_data.process(data=self.request.arguments)
            data = {'questions': form_data.data}

            redis.hset(human_survey_id, page_number, dumps(data))

        progress = int(100.0*(page_number+2)/(len(primary_human_survey.groups) + 1))

        # if this is not the last page, render the next page
        if next_page_number < len(surveys):
            the_form = surveys[next_page_number]()

            existing_responses = redis.hget(human_survey_id, 'existing')
            if existing_responses:
                existing_responses = loads(existing_responses)
                the_form = surveys[next_page_number](data=existing_responses)

            title = primary_human_survey.groups[next_page_number].name

            self.render('human_survey.html', the_form=the_form,
                        skid=self.current_user, TITLE=title,
                        page_number=next_page_number,
                        progress=progress)
        else:
            # only get the cookie if you complete the survey
            self.clear_cookie('human_survey_id')
            self.set_secure_cookie('completed_survey_id', human_survey_id)
            store_survey(primary_human_survey, human_survey_id)
            existing = redis.hget(human_survey_id, 'existing')
            if existing is None:
                # Send consent info email since new participant
                consent_info = ag_data.getConsent(human_survey_id)
                try:
                    message = build_consent_form(consent_info)
                    send_email(message, 'American Gut-Signed Consent Form(s)',
                               recipient=consent_info['participant_email'],
                               sender='donotreply@americangut.com', html=True)
                except:
                    logging.exception('Error sending signed consent form for '
                                      'survey ID: %s to email: %s' %
                                      (human_survey_id,
                                       consent_info['participant_email']))

            self.redirect(media_locale['SITEBASE'] +
                          '/authed/human_survey_completed/')

    @authenticated
    def get(self, *args, **kwargs):
        self.redirect(media_locale['SITEBASE'] + "/")
