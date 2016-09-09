-- Sep. 9, 2016
-- Add the first part of the "Plate Mapper" funtionality

-- Create new tables

CREATE TABLE ag.extraction_kit_lot (
	extraction_kit_lot_id bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_extraction_kit_lot PRIMARY KEY ( extraction_kit_lot_id ),
	CONSTRAINT uq_extraction_kit_lot_name UNIQUE ( name )
 );

CREATE TABLE ag.extraction_robot (
	extraction_robot_id  bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_extraction_robot PRIMARY KEY ( extraction_robot_id ),
	CONSTRAINT uq_extraction_robot_name UNIQUE ( name )
 );

CREATE TABLE ag.master_mix_lot (
	master_mix_lot_id    bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_master_mix_lot PRIMARY KEY ( master_mix_lot_id ),
	CONSTRAINT uq_master_mix_lot_name UNIQUE ( name )
 );

CREATE TABLE ag.plate_type (
	plate_type_id        bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	cols                 smallint  NOT NULL,
	rows                 smallint  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_plate_type PRIMARY KEY ( plate_type_id ),
	CONSTRAINT uq_plate_type_name UNIQUE ( name )
 );

CREATE TABLE ag.processing_robot (
	processing_robot_id  bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_processing_robot PRIMARY KEY ( processing_robot_id ),
	CONSTRAINT uq_processing_robot_name UNIQUE ( name )
 );

CREATE TABLE ag.run (
	run_id               bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	"date"               date  ,
	notes                varchar  ,
	CONSTRAINT pk_run PRIMARY KEY ( run_id ),
	CONSTRAINT uq_run_name UNIQUE ( name )
 );

CREATE TABLE ag.sample (
	sample_id            varchar  NOT NULL,
	is_blank             bool DEFAULT 'F' NOT NULL,
	barcode              varchar  ,
	notes                varchar  ,
	CONSTRAINT pk_sample PRIMARY KEY ( sample_id ),
	CONSTRAINT fk_sample_barcode FOREIGN KEY ( barcode ) REFERENCES barcodes.barcode( barcode )
 );

CREATE INDEX idx_sample_barcode ON ag.sample ( barcode );

CREATE TABLE ag.study (
	study_id             bigint  NOT NULL,
	title                varchar  ,
	alias                varchar  ,
	notes                varchar  ,
	CONSTRAINT pk_study PRIMARY KEY ( study_id ),
	CONSTRAINT uq_study_title UNIQUE ( title )
 );
COMMENT ON COLUMN ag.study.study_id IS 'positive if Qiita study ID, negative if others';

CREATE TABLE ag.study_sample (
	study_id             bigint  NOT NULL,
	sample_id            varchar  NOT NULL,
	CONSTRAINT fk_study_sample_study_id FOREIGN KEY ( study_id ) REFERENCES ag.study( study_id )    ,
	CONSTRAINT fk_study_sample_sample_id FOREIGN KEY ( sample_id ) REFERENCES ag.sample( sample_id )
 );
CREATE INDEX idx_study_sample_study_id ON ag.study_sample ( study_id );
CREATE INDEX idx_study_sample_sample_id ON ag.study_sample ( sample_id );

CREATE TABLE ag.template (
	template_id          bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	plate_type_id        bigint  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_plate_template PRIMARY KEY ( template_id ),
	CONSTRAINT uq_template_name UNIQUE ( name ) ,
	CONSTRAINT fk_plate_template_plate_type FOREIGN KEY ( plate_type_id ) REFERENCES ag.plate_type( plate_type_id )
 );
CREATE INDEX idx_plate_template ON ag.template ( plate_type_id );

CREATE TABLE ag.template_barcode_seq (
	template_id          bigint  NOT NULL,
	col                  smallint  NOT NULL,
	row                  smallint  NOT NULL,
	barcode_seq          varchar  ,
	CONSTRAINT fk_plate_temp_barseq FOREIGN KEY ( template_id ) REFERENCES ag.template( template_id )
 );
CREATE INDEX idx_template_barcode_seq_template_id ON ag.template_barcode_seq ( template_id );

CREATE TABLE ag.tm1000_8_tool (
	tm1000_8_tool_id     bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_tm1000_8_tool PRIMARY KEY ( tm1000_8_tool_id ),
	CONSTRAINT uq_tm1000_8_tool_name UNIQUE ( name )
 );

CREATE TABLE ag.tm300_8_tool (
	tm300_8_tool_id      bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_tm300_8_tool PRIMARY KEY ( tm300_8_tool_id ),
	CONSTRAINT uq_tm300_8_tool UNIQUE ( name )
 );

CREATE TABLE ag.tm50_8_tool (
	tm50_8_tool_id       bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_tm50_8_tool PRIMARY KEY ( tm50_8_tool_id ),
	CONSTRAINT uq_tm50_8_tool_name UNIQUE ( name )
 );

CREATE TABLE ag.water_lot (
	water_lot_id         bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_water_lot PRIMARY KEY ( water_lot_id ),
	CONSTRAINT uq_water_lot_name UNIQUE ( name )
 );

CREATE TABLE ag.plate (
	plate_id             bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	email                varchar  NOT NULL,
	plate_type_id        bigint  NOT NULL,
	template_id          bigint  ,
	linker_seq           varchar  ,
	extraction_kit_lot_id bigint  ,
	extraction_robot_id  bigint  ,
	tm1000_8_tool_id     bigint  ,
	master_mix_lot_id    bigint  ,
	water_lot_id         bigint  ,
	processing_robot_id  bigint  ,
	tm300_8_tool_id      bigint  NOT NULL,
	tm50_8_tool_id       bigint  ,
	notes                varchar  ,
	CONSTRAINT pk_plate PRIMARY KEY ( plate_id ),
	CONSTRAINT uq_plate_name UNIQUE ( name ) ,
	CONSTRAINT fk_plate_plate_type FOREIGN KEY ( plate_type_id ) REFERENCES ag.plate_type( plate_type_id )    ,
	CONSTRAINT fk_plate_template FOREIGN KEY ( template_id ) REFERENCES ag.template( template_id )    ,
	CONSTRAINT fk_plate_labadmin_users FOREIGN KEY ( email ) REFERENCES ag.labadmin_users( email )    ,
	CONSTRAINT fk_plate_extraction_kit_lot FOREIGN KEY ( extraction_kit_lot_id ) REFERENCES ag.extraction_kit_lot( extraction_kit_lot_id )    ,
	CONSTRAINT fk_plate_extraction_robot FOREIGN KEY ( extraction_robot_id ) REFERENCES ag.extraction_robot( extraction_robot_id )    ,
	CONSTRAINT fk_plate_tm1000_8_tool FOREIGN KEY ( tm1000_8_tool_id ) REFERENCES ag.tm1000_8_tool( tm1000_8_tool_id )    ,
	CONSTRAINT fk_plate_master_mix_lot FOREIGN KEY ( master_mix_lot_id ) REFERENCES ag.master_mix_lot( master_mix_lot_id )    ,
	CONSTRAINT fk_plate_water_lot FOREIGN KEY ( water_lot_id ) REFERENCES ag.water_lot( water_lot_id )    ,
	CONSTRAINT fk_plate_processing_robot FOREIGN KEY ( processing_robot_id ) REFERENCES ag.processing_robot( processing_robot_id )    ,
	CONSTRAINT fk_plate_tm300_8_tool FOREIGN KEY ( tm300_8_tool_id ) REFERENCES ag.tm300_8_tool( tm300_8_tool_id )    ,
	CONSTRAINT fk_plate_tm50_8_tool FOREIGN KEY ( tm50_8_tool_id ) REFERENCES ag.tm50_8_tool( tm50_8_tool_id )
 );
CREATE INDEX idx_plate_plate_type_id ON ag.plate ( plate_type_id );
CREATE INDEX idx_plate_template_id ON ag.plate ( template_id );
CREATE INDEX idx_plate_tm300_8_tool_id ON ag.plate ( tm300_8_tool_id );
CREATE INDEX idx_plate_email ON ag.plate ( email );
CREATE INDEX idx_plate_extraction_kit_lot_id ON ag.plate ( extraction_kit_lot_id );
CREATE INDEX idx_plate_extraction_robot_id ON ag.plate ( extraction_robot_id );
CREATE INDEX idx_plate_tm1000_8_tool_id ON ag.plate ( tm1000_8_tool_id );
CREATE INDEX idx_plate_master_mix_lot_id ON ag.plate ( master_mix_lot_id );
CREATE INDEX idx_plate_water_lot_id ON ag.plate ( water_lot_id );
CREATE INDEX idx_plate_processing_robot_id ON ag.plate ( processing_robot_id );
CREATE INDEX idx_plate_tm50_8_tool_id ON ag.plate ( tm50_8_tool_id );

CREATE TABLE ag.plate_sample (
	plate_id             bigint  NOT NULL,
	col                  smallint  NOT NULL,
	row                  smallint  NOT NULL,
	sample_id            varchar  NOT NULL,
	CONSTRAINT fk_plate_sample_plate_id FOREIGN KEY ( plate_id ) REFERENCES ag.plate( plate_id )    ,
	CONSTRAINT fk_plate_sample_sample_id FOREIGN KEY ( sample_id ) REFERENCES ag.sample( sample_id )
 );
CREATE INDEX idx_plate_sample_plate_id ON ag.plate_sample ( plate_id );
CREATE INDEX idx_plate_sample_sample_id ON ag.plate_sample ( sample_id );

CREATE TABLE ag.run_plate (
	run_id               bigint  NOT NULL,
	plate_id             bigint  NOT NULL,
	CONSTRAINT fk_run_plate_run_id FOREIGN KEY ( run_id ) REFERENCES ag.run( run_id )    ,
	CONSTRAINT fk_run_plate_plate_id FOREIGN KEY ( plate_id ) REFERENCES ag.plate( plate_id )
 );
CREATE INDEX idx_run_plate_run_id ON ag.run_plate ( run_id );
CREATE INDEX idx_run_plate_plate_id ON ag.run_plate ( plate_id );

-- Populate table fields with pre-defined options

INSERT INTO ag.plate_type (name, cols, rows, notes) VALUES ('96-well', 12, 8, 'Standard 96-well plate');

INSERT INTO ag.extraction_robot (name) VALUES ('HOWE_KF1');
INSERT INTO ag.extraction_robot (name) VALUES ('HOWE_KF2');
INSERT INTO ag.extraction_robot (name) VALUES ('HOWE_KF3');
INSERT INTO ag.extraction_robot (name) VALUES ('HOWE_KF4');

INSERT INTO ag.tm1000_8_tool (name) VALUES ('108379Z');

INSERT INTO ag.processing_robot (name) VALUES ('ROBE');
INSERT INTO ag.processing_robot (name) VALUES ('RIKE');
INSERT INTO ag.processing_robot (name) VALUES ('JERE');
INSERT INTO ag.processing_robot (name) VALUES ('CARMEN');

INSERT INTO ag.tm300_8_tool (name) VALUES ('208484Z');
INSERT INTO ag.tm300_8_tool (name) VALUES ('311318B');
INSERT INTO ag.tm300_8_tool (name) VALUES ('109375A');
INSERT INTO ag.tm300_8_tool (name) VALUES ('3076189');

INSERT INTO ag.tm50_8_tool (name) VALUES ('108364Z');
INSERT INTO ag.tm50_8_tool (name) VALUES ('311426B');
INSERT INTO ag.tm50_8_tool (name) VALUES ('311441B');
INSERT INTO ag.tm50_8_tool (name) VALUES ('409172Z');
