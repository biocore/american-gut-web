# -*- coding: utf-8 -*-

from unittest import TestCase, main
import datetime
from random import choice, randint
from string import ascii_letters
from uuid import UUID

from amgut.lib.data_access.ag_data_access import AGDataAccess
from amgut.lib.util import rollback
from amgut.lib.data_access.ag_data_access import TRN


class TestAGDataAccess(TestCase):
    def setUp(self):
        self.ag_data = AGDataAccess()

    def tearDown(self):
        del self.ag_data

    def test_authenticateWebAppUser(self):
        # Test right pass but non-existant kit ID
        obs = self.ag_data.authenticateWebAppUser('randomkitID', 'test')
        self.assertEqual(obs, False)

        kit_id = self.ag_data.ut_get_supplied_kit_id(
            'ded5101d-cafb-f6b3-e040-8a80115d6f03')
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

        email = self.ag_data.ut_get_arbitrary_email()
        obs = self.ag_data.check_login_exists(email)
        as_uuid = UUID(obs, version=4)
        self.assertTrue(as_uuid.version, 4)

    @rollback
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
        supplied_kit_id, barcode =\
            self.ag_data.ut_get_arbitrary_supplied_kit_id_scanned_unconsented()
        obs = self.ag_data.get_nonconsented_scanned_barcodes(supplied_kit_id)
        self.assertIn(barcode, obs)

    def test_getAGBarcodeDetails(self):
        # test existing AG barcode
        obs = self.ag_data.getAGBarcodeDetails('000001047')
        exp = {
            'barcode': '000001047',
            'status': 'Received',
            'ag_kit_id': 'd8592c74-7e35-2135-e040-8a80115d6401',
            'site_sampled': 'Stool',
            'environment_sampled': None,
            'sample_date': datetime.date(2013, 3, 28),
            'sample_time': datetime.time(23, 25),
            'overloaded': None,
            'withdrawn': None,
            'other': None,
            'moldy': None,
            'refunded': None,
            'ag_kit_barcode_id': 'd8592c74-7e36-2135-e040-8a80115d6401',
            'date_of_last_email': None,
        }
        # only look at those fields, that are not subject to scrubbing
        self.assertEqual({k: obs[k] for k in exp}, exp)

    def test_getAGKitDetails(self):
        # test non-existant kit
        with self.assertRaises(ValueError):
            self.ag_data.getAGKitDetails('IDONTEXI5T')

        # test existing AG kit
        obs = self.ag_data.getAGKitDetails(
            self.ag_data.ut_get_supplied_kit_id(
                'd8592c74-84ba-2135-e040-8a80115d6401'))
        # deleted password, since it is not stable along DB versions
        exp = {'ag_kit_id': 'd8592c74-84bb-2135-e040-8a80115d6401',
               'supplied_kit_id':
               self.ag_data.ut_get_supplied_kit_id(
                'd8592c74-84ba-2135-e040-8a80115d6401'),
               'swabs_per_kit': 1,
               'kit_password':
               '$2a$12$rX8UTcDkIj8bwcxZ22iRpebAxblEclT83xBiUIdJGUJGoUfznu1RK',
               'verification_email_sent': 'n',
               'kit_verified': 'y'}
        # only look at those fields, that are not subject to scrubbing
        self.assertEqual({k: obs[k] for k in exp}, exp)

    def test_get_all_handout_kits(self):
        obs = self.ag_data.get_all_handout_kits()
        self.assertTrue(isinstance(obs, list))
        self.assertTrue(len(obs) > 0)

        for kit_id in obs:
            self.assertRegex(kit_id, '[a-zA-Z_]*')

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

    @rollback
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
        ag_login_id = '000fc4cd-8fa4-db8b-e050-8a800c5d02b5'

        with TRN:
            sql = """SELECT survey_id
                     FROM ag.ag_login_surveys
                     WHERE ag_login_id = %s"""
            TRN.add(sql, [ag_login_id])
            old_survey_ids = [x[0] for x in TRN.execute_fetchindex()]

            sql = """SELECT barcode
                     FROM ag.source_barcodes_surveys
                     WHERE survey_id IN %s"""
            TRN.add(sql, [tuple(old_survey_ids)])
            old_barcodes = [x[0] for x in TRN.execute_fetchindex()]

        # make sure we can get the corresponding survey by ID
        self.ag_data.getConsent('8b2b45bb3390b585')

        names = self.ag_data.ut_get_participant_names_from_ag_login_id(
            ag_login_id)
        self.ag_data.deleteAGParticipantSurvey(ag_login_id, names[0])

        with self.assertRaises(ValueError):
            self.ag_data.getConsent('8b2b45bb3390b585')

        res = self.ag_data.get_withdrawn()
        today = datetime.datetime.now().date()
        self.assertIn(ag_login_id, [r[0] for r in res])
        # we cannot check name and email since they get randomly scrubbed
        for r in res:
            if r[0] == ag_login_id:
                self.assertEqual(r[3], today)

        with TRN:
            # check that barcode are really deleted from
            # source_barcodes_surveys
            sql = """SELECT COUNT(*)
                     FROM ag.source_barcodes_surveys
                     WHERE barcode IN %s"""
            TRN.add(sql, [tuple(old_barcodes)])
            self.assertEqual(TRN.execute_fetchindex()[0][0], 0)

            # check that survey_ids are really deleted from
            # source_barcodes_surveys
            sql = """SELECT COUNT(*)
                     FROM ag.source_barcodes_surveys
                     WHERE survey_id IN %s"""
            TRN.add(sql, [tuple(old_survey_ids)])
            self.assertEqual(TRN.execute_fetchindex()[0][0], 0)

            # check that barcode are really deleted from
            # ag_kit_barcodes
            sql = """SELECT COUNT(*)
                     FROM ag.ag_kit_barcodes
                     WHERE barcode IN %s"""
            TRN.add(sql, [tuple(old_barcodes)])
            self.assertEqual(TRN.execute_fetchindex()[0][0], 0)

    @rollback
    def test_deleteAGParticipantSurvey_with_sample_bug(self):
        ag_login_id = 'd8592c74-9694-2135-e040-8a80115d6401'
        names = self.ag_data.ut_get_participant_names_from_ag_login_id(
            ag_login_id)

        # issue 616
        self.ag_data.deleteAGParticipantSurvey(ag_login_id, names[0])
        with self.assertRaises(ValueError):
            self.ag_data.getConsent('be8516e8c5d4ff4d')

    @rollback
    def test_deleteAGParticipantSurvey_with_no_barcodes(self):
        ag_login_id = '000fc4cd-8fa4-db8b-e050-8a800c5d02b5'
        with TRN:
            sql = """SELECT survey_id
                     FROM ag.ag_login_surveys
                     WHERE ag_login_id = %s"""
            TRN.add(sql, [ag_login_id])
            old_survey_ids = [x[0] for x in TRN.execute_fetchindex()]

            sql = """SELECT barcode
                     FROM ag.source_barcodes_surveys
                     WHERE survey_id IN %s"""
            TRN.add(sql, [tuple(old_survey_ids)])
            old_barcodes = [x[0] for x in TRN.execute_fetchindex()]

            # deletes the barcode information belonging to the survey_id
            sql = """DELETE FROM ag.source_barcodes_surveys
                     WHERE survey_id IN %s"""
            TRN.add(sql, [tuple(old_survey_ids)])

            sql = """DELETE FROM ag.ag_kit_barcodes
                     WHERE barcode IN %s"""
            TRN.add(sql, [tuple(old_barcodes)])

        self.ag_data.getConsent('8b2b45bb3390b585')

        names = self.ag_data.ut_get_participant_names_from_ag_login_id(
            ag_login_id)
        self.ag_data.deleteAGParticipantSurvey(ag_login_id, names[0])

        with self.assertRaises(ValueError):
            self.ag_data.getConsent('8b2b45bb3390b585')

        res = self.ag_data.get_withdrawn()
        today = datetime.datetime.now().date()
        self.assertIn(ag_login_id, [r[0] for r in res])
        # we cannot check name and email since they get randomly scrubbed
        for r in res:
            if r[0] == ag_login_id:
                self.assertEqual(r[3], today)

        with TRN:
            # check that barcode are really deleted from
            # source_barcodes_surveys
            sql = """SELECT COUNT(*)
                     FROM ag.source_barcodes_surveys
                     WHERE barcode IN %s"""
            TRN.add(sql, [tuple(old_barcodes)])
            self.assertEqual(TRN.execute_fetchindex()[0][0], 0)

            # check that survey_ids are really deleted from
            # source_barcodes_surveys
            sql = """SELECT COUNT(*)
                     FROM ag.source_barcodes_surveys
                     WHERE survey_id IN %s"""
            TRN.add(sql, [tuple(old_survey_ids)])
            self.assertEqual(TRN.execute_fetchindex()[0][0], 0)

            # check that barcode are really deleted from
            # ag_kit_barcodes
            sql = """SELECT COUNT(*)
                     FROM ag.ag_kit_barcodes
                     WHERE barcode IN %s"""
            TRN.add(sql, [tuple(old_barcodes)])
            self.assertEqual(TRN.execute_fetchindex()[0][0], 0)

    def test_getConsent(self):
        obs = self.ag_data.getConsent("8b2b45bb3390b585")
        exp = {'date_signed': None,
               'age_range': None,
               'ag_login_id': '000fc4cd-8fa4-db8b-e050-8a800c5d02b5',
               'deceased_parent': 'false',
               'survey_id': '8b2b45bb3390b585',
               'is_juvenile': False}
        # only look at those fields, that are not subject to scrubbing
        self.assertEqual({k: obs[k] for k in exp}, exp)

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

    @rollback
    def test_logParticipantSample_tomultiplesurveys(self):
        ag_login_id = '5a10ea3e-9c7f-4ec3-9e96-3dc42e896668'
        participant_name = "Name - )?Åú*IüKb+"
        barcode = "000027913"

        # check that there are no barcode <-> survey assignments, prior to
        # logging
        with TRN:
            sql = """SELECT COUNT(*) FROM ag.source_barcodes_surveys
                     WHERE survey_id IN (SELECT survey_id
                                         FROM ag.ag_login_surveys
                                         WHERE ag_login_id = %s
                                         AND participant_name = %s)"""
            TRN.add(sql, [ag_login_id, participant_name])
            self.assertEqual(TRN.execute_fetchindex()[0][0], 0)

        self.ag_data.logParticipantSample(
            ag_login_id, barcode, 'Stool', None, datetime.date(2015, 9, 27),
            datetime.time(15, 54), participant_name, '')

        # check that single barcode gets assigned to BOTH surveys
        with TRN:
            TRN.add(sql, [ag_login_id, participant_name])
            self.assertEqual(TRN.execute_fetchindex()[0][0], 2)

    @rollback
    def test_deleteSample_removeallsurveys(self):
        ag_login_id = '5a10ea3e-9c7f-4ec3-9e96-3dc42e896668'
        participant_name = "Name - )?Åú*IüKb+"
        barcode = "000027913"
        self.ag_data.logParticipantSample(
            ag_login_id, barcode, 'Stool', None, datetime.date(2015, 9, 27),
            datetime.time(15, 54), participant_name, '')

        sql = """SELECT COUNT(*)
                 FROM ag.source_barcodes_surveys
                 WHERE barcode = %s"""
        # check that barcodes are assigned to surveys
        with TRN:
            TRN.add(sql, [barcode])
            self.assertEqual(TRN.execute_fetchindex()[0][0], 2)

        self.ag_data.deleteSample(barcode, ag_login_id)

        # ensure barcode to survey assignment is deleted
        with TRN:
            TRN.add(sql, [barcode])
            self.assertEqual(TRN.execute_fetchindex()[0][0], 0)

    @rollback
    def test_logParticipantSample(self):
        # regular sample
        ag_login_id = '7732aafe-c4e1-4ae4-8337-6f22704c1064'
        barcode = '000027376'
        names = self.ag_data.ut_get_participant_names_from_ag_login_id(
            ag_login_id)

        self.ag_data.logParticipantSample(
            ag_login_id, barcode, 'Stool', None, datetime.date(2015, 9, 27),
            datetime.time(15, 54), names[0], '')
        obs = self.ag_data.getAGBarcodeDetails(barcode)
        exp = {'status': None,
               'ag_kit_id': '5bfa9526-8dbb-492f-937c-bceb6b5a56fe',
               'ag_kit_barcode_id': '793dab39-d9bf-4a0f-8d67-f21796e3faae',
               'barcode': '000027376',
               'site_sampled': 'Stool',
               'environment_sampled': None,
               'sample_date': datetime.date(2015, 9, 27),
               'sample_time': datetime.time(15, 54),
               'notes': '', 'overloaded': None,
               'withdrawn': None,
               'other': None,
               'moldy': None,
               'refunded': None,
               'date_of_last_email': None,
               }
        self.ag_data.deleteSample(barcode, ag_login_id)
        # only look at those fields, that are not subject to scrubbing
        self.assertEqual({k: obs[k] for k in exp}, exp)

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
               'sample_date': datetime.date(2015, 9, 26),
               'sample_time': datetime.time(15, 00),
               'notes': '', 'overloaded': None,
               'withdrawn': None,
               'other': None,
               'moldy': None,
               'refunded': None,
               'date_of_last_email': None,
               }
        self.ag_data.deleteSample(barcode, ag_login_id)
        # only look at those fields, that are not subject to scrubbing
        self.assertEqual({k: obs[k] for k in exp}, exp)

    def test_getHumanParticipants(self):
        i = "d8592c74-9694-2135-e040-8a80115d6401"
        res = self.ag_data.getHumanParticipants(i)
        exp = self.ag_data.ut_get_participant_names_from_ag_login_id(i)
        # check if results are subset of all names for this ag_login_id
        for name in res:
            self.assertIn(name, exp)

    def test_getHumanParticipantsNotPresent(self):
        i = '00000000-0000-0000-0000-000000000000'
        res = self.ag_data.getHumanParticipants(i)
        self.assertEqual(res, [])

    @rollback
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
        exp = self.ag_data.ut_get_participant_names_from_ag_login_id(i)
        # check if results are subset of all names for this ag_login_id
        for name in res:
            self.assertIn(name, exp)

    def test_getAnimalParticipantsNotPresent(self):
        i = "00711b0a-67d6-0fed-e050-8a800c5d7570"
        res = self.ag_data.getAnimalParticipants(i)
        self.assertEqual(res, [])

    def test_getParticipantSamples(self):
        i = "d6b0f287-b9d9-40d4-82fd-a8fd3db6c476"
        names = self.ag_data.ut_get_participant_names_from_ag_login_id(i)
        # collect results for ALL names
        res = [self.ag_data.getParticipantSamples(i, name)
               for name in names]
        exp = {'sample_time': datetime.time(11, 55),
               'barcode': '000028432',
               'sample_date': datetime.date(2015, 6, 7),
               'site_sampled': 'Stool'}
        # transform results
        res = [dict((k, r[0][k]) for k in list(exp.keys())) for r in res if r != []]
        # only look at those fields, that are not subject to scrubbing
        self.assertIn(exp, res)

        i = "d8592c74-9694-2135-e040-8a80115d6401"
        # collect all results for ALL names for this ag_login_id and remove
        # field "notes" since it gets scrubbed.
        names = set(self.ag_data.ut_get_participant_names_from_ag_login_id(i))
        obs = []
        for name in names:
            res = self.ag_data.getParticipantSamples(i, name)
            for r in res:
                del r['notes']
                obs.append(r)
        exp = [{'status': 'Received',
                'sample_time': datetime.time(7, 40),
                'barcode': '000016704',
                'sample_date': datetime.date(2014, 6, 5),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(11, 30),
                'barcode': '000016705',
                'sample_date': datetime.date(2014, 6, 1),
                'site_sampled': 'Stool'},
               {'status': 'Received', 'sample_time': datetime.time(9, 20),
                'barcode': '000016706',
                'sample_date': datetime.date(2014, 6, 8),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(9, 20),
                'barcode': '000016707',
                'sample_date': datetime.date(2014, 6, 1),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(22, 0),
                'barcode': '000016708',
                'sample_date': datetime.date(2014, 5, 28),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(11, 0),
                'barcode': '000016709',
                'sample_date': datetime.date(2014, 5, 29),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(22, 20),
                'barcode': '000016710',
                'sample_date': datetime.date(2014, 5, 27),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(8, 0),
                'barcode': '000016711',
                'sample_date': datetime.date(2014, 6, 11),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(8, 15),
                'barcode': '000016712',
                'sample_date': datetime.date(2014, 6, 2),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(12, 0),
                'barcode': '000016713',
                'sample_date': datetime.date(2014, 5, 30),
                'site_sampled': 'Stool'},
               {'status': None,
                'sample_time': datetime.time(19, 30),
                'barcode': '000016496',
                'sample_date': datetime.date(2014, 4, 29),
                'site_sampled': 'Stool'},
               {'status': None,
                'sample_time': datetime.time(19, 30),
                'barcode': '000016497',
                'sample_date': datetime.date(2014, 4, 29),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(10, 20),
                'barcode': '000004213',
                'sample_date': datetime.date(2013, 10, 16),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(9, 50),
                'barcode': '000004214',
                'sample_date': datetime.date(2013, 10, 14),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(12, 0),
                'barcode': '000004215',
                'sample_date': datetime.date(2013, 10, 13),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(9, 30),
                'barcode': '000004216',
                'sample_date': datetime.date(2013, 10, 15),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(14, 25),
                'barcode': '000004218',
                'sample_date': datetime.date(2013, 10, 12),
                'site_sampled': 'Stool'},
               {'status': 'Received',
                'sample_time': datetime.time(10, 15),
                'barcode': '000004219',
                'sample_date': datetime.date(2013, 10, 17),
                'site_sampled': 'Stool'}]
        self.assertItemsEqual(obs, exp)

    def test_getParticipantSamplesNotPresent(self):
        i = '00000000-0000-0000-0000-000000000000'
        res = self.ag_data.getParticipantSamples(i, "REMOVED")
        self.assertEqual(res, [])

    def test_getEnvironmentalSamples(self):
        fields = ['sample_time', 'barcode', 'sample_date', 'site_sampled']

        i = "df62647f-c7e1-9de7-e040-8a80115d5c07"
        obs = []
        for bc in self.ag_data.ut_get_barcode_from_ag_login_id(i):
            obs.append(dict((k, bc[k]) for k in fields))

        for bc in self.ag_data.getEnvironmentalSamples(i):
            self.assertIn(dict((k, bc[k]) for k in fields), obs)

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
        exp = [x['barcode'] for x in
               self.ag_data.ut_get_barcode_from_ag_login_id(i)
               if x['kit_verified'] == 'y' and x['sample_date'] is None]
        self.assertItemsEqual(res, exp)

    def test_getAvailableBarcodesNotPresent(self):
        i = '00000000-0000-0000-0000-000000000000'
        res = self.ag_data.getAvailableBarcodes(i)
        self.assertEqual(res, [])

    @rollback
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
            self.assertRegex(kit_id, '[a-zA-Z_]*')
            obs = self.ag_data.getAGKitDetails(kit_id)
            self.assertEqual(obs['kit_verified'], 'n')

    @rollback
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
        obs = self.ag_data.handoutCheck(
            self.ag_data.ut_get_supplied_kit_id(
                'd8592c74-84ba-2135-e040-8a80115d6401'),
            'test')
        self.assertEqual(obs, False)
        obs = self.ag_data.handoutCheck('randomKitID', 'test')
        self.assertEqual(obs, False)

    def test_check_access(self):
        # Has access
        obs = self.ag_data.check_access(
            self.ag_data.ut_get_supplied_kit_id(
                'd8592c74-7e34-2135-e040-8a80115d6401'),
            '000001047')
        self.assertEqual(obs, True)

        # No access
        obs = self.ag_data.check_access(
            self.ag_data.ut_get_supplied_kit_id(
                'd8592c74-7e34-2135-e040-8a80115d6401'),
            '000001111')
        self.assertEqual(obs, False)

    @rollback
    def test_ag_set_pass_change_code(self):
        ag_login_id = 'd8592c74-8416-2135-e040-8a80115d6401'

        # Generate new random code and assign it
        testcode = ''.join(choice(ascii_letters) for i in list(range(10)))
        email = self.ag_data.ut_get_email_from_ag_login_id(ag_login_id)
        self.ag_data.ag_set_pass_change_code(
            email,
            self.ag_data.ut_get_supplied_kit_id(ag_login_id),
            testcode)

        # Actually test the code change
        obs = self.ag_data.ag_verify_kit_password_change_code(
            email,
            self.ag_data.ut_get_supplied_kit_id(ag_login_id),
            'SOMELONGTHINGTHATWILLFAIL')
        self.assertEqual(obs, False)
        obs = self.ag_data.ag_verify_kit_password_change_code(
            email,
            self.ag_data.ut_get_supplied_kit_id(ag_login_id),
            testcode)
        # Using equal to make sure boolean True is returned, not something that
        # equates to True
        self.assertEqual(obs, True)

        # Test giving nonsense email
        # TODO: make this raise error and test
        self.ag_data.ag_set_pass_change_code(
            'Fake@notarealemail.com',
            self.ag_data.ut_get_supplied_kit_id(ag_login_id),
            testcode)

        # Test giving bad skid
        # TODO: make this raise error and test
        self.ag_data.ag_set_pass_change_code('REMOVED', 'NOTINTHEDB', testcode)

    @rollback
    def test_ag_update_kit_password(self):
        # Generate new pass and make sure is different from current pass
        newpass = ''.join(choice(ascii_letters) for i in list(range(randint(8, 15))))
        auth = self.ag_data.authenticateWebAppUser(
            self.ag_data.ut_get_supplied_kit_id(
                'd8592c74-8416-2135-e040-8a80115d6401'),
            newpass)
        self.assertFalse(
            auth, msg="Randomly generated password matches existing")

        # Actually test password change
        self.ag_data.ag_update_kit_password(
            self.ag_data.ut_get_supplied_kit_id(
                'd8592c74-8416-2135-e040-8a80115d6401'),
            newpass)
        auth = self.ag_data.authenticateWebAppUser(
            self.ag_data.ut_get_supplied_kit_id(
                'd8592c74-8416-2135-e040-8a80115d6401'),
            newpass)
        self.assertTrue(isinstance(auth, dict))
        self.assertEqual(auth['ag_login_id'],
                         'd8592c74-8416-2135-e040-8a80115d6401')

        # Test giving bad skid
        # TODO: make this raise error and test
        self.ag_data.ag_update_kit_password('NOTINTHEDB', newpass)

    @rollback
    def test_ag_verify_kit_password_change_code(self):
        ag_login_id = '6165453f-e8bc-4edc-b00e-50e72fe550c9'
        email = self.ag_data.ut_get_email_from_ag_login_id(ag_login_id)

        # Test actual functionality
        obs = self.ag_data.ag_verify_kit_password_change_code(
            email,
            self.ag_data.ut_get_supplied_kit_id(ag_login_id),
            'FAIL')
        # Using assertEqual to make sure boolean False is returned, not
        # something that equates to False. Same for rest of assertEquals below
        self.assertEqual(obs, False)
        # Outside reset time, should fail
        obs = self.ag_data.ag_verify_kit_password_change_code(
            email,
            self.ag_data.ut_get_supplied_kit_id(
                ag_login_id),
            'Mw1eY4wWVXpE0cQlvQwS')
        self.assertEqual(obs, False)

        # Reset code and make sure it works
        testcode = ''.join(choice(ascii_letters) for i in list(range(10)))
        self.ag_data.ag_set_pass_change_code(
            email,
            self.ag_data.ut_get_supplied_kit_id(ag_login_id),
            testcode)
        obs = self.ag_data.ag_verify_kit_password_change_code(
            email,
            self.ag_data.ut_get_supplied_kit_id(ag_login_id),
            testcode)
        self.assertEqual(obs, True)

        # Test with incorrect kit id
        obs = self.ag_data.ag_verify_kit_password_change_code(
            'REMOVED', 'NOTAREALKITID', 'FAIL')
        self.assertEqual(obs, False)

        # Test with incorrect email
        ag_login_id = 'd8592c74-8416-2135-e040-8a80115d6401'
        email = self.ag_data.ut_get_email_from_ag_login_id(ag_login_id)
        obs = self.ag_data.ag_verify_kit_password_change_code(
            email,
            self.ag_data.ut_get_supplied_kit_id(ag_login_id),
            testcode)
        self.assertEqual(obs, False)

    def test_getBarcodesByKit(self):
        res = self.ag_data.getBarcodesByKit(
            self.ag_data.ut_get_supplied_kit_id(
                'd8592c74-7e7f-2135-e040-8a80115d6401'))
        exp = ['000001322']
        self.assertItemsEqual(res, exp)

    def test_getBarcodesByKitNotPresent(self):
        res = self.ag_data.getBarcodesByKit('42')
        self.assertEqual(res, [])

    def test_getAGSurveyDetails_primary(self):
        res = self.ag_data.getAGSurveyDetails(1, 'american')

        res_column = set(res.loc[:, 'american'])
        exp_column = {'Gender:', 'Birth year:', 'Country of residence:',
                      'How were you fed as an infant?',
                      'Have you ever been diagnosed with cancer?',
                      'I have received a flu vaccine in ' +
                      'the last ____________.',
                      'Please write anything else about yourself that ' +
                      'you think could affect your personal microorganisms.'
                      }
        self.assertTrue(exp_column.issubset(res_column))

    def test_getAGSurveyDetails_compare_survey_diff_lang(self):
        surveys = []
        survey_columns = ['survey_question_id',
                          'question_shortname',
                          'response_index']

        # loops through known languages for surveys
        for language in self.ag_data.getKnownLanguages():
            survey = self.ag_data.getAGSurveyDetails(1, language)
            surveys.append(survey[survey_columns])

        # compares contents of survey_question_id, question_shortname, and
        # response_index of different language surveys to american survey
        for survey in surveys[1:]:
            for column in survey_columns:
                self.assertEqual(list(surveys[0].loc[:, column]),
                                 list(survey.loc[:, column]))

    def test_getAGSurveyDetails_compare_survey_diff_id(self):
        surveys = []
        columns = ['survey_question_id',
                   'american',
                   'question_shortname',
                   'response',
                   'response_index']

        # loops through known ids for surveys
        for survey_id in self.ag_data.getKnownSurveyIds():
            survey = self.ag_data.getAGSurveyDetails(survey_id, 'american')
            surveys.append(list(survey.columns))

        # confirms if columns have the same names
        for survey in surveys[1:]:
            self.assertEqual(columns, survey)

    def test_getAGSurveyDetails_invalid_param(self):
        with self.assertRaises(ValueError):
            self.ag_data.getAGSurveyDetails(0, 'inval_language')

        with self.assertRaises(ValueError):
            self.ag_data.getAGSurveyDetails(0, 'american')

        with self.assertRaises(ValueError):
            self.ag_data.getAGSurveyDetails(1, 'inval_language')

    def test_getKnownSurveyIds(self):
        res = self.ag_data.getKnownSurveyIds()
        exp = {1, 2, 3, 4, 5}
        self.assertTrue(exp.issubset(res))

    def test_getKnownLanguages(self):
        res = self.ag_data.getKnownLanguages()
        exp = {'american', 'british'}
        self.assertTrue(exp.issubset(res))

    def test_checkPrintResults(self):
        obs = self.ag_data.checkPrintResults(
            self.ag_data.ut_get_supplied_kit_id(
                'dc3172b2-792c-4087-8a20-714297821c6a'))
        self.assertFalse(obs)

        kit_id = self.ag_data\
            .ut_get_arbitrary_handout_printed_min6_supplied_kit_id()
        obs = self.ag_data.checkPrintResults(kit_id)
        self.assertTrue(obs)

    def test_checkPrintResults_invalid_ids(self):
        obs = self.ag_data.checkPrintResults('xxx00112333123---123222')
        self.assertFalse(obs)

        obs = self.ag_data.checkPrintResults(':Lfoo:Lbar:Lbaz:Ospam:Leggs')
        self.assertFalse(obs)

    def test_get_user_for_kit(self):
        obs = self.ag_data.get_user_for_kit(
            self.ag_data.ut_get_supplied_kit_id(
                'ded5101d-c8e3-f6b3-e040-8a80115d6f03'))
        self.assertEqual('ded5101d-c8e3-f6b3-e040-8a80115d6f03', obs)

        obs = self.ag_data.get_user_for_kit(
            self.ag_data.ut_get_supplied_kit_id(
                'd8592c74-8421-2135-e040-8a80115d6401'))
        self.assertEqual('d8592c74-8421-2135-e040-8a80115d6401', obs)

    def test_get_user_for_kit_errors(self):
        with self.assertRaises(ValueError):
            self.ag_data.get_user_for_kit('the_fooster')

        with self.assertRaises(ValueError):
            self.ag_data.get_user_for_kit('NOT_IN_DB')

    def test_get_menu_items(self):
        obs = self.ag_data.get_menu_items(
            self.ag_data.ut_get_supplied_kit_id(
                'd8592c74-844b-2135-e040-8a80115d6401'))
        self.assertEqual(({}, {}, [], True), obs)

        ag_login_id = 'd8592c74-84c9-2135-e040-8a80115d6401'
        obs = self.ag_data.get_menu_items(
            self.ag_data.ut_get_supplied_kit_id(ag_login_id))
        names = self.ag_data.ut_get_participant_names_from_ag_login_id(
            ag_login_id)
        self.assertEqual((dict((name, []) for name in names),
                         {}, [], True), obs)

    def test_get_menu_items_errors(self):
        with self.assertRaises(ValueError):
            self.ag_data.get_menu_items('NOT_IN_DB')

    def test_check_if_consent_exists(self):
        ag_login_id = '00711b0a-67d6-0fed-e050-8a800c5d7570'
        names = self.ag_data.ut_get_participant_names_from_ag_login_id(
            ag_login_id)
        obs = self.ag_data.check_if_consent_exists(
            ag_login_id, names[0])
        self.assertTrue(obs)

    def test_check_if_consent_exists_non_existent_user(self):
        ag_login_id = '00711b0a-67d6-0fed-e050-8a800c5d7570'
        obs = self.ag_data.check_if_consent_exists(ag_login_id, 'REMOVED-111')
        self.assertFalse(obs)

    def test_get_user_info(self):
        ag_login_id = 'd8592c74-84a5-2135-e040-8a80115d6401'
        obs = self.ag_data.get_user_info(
            self.ag_data.ut_get_supplied_kit_id(ag_login_id))
        # unfortunatly, most fields are scrubbed in the database, thus we
        # cannot compare them over DB versions
        exp = {'ag_login_id': ag_login_id,
               'email': self.ag_data.ut_get_email_from_ag_login_id(
                ag_login_id)}
        self.assertEqual(exp, dict((k, obs[k]) for k in list(exp.keys())))
        exp = ['address', 'ag_login_id', 'city', 'country', 'email', 'name',
               'state', 'zip']
        self.assertItemsEqual(list(obs.keys()), exp)

    def test_get_user_info_non_existent(self):
        with self.assertRaises(ValueError):
            self.ag_data.get_user_info('NOT_IN_DB')

    def test_get_barcode_results(self):
        ag_login_id = 'd8592c74-9694-2135-e040-8a80115d6401'
        obs = self.ag_data.get_barcode_results(
            self.ag_data.ut_get_supplied_kit_id(ag_login_id))
        # remove participant_names from results
        for o in obs:
            del o['participant_name']
        # we cannot compare participant_names, since they are scrubbed
        exp = [{'barcode': '000016704'},
               {'barcode': '000016705'},
               {'barcode': '000016706'},
               {'barcode': '000016707'},
               {'barcode': '000016708'},
               {'barcode': '000016709'},
               {'barcode': '000016710'},
               {'barcode': '000016711'},
               {'barcode': '000016712'},
               {'barcode': '000016713'},
               {'barcode': '000004213'},
               {'barcode': '000004214'},
               {'barcode': '000004215'},
               {'barcode': '000004216'},
               {'barcode': '000004218'},
               {'barcode': '000004219'}]
        self.assertItemsEqual(obs, exp)

    def test_get_barcode_results_non_existant_id(self):
        with self.assertRaises(ValueError):
            self.ag_data.get_barcode_results("something that doesn't exist")

    def test_get_login_info(self):
        id_ = 'fecebeae-4244-2d78-e040-8a800c5d4f50'
        exp = {'ag_login_id': id_,
               'email': self.ag_data.ut_get_email_from_ag_login_id(id_)}
        obs = self.ag_data.get_login_info(id_)
        self.assertEqual(dict((k, obs[0][k]) for k in list(exp.keys())), exp)

    def test_get_login_info_non_existant_id(self):
        id_ = '00000000-0000-0000-0000-000000000000'
        with self.assertRaises(ValueError):
            self.ag_data.get_login_info(id_)

    def test_get_survey_ids(self):
        id_ = '8ca47059-000a-469f-aa64-ff1afbd6fcb1'
        names = self.ag_data.ut_get_participant_names_from_ag_login_id(id_)
        obs = [self.ag_data.get_survey_ids(id_, name) for name in names]
        self.assertIn({1: 'd08758a1510256f0'}, obs)

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
        barcode = self.ag_data.ut_get_arbitrary_barcode(deposited=False)
        obs = self.ag_data.is_deposited_ebi(barcode)
        self.assertFalse(obs)

    def test_is_deposited_ebi_bad_barcode(self):
        with self.assertRaises(ValueError):
            self.ag_data.is_deposited_ebi('NOTABARCODE')


if __name__ == "__main__":
    main()
