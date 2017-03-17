from unittest import TestCase, main
from amgut.lib.util import (survey_fermented, survey_surf, survey_vioscreen,
                            survey_asd, rollback)
from amgut.lib.data_access.ag_data_access import AGDataAccess


class TestUtil(TestCase):
    def setUp(self):
        self.ag_data = AGDataAccess()

    def tearDown(self):
        del self.ag_data

    def test_survey_fermented(self):
        obs = survey_fermented('survey_id', {'participant_name': 'test'})
        exp = ('<h3 style="text-align: center"><a href="/authed/'
               'secondary_survey/?type=fermented&participant_name=test" '
               'target="_blank">Fermented Foods Survey</a></h3>As part of our '
               'onging research into what drive changes in the human gut '
               'microbiome, we are looking at fermented foods and the '
               'microbiomes of fermented food eaters. Please click the link '
               'above if you would like to participate in this survey.')
        self.assertEqual(obs, exp)

    def test_survey_surf(self):
        obs = survey_surf('survey_id', {'participant_name': 'test'})
        exp = ('<h3 style="text-align: center"><a href="/authed/'
               'secondary_survey/?type=surf&participant_name=test" target='
               '"_blank">Surfing Survey</a></h3>As part of our study, we are '
               'interested in the effects of frequent and prolonged exposure '
               'to salt water and the ocean, as it pertains to surfing and '
               'surfers. If you are interested in participating, you can click'
               ' the link above and take the survey.')
        self.assertEqual(obs, exp)

    def test_survey_asd(self):
        obs = survey_asd('survey_id', {'participant_name': 'test'})
        exp = ('<h3 style="text-align: center"><a href="https://docs.google.'
               'com/forms/d/1ZlaQzENj7NA7TcdfFhXfW0jshrToTywAarV0fjTZQxc/'
               'viewform?entry.1089722816=survey_id&entry.1116725993&entry.'
               '1983725631&entry.2036966278&entry.1785627282&entry.1461731626'
               '&entry.1203990558&entry.843049551&entry.476318397&entry.'
               '383297943&entry.228366248&entry.1651855735&entry.1234457826&'
               'entry.1079752165" target="_blank">ASD-Cohort survey</a></h3>'
               '<a href="http://www.anl.gov/contributors/jack-gilbert">Dr. '
               'Jack Gilbert</a> is exploring the relationship between gut '
               'dysbiosis and Autism Spectrum Disorders, and in conjunction '
               'with the American Gut Project, we started an ASD-Cohort '
               'study. This additional survey contains questions specific to '
               'that cohort, but it is open to any participant to take if '
               'they so choose.')
        self.assertEqual(obs, exp)

    def test_survey_vioscreen(self):
        obs = survey_vioscreen('survey_id', {'participant_name': 'test'})
        # Validate using in because key changes every time due to encription
        self.assertIn('This is a validated FFQ, and is the one used '
                      'by the Mayo Clinic.', obs)
        self.assertIn('<h3 style="text-align: center"><a href="'
                      'https://vioscreen.com/remotelogin.aspx?Key=', obs)

    def test_rolback(self):
        # fetching a random kit ID from DB that is not yet verified
        kit = self.ag_data.get_random_supplied_kit_id_unverified()

        @rollback
        def tf(kit):
            self.ag_data.verifyKit(kit)

        obs = self.ag_data.getAGKitDetails(kit)
        self.assertEqual(obs['kit_verified'], 'n')

        tf(kit)
        obs = self.ag_data.getAGKitDetails(kit)
        self.assertEqual(obs['kit_verified'], 'n')


if __name__ == '__main__':
    main()
