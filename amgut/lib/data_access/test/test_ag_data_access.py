from unittest import TestCase, main
from random import choice, randint
from string import ascii_letters
from uuid import UUID
import datetime

from amgut.lib.data_access.ag_data_access import AGDataAccess


class TestAGDataAccess(TestCase):
    def setUp(self):
        self.ag_data = AGDataAccess()

    def tearDown(self):
        del self.ag_data

    def test___init__(self):
        raise NotImplementedError()

    def test___del__(self):
        raise NotImplementedError()

    def test_get_cursor(self):
        raise NotImplementedError()

    def test__open_connection(self):
        raise NotImplementedError()

    def test__get_col_names_from_cursor(self):
        raise NotImplementedError()

    def test_authenticateWebAppUser(self):
        raise NotImplementedError()

    def test_addAGLogin(self):
        # test new user
        exists = 'EXISTS'
        while exists is not None:
            email = ''.join([choice(ascii_letters)
                             for i in range(randint(5, 10))])
            domain = ''.join([choice(ascii_letters)
                             for i in range(randint(5, 10))])
            new_email = '@'.join([email, domain]) + '.com'
            exists = self.ag_data.check_login_exists(new_email)

        # make sure the ag_login_id is a UUID4 string
        ag_login_id = self.ag_data.addAGLogin(
            new_email, 'TESTDUDE', '123 fake test street', 'testcity',
            'teststate', '1L2 2G3', 'United Kingdom')
        as_uuid = UUID(ag_login_id)
        self.assertTrue(as_uuid.version, 4)

        # test existing user
        ag_login_id = self.ag_data.addAGLogin(
            'TEST@EMAIL.com', 'TESTOTHER', '123 fake test street', 'testcity',
            'teststate', '1L2 2G3', 'United Kingdom')

        obs = self.ag_data.addAGLogin(
            'test@EMAIL.com', 'TESTDUDE', '123 fake test street', 'testcity',
            'teststate', '1L2 2G3', 'United Kingdom')
        self.assertEqual(ag_login_id, obs)

    def test_getAGBarcodeDetails_bad_barcode(self):
        # test non-existant barcode
        obs = self.ag_data.getAGBarcodeDetails('99')
        self.assertEqual(obs, {})

        # test existing barcode but not in AG
        obs = self.ag_data.getAGBarcodeDetails('000006232')
        self.assertEqual(obs, {})

    def test_getAGBarcodeDetails(self):
        # test existing AG barcode
        obs = self.ag_data.getAGBarcodeDetails('000001047')
        exp = {
            'barcode': '000001047',
            'status': 'Received',
            'ag_kit_id': 'd8592c74-7e35-2135-e040-8a80115d6401',
            'name': 'REMOVED',
            'participant_name': 'REMOVED',
            'email': 'REMOVED',
            'site_sampled': 'Stool',
            'environment_sampled': None,
            'sample_date': datetime.date(2013, 3, 28),
            'sample_time': datetime.time(23, 25),
            'notes': 'REMOVED',
            'overloaded': None,
            'withdrawn': None,
            'other': None,
            'moldy': None,
            'refunded': None,
            'ag_kit_barcode_id': 'd8592c74-7e36-2135-e040-8a80115d6401',
            'date_of_last_email': None,
            'other_text': 'REMOVED'
        }
        self.assertEqual(obs, exp)

    def test_getAGKitDetails(self):
        # test non-existant kit
        obs = self.ag_data.getAGKitDetails('IDONTEXI5T')
        self.assertEqual(obs, {})

        # test existing AG kit
        obs = self.ag_data.getAGKitDetails('tst_ODmhG')
        exp = {'ag_kit_id': 'd8592c74-84bb-2135-e040-8a80115d6401',
               'supplied_kit_id': 'tst_ODmhG',
               'swabs_per_kit': 1,
               'verification_email_sent': 'n',
               'kit_verification_code': 'f4UjhV4B',
               'kit_password': '$2a$12$LiakUCHOpAMvEp9Wxehw5OIlD/TIIP0Bs3blw18'
                               'ePcmKHWWAePrQ.',
               'kit_verified': 'y'}
        self.assertEqual(obs, exp)

    def test_registerHandoutKit_bad_data(self):
        # run on bad data
        with self.assertRaises(ValueError):
            self.ag_data.registerHandoutKit('BAD', 'DATA')

    def test_registerHandoutKit_bad_idz(self):
        # run on non-existant login id
        ag_login_id = '11111111-1111-1111-1111-714297821c6a'
        kit = self.ag_data.get_all_handout_kits()[0]
        obs = self.ag_data.registerHandoutKit(ag_login_id, kit)
        self.assertFalse(obs)

        # run on non-existant kit_id
        ag_login_id = 'dc3172b2-792c-4087-8a20-714297821c6a'
        kit = 'NoTR3AL'
        obs = self.ag_data.registerHandoutKit(ag_login_id, kit)
        self.assertFalse(obs)

    def test_registerHandoutKit(self):
        # run on real data
        ag_login_id = 'dc3172b2-792c-4087-8a20-714297821c6a'
        kit = self.ag_data.get_all_handout_kits()[0]
        obs = self.ag_data.registerHandoutKit(ag_login_id, kit)
        self.assertTrue(obs)
        # make sure kit removed from ag_handout_kits and inserted in ag_kit
        kits = self.ag_data.get_all_handout_kits()
        self.assertTrue(kit not in kits)
        obs = self.ag_data.getAGKitDetails(kit)
        self.assertEqual(obs['supplied_kit_id'], kit)

    def test_deleteAGParticipantSurvey(self):
        raise NotImplementedError()

    def test_getConsent(self):
        raise NotImplementedError()

    def test_logParticipantSample_badinfo(self):
        # bad ag_login_id
        with self.assertRaises(RuntimeError):
            self.ag_data.logParticipantSample(
                '11111111-1111-1111-1111-714297821c6a', '000001047',
                'stool', None, datetime.date(2015, 9, 27),
                datetime.time(15, 54), 'BADNAME', '')

    def test_logParticipantSample(self):
        # regular sample
        ag_login_id = 'd8592c74-9694-2135-e040-8a80115d6401'
        barcode = '000005626'

        self.ag_data.logParticipantSample(
            ag_login_id, barcode, 'Stool', None, datetime.date(2015, 9, 27),
            datetime.time(15, 54), 'REMOVED-0', '')
        obs = self.ag_data.getAGBarcodeDetails('000005626')
        exp = {
            'status': None,
            'ag_kit_id': 'db447092-6209-54d8-e040-8a80115d3637',
            'ag_kit_barcode_id': 'db447092-620c-54d8-e040-8a80115d3637',
            'barcode': '000005626',
            'environment_sampled': None,
            'site_sampled': 'Stool',
            'name': 'REMOVED',
            'sample_date': datetime.date(2015, 9, 27),
            'sample_time': datetime.time(15, 54),
            'notes': '', 'overloaded': None,
            'withdrawn': None,
            'email': 'REMOVED',
            'other': None,
            'moldy': None,
            'participant_name': 'REMOVED-0',
            'refunded': None,
            'date_of_last_email': None,
            'other_text': 'REMOVED'
        }
        self.assertEqual(obs, exp)
        self.ag_data.deleteSample(barcode, ag_login_id)

        # env sample
        self.ag_data.logParticipantSample(
            ag_login_id, barcode, None, 'animal_habitat',
            datetime.date(2015, 9, 26), datetime.time(15, 00), 'REMOVED', '')
        obs = self.ag_data.getAGBarcodeDetails('000005626')
        exp = {
            'status': None,
            'ag_kit_id': 'db447092-6209-54d8-e040-8a80115d3637',
            'ag_kit_barcode_id': 'db447092-620c-54d8-e040-8a80115d3637',
            'barcode': '000005626',
            'environment_sampled': 'animal_habitat',
            'site_sampled': None,
            'name': 'REMOVED',
            'sample_date': datetime.date(2015, 9, 26),
            'sample_time': datetime.time(15, 00),
            'notes': '', 'overloaded': None,
            'withdrawn': None,
            'email': 'REMOVED',
            'other': None,
            'moldy': None,
            'participant_name': 'REMOVED-0',
            'refunded': None,
            'date_of_last_email': None,
            'other_text': 'REMOVED'
        }
        self.assertEqual(obs, exp)

        self.ag_data.deleteSample(barcode, ag_login_id)

    def test_deleteSample(self):
        raise NotImplementedError()

    def test_getHumanParticipants(self):
        raise NotImplementedError()

    def test_is_old_survey(self):
        raise NotImplementedError()

    def test_updateVioscreenStatus(self):
        raise NotImplementedError()

    def test_getAnimalParticipants(self):
        raise NotImplementedError()

    def test_getParticipantSamples(self):
        raise NotImplementedError()

    def test_getEnvironmentalSamples(self):
        raise NotImplementedError()

    def test_getAvailableBarcodes(self):
        raise NotImplementedError()

    def test_verifyKit(self):
        raise NotImplementedError()

    def test_getMapMarkers(self):
        raise NotImplementedError()

    def test_handoutCheck(self):
        raise NotImplementedError()

    def test_check_access(self):
        raise NotImplementedError()

    def test_getAGKitIDsByEmail(self):
        raise NotImplementedError()

    def test_ag_set_pass_change_code(self):
        raise NotImplementedError()

    def test_ag_update_kit_password(self):
        raise NotImplementedError()

    def test_ag_verify_kit_password_change_code(self):
        raise NotImplementedError()

    def test_getBarcodesByKit(self):
        raise NotImplementedError()

    def test_checkPrintResults(self):
        raise NotImplementedError()

    def test_get_user_for_kit(self):
        raise NotImplementedError()

    def test_get_menu_items(self):
        raise NotImplementedError()

    def test_check_if_consent_exists(self):
        raise NotImplementedError()

    def test_get_user_info(self):
        raise NotImplementedError()

    def test_get_person_info(self):
        raise NotImplementedError()

    def test_get_barcode_results(self):
        raise NotImplementedError()

    def test_get_login_info(self):
        raise NotImplementedError()

    def test_get_survey_id(self):
        raise NotImplementedError()

    def test_get_countries(self):
        raise NotImplementedError()


if __name__ == "__main__":
    main()
