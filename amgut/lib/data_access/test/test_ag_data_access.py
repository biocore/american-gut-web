from unittest import TestCase, main
import datetime
from random import choice, randint
from string import ascii_letters
from uuid import UUID

from psycopg2 import DataError

from amgut.lib.data_access.ag_data_access import AGDataAccess


class TestAGDataAccess(TestCase):
    def setUp(self):
        self.ag_data = AGDataAccess()

    def tearDown(self):
        del self.ag_data

    def test_authenticateWebAppUser(self):
        raise NotImplementedError()

    def test_check_login_exists(self):
        email = 'Reallylongemailthatshouldntexist@someplacenotreal.com'
        obs = self.ag_data.check_login_exists(email)
        self.assertEqual(obs, None)

        email = 'REMOVED'
        obs = self.ag_data.check_login_exists(email)
        as_uuid = UUID(obs)
        self.assertTrue(as_uuid.version, 4)

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

    def test_get_all_handout_kits(self):
        obs = self.ag_data.get_all_handout_kits()
        self.assertTrue(isinstance(obs, list))
        self.assertTrue(len(obs) > 0)

        for kit_id in obs:
            self.assertRegexpMatches(kit_id, 'tst_[a-zA-Z]{5}')

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
        self.assertNotIn(kit, kits)
        obs = self.ag_data.getAGKitDetails(kit)
        self.assertEqual(obs['supplied_kit_id'], kit)

    def test_deleteAGParticipantSurvey(self):
        raise NotImplementedError()

    def test_getConsent(self):

        res = self.ag_data.getConsent("8b2b45bb3390b585")
        exp = {'date_signed': 'None',
               'assent_obtainer': None,
               'age_range': None,
               'parent_1_name': 'REMOVED',
               'participant_email': 'REMOVED',
               'parent_2_name': 'REMOVED',
               'ag_login_id': '000fc4cd-8fa4-db8b-e050-8a800c5d02b5',
               'deceased_parent': 'false',
               'participant_name': 'REMOVED-0',
               'survey_id': '8b2b45bb3390b585',
               'is_juvenile': False}
        self.assertEquals(res, exp)

    def test_getConsentNotPresent(self):
        res = self.ag_data.getConsent("42")
        self.assertEquals(res, None)

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
            'status': '',
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
            'status': '',
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
            'participant_name': 'REMOVED',
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
        i = "d6b0f287-b9d9-40d4-82fd-a8fd3db6c476"
        res = self.ag_data.getParticipantSamples(i, "REMOVED")
        exp = [{'status': None,
                'sample_time': datetime.time(11, 55),
                'notes': 'REMOVED',
                'barcode': '000028432',
                'sample_date': datetime.date(2015, 6, 7),
                'site_sampled': 'Stool'}]
        self.assertEqual(res, exp)

        i = "d8592c74-9694-2135-e040-8a80115d6401"
        res = self.ag_data.getParticipantSamples(i, "REMOVED")
        exp = [{'status': 'Received',
                'sample_time': datetime.time(7, 40),
                'notes': 'REMOVED',
                'barcode': '000016704',
                'sample_date': datetime.date(2014, 6, 5),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(11, 30),
                'notes': 'REMOVED',
                'barcode': '000016705',
                'sample_date': datetime.date(2014, 6, 1),
                'site_sampled': 'Stool'},
               {'status': 'Received', 'sample_time': datetime.time(9, 20),
                'notes': 'REMOVED',
                'barcode': '000016706',
                'sample_date': datetime.date(2014, 6, 8),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(9, 20),
                'notes': 'REMOVED',
                'barcode': '000016707',
                'sample_date': datetime.date(2014, 6, 1),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(22, 0),
                'notes': 'REMOVED',
                'barcode': '000016708',
                'sample_date': datetime.date(2014, 5, 28),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(11, 0),
                'notes': 'REMOVED',
                'barcode': '000016709',
                'sample_date': datetime.date(2014, 5, 29),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(22, 20),
                'notes': 'REMOVED',
                'barcode': '000016710',
                'sample_date': datetime.date(2014, 5, 27),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(8, 0),
                'notes': 'REMOVED',
                'barcode': '000016711',
                'sample_date': datetime.date(2014, 6, 11),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(8, 15),
                'notes': 'REMOVED',
                'barcode': '000016712',
                'sample_date': datetime.date(2014, 6, 2),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(12, 0),
                'notes': 'REMOVED',
                'barcode': '000016713',
                'sample_date': datetime.date(2014, 5, 30),
                'site_sampled': 'Stool'},
               {'status': None,
                'sample_time': datetime.time(19, 30),
                'notes': 'REMOVED',
                'barcode': '000016496',
                'sample_date': datetime.date(2014, 4, 29),
                'site_sampled': 'Stool'},
               {'status': None,
                'sample_time': datetime.time(19, 30),
                'notes': 'REMOVED',
                'barcode': '000016497',
                'sample_date': datetime.date(2014, 4, 29),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(10, 20),
                'notes': 'REMOVED',
                'barcode': '000004213',
                'sample_date': datetime.date(2013, 10, 16),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(9, 50),
                'notes': 'REMOVED',
                'barcode': '000004214',
                'sample_date': datetime.date(2013, 10, 14),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(12, 0),
                'notes': 'REMOVED',
                'barcode': '000004215',
                'sample_date': datetime.date(2013, 10, 13),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(9, 30),
                'notes': 'REMOVED',
                'barcode': '000004216',
                'sample_date': datetime.date(2013, 10, 15),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(14, 25),
                'notes': 'REMOVED',
                'barcode': '000004218',
                'sample_date': datetime.date(2013, 10, 12),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(10, 15),
                'notes': 'REMOVED',
                'barcode': '000004219',
                'sample_date': datetime.date(2013, 10, 17),
                'site_sampled': 'Stool'}]
        self.assertItemsEqual(res, exp)

    def test_getParticipantSamplesNotPresent(self):
        i = '00000000-0000-0000-0000-000000000000'
        res = self.ag_data.getParticipantSamples(i, "REMOVED")
        self.assertEqual(res, [])

    def test_getEnvironmentalSamples(self):
        i = "d6b0f287-b9d9-40d4-82fd-a8fd3db6c476"
        res = self.ag_data.getEnvironmentalSamples(i)
        exp = [{'status': None, 'sample_time': datetime.time(21, 45),
                'notes': 'REMOVED', 'barcode': '000028433',
                'sample_date': datetime.date(2015, 6, 7),
                'site_sampled': None}]
        self.assertItemsEqual(res, exp)

    def test_getEnvironmentalSamplesNotPresent(self):
        i = '00000000-0000-0000-0000-000000000000'
        res = self.ag_data.getEnvironmentalSamples(i)
        self.assertEqual(res, [])

    def test_getAvailableBarcodes(self):
        i = "d8592c74-9694-2135-e040-8a80115d6401"
        res = self.ag_data.getAvailableBarcodes(i)
        exp = ['000005628', '000005627', '000005624',
               '000005625', '000005626', '000004217']
        self.assertItemsEqual(res, exp)

        i = "d6b0f287-b9d9-40d4-82fd-a8fd3db6c476"
        res = self.ag_data.getAvailableBarcodes(i)
        exp = ['000028434']
        self.assertItemsEqual(res, exp)

    def test_getAvailableBarcodesNotPresent(self):
        i = '00000000-0000-0000-0000-000000000000'
        res = self.ag_data.getAvailableBarcodes(i)
        self.assertEqual(res, [])

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
        res = self.ag_data.getBarcodesByKit('tst_qmhLX')
        exp = ['000001322']
        self.assertItemsEqual(res, exp)

    def test_getBarcodesByKitNotPresent(self):
        res = self.ag_data.getBarcodesByKit('42')
        self.assertEqual(res, [])

    def test_checkPrintResults(self):
        obs = self.ag_data.checkPrintResults('tst_oasoR')
        self.assertFalse(obs)

        obs = self.ag_data.checkPrintResults('tst_TMYwD')
        self.assertTrue(obs)

    def test_checkPrintResults_invalid_ids(self):
        obs = self.ag_data.checkPrintResults('xxx00112333123---123222')
        self.assertFalse(obs)

        obs = self.ag_data.checkPrintResults(':Lfoo:Lbar:Lbaz:Ospam:Leggs')
        self.assertFalse(obs)

    def test_get_user_for_kit(self):
        obs = self.ag_data.get_user_for_kit('tst_IueFX')
        self.assertEqual('ded5101d-c8e3-f6b3-e040-8a80115d6f03', obs)

        obs = self.ag_data.get_user_for_kit('tst_esABz')
        self.assertEqual('d8592c74-8421-2135-e040-8a80115d6401', obs)

    def test_get_user_for_kit_errors(self):
        with self.assertRaises(RuntimeError):
            self.ag_data.get_user_for_kit('the_fooster')

        with self.assertRaises(RuntimeError):
            self.ag_data.get_user_for_kit('tst_esXXX')

    def test_get_menu_items(self):
        obs = self.ag_data.get_menu_items('tst_pDWcB')
        self.assertEqual(({}, {}, [], True), obs)

        obs = self.ag_data.get_menu_items('tst_VpQsT')
        self.assertEqual(({'REMOVED-0': []}, {}, [], True), obs)

    def test_get_menu_items_errors(self):
        with self.assertRaises(RuntimeError):
            self.ag_data.get_menu_items('tst_esXXX')

    def test_check_if_consent_exists(self):
        obs = self.ag_data.check_if_consent_exists(
            '00711b0a-67d6-0fed-e050-8a800c5d7570', 'REMOVED-42')
        self.assertTrue(obs)

    def test_check_if_consent_exists_non_existent_user(self):
        obs = self.ag_data.check_if_consent_exists(
            '00711b0a-67d6-0fed-e050-8a800c5d7570', 'REMOVED-111')
        self.assertFalse(obs)

    def test_get_user_info(self):
        obs = self.ag_data.get_user_info('tst_wAhSB')
        exp = {'address': 'REMOVED', 'ag_login_id':
               'd8592c74-84a5-2135-e040-8a80115d6401', 'city': 'REMOVED',
               'country': 'REMOVED', 'email': 'REMOVED', 'name': 'REMOVED',
               'state': 'REMOVED', 'zip': 'REMOVED'}
        self.assertEqual(exp, obs)

    def test_get_user_info_non_existent(self):
        obs = self.ag_data.get_user_info('tst_XX1123')
        self.assertEqual({}, obs)

    def test_get_barcode_results(self):
        obs = self.ag_data.get_barcode_results('tst_yCzro')
        exp = [{'barcode': '000016704', 'participant_name': 'REMOVED'},
               {'barcode': '000016705', 'participant_name': 'REMOVED'},
               {'barcode': '000016706', 'participant_name': 'REMOVED'},
               {'barcode': '000016707', 'participant_name': 'REMOVED'},
               {'barcode': '000016708', 'participant_name': 'REMOVED'},
               {'barcode': '000016709', 'participant_name': 'REMOVED'},
               {'barcode': '000016710', 'participant_name': 'REMOVED'},
               {'barcode': '000016711', 'participant_name': 'REMOVED'},
               {'barcode': '000016712', 'participant_name': 'REMOVED'},
               {'barcode': '000016713', 'participant_name': 'REMOVED'},
               {'barcode': '000004213', 'participant_name': 'REMOVED'},
               {'barcode': '000004214', 'participant_name': 'REMOVED'},
               {'barcode': '000004215', 'participant_name': 'REMOVED'},
               {'barcode': '000004216', 'participant_name': 'REMOVED'},
               {'barcode': '000004218', 'participant_name': 'REMOVED'},
               {'barcode': '000004219', 'participant_name': 'REMOVED'}]
        self.assertEqual(obs, exp)

    def test_get_barcode_results_non_existant_id(self):
        with self.assertRaises(RuntimeError):
            self.ag_data.get_barcode_results("something that doesn't exist")

    def test_get_login_info(self):
        id_ = 'fecebeae-4244-2d78-e040-8a800c5d4f50'
        exp = [{'ag_login_id': id_,
                'email': 'REMOVED',
                'name': 'REMOVED',
                'address': 'REMOVED',
                'city': 'REMOVED',
                'state': 'REMOVED',
                'zip': 'REMOVED',
                'country': 'REMOVED'}]
        obs = self.ag_data.get_login_info(id_)
        self.assertEqual(obs, exp)

    def test_get_login_info_non_existant_id(self):
        with self.assertRaises(DataError):
            self.ag_data.get_login_info("id does not exist")

    def test_get_survey_id(self):
        id_ = '8ca47059-000a-469f-aa64-ff1afbd6fcb1'
        obs = self.ag_data.get_survey_id(id_, 'REMOVED-0')
        self.assertEquals(obs, 'd08758a1510256f0')

    def test_get_survey_id_non_existant_id(self):
        id_ = 'does not exist'
        with self.assertRaises(DataError):
            self.ag_data.get_survey_id(id_, 'REMOVED')

    def test_get_countries(self):
        raise NotImplementedError()


if __name__ == "__main__":
    main()
