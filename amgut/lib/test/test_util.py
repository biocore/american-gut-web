from unittest import TestCase, main
from amgut.lib.util import survey_fermented, survey_surf


class TestUtil(TestCase):
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


if __name__ == '__main__':
    main()
