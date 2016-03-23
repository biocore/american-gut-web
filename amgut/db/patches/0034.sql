--Feb 10, 2016
--Create and rearrange tables for redcap survey integration
CREATE TABLE ag.languages ( 
    lang                 varchar(5)  NOT NULL,
    CONSTRAINT pk_languages PRIMARY KEY ( lang )
 );
COMMENT ON COLUMN ag.languages.lang IS 'ISO 639-1 language code with sub-code';
INSERT INTO ag.languages (lang) VALUES ('en-US'), ('en-GB');

ALTER TABLE ag.ag_consent ADD COLUMN redcap_record_id bigserial UNIQUE NOT NULL;
ALTER TABLE ag.ag_consent ADD COLUMN lang varchar(5) NOT NULL DEFAULT 'en-US';
ALTER TABLE ag.ag_consent ADD CONSTRAINT fk_language FOREIGN KEY ( lang ) REFERENCES ag.languages( lang );
-- Create type column and set it to human or animal for current surveys
ALTER TABLE ag.ag_consent ADD COLUMN type varchar NOT NULL DEFAULT 'human';
UPDATE ag.ag_consent SET type='animal' WHERE parent_1_name = 'ANIMAL_SURVEY';
ALTER TABLE ag.ag_consent ALTER COLUMN type DROP DEFAULT;

CREATE TABLE ag.survey_types (
    survey_type          varchar  NOT NULL,
    CONSTRAINT pk_survey_types PRIMARY KEY ( survey_type )
 );
COMMENT ON COLUMN ag.survey_types.survey_type IS 'Human, Animal, etc';
INSERT INTO ag.survey_types (survey_type) VALUES ('Human'), ('Animal'), ('Environmental');

CREATE TABLE ag.redcap_instruments (
    redcap_instrument_id varchar(500)  NOT NULL,
    survey_type          varchar  NOT NULL,
    survey_name          varchar(100)  NOT NULL,
    description          varchar(500)  Not NULL,
    lang                 varchar(5)  NOT NULL,
    secondary            bool DEFAULT TRUE,
    CONSTRAINT pk_redcap_instruments PRIMARY KEY ( redcap_instrument_id )
 );
CREATE INDEX idx_redcap_instruments ON ag.redcap_instruments ( lang );
CREATE INDEX idx_redcap_instruments_0 ON ag.redcap_instruments ( survey_type );
COMMENT ON COLUMN ag.redcap_instruments.survey_type IS 'What the survey is (Human, Animal, etc)';
COMMENT ON COLUMN ag.redcap_instruments.survey_name IS 'Survey name, in language given';
COMMENT ON COLUMN ag.redcap_instruments.description IS 'human readable description of survey, in language given (for website)';
COMMENT ON COLUMN ag.redcap_instruments.secondary IS 'If this is a secondary survey or not (default true)';
ALTER TABLE ag.redcap_instruments ADD CONSTRAINT fk_redcap_instruments FOREIGN KEY ( lang ) REFERENCES ag.languages( lang );
ALTER TABLE ag.redcap_instruments ADD CONSTRAINT fk_redcap_instruments_0 FOREIGN KEY ( survey_type ) REFERENCES ag.survey_types( survey_type );
INSERT INTO ag.redcap_instruments (redcap_instrument_id,survey_type, survey_name, description, lang, secondary) VALUES
  ('ag-human-en-US', 'Human', 'American Gut Human Survey', 'General human survey for the American Gut Project', 'en-US', 'F');

ALTER TABLE ag.ag_login_surveys
ADD COLUMN  redcap_instrument_id varchar(500),
ADD COLUMN redcap_record_id bigint,
ADD COLUMN redcap_event_id integer NOT NULL DEFAULT 0,
ADD COLUMN survey_timestamp timestamp DEFAULT NOW(),
ADD CONSTRAINT idx_surveys_1 UNIQUE ( redcap_record_id, redcap_event_id, redcap_instrument_id );
CREATE INDEX idx_surveys_2 ON ag.ag_login_surveys ( redcap_record_id );
CREATE INDEX idx_surveys_3 ON ag.ag_login_surveys ( redcap_instrument_id );
ALTER TABLE ag.ag_login_surveys ADD CONSTRAINT fk_surveys FOREIGN KEY ( redcap_record_id ) REFERENCES ag.ag_consent( redcap_record_id );
ALTER TABLE ag.ag_login_surveys ADD CONSTRAINT fk_surveys_0 FOREIGN KEY ( redcap_instrument_id ) REFERENCES ag.redcap_instruments( redcap_instrument_id );
UPDATE ag.ag_login_surveys ls
SET redcap_record_id = c.redcap_record_id,
    survey_timestamp = c.date_signed
FROM ag.ag_consent AS c
WHERE c.participant_name = ls.participant_name AND c.ag_login_id = ls.ag_login_id;
ALTER TABLE ag.ag_login_surveys DROP COLUMN participant_name, DROP COLUMN ag_login_id;
ALTER TABLE ag.ag_login_surveys ALTER COLUMN redcap_event_id DROP DEFAULT;
ALTER TABLE ag.ag_login_surveys ALTER COLUMN redcap_record_id SET NOT NULL;
