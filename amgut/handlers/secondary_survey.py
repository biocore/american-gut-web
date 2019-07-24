from urllib import urlencode
from tornado.escape import url_unescape
from json import dumps
import os

from tornado.web import authenticated

from amgut.handlers.base_handlers import BaseHandler
from amgut.lib.survey_supp import (
    fermented_survey, surf_survey, personal_microbiome_survey)
from amgut.lib.util import make_survey_class, store_survey
from amgut.connections import ag_data, redis
from amgut import text_locale, media_locale


class SecondarySurveyHandler(BaseHandler):
    sec_surveys = {'fermented': fermented_survey,
                   'surf': surf_survey,
                   'personal_microbiome': personal_microbiome_survey}

    @authenticated
    def get(self):
        skid = self.current_user
        survey_id = self.get_argument('survey', '')
        survey_type = self.get_argument('type')
        participant_name = url_unescape(self.get_argument('participant_name'))

        sec_survey = self.sec_surveys[survey_type]
        survey_class = make_survey_class(sec_survey.groups[0],
                                         survey_type='SecondarySurvey')

        form = survey_class()
        if survey_id:
            form.process(data=sec_survey.fetch_survey(survey_id))

        # load existing information into the form
        if survey_id != '':
            data = sec_survey.fetch_survey(survey_id)
            form = survey_class(data=data)

        self.render('secondary_survey.html', skid=skid,
                    the_form=form, survey_id=survey_id,
                    type=survey_type, participant_name=participant_name)

    @authenticated
    def post(self):
        skid = self.current_user
        tl = text_locale['handlers']
        ag_login_id = ag_data.get_user_for_kit(skid)
        survey_id = self.get_argument('survey_id', None)
        survey_type = self.get_argument('type')
        participant_name = url_unescape(self.get_argument('participant_name'))
        sitebase = media_locale['SITEBASE']

        if not survey_id:
            survey_id = ag_data.get_new_survey_id()

        sec_survey = self.sec_surveys[survey_type]
        survey_class = make_survey_class(sec_survey.groups[0],
                                         survey_type='SecondarySurvey')

        form = survey_class()
        form.process(data=self.request.arguments)
        data = {'questions': form.data}

        consent = {
            'login_id': ag_login_id,
            'participant_name': participant_name,
            'survey_id': survey_id,
            'secondary': True
        }
        redis.hset(survey_id, 'consent', dumps(consent))
        redis.hset(survey_id, 0, dumps(data))
        redis.expire(survey_id, 86400)

        store_survey(sec_survey, survey_id)
        if survey_id:
            message = urlencode([('errmsg', tl['SUCCESSFULLY_EDITED'] %
                                 participant_name)])
        else:
            message = urlencode([('errmsg', tl['SUCCESSFULLY_ADDED'] %
                                 participant_name)])

        url = '%s/authed/portal/?%s' % (sitebase, message)
        self.redirect(url)
