from urllib import urlencode
from json import dumps
import binascii
import os

from tornado.web import authenticated
from tornado.escape import url_escape
from tornado.websocket import WebSocketHandler

from amgut.handlers.base_handlers import BaseHandler
from amgut.lib.survey_supp import primary_animal_survey
from amgut.lib.util import make_survey_class, store_survey
from amgut.connections import ag_data, redis
from amgut import text_locale, media_locale


class AnimalSurveyHandler(BaseHandler):
    animal_survey = make_survey_class(primary_animal_survey.groups[0],
                                      survey_type='AnimalSurvey')

    @authenticated
    def get(self):
        skid = self.current_user
        survey_id = self.get_argument('survey', '')

        form = self.animal_survey()
        if survey_id:
            form.process(data=primary_animal_survey.fetch_survey(survey_id))
        self.render('animal_survey.html', skid=skid,
                    the_form=form, survey_id=survey_id)

    @authenticated
    def post(self):
        skid = self.current_user
        tl = text_locale['handlers']
        ag_login_id = ag_data.get_user_for_kit(skid)
        ag_login_info = ag_data.get_login_info(ag_login_id)[0]
        animal_survey_id = self.get_argument('survey_id', None)
        sitebase = media_locale['SITEBASE']

        if not animal_survey_id:
            animal_survey_id = binascii.hexlify(os.urandom(8))
            new_survey = True
        else:
            new_survey = False

        form = self.animal_survey()
        form.process(data=self.request.arguments)
        data = {'questions': form.data}
        participant_name = form['Pet_Information_127_0'].data[0]
        # If the participant already exists, stop them outright
        if new_survey and \
                ag_data.check_if_consent_exists(ag_login_id, participant_name):
            errmsg = url_escape(tl['PARTICIPANT_EXISTS'] % participant_name)
            url = sitebase + "/authed/portal/?errmsg=%s" % errmsg
            self.redirect(url)
            return

        consent = {
            'login_id': ag_login_id,
            'participant_name': participant_name,
            'participant_email': ag_login_info['email'],
            'assent_obtainer': 'ANIMAL_SURVEY',
            'parent_1_name': 'ANIMAL_SURVEY',
            'parent_2_name': 'ANIMAL_SURVEY',
            'survey_id': animal_survey_id,
            'is_juvenile': True,
            'deceased_parent': False,
            'obtainer_name': 'ANIMAL_SURVEY',
            'age_range': 'ANIMAL_SURVEY'
        }
        redis.hset(animal_survey_id, 'consent', dumps(consent))
        redis.hset(animal_survey_id, 0, dumps(data))
        redis.expire(animal_survey_id, 86400)

        store_survey(primary_animal_survey, animal_survey_id)
        if not new_survey:
            message = urlencode([('errmsg', tl['SUCCESSFULLY_EDITED'] %
                                 participant_name)])
        else:
            message = urlencode([('errmsg', tl['SUCCESSFULLY_ADDED'] %
                                 participant_name)])

        url = sitebase + '/authed/portal/?%s' % message
        self.redirect(url)


class CheckParticipantName(WebSocketHandler, BaseHandler):
    @authenticated
    def on_message(self, msg):
        tl = text_locale['handlers']
        skid = self.current_user
        participant_name = msg

        ag_login_id = ag_data.get_user_for_kit(skid)
        human_participants = ag_data.getHumanParticipants(ag_login_id)
        animal_participants = ag_data.getAnimalParticipants(ag_login_id)

        if participant_name in (human_participants + animal_participants):
            # if the participant already exists in the system, fail nicely
            output_message = (tl['PARTICIPANT_EXISTS'] % participant_name)
        else:
            # otherwise, success!
            output_message = 'success'

        self.write_message(output_message)
