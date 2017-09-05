from unittest import main
from amgut.test.tornado_test_base import TestHandlerBase
from amgut.connections import ag_data, redis
from amgut.lib.util import rollback, store_survey
from amgut.lib.data_access.survey import Survey
from amgut.lib.survey_supp import (fermented_survey,
                                   surf_survey,
                                   personal_microbiome_survey)
from json import dumps


class TestHumanSurveyCompleted(TestHandlerBase):
    sec_surveys = {'fermented': fermented_survey,
                   'surf': surf_survey,
                   'personal_microbiome': personal_microbiome_survey}

    @rollback
    def test_edit_survey(self):
        # creating a new participant for existing ag_login_id
        main_survey_id = '38792874'
        sec_survey_id_fermented = '3879287455'
        sec_survey_id_surfer = '3879287456'
        ag_login_id = 'd8592c74-9694-2135-e040-8a80115d6401'
        participant_name = 'test_dude_stefan'
        email = 'STEFAN@STEFAN.STEFAN'

        with_fk_inserts =\
            [(main_survey_id, _id, 'Unspecified') for _id in
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
                 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
                 50, 51, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65,
                 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
                 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95,
                 96, 107, 109, 110, 111, 112, 114, 146, 148, 149, 153, 154,
                 155, 156, 157, 158, 159, 160, 162, 163, 164]]
        without_fk_inserts =\
            [(main_survey_id, _id, '[""]') for _id in
                [98, 99, 150, 103, 104, 105, 106, 108, 113, 115, 116, 117, 118,
                 119, 120, 122, 124, 126, 101]]
        self.mock_login(ag_data.ut_get_supplied_kit_id(ag_login_id))

        s = Survey(main_survey_id)
        s.store_survey(
            {u'login_id': ag_login_id,
             u'age_range': u'18-plus',
             u'parent_1_name': None,
             u'participant_email': email,
             u'obtainer_name': None,
             u'parent_2_name': None,
             u'deceased_parent': u'No',
             u'participant_name': participant_name,
             u'survey_id': main_survey_id,
             u'is_juvenile': False},
            with_fk_inserts, without_fk_inserts)

        # confirm that no secondary surveys are present
        response = self.post('/participants/%s' % participant_name,
                             {'participant_type': 'human'})
        self.assertEqual(response.code, 200)
        self.assertNotIn('fermented', response.body)
        self.assertNotIn('surf', response.body)

        # add a new fermented food survey
        data = {'questions': {'Fermented_Foods_170_0': [''],
                              'Fermented_Foods_173_0': [''],
                              'Fermented_Foods_169_0': None,
                              'Fermented_Foods_171_0': ['13'],
                              'Fermented_Foods_168_0': [''],
                              'Fermented_Foods_167_0': ['1'],
                              'Fermented_Foods_166_0': ['0'],
                              'Fermented_Foods_165_0': ['0'],
                              'Fermented_Foods_172_0': ['']}}
        consent = {
            'login_id': ag_login_id,
            'participant_name': participant_name,
            'survey_id': sec_survey_id_fermented,
            'secondary': True
        }
        redis.hset(sec_survey_id_fermented, 'consent', dumps(consent))
        redis.hset(sec_survey_id_fermented, 0, dumps(data))
        redis.expire(sec_survey_id_fermented, 86400)
        store_survey(fermented_survey, sec_survey_id_fermented)

        # confirm that now a fermented food survey is present
        response = self.post('/participants/%s' % participant_name,
                             {'participant_type': 'human'})
        self.assertEqual(response.code, 200)
        self.assertIn('fermented', response.body)
        self.assertNotIn('surf', response.body)
        self.assertIn('secondary_survey/?type=%s&participant_name=%s&survey=%s'
                      % ('fermented',
                         participant_name,
                         sec_survey_id_fermented), response.body)
        # check human_survey_completed links:
        # TODO: I don't know how to set a secured cookie for
        # completed_survey_id and could need some help to actually test values
        # for the rendered page /authed/human_survey_completed/
        # response = self.get('/authed/human_survey_completed/')

        # add a new surfers survey
        data = {'questions': {'Surfers_182_0': ['0'],
                              'Surfers_176_0': ['0'],
                              'Surfers_175_0': ['0'],
                              'Surfers_185_0': ['0'],
                              'Surfers_179_0': ['0'],
                              'Surfers_183_0': ['0'],
                              'Surfers_180_0': ['0'],
                              'Surfers_174_0': ['0'],
                              'Surfers_178_0': ['0'],
                              'Surfers_181_0': ['0'],
                              'Surfers_177_0': ['0'],
                              'Surfers_184_0': ['0']}}
        consent = {
            'login_id': ag_login_id,
            'participant_name': participant_name,
            'survey_id': sec_survey_id_surfer,
            'secondary': True
        }
        redis.hset(sec_survey_id_surfer, 'consent', dumps(consent))
        redis.hset(sec_survey_id_surfer, 0, dumps(data))
        redis.expire(sec_survey_id_surfer, 86400)
        store_survey(surf_survey, sec_survey_id_surfer)

        # confirm that now a surfers and fermented food survey is present
        response = self.post('/participants/%s' % participant_name,
                             {'participant_type': 'human'})
        self.assertEqual(response.code, 200)
        self.assertIn('fermented', response.body)
        self.assertIn('surf', response.body)
        self.assertIn('secondary_survey/?type=%s&participant_name=%s&survey=%s'
                      % ('fermented',
                         participant_name,
                         sec_survey_id_fermented),
                      response.body)
        self.assertIn('secondary_survey/?type=%s&participant_name=%s&survey=%s'
                      % ('surf',
                         participant_name,
                         sec_survey_id_surfer),
                      response.body)


if __name__ == '__main__':
    main()
