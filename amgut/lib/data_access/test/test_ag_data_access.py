from unittest import TestCase, main
from amgut.lib.data_access.ag_data_access import AGDataAccess
import datetime


class TestAGDataAccess(TestCase):
    def setUp(self):
        self.ag_data = AGDataAccess()

    def tearDown(self):
        del self.ag_data

    def test_authenticateWebAppUser(self):
        raise NotImplementedError()

    def test_addAGLogin(self):
        raise NotImplementedError()

    def test_getAGBarcodeDetails(self):
        raise NotImplementedError()

    def test_getAGKitDetails(self):
        raise NotImplementedError()

    def test_registerHandoutKit(self):
        raise NotImplementedError()

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

    def test_logParticipantSample(self):
        raise NotImplementedError()

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
        res = self.ag_data.getBarcodesByKit('tst_iqyYo')
        exp = ['000027561']
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
