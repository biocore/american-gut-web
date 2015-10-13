-- October 12, 2015
-- Add tables needed to track plate maps and create prep templates
--Need to wipe out old, bad data in the plate table
DROP TABLE barcodes.plate_barcode CASCADE;
DROP TABLE barcodes.plate;

ALTER TABLE barcodes.barcode ALTER COLUMN barcode TYPE varchar;
ALTER TABLE barcodes.project ADD description varchar  NOT NULL DEFAULT '';

CREATE TABLE barcodes.person ( 
	person_id            bigint  NOT NULL,
	name                 varchar(100)  NOT NULL,
	email                varchar  NOT NULL,
	date_added           date DEFAULT current_date NOT NULL,
	CONSTRAINT pk_person PRIMARY KEY ( person_id )
 );

CREATE TABLE barcodes.robot ( 
	robot_name           varchar(100)  NOT NULL,
	robot_type           varchar  NOT NULL,
	date_added           date DEFAULT current_date NOT NULL,
	CONSTRAINT pk_robot PRIMARY KEY ( robot_name )
 );

CREATE TABLE barcodes.sequencer ( 
	sequencer_id         bigserial  NOT NULL,
	platform             varchar  NOT NULL,
	instrument_model     varchar  NOT NULL,
	sequencing_method    varchar  NOT NULL,
	CONSTRAINT pk_sequencer PRIMARY KEY ( sequencer_id )
 );
COMMENT ON TABLE barcodes.sequencer IS 'Short name appened to protocol name';

CREATE TABLE barcodes.protocol ( 
	protocol             varchar(100)  NOT NULL,
	template_dna         integer  NOT NULL,
	target_gene          varchar  NOT NULL,
	target_subfragment   varchar  NOT NULL,
	linker               varchar  NOT NULL,
	pcr_primers          varchar  NOT NULL,
	CONSTRAINT pk_protocol PRIMARY KEY ( protocol )
 );
COMMENT ON COLUMN barcodes.protocol.protocol IS 'Name of the protocol';
COMMENT ON COLUMN barcodes.protocol.template_dna IS 'Template DNA added, in uL';

CREATE TABLE barcodes.run_information ( 
	run_id               bigserial  NOT NULL,
	nickname             varchar(100)  NOT NULL,
	run_prefix           varchar  NOT NULL,
	sequencer_id         bigint  NOT NULL,
	created_on           timestamp DEFAULT current_timestamp NOT NULL,
	run_date             date  ,
	finalized            bool DEFAULT 'F' NOT NULL,
	CONSTRAINT pk_run_information PRIMARY KEY ( run_id )
 );
CREATE INDEX idx_run_information ON barcodes.run_information ( sequencer_id );
ALTER TABLE barcodes.run_information ADD CONSTRAINT fk_run_information FOREIGN KEY ( sequencer_id ) REFERENCES barcodes.sequencer( sequencer_id );

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
	ext_robot_tool       varchar  NOT NULL,
	kf_robot             varchar  NOT NULL,
	ext_kit_lot          varchar  NOT NULL,
	person               bigint  NOT NULL,
	finalized            bool DEFAULT 'F' NOT NULL,
	ext_created          timestamp DEFAULT current_date NOT NULL,
	ext_finalized        timestamp  ,
	CONSTRAINT plate_pkey PRIMARY KEY ( barcode )
 );
CREATE INDEX idx_plate_0 ON barcodes.extraction_plate ( ext_robot );
CREATE INDEX idx_plate_1 ON barcodes.extraction_plate ( kf_robot );
CREATE INDEX idx_plate_2 ON barcodes.extraction_plate ( ext_kit_lot );
CREATE INDEX idx_plate_4 ON barcodes.extraction_plate ( person );
COMMENT ON COLUMN barcodes.extraction_plate.ext_robot IS 'Extraction robot used for this plate';
COMMENT ON COLUMN barcodes.extraction_plate.ext_robot_tool IS 'Extraction robot pipette head used';
COMMENT ON COLUMN barcodes.extraction_plate.kf_robot IS 'kingifsher robot used for extracton';
COMMENT ON COLUMN barcodes.extraction_plate.ext_kit_lot IS 'Extraction kit lot number';
COMMENT ON COLUMN barcodes.extraction_plate.person IS 'Person running the extraction';
COMMENT ON COLUMN barcodes.extraction_plate.finalized IS 'Whether the plate map is complete or still being filled.';
ALTER TABLE barcodes.extraction_plate ADD CONSTRAINT fk_plate FOREIGN KEY ( barcode ) REFERENCES barcodes.barcode( barcode );
ALTER TABLE barcodes.extraction_plate ADD CONSTRAINT fk_plate_5 FOREIGN KEY ( person ) REFERENCES barcodes.person( person_id );
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
	tool_300_8           bigint  NOT NULL,
	tool_50_8            bigint  NOT NULL,
	person               bigint  NOT NULL,
	pcr_created          timestamp DEFAULT current_timestamp NOT NULL,
	CONSTRAINT pkey_pcr_plate PRIMARY KEY ( barcode, nickname ),
	CONSTRAINT idx_pcr_plate UNIQUE ( barcode ) ,
	CONSTRAINT pk_pcr_plate UNIQUE ( nickname ) 
 );
CREATE INDEX idx_pcr_plate_0 ON barcodes.pcr_plate ( pcr_robot );
CREATE INDEX idx_pcr_plate_1 ON barcodes.pcr_plate ( primer_plate_lot );
CREATE INDEX idx_pcr_plate_2 ON barcodes.pcr_plate ( master_mix_lot );
CREATE INDEX idx_pcr_plate_3 ON barcodes.pcr_plate ( water_lot );
CREATE INDEX idx_pcr_plate_5 ON barcodes.pcr_plate ( person );
COMMENT ON COLUMN barcodes.pcr_plate.tool_300_8 IS '300uL pipette head used';
COMMENT ON COLUMN barcodes.pcr_plate.tool_50_8 IS '50uL pipette head used';
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate FOREIGN KEY ( barcode ) REFERENCES barcodes.extraction_plate( barcode );
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate_5 FOREIGN KEY ( person ) REFERENCES barcodes.person( person_id );
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate_0 FOREIGN KEY ( primer_plate_lot ) REFERENCES barcodes.primer_plate_lot( primer_plate_lot );
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate_1 FOREIGN KEY ( master_mix_lot ) REFERENCES barcodes.master_mix_lot( master_mix_lot );
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate_2 FOREIGN KEY ( water_lot ) REFERENCES barcodes.water_lot( water_lot );
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate_3 FOREIGN KEY ( pcr_robot ) REFERENCES barcodes.robot( robot_name );

CREATE TABLE barcodes.pcr_plate_run ( 
	run_id               bigint  NOT NULL,
	barcode              varchar  NOT NULL,
	nickname             varchar(100)  NOT NULL,
	center_project_name  varchar(100)  ,
	CONSTRAINT pk_pcr_plate_run PRIMARY KEY ( run_id, barcode, nickname )
 );
CREATE INDEX idx_pcr_plate_run ON barcodes.pcr_plate_run ( run_id );
CREATE INDEX idx_pcr_plate_run_0 ON barcodes.pcr_plate_run ( barcode );
CREATE INDEX idx_pcr_plate_run_1 ON barcodes.pcr_plate_run ( nickname );
ALTER TABLE barcodes.pcr_plate_run ADD CONSTRAINT fk_pcr_plate_run FOREIGN KEY ( run_id ) REFERENCES barcodes.run_information( run_id );
ALTER TABLE barcodes.pcr_plate_run ADD CONSTRAINT fk_pcr_plate_run_0 FOREIGN KEY ( barcode ) REFERENCES barcodes.pcr_plate( barcode );
ALTER TABLE barcodes.pcr_plate_run ADD CONSTRAINT fk_pcr_plate_run_1 FOREIGN KEY ( nickname ) REFERENCES barcodes.pcr_plate( nickname );

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
