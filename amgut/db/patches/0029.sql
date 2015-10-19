-- October 12, 2015
-- Add tables needed to track plate maps and create prep templates
--Need to wipe out old, bad data in the plate table
DROP TABLE barcodes.plate_barcode CASCADE;
DROP TABLE barcodes.plate;

ALTER TABLE barcodes.barcode ALTER COLUMN barcode TYPE varchar;
ALTER TABLE barcodes.barcode ADD COLUMN priority bool NOT NULL DEFAULT 'F';
COMMENT ON COLUMN barcodes.barcode.priority IS 'Whether barcode is in priority queue';
ALTER TABLE barcodes.barcode ADD COLUMN priority_reason varchar;
ALTER TABLE barcodes.project ADD description varchar  NOT NULL DEFAULT '';

CREATE TYPE sequencer_instrument_model AS ENUM ('Genome Analyzer', 'Genome Analyzer II', 'Genome Analyzer Ix', 'HiSeq 2500', 'HiSeq 2000', 'HiSeq 1500', 'HiSeq 1000', 'MiSeq', 'HiScanSQ', 'HiSeq X Ten', 'NextSeq 500', 'GS', 'GS 20', 'GS FLX', 'GS FLX+', 'GS FLX Titanium', 'GS Junior', 'unspecified');
CREATE TYPE sequencer_platform AS ENUM ('Illumina', '454');
CREATE TYPE protocol_target_subfragment AS ENUM ('V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'ITS1', 'ITS2');

CREATE TYPE robot_robot_type AS ENUM ('kingfisher', 'eppendorf');
CREATE TYPE extraction_plate_ext_robot_tool AS ENUM ('4090642', '109383A', '110737B', '311169B', '110728B', '1083792', '311172B');
CREATE TYPE pcr_plate_tool_300_8 AS ENUM ('311318B', '311313B', '2084842', '109520A', '311466B', '3076189', '109375A');
CREATE TYPE pcr_plate_tool_50_8 AS ENUM ('311426B', '110705B', '109257A', '311441B', '110698B', '1083642', '4091722');

CREATE TABLE barcodes.person ( 
	person_id            bigint  NOT NULL,
	name                 varchar(100)  NOT NULL,
	email                varchar  NOT NULL,
	date_added           date DEFAULT current_date NOT NULL,
	CONSTRAINT pk_person PRIMARY KEY ( person_id )
 );

CREATE TABLE barcodes.robot ( 
	robot_name           varchar(100)  NOT NULL,
	robot_type           robot_robot_type  NOT NULL,
	date_added           date DEFAULT current_date NOT NULL,
	CONSTRAINT pk_robot PRIMARY KEY ( robot_name )
 );

CREATE TABLE barcodes.sequencer ( 
	sequencer_id         bigserial  NOT NULL,
	platform             sequencer_platform  NOT NULL,
	instrument_model     sequencer_instrument_model  NOT NULL,
	sequencing_method    varchar  NOT NULL,
	lanes                integer  NOT NULL,
	CONSTRAINT pk_sequencer PRIMARY KEY ( sequencer_id )
 );

CREATE TABLE barcodes.protocol ( 
	protocol             varchar(100)  NOT NULL,
	template_dna         integer  NOT NULL,
	target_gene          varchar  NOT NULL,
	target_subfragment   protocol_target_subfragment  NOT NULL,
	linker               varchar  NOT NULL,
	pcr_primers          varchar  NOT NULL,
	CONSTRAINT pk_protocol PRIMARY KEY ( protocol )
 );
COMMENT ON COLUMN barcodes.protocol.protocol IS 'Name of the protocol';
COMMENT ON COLUMN barcodes.protocol.template_dna IS 'Template DNA added, in uL';

CREATE TABLE barcodes.run_information ( 
	run_id               bigserial  NOT NULL,
	run_name             varchar(100)  NOT NULL,
	sequencer_id         bigint  NOT NULL,
	created_on           timestamp DEFAULT current_timestamp NOT NULL,
	run_date             date  ,
	finalized            bool DEFAULT 'F' NOT NULL,
	CONSTRAINT pk_run_information PRIMARY KEY ( run_id ),
	CONSTRAINT idx_run_information_0 UNIQUE ( run_name ) 
 );
CREATE INDEX idx_run_information ON barcodes.run_information ( sequencer_id );
ALTER TABLE barcodes.run_information ADD CONSTRAINT fk_run_information FOREIGN KEY ( sequencer_id ) REFERENCES barcodes.sequencer( sequencer_id );

CREATE TABLE barcodes.lane_information ( 
	run_id               integer  NOT NULL,
	run_prefix           varchar  NOT NULL,
	finalized            bool DEFAULT 'F' NOT NULL,
	CONSTRAINT pk_lane_information UNIQUE ( run_prefix ) ,
	CONSTRAINT idx_lane_information_0 PRIMARY KEY ( run_id, run_prefix )
 );
CREATE INDEX idx_lane_information ON barcodes.lane_information ( run_id );
COMMENT ON TABLE barcodes.lane_information IS 'Name for the lane on the run';
COMMENT ON COLUMN barcodes.lane_information.run_prefix IS 'Name for the lane on the run';
ALTER TABLE barcodes.lane_information ADD CONSTRAINT fk_lane_information FOREIGN KEY ( run_id ) REFERENCES barcodes.run_information( run_id );

CREATE TABLE barcodes.water ( 
	water_id             bigserial  NOT NULL,
	company              integer  NOT NULL,
	product_name         varchar(100)  NOT NULL,
	product_number       varchar  NOT NULL,
	CONSTRAINT pk_extraction_kit_1 UNIQUE ( water_id ) ,
	CONSTRAINT pk_water PRIMARY KEY ( water_id )
 );

CREATE TABLE barcodes.water_lot ( 
	water_id             integer  NOT NULL,
	water_lot            varchar  NOT NULL UNIQUE,
	date_added           date DEFAULT current_date NOT NULL,
	CONSTRAINT pk_water_lot PRIMARY KEY ( water_lot, water_id )
 );
CREATE INDEX idx_water_lot ON barcodes.water_lot ( water_id );
ALTER TABLE barcodes.water_lot ADD CONSTRAINT fk_water_lot FOREIGN KEY ( water_id ) REFERENCES barcodes.water( water_id );

CREATE TABLE barcodes.ext_kit_lot ( 
	extraction_kit_id    bigint  NOT NULL,
	ext_kit_lot          varchar  NOT NULL UNIQUE,
	date_added           date DEFAULT current_date NOT NULL,
	CONSTRAINT pk_ext_kit_lot PRIMARY KEY ( ext_kit_lot, extraction_kit_id )
 );

CREATE TABLE barcodes.extraction_kit ( 
	extraction_kit_id    bigserial  NOT NULL,
	company              integer  NOT NULL,
	product_name         varchar(100)  NOT NULL,
	product_number       varchar  NOT NULL,
	CONSTRAINT pk_extraction_kit UNIQUE ( extraction_kit_id ) ,
	CONSTRAINT pk_extraction_kit_2 PRIMARY KEY ( extraction_kit_id )
 );

CREATE TABLE barcodes.extraction_plate ( 
	barcode              varchar  NOT NULL,
	nickname             varchar(50)  NOT NULL,
	ext_robot            varchar  NOT NULL,
	ext_robot_tool       extraction_plate_ext_robot_tool  NOT NULL,
	kf_robot             varchar  NOT NULL,
	ext_kit_lot          varchar  NOT NULL,
	person_id            bigint  NOT NULL,
	finalized            bool DEFAULT 'F' NOT NULL,
	ext_created          timestamp DEFAULT current_date NOT NULL,
	ext_finalized        timestamp  ,
	CONSTRAINT plate_pkey PRIMARY KEY ( barcode )
 );
CREATE INDEX idx_plate_0 ON barcodes.extraction_plate ( ext_robot );
CREATE INDEX idx_plate_1 ON barcodes.extraction_plate ( kf_robot );
CREATE INDEX idx_plate_2 ON barcodes.extraction_plate ( ext_kit_lot );
CREATE INDEX idx_plate_4 ON barcodes.extraction_plate ( person_id );
COMMENT ON COLUMN barcodes.extraction_plate.ext_robot IS 'Extraction robot used for this plate';
COMMENT ON COLUMN barcodes.extraction_plate.ext_robot_tool IS 'Extraction robot pipette head used';
COMMENT ON COLUMN barcodes.extraction_plate.kf_robot IS 'kingfisher robot used for extracton';
COMMENT ON COLUMN barcodes.extraction_plate.ext_kit_lot IS 'Extraction kit lot number';
COMMENT ON COLUMN barcodes.extraction_plate.person_id IS 'Person running the extraction';
COMMENT ON COLUMN barcodes.extraction_plate.finalized IS 'Whether the plate map is complete or still being filled.';
ALTER TABLE barcodes.extraction_plate ADD CONSTRAINT fk_plate FOREIGN KEY ( barcode ) REFERENCES barcodes.barcode( barcode );
ALTER TABLE barcodes.extraction_plate ADD CONSTRAINT fk_plate_5 FOREIGN KEY ( person_id ) REFERENCES barcodes.person( person_id );
ALTER TABLE barcodes.extraction_plate ADD CONSTRAINT fk_plate_1 FOREIGN KEY ( ext_kit_lot ) REFERENCES barcodes.ext_kit_lot( ext_kit_lot );
ALTER TABLE barcodes.extraction_plate ADD CONSTRAINT fk_extraction_plate FOREIGN KEY ( ext_robot ) REFERENCES barcodes.robot( robot_name );
ALTER TABLE barcodes.extraction_plate ADD CONSTRAINT fk_extraction_plate_0 FOREIGN KEY ( kf_robot ) REFERENCES barcodes.robot( robot_name );

CREATE TABLE barcodes.master_mix ( 
	master_mix_id        bigserial  NOT NULL,
	company              integer  NOT NULL,
	product_name         varchar(100)  NOT NULL,
	product_number       varchar  NOT NULL,
	CONSTRAINT pk_extraction_kit_0 UNIQUE ( master_mix_id ) ,
	CONSTRAINT pk_master_mix PRIMARY KEY ( master_mix_id )
 );

CREATE TABLE barcodes.master_mix_lot ( 
	master_mix_id        bigint  NOT NULL,
	master_mix_lot       varchar  NOT NULL UNIQUE,
	date_added           date DEFAULT current_date NOT NULL,
	CONSTRAINT pk_master_mix_lot PRIMARY KEY ( master_mix_lot, master_mix_id )
 );
CREATE INDEX idx_master_mix_lot ON barcodes.master_mix_lot ( master_mix_id );
ALTER TABLE barcodes.master_mix_lot ADD CONSTRAINT fk_master_mix_lot FOREIGN KEY ( master_mix_id ) REFERENCES barcodes.master_mix( master_mix_id );

CREATE TABLE barcodes.primer_plate ( 
	primer_plate_id      bigserial  NOT NULL,
	nickname             varchar(100)  NOT NULL,
	protocol             varchar  NOT NULL,
	sequencing_barcodes  json  NOT NULL,
	CONSTRAINT pk_sequencing_plates PRIMARY KEY ( primer_plate_id )
 );
CREATE INDEX idx_sequencing_plate ON barcodes.primer_plate ( protocol );
COMMENT ON COLUMN barcodes.primer_plate.sequencing_barcodes IS 'dict of barcode keyed to well, e.g.{A1: ACTACTCCATAC';
ALTER TABLE barcodes.primer_plate ADD CONSTRAINT fk_primer_plate FOREIGN KEY ( protocol ) REFERENCES barcodes.protocol( protocol );

CREATE TABLE barcodes.primer_plate_lot ( 
	primer_plate_id      bigint  NOT NULL,
	primer_plate_lot     varchar  NOT NULL UNIQUE,
	date_added           date DEFAULT current_date NOT NULL,
	CONSTRAINT pk_primer_plate_lot PRIMARY KEY ( primer_plate_lot, primer_plate_id )
 );
CREATE INDEX idx_primer_plate_lot ON barcodes.primer_plate_lot ( primer_plate_id );
ALTER TABLE barcodes.primer_plate_lot ADD CONSTRAINT fk_primer_plate_lot FOREIGN KEY ( primer_plate_id ) REFERENCES barcodes.primer_plate( primer_plate_id );


CREATE TABLE barcodes.pcr_plate ( 
	barcode              varchar  NOT NULL,
	nickname             varchar(100)  NOT NULL,
	primer_plate_lot     varchar  NOT NULL,
	amplicon             varchar  NOT NULL,
	master_mix_lot       varchar  NOT NULL,
	water_lot            varchar  NOT NULL,
	pcr_robot            varchar  NOT NULL,
	tool_300_8           pcr_plate_tool_300_8  NOT NULL,
	tool_50_8            pcr_plate_tool_50_8  NOT NULL,
	person_id            bigint  NOT NULL,
	pcr_created          timestamp DEFAULT current_timestamp NOT NULL,
	CONSTRAINT pkey_pcr_plate PRIMARY KEY ( barcode, nickname ),
	CONSTRAINT idx_pcr_plate UNIQUE ( barcode ) ,
	CONSTRAINT pk_pcr_plate UNIQUE ( nickname ) 
 );
CREATE INDEX idx_pcr_plate_0 ON barcodes.pcr_plate ( pcr_robot );
CREATE INDEX idx_pcr_plate_1 ON barcodes.pcr_plate ( primer_plate_lot );
CREATE INDEX idx_pcr_plate_2 ON barcodes.pcr_plate ( master_mix_lot );
CREATE INDEX idx_pcr_plate_3 ON barcodes.pcr_plate ( water_lot );
CREATE INDEX idx_pcr_plate_5 ON barcodes.pcr_plate ( person_id );
COMMENT ON COLUMN barcodes.pcr_plate.tool_300_8 IS '300uL pipette head used';
COMMENT ON COLUMN barcodes.pcr_plate.tool_50_8 IS '50uL pipette head used';
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate FOREIGN KEY ( barcode ) REFERENCES barcodes.extraction_plate( barcode );
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate_5 FOREIGN KEY ( person_id ) REFERENCES barcodes.person( person_id );
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate_0 FOREIGN KEY ( primer_plate_lot ) REFERENCES barcodes.primer_plate_lot( primer_plate_lot );
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate_1 FOREIGN KEY ( master_mix_lot ) REFERENCES barcodes.master_mix_lot( master_mix_lot );
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate_2 FOREIGN KEY ( water_lot ) REFERENCES barcodes.water_lot( water_lot );
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate_3 FOREIGN KEY ( pcr_robot ) REFERENCES barcodes.robot( robot_name );

CREATE TABLE barcodes.pcr_plate_lane ( 
	run_prefix           varchar  NOT NULL,
	barcode              varchar  NOT NULL,
	nickname             varchar(100)  NOT NULL,
	CONSTRAINT pk_pcr_plate_lane PRIMARY KEY ( barcode, nickname, run_prefix )
 );
CREATE INDEX idx_pcr_plate_lane_0 ON barcodes.pcr_plate_lane ( barcode );
CREATE INDEX idx_pcr_plate_lane_1 ON barcodes.pcr_plate_lane ( nickname );
CREATE INDEX idx_pcr_plate_lane ON barcodes.pcr_plate_lane ( run_prefix );
ALTER TABLE barcodes.pcr_plate_lane ADD CONSTRAINT fk_pcr_plate_lane_0 FOREIGN KEY ( barcode ) REFERENCES barcodes.pcr_plate( barcode );
ALTER TABLE barcodes.pcr_plate_lane ADD CONSTRAINT fk_pcr_plate_lane_1 FOREIGN KEY ( nickname ) REFERENCES barcodes.pcr_plate( nickname );
ALTER TABLE barcodes.pcr_plate_lane ADD CONSTRAINT fk_pcr_plate_lane_2 FOREIGN KEY ( run_prefix ) REFERENCES barcodes.lane_information( run_prefix );

CREATE TABLE barcodes.plate_sample ( 
	barcode              varchar  NOT NULL,
	well                 varchar(3)  NOT NULL,
	sample               varchar  NOT NULL,
	project_id           bigint  NOT NULL,
	sample_size          float8  NOT NULL,
	CONSTRAINT pkey_plate_barcode_1 PRIMARY KEY ( barcode, well )
 );
CREATE INDEX idx_plate_barcode ON barcodes.plate_sample ( well );
CREATE INDEX idx_plate_barcode_0 ON barcodes.plate_sample ( barcode );
CREATE INDEX idx_plate_sample ON barcodes.plate_sample ( project_id );
COMMENT ON COLUMN barcodes.plate_sample.sample_size IS 'Sample size, in grams';
ALTER TABLE barcodes.plate_sample ADD CONSTRAINT fk_plate_barcode_0 FOREIGN KEY ( barcode ) REFERENCES barcodes.extraction_plate( barcode );
ALTER TABLE barcodes.plate_sample ADD CONSTRAINT fk_plate_sample FOREIGN KEY ( project_id ) REFERENCES barcodes.project( project_id );
