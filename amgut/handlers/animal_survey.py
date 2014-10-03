from urllib import urlencode
from json import loads

from tornado.web import authenticated
from tornado.websocket import WebSocketHandler

from amgut.handlers.base_handlers import BaseHandler
from amgut.util import AG_DATA_ACCESS
from amgut import text_locale, media_locale


class AnimalSurveyHandler(BaseHandler):
    @authenticated
    def get(self):
        skid = self.current_user
        self.render('animal_survey.html', message='', skid=skid)

    @authenticated
    def post(self):
        skid = self.current_user
        tl = text_locale['handlers']
        participant_name = self.get_argument('animal_name')

        # Add values to tables
        singles = {}
        singles['type'] = self.get_argument('type', default=None)
        singles['origin'] = self.get_argument('origin', default=None)
        singles['age'] = self.get_argument('age', default=None)
        singles['gender'] = self.get_argument('gender', default=None)
        singles['setting'] = self.get_argument('setting', default=None)
        singles['weight'] = self.get_argument('weight', default=None)
        singles['diet'] = self.get_argument('diet', default=None)
        singles['food_source_store'] = self.get_argument('food_source_store',
                                              default=None)
        singles['food_source_human'] = self.get_argument('food_source_human',
                                              default=None)
        singles['food_source_wild'] = self.get_argument('food_source_wild', default=None)
        singles['food_type'] = self.get_argument('food_type', default=None)
        singles['organic_food'] = self.get_argument('organic_food',
                                                    default=None)
        singles['grain_free_food'] = self.get_argument('grain_free_food',
                                                       default=None)
        singles['living_status'] = self.get_argument('living_status',
                                                     default=None)
        singles['outside_time'] = self.get_argument('outside_time',
                                                    default=None)
        singles['toilet'] = self.get_argument('toilet', default=None)
        singles['coprophage'] = self.get_argument('coprophage', default=None)
        singles['comments'] = self.get_argument('comments', default=None)

        multiples = {k: v[0] for k, v in self.request.body_arguments.items()
                     if k.startswith('human_') or k.startswith('pet_')}

        ag_login_id = AG_DATA_ACCESS.get_user_for_kit(skid)
        AG_DATA_ACCESS.deleteAGParticipant(ag_login_id, participant_name)

        for sample in AG_DATA_ACCESS.getParticipantSamples(ag_login_id,
                participant_name):
            AG_DATA_ACCESS.deleteSample(sample['barcode'], ag_login_id)

        # Create the new participant if it doesn't exist (merges)
        AG_DATA_ACCESS.addAGAnimalParticipant(ag_login_id, participant_name)

        for field, value in singles.items():
            if value is None:
                continue

            AG_DATA_ACCESS.addAGGeneralValue(ag_login_id, participant_name,
                                             field, value)
            AG_DATA_ACCESS.addAGSingle(ag_login_id, participant_name,
                                       field, value, 'ag_animal_survey')

        for field, value in multiples.items():
            if value is None:
                continue

            AG_DATA_ACCESS.addAGGeneralValue(ag_login_id, participant_name,
                                             field, value)
            AG_DATA_ACCESS.insertAGMultiple(ag_login_id, participant_name,
                                            field, value)

        message = urlencode([('errmsg', tl['SUCCESSFULLY_ADDED'] %
                              participant_name)])
        self.redirect(media_locale['SITEBASE'] + '/authed/portal/?%s' % message)


class CheckParticipantName(WebSocketHandler, BaseHandler):
    @authenticated
    def on_message(self, msg):
        tl = text_locale['handlers']
        skid = self.current_user
        participant_name = msg

        ag_login_id = AG_DATA_ACCESS.get_user_for_kit(skid)
        human_participants = AG_DATA_ACCESS.getHumanParticipants(ag_login_id)
        animal_participants = AG_DATA_ACCESS.getAnimalParticipants(ag_login_id)

        if participant_name in (human_participants + animal_participants):
            # if the participant already exists in the system, fail nicely
            output_message = (tl['PARTICIPANT_EXISTS'] % participant_name)
        else:
            # otherwise, success!
            output_message = 'success'

        self.write_message(output_message)
