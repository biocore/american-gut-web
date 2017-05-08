from unittest import TestCase, main

from amgut.lib.data_access.sql_connection import TRN


class TestMigration(TestCase):
    def test_oldtables(self):
        # check that we have 13512 distinct "sources" in ag_login_surveys,
        # which are of tuple ag_login_id, participant_name
        with TRN:
            sql = """SELECT COUNT(*)
                     FROM (SELECT DISTINCT ag_login_id, participant_name
                           FROM ag.ag_login_surveys) AS foo"""
            TRN.add(sql, [])
            num_sources = TRN.execute_fetchindex()[0][0]
        self.assertEqual(num_sources, 13512)

        with TRN:
            sql = """SELECT COUNT(*)
                     FROM (SELECT DISTINCT ag_login_id, participant_name
                           FROM ag.ag_login_surveys
                           WHERE vioscreen_status IS NOT NULL) AS foo"""
            TRN.add(sql, [])
            num_vio_sources = TRN.execute_fetchindex()[0][0]
        self.assertEqual(num_vio_sources, 1692)

        # check number of unique surveys
        with TRN:
            sql = """SELECT COUNT(DISTINCT survey_id)
                     FROM ag.ag_login_surveys"""
            TRN.add(sql, [])
            num_surveys = TRN.execute_fetchindex()[0][0]
        self.assertEqual(num_surveys, 13850)

        # check number of sources with more than one survey
        with TRN:
            sql = """SELECT COUNT(*)
                     FROM (SELECT ag_login_id,
                                  participant_name,
                                  count(survey_id) AS cs
                           FROM ag.ag_login_surveys
                           GROUP BY ag_login_id, participant_name) AS foo
                           WHERE cs > 1"""
            TRN.add(sql, [])
            num_multi_sources = TRN.execute_fetchindex()[0][0]
        self.assertEqual(num_multi_sources, 314)

        # check number of consents
        with TRN:
            sql = """SELECT COUNT(*)
                     FROM (SELECT DISTINCT ag_login_id, participant_name
                           FROM ag.ag_consent) AS foo"""
            TRN.add(sql, [])
            num_consent = TRN.execute_fetchindex()[0][0]
        self.assertEqual(num_consent, 13514)
        # why do we have two more consents than sources (both for ag_login_id
        # e1934ceb-6e92-c36a-e040-8a80115d2d64)??

        # check number of barcodes
        with TRN:
            sql = """SELECT COUNT(*)
                     FROM (SELECT DISTINCT barcode
                           FROM ag.ag_kit_barcodes) AS foo"""
            TRN.add(sql, [])
            num_barcodes = TRN.execute_fetchindex()[0][0]
        self.assertEqual(num_barcodes, 28865)

    def test_sources(self):
        with TRN:
            sql = """SELECT barcode
                     FROM source_barcodes_surveys
                     JOIN ag.ag_login_surveys USING (survey_id)
                     WHERE ag_login_id = %s AND survey_id = %s"""

            exp_barcodes = ['000063476', '000063477', '000063478',
                            '000063479', '000063480', '000063481',
                            '000063482', '000063483', '000063484',
                            '000063487']
            TRN.add(sql, ['0097e665-ea1d-483d-b248-402bcf6abf2a',
                          '5c7106b35dda787d'])
            obs_barcodes = [x[0] for x in TRN.execute_fetchindex()]
            self.assertEqual(set(exp_barcodes), set(obs_barcodes))
            TRN.add(sql, ['0097e665-ea1d-483d-b248-402bcf6abf2a',
                          'fb6d5a66ef0dd8c7'])
            obs_barcodes = [x[0] for x in TRN.execute_fetchindex()]
            self.assertEqual(set(exp_barcodes), set(obs_barcodes))

            exp_barcodes = ['000046215']
            TRN.add(sql, ['0073af72-39e5-4bc8-9908-eff6c4ce2d6c',
                          'db2e324b45e34b97'])
            obs_barcodes = [x[0] for x in TRN.execute_fetchindex()]
            self.assertEqual(set(exp_barcodes), set(obs_barcodes))
            TRN.add(sql, ['0073af72-39e5-4bc8-9908-eff6c4ce2d6c',
                          'eea585c6eb5dd4b5'])
            obs_barcodes = [x[0] for x in TRN.execute_fetchindex()]
            self.assertEqual(set(exp_barcodes), set(obs_barcodes))
            TRN.add(sql, ['0073af72-39e5-4bc8-9908-eff6c4ce2d6c',
                          'fb420871cdcf5adb'])
            obs_barcodes = [x[0] for x in TRN.execute_fetchindex()]
            self.assertEqual(set(exp_barcodes), set(obs_barcodes))


if __name__ == "__main__":
    main()
