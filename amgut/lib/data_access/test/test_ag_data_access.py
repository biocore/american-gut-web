from unittest import TestCase, main
import datetime
from random import choice, randint
from string import ascii_letters
from uuid import UUID

from amgut.lib.data_access.ag_data_access import AGDataAccess
from amgut.lib.util import rollback


class TestAGDataAccess(TestCase):
    def setUp(self):
        self.ag_data = AGDataAccess()

    def tearDown(self):
        del self.ag_data

    def test_authenticateWebAppUser(self):
        # Test right pass but non-existant kit ID
        obs = self.ag_data.authenticateWebAppUser('randomkitID', 'test')
        self.assertEqual(obs, False)

        kit_id = 'tst_xfphP'
        # Test wrong password
        obs = self.ag_data.authenticateWebAppUser(kit_id, 'wrongPass')
        self.assertEqual(obs, False)

        # Test corect password
        obs = self.ag_data.authenticateWebAppUser(kit_id, 'test')
        self.assertTrue(isinstance(obs, dict))
        self.assertEqual(obs['ag_login_id'],
                         'ded5101d-cafb-f6b3-e040-8a80115d6f03')

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
        with self.assertRaises(ValueError):
            self.ag_data.getAGBarcodeDetails('99')

        # test existing barcode but not in AG
        with self.assertRaises(ValueError):
            self.ag_data.getAGBarcodeDetails('000006232')

    def test_get_nonconsented_scanned_barcodes(self):
        obs = self.ag_data.get_nonconsented_scanned_barcodes('tst_KWfyv')
        exp = ['000027262']
        self.assertEqual(obs, exp)

    def test_getAGBarcodeDetails(self):
        # test existing AG barcode
        obs = self.ag_data.getAGBarcodeDetails('000001047')
        exp = {
            'barcode': '000001047',
            'status': 'Received',
            'ag_kit_id': 'd8592c74-7e35-2135-e040-8a80115d6401',
            'name': 'REMOVED',
            'participant_name': 'REMOVED-0',
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
        with self.assertRaises(ValueError):
            self.ag_data.getAGKitDetails('IDONTEXI5T')

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
        ag_login_id = '877bb1b5-7352-48bf-a7b1-1248c689b819'
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

    @rollback
    def test_deleteAGParticipantSurvey(self):
        # make sure we can get the corresponding survey by ID
        _ = self.ag_data.getConsent('8b2b45bb3390b585')

        self.ag_data.deleteAGParticipantSurvey(
            '000fc4cd-8fa4-db8b-e050-8a800c5d02b5', 'REMOVED-0')

        with self.assertRaises(ValueError):
            self.ag_data.getConsent('8b2b45bb3390b585')

        res = self.ag_data.get_withdrawn()
        today = datetime.datetime.now().date()
        exp = [['000fc4cd-8fa4-db8b-e050-8a800c5d02b5', 'REMOVED-0',
                'REMOVED', today]]
        self.assertItemsEqual(res, exp)

    @rollback
    def test_deleteAGParticipantSurvey_with_sample_bug(self):
        # issue 616
        self.ag_data.deleteAGParticipantSurvey(
            'd8592c74-9694-2135-e040-8a80115d6401', 'REMOVED-0')
        with self.assertRaises(ValueError):
            self.ag_data.getConsent('be8516e8c5d4ff4d')

    def test_getConsent(self):
        res = self.ag_data.getConsent("8b2b45bb3390b585")
        exp = {'date_signed': None,
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
        with self.assertRaises(ValueError):
            self.ag_data.getConsent("42")

    def test_logParticipantSample_badinfo(self):
        # bad ag_login_id
        with self.assertRaises(ValueError):
            self.ag_data.logParticipantSample(
                '11111111-1111-1111-1111-714297821c6a', '000001047',
                'stool', None, datetime.date(2015, 9, 27),
                datetime.time(15, 54), 'BADNAME', '')

    def test_logParticipantSample(self):
        # regular sample
        ag_login_id = '7732aafe-c4e1-4ae4-8337-6f22704c1064'
        barcode = '000027376'

        self.ag_data.logParticipantSample(
            ag_login_id, barcode, 'Stool', None, datetime.date(2015, 9, 27),
            datetime.time(15, 54), 'REMOVED-0', '')
        obs = self.ag_data.getAGBarcodeDetails(barcode)
        exp = {'status': None,
               'ag_kit_id': '5bfa9526-8dbb-492f-937c-bceb6b5a56fe',
               'ag_kit_barcode_id': '793dab39-d9bf-4a0f-8d67-f21796e3faae',
               'barcode': '000027376',
               'site_sampled': 'Stool',
               'environment_sampled': None,
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
        self.ag_data.deleteSample(barcode, ag_login_id)
        self.assertEqual(obs, exp)

        # env sample
        self.ag_data.logParticipantSample(
            ag_login_id, barcode, None, 'animal_habitat',
            datetime.date(2015, 9, 26), datetime.time(15, 00), 'REMOVED', '')
        obs = self.ag_data.getAGBarcodeDetails(barcode)
        exp = {'status': None,
               'ag_kit_id': '5bfa9526-8dbb-492f-937c-bceb6b5a56fe',
               'ag_kit_barcode_id': '793dab39-d9bf-4a0f-8d67-f21796e3faae',
               'barcode': '000027376',
               'site_sampled': None,
               'environment_sampled': 'animal_habitat',
               'name': 'REMOVED',
               'sample_date': datetime.date(2015, 9, 26),
               'sample_time': datetime.time(15, 00),
               'notes': '', 'overloaded': None,
               'withdrawn': None,
               'email': 'REMOVED',
               'other': None,
               'moldy': None,
               'participant_name': None,
               'refunded': None,
               'date_of_last_email': None,
               'other_text': 'REMOVED'
               }
        self.ag_data.deleteSample(barcode, ag_login_id)
        self.assertEqual(obs, exp)

    def test_getHumanParticipants(self):
        i = "d8592c74-9694-2135-e040-8a80115d6401"
        res = self.ag_data.getHumanParticipants(i)
        exp = ['REMOVED-2', 'REMOVED-0', 'REMOVED-3', 'REMOVED-1']
        self.assertItemsEqual(res, exp)

    def test_getHumanParticipantsNotPresent(self):
        i = '00000000-0000-0000-0000-000000000000'
        res = self.ag_data.getHumanParticipants(i)
        self.assertEqual(res, [])

    def test_vioscreen_status(self):
        survey_id = 'eba20dea4f54b997'
        self.ag_data.updateVioscreenStatus(survey_id, 3)
        obs = self.ag_data.get_vioscreen_status(survey_id)
        self.assertEqual(obs, 3)

        self.ag_data.updateVioscreenStatus(survey_id, None)
        obs = self.ag_data.get_vioscreen_status(survey_id)
        self.assertEqual(obs, None)

    def test_get_vioscreen_status_unknown_survey(self):
        with self.assertRaises(ValueError):
            self.ag_data.get_vioscreen_status('SomeRandomSurveyID')

    def test_getAnimalParticipants(self):
        i = "ed5ab96f-fe3b-ead5-e040-8a80115d1c4b"
        res = self.ag_data.getAnimalParticipants(i)
        exp = ['REMOVED-0']
        self.assertItemsEqual(res, exp)

    def test_getAnimalParticipantsNotPresent(self):
        i = "00711b0a-67d6-0fed-e050-8a800c5d7570"
        res = self.ag_data.getAnimalParticipants(i)
        self.assertEqual(res, [])

    def test_getParticipantSamples(self):
        i = "d6b0f287-b9d9-40d4-82fd-a8fd3db6c476"
        res = self.ag_data.getParticipantSamples(i, "REMOVED-0")
        exp = [{'status': None,
                'sample_time': datetime.time(11, 55),
                'notes': 'REMOVED',
                'barcode': '000028432',
                'sample_date': datetime.date(2015, 6, 7),
                'site_sampled': 'Stool'}]
        self.assertEqual(res, exp)

        i = "d8592c74-9694-2135-e040-8a80115d6401"
        res = self.ag_data.getParticipantSamples(i, "REMOVED-0")
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
        # Test verifying works
        kit = self.ag_data._get_unverified_kits()[0]
        self.ag_data.verifyKit(kit)
        obs = self.ag_data.getAGKitDetails(kit)
        self.assertEqual(obs['kit_verified'], 'y')

        # Test verifying a non-existant kit
        with self.assertRaises(ValueError):
            self.ag_data.getAGKitDetails('NOTAREALKITID')

    def test__get_unverified_kits(self):
        obs = self.ag_data._get_unverified_kits()
        self.assertTrue(isinstance(obs, list))
        self.assertTrue(len(obs) > 0)

        for kit_id in obs:
            self.assertRegexpMatches(kit_id, 'tst_[a-zA-Z]{5}')
            obs = self.ag_data.getAGKitDetails(kit_id)
            self.assertEqual(obs['kit_verified'], 'n')

    def test_handoutCheck(self):
        # Test proper password for handout
        # All tests use assertEqual to make sure bool object returned
        kit = self.ag_data.get_all_handout_kits()[0]
        obs = self.ag_data.handoutCheck(kit, 'test')
        self.assertEqual(obs, True)

        # Test wrong password
        obs = self.ag_data.handoutCheck(kit, 'badPass')
        self.assertEqual(obs, False)

        # Test non-handout kit
        obs = self.ag_data.handoutCheck('tst_ODmhG', 'test')
        self.assertEqual(obs, False)
        obs = self.ag_data.handoutCheck('randomKitID', 'test')
        self.assertEqual(obs, False)

    def test_check_access(self):
        # Has access
        obs = self.ag_data.check_access('tst_BudVu', '000001047')
        self.assertEqual(obs, True)

        # No access
        obs = self.ag_data.check_access('tst_BudVu', '000001111')
        self.assertEqual(obs, False)

    def test_ag_set_pass_change_code(self):
        # Generate new random code and assign it
        testcode = ''.join(choice(ascii_letters) for i in range(10))
        self.ag_data.ag_set_pass_change_code('REMOVED', 'tst_ULGcr', testcode)

        # Actually test the code change
        obs = self.ag_data.ag_verify_kit_password_change_code(
            'REMOVED', 'tst_ULGcr', 'SOMELONGTHINGTHATWILLFAIL')
        self.assertEqual(obs, False)
        obs = self.ag_data.ag_verify_kit_password_change_code(
            'REMOVED', 'tst_ULGcr', testcode)
        # Using equal to make sure boolean True is returned, not something that
        # equates to True
        self.assertEqual(obs, True)

        # Test giving nonsense email
        # TODO: make this raise error and test
        self.ag_data.ag_set_pass_change_code('Fake@notarealemail.com',
                                             'tst_ULGcr', testcode)

        # Test giving bad skid
        # TODO: make this raise error and test
        self.ag_data.ag_set_pass_change_code('REMOVED', 'NOTINTHEDB', testcode)

    def test_ag_update_kit_password(self):
        # Generate new pass and make sure is different from current pass
        newpass = ''.join(choice(ascii_letters) for i in range(randint(8, 15)))
        auth = self.ag_data.authenticateWebAppUser('tst_ULGcr', newpass)
        self.assertFalse(
            auth, msg="Randomly generated password matches existing")

        # Actually test password change
        self.ag_data.ag_update_kit_password('tst_ULGcr', newpass)
        auth = self.ag_data.authenticateWebAppUser('tst_ULGcr', newpass)
        self.assertTrue(isinstance(auth, dict))
        self.assertEqual(auth['ag_login_id'],
                         'd8592c74-8416-2135-e040-8a80115d6401')

        # Test giving bad skid
        # TODO: make this raise error and test
        self.ag_data.ag_update_kit_password('NOTINTHEDB', newpass)

    def test_ag_verify_kit_password_change_code(self):
        # Test actual functionality
        obs = self.ag_data.ag_verify_kit_password_change_code(
            'REMOVED', 'tst_omubN', 'FAIL')
        # Using assertEqual to make sure boolean False is returned, not
        # something that equates to False. Same for rest of assertEquals below
        self.assertEqual(obs, False)
        # Outside reset time, should fail
        obs = self.ag_data.ag_verify_kit_password_change_code(
            'REMOVED', 'tst_omubN', 'Mw1eY4wWVXpE0cQlvQwS')
        self.assertEqual(obs, False)

        # Reset code and make sure it works
        testcode = ''.join(choice(ascii_letters) for i in range(10))
        self.ag_data.ag_set_pass_change_code('REMOVED', 'tst_ULGcr', testcode)
        obs = self.ag_data.ag_verify_kit_password_change_code(
            'REMOVED', 'tst_ULGcr', testcode)
        self.assertEqual(obs, True)

        # Test with incorrect kit id
        obs = self.ag_data.ag_verify_kit_password_change_code(
            'REMOVED', 'NOTAREALKITID', 'FAIL')
        self.assertEqual(obs, False)

        # Test with incorrect email
        obs = self.ag_data.ag_verify_kit_password_change_code(
            'notreal@fake.com', 'tst_ULGcr', testcode)
        self.assertEqual(obs, False)

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
        with self.assertRaises(ValueError):
            self.ag_data.get_user_for_kit('the_fooster')

        with self.assertRaises(ValueError):
            self.ag_data.get_user_for_kit('tst_esXXX')

    def test_get_menu_items(self):
        obs = self.ag_data.get_menu_items('tst_pDWcB')
        self.assertEqual(({}, {}, [], True), obs)

        obs = self.ag_data.get_menu_items('tst_VpQsT')
        self.assertEqual(({'REMOVED-0': []}, {}, [], True), obs)

    def test_get_menu_items_errors(self):
        with self.assertRaises(ValueError):
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
        with self.assertRaises(ValueError):
            self.ag_data.get_user_info('tst_XX1123')

    def test_get_barcode_results(self):
        obs = self.ag_data.get_barcode_results('tst_yCzro')
        exp = [{'barcode': '000016704', 'participant_name': 'REMOVED-0'},
               {'barcode': '000016705', 'participant_name': 'REMOVED-0'},
               {'barcode': '000016706', 'participant_name': 'REMOVED-0'},
               {'barcode': '000016707', 'participant_name': 'REMOVED-0'},
               {'barcode': '000016708', 'participant_name': 'REMOVED-0'},
               {'barcode': '000016709', 'participant_name': 'REMOVED-0'},
               {'barcode': '000016710', 'participant_name': 'REMOVED-0'},
               {'barcode': '000016711', 'participant_name': 'REMOVED-0'},
               {'barcode': '000016712', 'participant_name': 'REMOVED-0'},
               {'barcode': '000016713', 'participant_name': 'REMOVED-0'},
               {'barcode': '000004213', 'participant_name': 'REMOVED-0'},
               {'barcode': '000004214', 'participant_name': 'REMOVED-0'},
               {'barcode': '000004215', 'participant_name': 'REMOVED-0'},
               {'barcode': '000004216', 'participant_name': 'REMOVED-0'},
               {'barcode': '000004218', 'participant_name': 'REMOVED-0'},
               {'barcode': '000004219', 'participant_name': 'REMOVED-0'}]
        self.assertItemsEqual(obs, exp)

    def test_get_barcode_results_non_existant_id(self):
        with self.assertRaises(ValueError):
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
        id_ = '00000000-0000-0000-0000-000000000000'
        with self.assertRaises(ValueError):
            self.ag_data.get_login_info(id_)

    def test_get_survey_ids(self):
        id_ = '8ca47059-000a-469f-aa64-ff1afbd6fcb1'
        obs = self.ag_data.get_survey_ids(id_, 'REMOVED-0')
        self.assertEquals(obs, {1: 'd08758a1510256f0'})

    def test_get_survey_ids_non_existant_id(self):
        id_ = '00000000-0000-0000-0000-000000000000'
        with self.assertRaises(ValueError):
            self.ag_data.get_survey_ids(id_, 'REMOVED')

    def test_get_countries(self):
        obs = self.ag_data.get_countries()
        # Make sure is a list with proper length
        self.assertTrue(isinstance(obs, list))
        self.assertEqual(len(obs), 244)

        # Spot check a few countries
        self.assertIn('United States', obs)
        self.assertIn('United Kingdom', obs)

    def test_is_deposited_ebi(self):
        obs = self.ag_data.is_deposited_ebi('000027262')
        self.assertFalse(obs)

    def test_is_deposited_ebi_bad_barcode(self):
        with self.assertRaises(ValueError):
            self.ag_data.is_deposited_ebi('NOTABARCODE')


if __name__ == "__main__":
    main()
