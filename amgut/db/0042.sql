CREATE TABLE ag."source" (
	source_id            uuid DEFAULT ag.uuid_generate_v4() ,
	source_name          varchar(100)  ,
	ag_login_id          uuid  ,
	vioscreen_status     integer  ,
	CONSTRAINT pk_source UNIQUE ( source_id )
 );

CREATE INDEX idx_source_1 ON ag."source" ( ag_login_id );

COMMENT ON TABLE ag."source" IS 'A "source" is the human, animal or environment that was swapped for microbial analysis.';
COMMENT ON COLUMN ag."source".source_id IS 'A unique ID to identify the source.';
COMMENT ON COLUMN ag."source".source_name IS 'Sources can come with names, e.g. names for the humans that have been swapped.';
COMMENT ON COLUMN ag."source".ag_login_id IS 'Points to the "user" that owns this source.';

CREATE TABLE ag.source_barcodes_surveys (
	source_id            uuid  NOT NULL,
	barcode              varchar  ,
	survey_id            varchar
 );

CREATE INDEX idx_source ON ag.source_barcodes_surveys ( barcode );
CREATE INDEX idx_source_0 ON ag.source_barcodes_surveys ( survey_id );
CREATE INDEX idx_source_barcodes_surveys ON ag.source_barcodes_surveys ( source_id );

COMMENT ON COLUMN ag.source_barcodes_surveys.source_id IS 'Points to information about the source, like its name.';
COMMENT ON COLUMN ag.source_barcodes_surveys.barcode IS 'Points to barcode(s) that are assigned to this source.';
COMMENT ON COLUMN ag.source_barcodes_surveys.survey_id IS 'Points to survey(s) that are assigned to this source.';

ALTER TABLE ag.source_barcodes_surveys ADD CONSTRAINT fk_source_barcode FOREIGN KEY ( barcode ) REFERENCES barcodes.barcode( barcode );
ALTER TABLE ag.source_barcodes_surveys ADD CONSTRAINT fk_source_barcodes_surveys FOREIGN KEY ( source_id ) REFERENCES ag."source"( source_id );

-- Re-use Daniels SQL statements to fill the new tables:

-- create a view of all of the participants with multiple survey ids
CREATE OR REPLACE TEMP VIEW multiple_ids AS
SELECT ag_login_id,
       participant_name,
       unnest(survey_ids) AS survey_id
FROM (SELECT DISTINCT ag_login_id,
                      participant_name,
                      array_agg(survey_id) AS survey_ids
      FROM ag.ag_login_surveys
      GROUP BY ag_login_id, participant_name) AS foo
where array_length(survey_ids, 1) > 1;

-- create a view of all of the barcodes associated with the participants
CREATE OR REPLACE TEMP VIEW participant_barcodes AS
SELECT ag_login_id, participant_name, barcode
FROM multiple_ids mi
JOIN ag.ag_kit_barcodes USING(survey_id);

-- produce the cartesian product of barcodes and survey ids into a temp
-- view that is in a common column structure to ag_kit_barcodes
CREATE OR REPLACE TEMP VIEW like_ag_kit_barcodes AS
SELECT ag_kit_barcode_id,
       ag_kit_id,
       barcode,
       CASE WHEN multiple_ids.survey_id IS NOT NULL
            THEN multiple_ids.survey_id
            ELSE ag.ag_kit_barcodes.survey_id
       END,
       sample_barcode_file,
       sample_barcode_file_md5,
       site_sampled,
       sample_date,
       sample_time,
       notes,
       environment_sampled,
       moldy,
       overloaded,
       other,
       other_text,
       date_of_last_email,
       results_ready,
       withdrawn,
       refunded,
       deposited,
			 ag_login_id,
			 participant_name
FROM participant_barcodes
JOIN multiple_ids USING (ag_login_id, participant_name)
FULL JOIN ag.ag_kit_barcodes USING (barcode);

-- enrich with ag_login_id and participant_name; the later becomes source_name
CREATE OR REPLACE TEMP VIEW foo AS
SELECT barcode,
			 survey_id,
			 ag_login_id,
			 participant_name,
			 vioscreen_status
FROM like_ag_kit_barcodes
JOIN ag.ag_login_surveys USING (survey_id);

-- fill ag.source table with all unique pairs of ag_login_id, source_name, which have assigned barcodes
INSERT INTO ag.source (ag_login_id, source_name, vioscreen_status)
SELECT DISTINCT ag_login_id, participant_name, vioscreen_status FROM foo;

-- create a view that holds all ag_login_id, participant_name combinations that have NO assigned barcodes, yet.
CREATE OR REPLACE TEMP VIEW nobarcodes AS
SELECT DISTINCT ag_login_id, participant_name, vioscreen_status FROM ag.ag_login_surveys WHERE (ag_login_id, participant_name) NOT IN (SELECT ag_login_id, source_name FROM ag.source);

-- fill ag.source table with all unique pairs of ag_login_id, source_name, which have no assigned barcodes yet.
WITH ins1 AS (
	INSERT INTO ag.source (ag_login_id, source_name, vioscreen_status)
	SELECT DISTINCT ag_login_id, participant_name, vioscreen_status FROM nobarcodes
	RETURNING *
)
INSERT INTO ag.source_barcodes_surveys (source_id, survey_id)
SELECT source_id, survey_id FROM ins1 JOIN ag.ag_login_surveys ON (ins1.ag_login_id = ag_login_surveys.ag_login_id AND ins1.source_name = ag_login_surveys.participant_name);

-- fill many-to-many relation source_barcodes_surveys
INSERT INTO ag.source_barcodes_surveys (source_id, barcode, survey_id)
SELECT source_id, barcode, survey_id
FROM foo
JOIN ag.source ON (foo.ag_login_id = ag.source.ag_login_id AND
									 foo.participant_name = ag.source.source_name);


-- remove now duplicate information:
--ALTER TABLE ag.ag_kit_barcodes DROP COLUMN survey_id;
--ALTER TABLE ag.ag_login_surveys DROP COLUMN vioscreen_status;

-- looks like we have two consents for sources that do not exist otherwise, ie in ag_login_surveys tables:
-- e1934ceb-6e92-c36a-e040-8a80115d2d64 | Name - sO%Ze\WáGö
-- e1934ceb-6e92-c36a-e040-8a80115d2d64 | Name - ÅfúEé#m+uø

-- why are there 68 duplicate entries:
-- SELECT source_name, ag_login_id, count(*), array_agg(source_id) FROM ag.source GROUP BY source_name, ag_login_id HAVING count(*) > 1;
