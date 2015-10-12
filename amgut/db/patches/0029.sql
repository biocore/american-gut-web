-- October 12, 2015
-- Add tables needed to track plate maps and create prep templates
--Need to wipe out old, bad data in the plate table
DELETE FROM barcodes.plate;
DROP TABLE barcodes.plate_barcode CASCADE;

ALTER TABLE barcodes.barcode ALTER COLUMN barcode TYPE varchar;
ALTER TABLE barcodes.project ADD description varchar  NOT NULL;

CREATE TABLE barcodes.lot ( 
	lot_id               bigserial  NOT NULL,
	lot_type             varchar  NOT NULL,
	lot                  varchar  NOT NULL,
	date_added           date DEFAULT current_date NOT NULL,
	CONSTRAINT pk_lots PRIMARY KEY ( lot_id )
 );

CREATE TABLE barcodes.robots ( 
	robot_id             bigserial  NOT NULL,
	robot_type           varchar  NOT NULL,
	robot_name           varchar(100)  NOT NULL,
	date_added           date DEFAULT current_date NOT NULL,
	CONSTRAINT pk_robots PRIMARY KEY ( robot_id )
 );

CREATE TABLE barcodes.person ( 
	person_id            bigint  NOT NULL,
	name                 varchar(100)  NOT NULL,
	email                varchar  NOT NULL,
	date_added           date DEFAULT current_date NOT NULL,
	CONSTRAINT pk_person PRIMARY KEY ( person_id )
 );


CREATE TABLE barcodes.plate_sample ( 
	barcode              bigint  NOT NULL,
	well                 varchar(3)  NOT NULL,
	sample               varchar  NOT NULL,
	sample_size          float8  NOT NULL,
	CONSTRAINT pkey_plate_barcode_1 PRIMARY KEY ( barcode, well )
 );
CREATE INDEX idx_plate_barcode ON barcodes.plate_sample ( well );
CREATE INDEX idx_plate_barcode_0 ON barcodes.plate_sample ( barcode );
COMMENT ON COLUMN barcodes.plate_sample.sample_size IS 'Sample size, in grams';
ALTER TABLE barcodes.plate_sample ADD CONSTRAINT fk_plate_barcode_0 FOREIGN KEY ( barcode ) REFERENCES barcodes.plate( barcode );

CREATE TABLE barcodes.protocol ( 
	protocol_id          bigserial  NOT NULL,
	protocol_name        varchar(100)  NOT NULL,
	template_dna         integer  NOT NULL,
	platform             varchar  NOT NULL,
	pcr_primers          varchar  NOT NULL,
	instrument_model     varchar  NOT NULL,
	linker               varchar  NOT NULL,
	sequencing_method    varchar  NOT NULL,
	target_gene          varchar  NOT NULL,
	target_subfragment   varchar  NOT NULL,
	CONSTRAINT pk_protocol PRIMARY KEY ( protocol_id )
 );
COMMENT ON COLUMN barcodes.protocol.template_dna IS 'Template DNA added, in uL';

CREATE TABLE barcodes.pcr_plate ( 
	barcode              varchar  NOT NULL,
	nickname             varchar(100)  NOT NULL,
	protocol             bigint  NOT NULL,
	primer_plate         integer  NOT NULL,
	primer_plate_lot     bigint  NOT NULL,
	amplicon             varchar  NOT NULL,
	master_mix_lot       bigint  NOT NULL,
	water_lot            bigint  NOT NULL,
	pcr_robot            bigint  NOT NULL,
	tool_300_8           bigint  NOT NULL,
	tool_50_8            bigint  NOT NULL,
	person               bigint  NOT NULL,
	pcr_created          timestamp DEFAULT current_timestamp NOT NULL,
	CONSTRAINT pkey_pcr_plate PRIMARY KEY ( barcode, nickname ),
	CONSTRAINT idx_pcr_plate UNIQUE ( barcode ) ,
	CONSTRAINT pk_pcr_plate UNIQUE ( nickname ) 
 );
CREATE INDEX idx_pcr_plate_run ON barcodes.pcr_plate_run ( run_id );
CREATE INDEX idx_pcr_plate_run_0 ON barcodes.pcr_plate_run ( barcode );
CREATE INDEX idx_pcr_plate_run_1 ON barcodes.pcr_plate_run ( nickname );
ALTER TABLE barcodes.pcr_plate_run ADD CONSTRAINT fk_pcr_plate_run FOREIGN KEY ( run_id ) REFERENCES barcodes.run_information( run_id );
ALTER TABLE barcodes.pcr_plate_run ADD CONSTRAINT fk_pcr_plate_run_0 FOREIGN KEY ( barcode ) REFERENCES barcodes.pcr_plate( barcode );
ALTER TABLE barcodes.pcr_plate_run ADD CONSTRAINT fk_pcr_plate_run_1 FOREIGN KEY ( nickname ) REFERENCES barcodes.pcr_plate( nickname );
CREATE INDEX idx_pcr_plate_0 ON barcodes.pcr_plate ( pcr_robot );
CREATE INDEX idx_pcr_plate_1 ON barcodes.pcr_plate ( primer_plate_lot );
CREATE INDEX idx_pcr_plate_2 ON barcodes.pcr_plate ( master_mix_lot );
CREATE INDEX idx_pcr_plate_3 ON barcodes.pcr_plate ( water_lot );
CREATE INDEX idx_pcr_plate_4 ON barcodes.pcr_plate ( protocol );
CREATE INDEX idx_pcr_plate_5 ON barcodes.pcr_plate ( person );
COMMENT ON COLUMN barcodes.pcr_plate.tool_300_8 IS '300uL pipette head used';
COMMENT ON COLUMN barcodes.pcr_plate.tool_50_8 IS '50uL pipette head used';
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate FOREIGN KEY ( barcode ) REFERENCES barcodes.plate( barcode );
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate_0 FOREIGN KEY ( pcr_robot ) REFERENCES barcodes.robots( robot_id );
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate_1 FOREIGN KEY ( primer_plate_lot ) REFERENCES barcodes.lot( lot_id );
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate_2 FOREIGN KEY ( master_mix_lot ) REFERENCES barcodes.lot( lot_id );
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate_3 FOREIGN KEY ( water_lot ) REFERENCES barcodes.lot( lot_id );
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate_4 FOREIGN KEY ( protocol ) REFERENCES barcodes.protocol( protocol_id );
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate_5 FOREIGN KEY ( person ) REFERENCES barcodes.person( person_id );

CREATE TABLE barcodes.pcr_plate_run ( 
	run_id               bigint  NOT NULL,
	barcode              varchar  NOT NULL,
	nickname             varchar(100)  NOT NULL,
	center_project_name  varchar(100)  ,
	CONSTRAINT pk_pcr_plate_run PRIMARY KEY ( run_id, barcode, nickname )
 );

CREATE TABLE barcodes.run_information ( 
	run_id               bigserial  NOT NULL,
	nickname             varchar(100)  NOT NULL,
	run_prefix           varchar  NOT NULL,
	created_on           timestamp DEFAULT current_timestamp NOT NULL,
	run_date             date  ,
	finalized            bool DEFAULT 'F' NOT NULL,
	CONSTRAINT pk_run_information PRIMARY KEY ( run_id )
 );

ALTER TABLE barcodes.plate DROP COLUMN plate_id;
ALTER TABLE barcodes.plate DROP COLUMN plate;
ALTER TABLE barcodes.plate DROP COLUMN sequence_date;
ALTER TABLE barcodes.plate ADD barcode varchar  NOT NULL;
ALTER TABLE barcodes.plate ADD nickname varchar(50)  NOT NULL;
ALTER TABLE barcodes.plate ADD project_id varchar(20)  NOT NULL;
ALTER TABLE barcodes.plate ADD protocol bigint  NOT NULL;
ALTER TABLE barcodes.plate ADD ext_robot bigint  NOT NULL;
ALTER TABLE barcodes.plate ADD ext_robot_tool varchar  NOT NULL;
ALTER TABLE barcodes.plate ADD kf_robot bigint  NOT NULL;
ALTER TABLE barcodes.plate ADD ext_kit_lot bigint  NOT NULL;
ALTER TABLE barcodes.plate ADD person bigint  NOT NULL;
ALTER TABLE barcodes.plate ADD finalized bool DEFAULT 'F' NOT NULL;
ALTER TABLE barcodes.plate ADD creation_timestamp timestamp DEFAULT current_date NOT NULL;
ALTER TABLE barcodes.plate ADD finalized_timestamp timestamp;

COMMENT ON COLUMN barcodes.plate.finalized IS 'Whether the plate map is complete or still being filled.';
COMMENT ON COLUMN barcodes.plate.person IS 'Person running the extraction';
COMMENT ON COLUMN barcodes.plate.ext_kit_lot IS 'Extraction kit lot number';
COMMENT ON COLUMN barcodes.plate.kf_robot IS 'kingifsher robot used for extracton';
COMMENT ON COLUMN barcodes.plate.ext_robot_tool IS 'Extraction robot pipette head used';
COMMENT ON COLUMN barcodes.plate.ext_robot IS 'Extraction robot used for this plate';

ALTER TABLE barcodes.plate DROP CONSTRAINT plate_pkey;
ALTER TABLE barcodes.plate ADD CONSTRAINT plate_pkey PRIMARY KEY ( barcode );
CREATE INDEX idx_plate ON barcodes.plate ( project_id );
CREATE INDEX idx_plate_0 ON barcodes.plate ( ext_robot );
CREATE INDEX idx_plate_1 ON barcodes.plate ( kf_robot );
CREATE INDEX idx_plate_2 ON barcodes.plate ( ext_kit_lot );
CREATE INDEX idx_plate_3 ON barcodes.plate ( protocol );
CREATE INDEX idx_plate_4 ON barcodes.plate ( person );
ALTER TABLE barcodes.plate ADD CONSTRAINT fk_plate FOREIGN KEY ( barcode ) REFERENCES barcodes.barcode( barcode );
ALTER TABLE barcodes.plate ADD CONSTRAINT fk_plate_0 FOREIGN KEY ( project_id ) REFERENCES barcodes.project( project_id );
ALTER TABLE barcodes.plate ADD CONSTRAINT fk_plate_1 FOREIGN KEY ( ext_robot ) REFERENCES barcodes.robots( robot_id );
ALTER TABLE barcodes.plate ADD CONSTRAINT fk_plate_2 FOREIGN KEY ( kf_robot ) REFERENCES barcodes.robots( robot_id );
ALTER TABLE barcodes.plate ADD CONSTRAINT fk_plate_3 FOREIGN KEY ( ext_kit_lot ) REFERENCES barcodes.lot( lot_id );
ALTER TABLE barcodes.plate ADD CONSTRAINT fk_plate_4 FOREIGN KEY ( protocol ) REFERENCES barcodes.protocol( protocol_id );
ALTER TABLE barcodes.plate ADD CONSTRAINT fk_plate_5 FOREIGN KEY ( person ) REFERENCES barcodes.person( person_id );
