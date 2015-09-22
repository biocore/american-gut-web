-- September 21, 2015
-- remove question 146 from non-human surveys

DELETE FROM ag.survey_answers
WHERE survey_question_id = 146
AND survey_id IN (
    SELECT survey_id FROM ag.ag_login_surveys
    JOIN ag.ag_consent USING (ag_login_id, participant_name)
    WHERE parent_1_name = 'ANIMAL_SURVEY');