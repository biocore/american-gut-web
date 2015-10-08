from unittest import main
import datetime
from amgut.test.tornado_test_base import TestHandlerBase
from amgut.connections import ag_data


class TestAddSampleOverview(TestHandlerBase):

    def test_get_overview_not_authed(self):
        response = self.get(
            '/authed/add_sample_overview')
        self.assertEqual(response.code, 404)
        self.assertTrue(
            response.effective_url.endswith('/authed/add_sample_overview'))

    def test_get_overview(self):
        self.mock_login('tst_LbxUH')
        response = self.get(
            '/authed/add_sample_overview/')
        self.assertEqual(response.code, 200)
        self.assertTrue(
            response.effective_url.endswith('/authed/add_sample_overview/'))

        # Check for some main text
        self.assertIn('sample source', response.body)


if __name__ == '__main__':
    main()
