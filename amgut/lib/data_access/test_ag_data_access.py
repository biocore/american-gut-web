"""
Centralized database access testsfor the American Gut web portal
"""

__author__ = "Emily TerAvest"
__copyright__ = "Copyright 2014, American Gut Project"
__credits__ = ["Emily TerAvest"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Emily TerAvest"]
__email__ = "emily.teravest@colorado.edu"
__status__ = "Production"

import psycopg2
import psycopg2.extras
from unittest import TestCase, main

from ag_data_access import NewAGDataAccess


#class TestGoogleAPILimitExceeded(TestCase):

class TestNewAGDataAccess(TestCase):
    def setUp(self):
        self.con = psycopg2.connect(user='',
                                    password='',
                                    database='',
                                    host='',
                                    port='5432')
        self.data_access = NewAGDataAccess(self.con)

    def tearDown(self):
        self.con.close()

    def test_testDatabase(self):
        self.assertTrue(self.data_access.testDatabase())

    # def test_dynamicMetadataSelect(self):
    #     raise NotImplementedError()

    def test_addAGLogin(self):
        self.data_access.addAGLogin('deleteme@no.no', 'test', 'test',
                                    'test', 'CO', '80303', 'USA')
        cur = self.con.cursor()
        cur.execute(
            'select * from ag_login where email = %s', ('deleteme@no.no',))
        rec = cur.fetchall()
        self.assertEqual(len(rec), 1)
        cur.execute('delete from ag_login where email = %s',
                   ('deleteme@no.no',))
        self.con.commit()
        cur.execute(
            'select * from ag_login where email = %s', ('deleteme@no.no',))
        rec = cur.fetchall()
        self.assertEqual(len(rec), 0)

    def test_updateAGLogin(self):
        self.data_access.updateAGLogin('d8592c74-7da1-2135-e040-8a80115d6401',
                                       'changed@changed.com', '', 'add',
                                       'city', 'state', 'zip', 'USA')
        cur = self.con.cursor()
        cur.execute('select * from ag_login where ag_login_id = %s',
                    ('d8592c74-7da1-2135-e040-8a80115d6401',))
        rec = cur.fetchone()
        self.assertEqual(rec[1], 'changed@changed.com')
        self.data_access.updateAGLogin('d8592c74-7da1-2135-e040-8a80115d6401',
                                       'test@microbio.me', 'Test', 'Test',
                                       'Boulder', 'CO', '80303',
                                       'United States')
        cur.execute('select * from ag_login where ag_login_id = %s',
                    ('d8592c74-7da1-2135-e040-8a80115d6401',))
        rec = cur.fetchone()
        self.assertEqual(rec[1], 'test@microbio.me')

    def test_getAGSurveyDetails(self):
        ag_login_id = 'd8592c74-7da1-2135-e040-8a80115d6401'
        participant_name = 'test'
        data = self.data_access.getAGSurveyDetails(ag_login_id,
                                                   participant_name)
        self.assertEqual(data['participant_name'], 'test')
        self.assertEqual(data['consent'], 'Yes')

    def test_getAGLogins(self):
        data = self.data_access.getAGLogins()
        self.assertTrue(('d8592c74-7da1-2135-e040-8a80115d6401',
                         'test@microbio.me', 'Test') in data)

    def test_getAGKitsByLogin(self):
        data = self.data_access.getAGKitsByLogin()
        self.assertTrue(('test@microbio.me', 'test',
                         'd8592c74-7da2-2135-e040-8a80115d6401') in data)

    def test_getAGBarcodes(self):
        data = self.data_access.getAGBarcodes()
        self.assertEqual(data[0], '000000001')
        self.assertEqual(data[-1], '999999999')

    def test_getAGBarcodesByLogin(self):
        data = self.data_access.getAGBarcodesByLogin(
            'd8592c74-7da1-2135-e040-8a80115d6401')
        barcodes = {row[3] for row in data}
        self.assertEqual({'000010860', '000010859', '000006616', '000000001'},
                         barcodes)

    def test_getAGBarcodeDetails(self):
        data = self.data_access.getAGBarcodeDetails('000000001')
        self.assertEqual(data['participant_name'], 'foo')
        self.assertEqual(data['site_sampled'], 'Stool')

    def test_getAGKitDetails(self):
        data = self.data_access.getAGKitDetails('test')
        self.assertEqual(data['kit_verification_code'], 'test')

    # def test_getAGCode(self):
    #     raise NotImplementedError()

    # def test_getNewAGKitId(self):
    #     raise NotImplementedError()

    def test_getNextAGBarcode(self):
        barcode, barcode_text = self.data_access.getNextAGBarcode()
        data = self.data_access.getAGBarcodes()
        self.assertTrue(barcode_text not in data)

    def test_reassignAGBarcode(self):
        test = "d8592c74-7da2-2135-e040-8a80115d6401"
        oneone = "dbd466b5-651b-bfb2-e040-8a80115d6775"
        self.data_access.reassignAGBarcode(oneone, '000010860')
        data = self.data_access.getBarcodesByKit('1111')
        self.assertEqual(len(data), 1)
        self.data_access.reassignAGBarcode(test, '000010860')
        data = self.data_access.getBarcodesByKit('1111')
        self.assertEqual(len(data), 0)

    def test_addAGKit(self):
        result = self.data_access.addAGKit('d8592c747da12135e0408a80115d6401',
                                           'somekit', 'pass', 2, 'ver', 'n')
        self.assertEqual(result, 1)
        cur = self.con.cursor()
        cur.execute('select * from ag_kit where ag_login_id = %s',
                    ('d8592c747da12135e0408a80115d6401',))
        rec = cur.fetchall()
        self.assertEqual(len(rec), 3)
        cur.execute(
            'delete from ag_kit where ag_login_id = %s '
            'and supplied_kit_id = %s', ('d8592c747da12135e0408a80115d6401',
                                         'somekit',))
        self.con.commit()
        cur.execute('select * from ag_kit where ag_login_id = %s',
                    ('d8592c747da12135e0408a80115d6401',))
        rec = cur.fetchall()
        self.assertEqual(len(rec), 2)
        result = self.data_access.addAGKit('d8592c747da12135e0408a80115d6401',
                                           'test', 'pass', 2, 'ver', 'n')
        self.assertEqual(result, -1)

    def test_updateAGKit(self):
        self.data_access.updateAGKit('d8592c74-7da2-2135-e040-8a80115d6401',
                                     'test22', 'newpass', 24, 'ver')
        cur = self.con.cursor()
        cur.execute('select * from ag_kit where ag_kit_id = %s',
                    ('d8592c74-7da2-2135-e040-8a80115d6401',))
        rec = cur.fetchone()
        self.assertEqual(rec[2], 'test22')
        self.data_access.updateAGKit('d8592c74-7da2-2135-e040-8a80115d6401',
                                     'test', 'oldpass', 1, 'test')
        cur.execute('select * from ag_kit where ag_kit_id = %s',
                    ('d8592c74-7da2-2135-e040-8a80115d6401',))
        rec = cur.fetchone()
        self.assertEqual(rec[2], 'test')

    def test_addAGBarcode(self):
        self.data_access.addAGBarcode('d8592c74-7da2-2135-e040-8a80115d6401',
                                      '991299')
        cur = self.con.cursor()
        cur.execute('select * from ag_kit_barcodes where barcode = %s',
                    ('991299',))
        rec = cur.fetchone()
        self.assertEqual(rec[1],  'd8592c74-7da2-2135-e040-8a80115d6401')
        cur.execute('select * from project_barcode where barcode = %s',
                    ('991299',))
        rec = cur.fetchone()
        self.assertEqual(rec[0], 1)
        cur.execute('delete from ag_kit_barcodes where barcode = %s',
                    ('991299',))
        cur.execute('delete from project_barcode where barcode = %s',
                    ('991299',))
        cur.execute('delete from barcode where barcode = %s', ('991299', ))
        self.con.commit()

    def test_updateAGBarcode(self):
        self.data_access.updateAGBarcode(
            '000010860', 'd8592c74-7da2-2135-e040-8a80115d6401', 'Stool', '',
            '07/30/2014', '9:30 AM', 'test', '')
        cur = self.con.cursor()
        cur.execute('select * from ag_kit_barcodes where barcode = %s',
                    ('000010860',))
        rec = cur.fetchone()
        self.assertEqual(rec[5], 'Stool')
        self.assertEqual(rec[6], '07/30/2014')
        self.data_access.updateAGBarcode(
            '000010860', 'd8592c74-7da2-2135-e040-8a80115d6401', '', '', '',
            '', '', '')
        cur.execute('select * from ag_kit_barcodes where barcode = %s',
                    ('000010860',))
        rec = cur.fetchone()
        self.assertEqual(rec[5], '')
        self.assertEqual(rec[6], '')

    def test_addAGHumanParticipant(self):
        self.data_access.addAGHumanParticipant(
            'd8592c747da12135e0408a80115d6401', 'sp_test')
        data = self.data_access.getHumanParticipants(
            'd8592c74-7da1-2135-e040-8a80115d6401')
        self.assertTrue('sp_test' in data)
        cur = self.con.cursor()
        cur.execute('delete from ag_human_survey where ag_login_id =   %s and '
                    'participant_name = %s',
                    ('d8592c747da12135e0408a80115d6401', 'sp_test',))
        self.con.commit()

    def test_addAGAnimalParticipant(self):
        self.data_access.addAGAnimalParticipant(
            'd8592c747da12135e0408a80115d6401', 'fuzzy2')
        data = self.data_access.getAnimalParticipants(
            'd8592c747da12135e0408a80115d6401')
        self.assertTrue('fuzzy2' in data)
        cur = self.con.cursor()
        cur.execute('delete from ag_animal_survey where ag_login_id = %s and '
                    'participant_name = %s',
                    ('d8592c747da12135e0408a80115d6401', 'fuzzy2',))
        self.con.commit()

    # def test_addAGSingle(self):
    #     raise NotImplementedError()

    def test_deleteAGParticipant(self):
        cur = self.con.cursor()
        cur.execute('insert into ag_human_survey (ag_login_id, '
                    'participant_name) values (%s, %s)',
                    ('d8592c747da12135e0408a80115d6401', 'sp_test',))
        self.con.commit()
        self.data_access.deleteAGParticipant(
            'd8592c747da12135e0408a80115d6401', 'sp_test')
        data = self.data_access.getHumanParticipants(
            'd8592c747da12135e0408a80115d6401')
        self.assertEqual(len(data), 3)

    def test_addAGGeneralValue(self):
        self.data_access.addAGGeneralValue('d8592c747da12135e0408a80115d6401',
                                           'test', 'badquest', 'badans')
        cur = self.con.cursor()
        cur.execute('select * from ag_survey_answer where question = %s',
                    ('badquest',))
        rec = cur.fetchall()
        self.assertEqual(len(rec), 1)
        cur.execute('delete from ag_survey_answer where ag_login_id = %s and '
                    'participant_name = %s and question =  %s',
                    ('d8592c747da12135e0408a80115d6401', 'test', 'badquest',))
        self.con.commit()

    def test_deleteAGGeneralValues(self):
        cur = self.con.cursor()
        cur.execute('insert into ag_survey_answer(ag_login_id, '
                    'participant_name, question, answer) values (%s, %s, '
                    '%s, %s), (%s,%s, %s, %s)',
                    ('d8592c747da12135e0408a80115d6401', 'Emily2', 'race',
                        'Caucasian', 'd8592c747da12135e0408a80115d6401',
                        'Emily2', 'cat', 'yes',))
        self.data_access.deleteAGGeneralValues(
            'd8592c747da12135e0408a80115d6401', 'Emily2')
        cur.execute('select * from ag_survey_answer where ag_login_id = %s and'
                    ' participant_name = %s',
                    ('d8592c747da12135e0408a80115d6401', 'Emily2',))
        rec = cur.fetchall()
        self.assertEqual(len(rec), 0)

    def test_logParticipantSample(self):
        self.data_access.logParticipantSample('000010860', 'Stool', '',
                                              '07/29/2014', '09:30 AM',
                                              'Emily', 'no notes')
        data = self.data_access.getAGBarcodeDetails('000010860')
        self.assertEqual(data['participant_name'], 'Emily')
        self.assertEqual(data['site_sampled'], 'Stool')
        self.assertEqual(data['sample_date'], '07/29/2014')
        self.data_access.deleteSample('000010860',
                                      'd8592c747da12135e0408a80115d6401')
        data = self.data_access.getAGBarcodeDetails('000010860')
        self.assertEqual(data['participant_name'], '')

    def test_deleteSample(self):
        cur = self.con.cursor()
        cur.execute('update ag_kit_barcodes set site_sampled = %s,'
                    'sample_date = %s, participant_name = %s, '
                    'sample_time = %s where barcode = %s', ('Stool',
                                                            '07/30/2014',
                                                            'test', '9:30 AM',
                                                            '000010860'))
        self.con.commit()
        data = self.data_access.getAGBarcodeDetails('000010860')
        self.assertEqual(data['site_sampled'], 'Stool')
        self.data_access.deleteSample('000010860',
                                      'd8592c747da12135e0408a80115d6401')
        data = self.data_access.getAGBarcodeDetails('000010860')
        self.assertEqual(data['participant_name'], '')

    def test_getHumanParticipants(self):
        data = self.data_access.getHumanParticipants(
            'd8592c74-7da1-2135-e040-8a80115d6401')
        self.assertEqual(set(data), {'Emily', 'foo', 'test'})

    def test_AGGetBarcodeMetadata(self):
        data = self.data_access.AGGetBarcodeMetadata('000000001')
        self.assertEqual(data[0]['FOODALLERGIES_PEANUTS'], 'unknown')
        self.assertEqual(data[0]['CHICKENPOX'], 'unknown')

    def test_AGGetBarcodeMetadataAnimal(self):
        data = self.data_access.AGGetBarcodeMetadataAnimal('000010860')
        #this test needs to be changed when the test database is updated
        self.assertEqual(len(data), 0)

    def test_getAnimalParticipants(self):
        data = self.data_access.getAnimalParticipants(
            'd8592c74-7da1-2135-e040-8a80115d6401')
        #this test needs updated when the test database is updated
        self.assertEqual(len(data), 1)

    def test_getParticipantExceptions(self):
        data = self.data_access.getParticipantExceptions(
            'd8592c74-7da1-2135-e040-8a80115d6401')
        self.assertEqual(len(data), 1)

    def test_getParticipantSamples(self):
        data = self.data_access.getParticipantSamples(
            'd8592c74-7da1-2135-e040-8a80115d6401', 'foo')
        self.assertEqual(data[0]['status'], 'Received')
        self.assertEqual(data[0]['barcode'],  '000000001')

    def test_getEnvironmentalSamples(self):
        data = self.data_access.getEnvironmentalSamples(
            'd8592c74-7da1-2135-e040-8a80115d6401')
        barcodes = {x['barcode'] for x in data}
        self.assertEqual(barcodes, {'000010859', '000006616'})

    def test_getAvailableBarcodes(self):
        data = self.data_access.getAvailableBarcodes(
            'd8592c74-7da1-2135-e040-8a80115d6401')
        #this test will change when test database is updated
        self.assertEqual(len(data), 1)

    def test_verifyKit(self):
        cur = self.con.cursor()
        cur.execute(' update ag_kit set kit_verified = %s where '
                    'supplied_kit_id = %s', ('n', 'test',))
        self.con.commit()
        self.data_access.verifyKit('test')
        cur.execute('select kit_verified from ag_kit where supplied_kit_id = '
                    '%s', ('test',))
        rec = cur.fetchone()
        self.assertEqual(rec[0], 'y')

    # def test_addGeocodingInfo(self):
    #     raise NotImplementedError()

    def test_getMapMarkers(self):
        data = self.data_access.getMapMarkers()
        self.assertNotEqual(len(data), 0)

    # def test_getGeocodeJSON(self):
    #     raise NotImplementedError()

    # def test_getElevationJSON(self):
    #     raise NotImplementedError()

    # def test_updateGeoInfo(self):
    #     raise NotImplementedError()

    def test_addBruceWayne(self):
        self.data_access.addBruceWayne('d8592c747da12135e0408a80115d6401',
                                       'random kid')
        data = self.data_access.getParticipantExceptions(
            'd8592c747da12135e0408a80115d6401')
        self.assertTrue('random kid' in data)
        cur = self.con.cursor()
        cur.execute('delete from ag_bruce_waynes where  ag_login_id = %s and '
                    'participant_name = %s',
                    ('d8592c747da12135e0408a80115d6401', 'random kid',))
        self.con.commit()

    def test_handoutCheck(self):
        is_handout = self.data_access.handoutCheck('test', 'wrongpass')
        self.assertEqual(is_handout, 'n')

    def test_checkBarcode(self):
        data = self.data_access.checkBarcode('000000001')
        self.assertEqual(data[0], 'Stool')
        self.assertEqual(data[-1], 'Test')

    # def test_updateAGSurvey(self):
    #     raise NotImplementedError()

    def test_getAGStats(self):
        data = self.data_access.getAGStats()
        self.assertEqual(len(data), 23)

    def test_updateAKB(self):
        self.data_access.updateAKB('000010860', 'n', 'n', 'y',
                                   'some other text', '07/30/2014')
        cur = self.con.cursor()
        cur.execute('select * from ag_kit_barcodes where barcode = %s',
                    ('000010860',))
        rec = cur.fetchone()
        self.assertEqual([rec[11], rec[12], rec[13]], ['n', 'n', 'y'])
        self.data_access.updateAKB('000010860', None, None, None, None, None)
        cur.execute('select * from ag_kit_barcodes where barcode = %s',
                    ('000010860',))
        rec = cur.fetchone()
        self.assertEqual([rec[11], rec[12], rec[13]], [None, None, None])

    def test_getAGKitbyEmail(self):
        data = self.data_access.getAGKitbyEmail('test@microbio.me')
        self.assertEqual(set(data), {'test', '1111'})

    def test_ag_set_pass_change_code(self):
        self.data_access.ag_set_pass_change_code('test@microbio.me', 'test',
                                                 '123456789')
        cur = self.con.cursor()
        cur.execute('select pass_reset_code from ag_kit where '
                    'supplied_kit_id = %s', ('test',))
        rec = cur.fetchone()
        self.assertEqual(rec[0], '123456789')
        cur.execute('update ag_kit set pass_reset_code = %s, '
                    'pass_reset_time = %s where supplied_kit_id = %s',
                    ('', None, 'test',))
        self.con.commit()

    def test_ag_update_kit_password(self):
        self.data_access.ag_update_kit_password('test', 'newpass')
        cur = self.con.cursor()
        cur.execute('select kit_password from ag_kit where supplied_kit_id = '
                    '%s', ('test',))
        rec = cur.fetchone()
        self.assertEqual(rec[0], 'newpass')

    def test_ag_verify_kit_password_change_code(self):
        self.data_access.ag_set_pass_change_code('test@microbio.me', 'test',
                                                 '123456789')
        result = self.data_access.ag_verify_kit_password_change_code(
            'test@microbio.me', 'test', '123456789')
        self.assertEqual(result, 1)
        cur = self.con.cursor()
        cur.execute('update ag_kit set pass_reset_code = %s, '
                    'pass_reset_time = %s where supplied_kit_id = %s',
                    ('', None, 'test',))
        self.con.commit()

    def test_getBarcodesByKit(self):
        data = self.data_access.getBarcodesByKit('test')
        self.assertEqual(set(data), {'000010860', '000010859', '000006616',
                                     '000000001'})

    def test_checkPrintResults(self):
        data = self.data_access.checkPrintResults('test')
        self.assertTrue(data is None)


if __name__ == "__main__":
    main()
