--Feb 9, 2016
--Add environmental sample survey

INSERT INTO survey_group (group_order, american, british) VALUES (-3, 'Environmental Information', 'Environmental Information');

----------------------------------------------------------
-- surveys
----------------------------------------------------------
INSERT INTO surveys (survey_id, survey_group) VALUES (3, -3);

----------------------------------------------------------
-- survey_question
----------------------------------------------------------
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES (162, 'ENV_NAME', 'Descriptive name for the sample', 'Descriptive name for the sample');
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES (163, 'ZIP', 'Zipcode sample was collected in', 'Zipcode sample was collected in');
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES (164, 'ENV_DESCRIPTION', 'Please describe the sample and where it was collected from', 'Please describe the sample and where it was collected from');

----------------------------------------------------------
-- group_questions
----------------------------------------------------------

INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-3, 162, 0);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-3, 163, 1);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-3, 164, 2);

----------------------------------------------------------
-- survey_question_response_type
----------------------------------------------------------
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (162, 'STRING');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (163, 'STRING');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (164, 'TEXT');
