from unittest import main
from amgut.test.tornado_test_base import TestHandlerBase
from amgut.connections import ag_data


class TestAddSampleOverview(TestHandlerBase):

    def test_get_overview_not_authed(self):
        response = self.get(
            '/authed/add_sample_overview')
        self.assertEqual(response.code, 404)
        self.assertTrue(
            response.effective_url.endswith('/authed/add_sample_overview'))

    def test_get_overview_human(self):
        # Test with human login id
        self.mock_login(
            ag_data.get_supplied_kit_id(
                'd8592c74-9694-2135-e040-8a80115d6401'))
        response = self.get(
            '/authed/add_sample_overview/')
        self.assertEqual(response.code, 200)
        self.assertTrue(
            response.effective_url.endswith('/authed/add_sample_overview/'))
        # Check for some main text
        self.assertIn('sample source', response.body)
        self.assertIn('REMOVED-2 - Human Source', response.body)
        self.assertIn('REMOVED-3 - Human Source', response.body)
        self.assertIn('REMOVED-0 - Human Source', response.body)
        self.assertIn('REMOVED-1 - Human Source', response.body)
        self.assertIn('Environmental', response.body)
        self.assertNotIn('- Animal Source', response.body)

    def test_get_overview_animal(self):
        # Test with animal login id
        self.mock_login(
            ag_data.get_supplied_kit_id(
                'd8592c74-8710-2135-e040-8a80115d6401'))
        response = self.get(
            '/authed/add_sample_overview/')
        self.assertEqual(response.code, 200)
        self.assertTrue(
            response.effective_url.endswith('/authed/add_sample_overview/'))
        # Check for some main text
        self.assertIn('sample source', response.body)
        self.assertIn('REMOVED-0 - Animal Source', response.body)
        self.assertIn('REMOVED-0 - Human Source', response.body)
        self.assertIn('REMOVED-1 - Human Source', response.body)
        self.assertIn('Environmental', response.body)


if __name__ == '__main__':
    main()
