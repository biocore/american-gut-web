from unittest import TestCase, main
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
        raise NotImplementedError()

    def test_ag_verify_kit_password_change_code(self):
        raise NotImplementedError()

    def test_getBarcodesByKit(self):
        raise NotImplementedError()

    def test_checkPrintResults(self):
        obs = self.ag_data.checkPrintResults('tst_PmaJU')
        self.assertFalse(obs)

        obs = self.ag_data.checkPrintResults('tst_Tnwce')
        self.assertTrue(obs)

    def test_checkPrintResults_invalid_ids(self):
        obs = self.ag_data.checkPrintResults('xxx00112333123---123222')
        self.assertFalse(obs)

        obs = self.ag_data.checkPrintResults(':Lfoo:Lbar:Lbaz:Ospam:Leggs')
        self.assertFalse(obs)

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
