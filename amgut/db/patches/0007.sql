/* 24 April 2015
Barcodes were not associated with the new survey IDs when the surveys were
promoted. Since (at this time) we only have one survey per participant,
we can assume that if there is an entry in ag_login_surveys for a given
participant, it is the only survey they have. So update any barcodes that are
associated with that participant in ag_kit_barcodes to have that survey id.

Adam Robbins-Pianka
*/

UPDATE ag_kit_barcodes akb1 SET survey_id = (
    SELECT als.survey_id
    FROM ag_kit ak JOIN ag_login_surveys als USING (ag_login_id)
    WHERE ak.ag_kit_id = akb1.ag_kit_id
    AND als.participant_name = akb1.participant_name);
