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
GRANT INSERT, UPDATE, DELETE, SELECT ON ALL TABLES IN SCHEMA ag, public, barcodes TO "ag_wwwuser";

-- Add plants question back as a retired question
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES (146, 'TYPES_OF_PLANTS', 'How many different species of plants did you consume during the last 7-day period?', 'How many different species of plants did you consume during the last 7-day period?');

INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (146, 'SINGLE');

INSERT INTO survey_response (american, british) VALUES ('Less than 5', 'Less than 5');
INSERT INTO survey_response (american, british) VALUES ('6 to 10', '6 to 10');
INSERT INTO survey_response (american, british) VALUES ('11 to 20', '11 to 20');
INSERT INTO survey_response (american, british) VALUES ('21 to 30', '21 to 30');
INSERT INTO survey_response (american, british) VALUES ('More than 30', 'More than 30');

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (146, 'Unspecified', 0);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (146, 'Less than 5', 1);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (146, '6 to 10', 2);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (146, '11 to 20', 3);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (146, '21 to 30', 4);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (146, 'More than 30', 5);

INSERT INTO survey_question_retired (survey_id, survey_question_id) VALUES (1, 146);

-- Promote answers
DO $do$
DECLARE
    top varchar;
    survey varchar;
    pid varchar;
    login varchar;
BEGIN
    -- Make sure not in test database so there's actually something to promote
    IF SELECT NOT EXISTS(SELECT 1
                         FROM information_schema.tables 
                         WHERE table_schema = 'ag' AND table_name = 'ag_human_survey')
    THEN
        RETURN;
    END IF;

    
END $do$