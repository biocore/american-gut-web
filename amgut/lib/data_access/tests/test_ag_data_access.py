from unittest import TestCase, main
from passlib.hash import bcrypt
from amgut.lib.data_access.sql_connection import SQLConnectionHandler
from amgut.lib.data_access.ag_data_access import AGDataAccess


class TestAGDataAccess(TestCase):
    conn_handler = SQLConnectionHandler()
    ag_data = AGDataAccess()

    def test_create_AGDataAccess(self):
        raise NotImplementedError()

    def test_delete_AGDataAccess(self):
        raise NotImplementedError()

    def test_get_cursor(self):
        raise NotImplementedError()

    def test_open_connection(self):
        raise NotImplementedError()

    def test_get_col_names_from_cursor(self):
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        skid = 'test'
        # Check and set pass_reset_code if needed
        sql = '''UPDATE ag.ag_kit
                 SET pass_reset_code = %s
                 WHERE supplied_kit_id = %s AND pass_reset_code IS NULL
                 RETURNING pass_reset_code'''
        re_code = self.conn_handler.execute_fetchone(sql, ['T3ST', skid])[0]
        # Verify password is not what we are changing it to
        sql = 'SELECT kit_password FROM ag.ag_kit WHERE supplied_kit_id = %s'
        old_pass = self.conn_handler.execute_fetchone(sql, [skid])[0]
        self.assertFalse(bcrypt.verify('password', old_pass))

        # Verify password change
        test_sql = '''SELECT kit_password, pass_reset_code
                      FROM ag.ag_kit
                      WHERE supplied_kit_id = %s'''
        try:
            self.ag_data.ag_update_kit_password(skid, 'password')
            new_pass, new_code = self.conn_handler.execute_fetchone(
                test_sql, [skid])
        finally:
            # reset to old password and pass_reset_code
            sql = '''UPDATE ag.ag_kit
                     SET kit_password = %s
                     WHERE supplied_kit_id = %s'''
            self.conn_handler.execute(sql, [old_pass, skid])
            sql = '''UPDATE ag.ag_kit
                     SET pass_reset_code = %s
                     WHERE supplied_kit_id = %s'''
            code = re_code if re_code != 'T3ST' else None
            self.conn_handler.execute(sql, [code, skid])

        self.assertEqual(new_code, None)
        self.assertTrue(bcrypt.verify('password', new_pass))

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
