-- Sept 16, 2015
-- Add way to retire questions
--promote unmappable questions from old survey

CREATE TABLE ag.survey_question_retired (
	survey_id            bigint  NOT NULL,
	survey_question_id   bigint  NOT NULL,
	CONSTRAINT pk_survey_question_retired PRIMARY KEY ( survey_id, survey_question_id )
 );
CREATE INDEX idx_survey_question_retired_0 ON ag.survey_question_retired ( survey_question_id );
-- No FK to survey_id so we can retire whole surveys
ALTER TABLE ag.survey_question_retired ADD CONSTRAINT fk_survey_question_retired FOREIGN KEY ( survey_question_id ) REFERENCES ag.survey_question( survey_question_id );

