from unittest import TestCase, main

from amgut.lib.util import (rollback)
from amgut.lib.geocode import geocode_aglogins
from amgut.lib.data_access.ag_data_access import AGDataAccess


class TestGeocoder(TestCase):
    def setUp(self):
        self.ag_data = AGDataAccess()

    def tearDown(self):
        del self.ag_data

    @rollback
    def test_force(self):
        # test if force leads to updating existing locations in DB
        logins = ["578f5c16-c8e3-40a4-a618-9661605678b0",
                  "d8592c74-8037-2135-e040-8a80115d6401",
                  "d8592c74-803a-2135-e040-8a80115d6401",
                  "884cba01-9d8a-4beb-816f-c74d85fb7227"]
        login_id = self.ag_data.addAGLogin('t1@sdjlhsd.dkzdj',
                                           'kurtjuergen_t1',
                                           '9500 Gilman Drive',
                                           'San Diego', 'CA', '', 'USA')
        logins.append(login_id)
        obs = geocode_aglogins(logins, force=True)
        exp = {'successful': 1, 'provided': 5, 'cannot_geocode': 4,
               'checked': 5}
        self.assertEqual(obs, exp)

    @rollback
    def test_multiple(self):
        logins = ["00164c87-73b3-deb2-e050-8a800c5d54e1",
                  "001b21ee-85a2-457c-adf6-492b42134376",
                  "0023cc03-3332-eec6-e050-8a800c5d3c04",
                  "d8592c74-967c-2135-e040-8a80115d6401",
                  "15370442-313f-452f-bf5b-cd155e3deefe"]
        login_id = self.ag_data.addAGLogin('t2@sdjlhsd.dkzdj',
                                           'kurtjuergen_t2',
                                           '9500 Gilman Drive',
                                           'San Diego', 'CA', '', 'USA')
        logins.append(login_id)
        obs = geocode_aglogins(logins)
        exp = {'successful': 1, 'provided': 6, 'cannot_geocode': 3,
               'checked': 4}
        self.assertEqual(obs, exp)

    @rollback
    def test_cannot_geocode(self):
        # check that a fantasy address cannot be geocoded.
        # Therefore we first need to insert a new ag_login_id
        login_id = self.ag_data.addAGLogin('notindb@sdjlhsd.dkzdj',
                                           'kurtjuergen_t4',
                                           'skdgsisdf', '', '', '', '')
        old_loc = self.ag_data.ut_get_location(login_id)
        self.assertEqual(old_loc, {'latitude': None,
                                   'cannot_geocode': None,
                                   'elevation': None,
                                   'longitude': None})
        obs = geocode_aglogins(login_id)
        exp = {'successful': 0, 'provided': 1, 'cannot_geocode': 1,
               'checked': 1}
        self.assertItemsEqual(obs, exp)
        new_loc = self.ag_data.ut_get_location(login_id)
        self.assertEqual(new_loc, {'latitude': None,
                                   'cannot_geocode': 'Y',
                                   'elevation': None,
                                   'longitude': None})

        # test that geocoding is re-done
        obs = geocode_aglogins(login_id)
        self.assertEqual(obs, exp)

    @rollback
    def test_update(self):
        # an ag_login_id without a location gets a new location assigned
        login_id = self.ag_data.addAGLogin('t3@sdjlhsd.dkzdj',
                                           'kurtjuergen_t3',
                                           '9500 Gilman Drive',
                                           'San Diego', 'CA', '', 'USA')
        old_loc = self.ag_data.ut_get_location(login_id)
        self.assertEqual(old_loc, {'latitude': None,
                                   'cannot_geocode': None,
                                   'elevation': None,
                                   'longitude': None})
        obs = geocode_aglogins(login_id)
        exp = {'successful': 1, 'provided': 1, 'cannot_geocode': 0,
               'checked': 1}
        self.assertItemsEqual(obs, exp)
        new_loc = self.ag_data.ut_get_location(login_id)
        self.assertEqual(new_loc, {'latitude': 32.8747486,
                                   'cannot_geocode': None,
                                   'elevation': 126.171813964844,
                                   'longitude': -117.2420258})

    @rollback
    def test_noupdate(self):
        # an ag_login_id already with location does not get updated
        login_id = "000fc4cd-8fa4-db8b-e050-8a800c5d02b5"
        old_loc = self.ag_data.ut_get_location(login_id)
        self.assertEqual(old_loc, {'latitude': 22.28661,
                                   'cannot_geocode': None,
                                   'elevation': 232.096176147461,
                                   'longitude': -80.73577})
        obs = geocode_aglogins(login_id)
        exp = {'successful': 0, 'provided': 1, 'cannot_geocode': 0,
               'checked': 0}
        self.assertItemsEqual(obs, exp)
        new_loc = self.ag_data.ut_get_location(login_id)
        self.assertEqual(new_loc, old_loc)


if __name__ == '__main__':
    main()
