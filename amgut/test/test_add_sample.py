from unittest import main
import datetime
from amgut.test.tornado_test_base import TestHandlerBase
from amgut.connections import ag_data


class TestAddSample(TestHandlerBase):
    def tearDown(self):
        ag_data.deleteSample('000005628',
                             'd8592c74-9694-2135-e040-8a80115d6401')
        ag_data.deleteSample('000002011',
                             'd8592c74-8710-2135-e040-8a80115d6401')
        super(TestAddSample, self).tearDown()

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
        self.mock_login('tst_DbGvP')
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
        self.mock_login('tst_LbxUH')
        # make sure barcode properly removed
        self.assertIn('000005628', ag_data.getAvailableBarcodes(
                      'd8592c74-9694-2135-e040-8a80115d6401'))

        # Run test
        response = self.post('/authed/add_sample_human/',
                             {'participant_name': 'REMOVED-0',
                              'barcode': '000005628',
                              'sample_site': 'Stool',
                              'sample_date': '12/13/14',
                              'sample_time': '11:12 pm',
                              'notes': 'TESTING TORNADO LOGGING HUMAN'})
        self.assertEqual(response.code, 200)
        self.assertTrue(
            response.effective_url.endswith('/authed/portal/'))

        obs = ag_data.getAGBarcodeDetails('000005628')
        exp = {
            'status': None,
            'ag_kit_barcode_id': 'db447092-620e-54d8-e040-8a80115d3637',
            'ag_kit_id': 'db447092-6209-54d8-e040-8a80115d3637',
            'barcode': '000005628',
            'site_sampled': 'Stool',
            'environment_sampled': None,
            'name': 'REMOVED',
            'sample_date': datetime.date(2014, 12, 13),
            'sample_time': datetime.time(23, 12),
            'notes': 'TESTING TORNADO LOGGING HUMAN',
            'overloaded': None,
            'withdrawn': None,
            'email': 'REMOVED',
            'other': None,
            'moldy': None,
            'participant_name': 'REMOVED-0',
            'refunded': None,
            'date_of_last_email': None,
            'other_text': 'REMOVED'
        }
        self.assertDictEqual(obs, exp)

    def test_post_animal(self):
        self.mock_login('tst_DbGvP')
        # make sure barcode properly removed
        self.assertIn('000002011', ag_data.getAvailableBarcodes(
                      'd8592c74-8710-2135-e040-8a80115d6401'))

    def test_post_general(self):
        self.mock_login('tst_LbxUH')
        # make sure barcode properly removed
        self.assertIn('000005628', ag_data.getAvailableBarcodes(
                      'd8592c74-9694-2135-e040-8a80115d6401'))

        # Run test
        response = self.post('/authed/add_sample_general/',
                             {'participant_name': 'environmental',
                              'barcode': '000005628',
                              'sample_site': 'Biofilm',
                              'sample_date': '12/11/14',
                              'sample_time': '10:12 pm',
                              'notes': 'TESTING TORNADO LOGGING GENERAL'})
        self.assertEqual(response.code, 200)
        self.assertTrue(
            response.effective_url.endswith('/authed/portal/'))

        obs = ag_data.getAGBarcodeDetails('000005628')
        exp = {
            'status': None,
            'ag_kit_barcode_id': 'db447092-620e-54d8-e040-8a80115d3637',
            'ag_kit_id': 'db447092-6209-54d8-e040-8a80115d3637',
            'barcode': '000005628',
            'site_sampled': None,
            'environment_sampled': 'Biofilm',
            'name': 'REMOVED',
            'sample_date': datetime.date(2014, 12, 11),
            'sample_time': datetime.time(22, 12),
            'notes': 'TESTING TORNADO LOGGING GENERAL',
            'overloaded': None,
            'withdrawn': None,
            'email': 'REMOVED',
            'other': None,
            'moldy': None,
            'participant_name': 'environmental',
            'refunded': None,
            'date_of_last_email': None,
            'other_text': 'REMOVED'
        }
        self.assertDictEqual(obs, exp)

    def test_post_bad_data(self):
        # Malformed date

        # Malformed Time

        # Missing data

        # Non-owned barcode
        raise NotImplementedError()

if __name__ == '__main__':
    main()
