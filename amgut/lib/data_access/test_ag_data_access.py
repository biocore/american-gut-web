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

from unittest import TestCase, main
from datetime import datetime

import psycopg2
import psycopg2.extras

from passlib.hash import bcrypt

from amgut.lib.data_access.ag_data_access import AGDataAccess
from amgut.lib.config_manager import AMGUT_CONFIG
from amgut.lib.util import ag_test_checker


@ag_test_checker()
class TestAGDataAccess(TestCase):
    def setUp(self):
        self.con = psycopg2.connect(user=AMGUT_CONFIG.user,
                                    password=AMGUT_CONFIG.password,
                                    database=AMGUT_CONFIG.database,
                                    host=AMGUT_CONFIG.host,
                                    port=AMGUT_CONFIG.port)
        self.data_access = AGDataAccess(self.con)
        self.data_access.ag_update_kit_password('test',
                                                AMGUT_CONFIG.badpassword)
        self.con.commit()

    def tearDown(self):
        self.data_access.ag_update_kit_password('test',
                                                AMGUT_CONFIG.goodpassword)
        self.con.close()

    def test_authenticateWebAppUser(self):
        self.assertFalse(self.data_access.authenticateWebAppUser('bad',
                                                                 'wrong'))
        data = self.data_access.authenticateWebAppUser(
            'test', AMGUT_CONFIG.badpassword)
        self.assertEqual(data['email'], 'test@microbio.me')

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

    def test_getAGKitsByLogin(self):
        data = self.data_access.getAGKitsByLogin()
        self.assertTrue({'email': 'test@microbio.me',
                         'supplied_kit_id': 'test',
                         'ag_kit_id': 'd8592c74-7da2-2135-e040-8a80115d6401'}
                        in data)

    def test_getAGBarcodes(self):
        data = self.data_access.getAGBarcodes()
        self.assertEqual(data[0], '000000001')
        self.assertEqual(data[-1], '000010860')

    def test_getAGBarcodeDetails(self):
        data = self.data_access.getAGBarcodeDetails('000000001')
        self.assertEqual(data['participant_name'], 'foo')
        self.assertEqual(data['site_sampled'], 'Stool')
        self.assertEqual(data['status'], 'Received')

    def test_getAGKitDetails(self):
        data = self.data_access.getAGKitDetails('test')
        self.assertEqual(data['kit_verification_code'], 'test')

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
            '07/30/2014', '9:30 AM', 'test', 'notes', 'n', 'n')
        cur = self.con.cursor()
        cur.execute('select * from ag_kit_barcodes where barcode = %s',
                    ('000010860',))
        rec = cur.fetchone()
        self.assertEqual(rec[6], 'Stool')
        self.assertEqual(rec[7], '07/30/2014')
        self.data_access.updateAGBarcode(
            '000010860', 'd8592c74-7da2-2135-e040-8a80115d6401', '', '', '',
            '', '', '', '', '')
        cur.execute('select * from ag_kit_barcodes where barcode = %s',
                    ('000010860',))
        rec = cur.fetchone()
        self.assertEqual(rec[6], '')
        self.assertEqual(rec[7], '')

    def test_registerHandoutKit(self):
        ag_login_id = 'd8592c74-7da1-2135-e040-8a80115d6401'
        self.data_access.registerHandoutKit(
            ag_login_id, 'test_ha')
        cur = self.con.cursor()
        # make sure handout kit removed
        cur.execute("SELECT * FROM ag_handout_kits")
        obs = cur.fetchall()
        self.assertEqual(obs, [])

        # make sure handout kit registered as regular kit
        cur.execute("SELECT * FROM ag_kit WHERE supplied_kit_id = 'test_ha'",
                    [ag_login_id])
        obs = cur.fetchall()
        exp = [('a70a398c-a29e-4367-8ae2-f291d5217b29',
                'd8592c74-7da1-2135-e040-8a80115d6401',
                'test_ha', '1234', 3, '5678', 'n', 'n', None, None, 'n', None)]
        self.assertEqual(obs, exp)
        kit_id = obs[0][0]

        # make sure barcodes registered
        cur.execute("SELECT * FROM barcode JOIN ag_kit_barcodes USING "
                    "(barcode) WHERE ag_kit_id = %s",
                    [kit_id])
        obs = cur.fetchall()
        exp = [
            ('000000004', datetime(2015, 4, 29, 9, 25, 51, 842222), None, None,
             None, None, None, None, 'f3033ee2-391c-4f24-b0eb-f9ed1d26444a',
             'a70a398c-a29e-4367-8ae2-f291d5217b29', None, '000000004.jpg',
             None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None),
            ('000000003', datetime(2015, 4, 29, 9, 25, 51, 842222), None, None,
             None, None, None, None, '8e3b037e-fc79-4523-9816-dc7e9d250ebb',
             'a70a398c-a29e-4367-8ae2-f291d5217b29', None, '000000003.jpg',
             None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None),
            ('000000002', datetime(2015, 4, 29, 9, 25, 51, 842222), None, None,
             None, None, None, None, 'f98bf005-d308-4994-a1fd-9826ab3dbb9d',
             'a70a398c-a29e-4367-8ae2-f291d5217b29', None, '000000002.jpg',
             None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None)]
        self.assertItemsEqual(obs, exp)

    def test_deleteAGParticipantSurvey(self):
        cur = self.con.cursor()
        cur.execute('insert into ag_consent (ag_login_id, '
                    'participant_name, participant_email) values (%s, %s, %s)',
                    ('d8592c747da12135e0408a80115d6401', 'sp_test',
                        'foo@bar.com'))
        self.con.commit()
        cur.execute('insert into ag_login_surveys (ag_login_id, survey_id,'
                    ' participant_name) values (%s, %s, %s)',
                    ('d8592c74-7da1-2135-e040-8a80115d6401', '1235',
                        'sp_test'))
        self.con.commit()
        self.data_access.deleteAGParticipantSurvey(
            'd8592c747da12135e0408a80115d6401', 'sp_test')
        data = self.data_access.getHumanParticipants(
            'd8592c747da12135e0408a80115d6401')
        self.assertEqual(len(data), 1)

    def test_logParticipantSample(self):
        self.data_access.logParticipantSample(
            'd8592c74-7da1-2135-e040-8a80115d6401', '000010860', 'Stool', '',
            '07/29/2014', '09:30 AM', 'foo', 'no notes')
        data = self.data_access.getAGBarcodeDetails('000010860')
        self.assertEqual(data['participant_name'], 'foo')
        self.assertEqual(data['site_sampled'], 'Stool')
        self.assertEqual(data['sample_date'], '07/29/2014')
        self.data_access.deleteSample('000010860',
                                      'd8592c747da12135e0408a80115d6401')
        data = self.data_access.getAGBarcodeDetails('000010860')
        self.assertEqual(data['participant_name'], None)

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
        self.assertEqual(data['participant_name'], None)

    def test_getHumanParticipants(self):
        data = self.data_access.getHumanParticipants(
            'd8592c74-7da1-2135-e040-8a80115d6401')
        self.assertEqual(set(data), {'foo'})

    def test_getAnimalParticipants(self):
        data = self.data_access.getAnimalParticipants(
            'd8592c74-7da1-2135-e040-8a80115d6401')
        # this test needs updated when the test database is updated
        self.assertEqual(len(data), 0)

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
        # TODO: This is broken -- there are no environmental samples associated
        # with the test user. We need to set something up like we have in qiita
        # where a test DB is set up and torn down for each individual test
        self.assertEqual(barcodes, set())

    def test_getAvailableBarcodes(self):
        data = self.data_access.getAvailableBarcodes(
            'd8592c74-7da1-2135-e040-8a80115d6401')
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

    def test_getMapMarkers(self):
        data = self.data_access.getMapMarkers()
        self.assertNotEqual(len(data), 0)

    def test_handoutCheck(self):
        is_handout = self.data_access.handoutCheck('test', 'wrongpass')
        self.assertFalse(is_handout)

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
        self.assertEqual([rec[12], rec[13], rec[14]], ['n', 'n', 'y'])
        self.data_access.updateAKB('000010860', None, None, None, None, None)
        cur.execute('select * from ag_kit_barcodes where barcode = %s',
                    ('000010860',))
        rec = cur.fetchone()
        self.assertEqual([rec[12], rec[13], rec[14]], [None, None, None])

    def test_getAGKitIDsByEmail(self):
        data = self.data_access.getAGKitIDsByEmail('test@microbio.me')
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
        self.assertTrue(bcrypt.verify('newpass', rec[0]))

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
        observed = self.data_access.getBarcodesByKit('test')
        expected = {'000010860', '000006616', '000000001'}

        self.assertEqual(set(observed), expected)

    def test_checkPrintResults(self):
        data = self.data_access.checkPrintResults('test')
        self.assertTrue(data is None)

    def test_get_user_for_kit(self):
        data = self.data_access.get_user_for_kit('test')
        self.assertEqual(data, 'd8592c74-7da1-2135-e040-8a80115d6401')

    def test_menu_items(self):
        data = self.data_access.get_menu_items('test')
        self.assertEqual(data[0]['foo'][0]['barcode'], '000000001')

    def test_get_user_info(self):
        data = self.data_access.get_user_info('test')
        self.assertEqual(data['email'], 'test@microbio.me')

    def test_get_barcode_results(self):
        data = self.data_access.get_barcode_results('test')
        self.assertEqual(len(data), 1)
        data = self.data_access.get_barcode_results('1111')
        self.assertEqual(len(data), 0)


if __name__ == "__main__":
    main()
