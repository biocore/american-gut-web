from unittest import main

from tornado.escape import url_escape

from amgut.connections import ag_data
from amgut.test.tornado_test_base import TestHandlerBase
from amgut import text_locale


class TestAuthBasehandler(TestHandlerBase):
    def test_set_current_user(self):
        # test if new cookie will be set
        response = self.get('/auth/register/')
        self.assertIn('Set-Cookie', response.headers.keys())

        # test that cookie is re-used
        self.mock_login('tst_ACJUJ')
        response = self.get('/auth/register/')
        self.assertNotIn('Set-Cookie', response.headers.keys())


class TestAuthRegisterHandoutHandler(TestHandlerBase):
    def test_get(self):
        response = self.get('/auth/register/')
        self.assertEqual(response.code, 200)
        port = self.get_http_port()
        self.assertEqual(response.effective_url,
                         'http://localhost:%d/auth/register/' % port)

    def test_post(self):
        # test reaction to invalid kit IDs
        response = self.post('/auth/register/',
                             {'kit_id': 'wrong_kit_id',
                              'password': 'test',
                              'email': 'e@mail',
                              'email2': 'e@mail',
                              'participantname': 'joe',
                              'address': 'street',
                              'city': 'metropolis',
                              'state': 'XX',
                              'zip': '12345',
                              'country': 'Afghanistan'})
        port = self.get_http_port()
        self.assertEqual(
            response.effective_url,
            'http://localhost:%d/?loginerror=%s' %
            (port, url_escape(text_locale['handlers']['INVALID_KITID'])))

        unregistered_kits = ag_data.get_all_handout_kits()
        if len(unregistered_kits) <= 0:
            raise Exception(("Test cannot be performed. No more un-registered "
                             "kit IDs in the database. Re-set test database!"))
        else:
            response = self.post('/auth/register/',
                                 {'kit_id': unregistered_kits[0],
                                  'password': 'test',
                                  'email': 'e@mail',
                                  'email2': 'e@mail',
                                  'participantname': 'joe',
                                  'address': 'street',
                                  'city': 'metropolis',
                                  'state': 'XX',
                                  'zip': '12345',
                                  'country': 'Afghanistan'})
            port = self.get_http_port()
            self.assertEqual(response.code, 200)
            self.assertEqual(
                response.effective_url,
                'http://localhost:%d/?next=%s' %
                (port, url_escape('/authed/portal/')))

            # Check that registration changed the DB. A proxy to test that no
            # ValueError is raised.
            self.assertNotEqual(ag_data.get_user_for_kit(unregistered_kits[0]),
                                'something')


class TestAuthLoginHandler(TestHandlerBase):
    def test_get(self):
        response = self.get('/auth/login/')
        self.assertEqual(response.code, 200)
        # make sure redirect happened properly
        port = self.get_http_port()
        self.assertEqual(response.effective_url, 'http://localhost:%d/' % port)

        # check if url is wrong. SJ: Is this in general a good idea?
        response = self.get('/authh/login/')
        self.assertEqual(response.code, 404)

    def test_post_correct_pass(self):
        # test a sucessful login, for a handout kit
        self.mock_login('tst_ACJUJ')
        response = self.get('/authed/portal/')
        self.assertEqual(response.code, 200)
        self.assertNotIn(text_locale['handlers']['REGISTER_KIT'],
                         response.body)

        # test a sucessful login, for a non-handout kit
        self.mock_login('tst_aAdKt')
        response = self.get('/authed/portal/')
        self.assertEqual(response.code, 200)
        self.assertIn(text_locale['portal.html']['VERIFICATION_HEADER_2'],
                      response.body)

    def test_post_wrong_pass(self):
        # check that invalid kit is reported for non existent skid
        response = self.post('/auth/login/', {'skid': 'wrong',
                                              'passwd': 'test'})
        self.assertIn(text_locale['handlers']['INVALID_KITID'], response.body)
        self.assertEqual(response.code, 200)

        # check that invalid Password is reported for wrong password
        response = self.post('/auth/login/', {'skid': 'tst_ACJUJ',
                                              'passwd': 'wrong'})
        self.assertIn(text_locale['handlers']['INVALID_KITID'], response.body)
        self.assertEqual(response.code, 200)

    def test_set_current_user(self):
        # TODO: add proper test for this once figure out how. Issue 567
        pass


class TestAuthLogoutHandler(TestHandlerBase):
    def test_get(self):
        response = self.get('/auth/login/')
        self.assertEqual(response.code, 200)
        # make sure redirect happened properly
        port = self.get_http_port()
        self.assertEqual(response.effective_url, 'http://localhost:%d/' % port)


if __name__ == "__main__":
    main()
