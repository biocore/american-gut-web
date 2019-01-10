from unittest import main
from amgut.test.tornado_test_base import TestHandlerBase
from amgut.connections import ag_data


class TestAddSampleOverview(TestHandlerBase):

    def test_get_not_authed(self):
        response = self.get(
            '/authed/secondary_survey/?type=surf&participant_name=test')
        self.assertEqual(response.code, 200)
        self.assertTrue(
            response.effective_url.endswith(
                '%2Fauthed%2Fsecondary_survey%2F%3Ftype%3Dsurf'
                '%26participant_name%3Dtest'))

    def test_get_missing_info(self):
        self.mock_login(
            ag_data.ut_get_supplied_kit_id(
                'd8592c74-9694-2135-e040-8a80115d6401'))
        response = self.get(
            '/authed/secondary_survey/?type=surf')
        self.assertEqual(response.code, 400)
        response = self.get(
            '/authed/secondary_survey/?participant_name=test')
        self.assertEqual(response.code, 400)

    def test_get_surf(self):
        self.mock_login(
            ag_data.ut_get_supplied_kit_id(
                'd8592c74-9694-2135-e040-8a80115d6401'))
        response = self.get(
            '/authed/secondary_survey/?type=surf&participant_name=test%2Bfoo')
        self.assertEqual(response.code, 200)
        self.assertIn(b'<h2>Surf Survey</h2>', response.body)
        self.assertIn(b'<td width="50%" class="tdmainform">How often do you '
                      b'travel to other surf breaks?</td>', response.body)

    def test_get_fermented(self):
        self.mock_login(
            ag_data.ut_get_supplied_kit_id(
                'd8592c74-9694-2135-e040-8a80115d6401'))
        response = self.get(
            '/authed/secondary_survey/?type=fermented&'
            'participant_name=test%20bar')
        self.assertEqual(response.code, 200)
        self.assertIn(b'<h2>Fermented Survey</h2>', response.body)
        self.assertIn(b'<td width="50%" class="tdmainform">How often do you '
                      b'consume one or more servings of fermented vegetables or'
                      b' plant products a day in an average week?',
                      response.body)

    def test_post(self):
        data = {'Fermented_Foods_164_0': '3',
                'Fermented_Foods_165_0': '2',
                'Fermented_Foods_166_0': ['5'],
                'Fermented_Foods_167_0': '',
                'Fermented_Foods_169_0': '',
                'Fermented_Foods_170_0': ['6', '11'],
                'Fermented_Foods_171_0': '',
                'Fermented_Foods_172_0': '',
                'participant_name': 'REMOVED_0',
                'survey_id': '',
                'type': 'fermented'}
        self.post('/authed/secondary_survey/', data)


if __name__ == '__main__':
    main()
