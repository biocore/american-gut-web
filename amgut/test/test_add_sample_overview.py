from unittest import main
from amgut.test.tornado_test_base import TestHandlerBase
from amgut.connections import ag_data
from tornado import escape


class TestAddSampleOverview(TestHandlerBase):

    def test_get_overview_not_authed(self):
        response = self.get(
            '/authed/add_sample_overview')
        self.assertEqual(response.code, 404)
        self.assertTrue(
            response.effective_url.endswith('/authed/add_sample_overview'))

    def test_get_overview_human(self):
        # Test with human login id
        ag_login_id = 'd8592c74-9694-2135-e040-8a80115d6401'
        self.mock_login(ag_data.get_supplied_kit_id(ag_login_id))
        response = self.get('/authed/add_sample_overview/')
        self.assertEqual(response.code, 200)
        self.assertTrue(
            response.effective_url.endswith('/authed/add_sample_overview/'))
        # Check for some main text
        self.assertIn('sample source', response.body)
        names = ag_data.get_participant_names_from_ag_login_id(
            ag_login_id)
        for name in names:
            self.assertIn(escape.xhtml_escape(name), response.body)
        self.assertIn('Environmental', response.body)
        self.assertNotIn('- Animal Source', response.body)

    def test_get_overview_animal(self):
        # Test with animal login id
        ag_login_id = 'd8592c74-8710-2135-e040-8a80115d6401'
        self.mock_login(ag_data.get_supplied_kit_id(ag_login_id))
        response = self.get('/authed/add_sample_overview/')
        self.assertEqual(response.code, 200)
        self.assertTrue(
            response.effective_url.endswith('/authed/add_sample_overview/'))
        # Check for some main text
        names = ag_data.get_participant_names_from_ag_login_id(
            ag_login_id)
        self.assertIn('sample source', response.body)
        for name in names:
            self.assertIn(escape.xhtml_escape(name), response.body)
        self.assertIn('Environmental', response.body)


if __name__ == '__main__':
    main()
