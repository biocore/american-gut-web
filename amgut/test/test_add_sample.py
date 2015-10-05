from unittest import main
from amgut.test.tornado_test_base import TestHandlerBase


class TestAddSample(TestHandlerBase):
    def test_get_not_authed(self):
        response = self.get(
            '/authed/add_sample_human/?participant_name=REMOVED-0')
        self.assertEqual(response.code, 200)
        # Make sure logged out URL
        self.assertTrue(
            response.effective_url.endswith(
                '/?next=%2Fauthed%2Fadd_sample_human%2F%3F'
                'participant_name%3DREMOVED-0'))

    def test_get_human(self):
        self.mock_login('tst_LbxUH')
        response = self.get(
            '/authed/add_sample_human/?participant_name=REMOVED-0')
        self.assertEqual(response.code, 200)
        # Make sure proper name in place
        self.assertIn(
            '<input type="hidden" name="participant_name" value="REMOVED-0"/>',
            response.body)

        # Spot check sample locations
        self.assertIn('Left hand', response.body)
        self.assertIn('Stool', response.body)
        self.assertIn('Ear wax', response.body)

        # Make sure proper form setup used
        self.assertIn('action="/authed/add_sample_human/"', response.body)

    def test_get_animal(self):
        self.mock_login('tst_tfqsD')
        response = self.get(
            '/authed/add_sample_animal/?participant_name=REMOVED-0')
        self.assertEqual(response.code, 200)
        # Make sure proper name in place
        self.assertIn(
            '<input type="hidden" name="participant_name" value="REMOVED-0"/>',
            response.body)

        # Spot check sample locations
        self.assertIn('Fur', response.body)
        self.assertIn('Ears', response.body)

        # Make sure proper form setup used
        self.assertIn('action="/authed/add_sample_animal/"', response.body)

    def test_get_general(self):
        self.mock_login('tst_LbxUH')
        response = self.get(
            '/authed/add_sample_general/?participant_name=environmental')
        self.assertEqual(response.code, 200)
        # Make sure proper name in place
        self.assertIn(
            '<input type="hidden" name="participant_name" '
            'value="environmental"/>',
            response.body)

        # Spot check sample locations
        self.assertIn('Animal Habitat', response.body)
        self.assertIn('Indoor Surface', response.body)
        self.assertIn('Biofilm', response.body)

        # Make sure proper form setup used
        self.assertIn('action="/authed/add_sample_general/"', response.body)

    def test_get_no_participant(self):
        self.mock_login('tst_LbxUH')
        response = self.get('/authed/add_sample_general/')
        self.assertEqual(response.code, 200)
        self.assertTrue(
            response.effective_url.endswith('/authed/add_sample_overview/'))

        response = self.get('/authed/add_sample_human/')
        self.assertEqual(response.code, 200)
        self.assertTrue(
            response.effective_url.endswith('/authed/add_sample_overview/'))

        response = self.get('/authed/add_sample_animal/')
        self.assertEqual(response.code, 200)
        self.assertTrue(
            response.effective_url.endswith('/authed/add_sample_overview/'))

    def test_post_not_authed(self):
        response = self.post('/authed/add_sample_human/',
                             {'participant_name': 'REMOVED-0'})
        self.assertEqual(response.code, 403)

    def test_post_human(self):
        raise NotImplementedError()

    def test_post_animal(self):
        raise NotImplementedError()

    def test_post_general(self):
        raise NotImplementedError()

    def test_post_bad_data(self):
        # Malformed date

        # Malformed Time

        # Missing data
        raise NotImplementedError()

if __name__ == '__main__':
    main()
