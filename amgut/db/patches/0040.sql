-- Sep. 9, 2016
-- Add the first part of the "Plate Mapper" funtionality

-- Create new tables

CREATE SCHEMA pm;

CREATE TABLE pm.extraction_kit_lot (
	extraction_kit_lot_id bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_extraction_kit_lot PRIMARY KEY ( extraction_kit_lot_id ),
	CONSTRAINT uq_extraction_kit_lot_name UNIQUE ( name )
 );

CREATE TABLE pm.extraction_robot (
	extraction_robot_id  bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_extraction_robot PRIMARY KEY ( extraction_robot_id ),
	CONSTRAINT uq_extraction_robot_name UNIQUE ( name )
 );

CREATE TABLE pm.master_mix_lot (
	master_mix_lot_id    bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_master_mix_lot PRIMARY KEY ( master_mix_lot_id ),
	CONSTRAINT uq_master_mix_lot_name UNIQUE ( name )
 );

CREATE TABLE pm.plate_type (
	plate_type_id        bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	cols                 smallint  NOT NULL,
	rows                 smallint  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_plate_type PRIMARY KEY ( plate_type_id ),
	CONSTRAINT uq_plate_type_name UNIQUE ( name )
 );

CREATE TABLE pm.processing_robot (
	processing_robot_id  bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_processing_robot PRIMARY KEY ( processing_robot_id ),
	CONSTRAINT uq_processing_robot_name UNIQUE ( name )
 );

CREATE TABLE pm.run (
	run_id               bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	run_on               date  ,
	notes                varchar  ,
	CONSTRAINT pk_run PRIMARY KEY ( run_id ),
	CONSTRAINT uq_run_name UNIQUE ( name )
 );

CREATE TABLE pm.sample (
	sample_id            varchar  NOT NULL,
	is_blank             bool DEFAULT FALSE NOT NULL,
	barcode              varchar  ,
	notes                varchar  ,
	CONSTRAINT pk_sample PRIMARY KEY ( sample_id ),
	CONSTRAINT fk_sample_barcode FOREIGN KEY ( barcode ) REFERENCES barcodes.barcode( barcode )
 );
CREATE INDEX idx_sample_barcode ON pm.sample ( barcode );

CREATE TABLE pm.study (
	study_id             bigint  NOT NULL,
	title                varchar  ,
	alias                varchar  ,
	notes                varchar  ,
	CONSTRAINT pk_study PRIMARY KEY ( study_id ),
	CONSTRAINT uq_study_title UNIQUE ( title )
 );
COMMENT ON COLUMN pm.study.study_id IS 'positive if Qiita study ID, negative if others';

CREATE TABLE pm.study_sample (
	study_id             bigint  NOT NULL,
	sample_id            varchar  NOT NULL,
	CONSTRAINT fk_study_sample_study_id FOREIGN KEY ( study_id ) REFERENCES pm.study( study_id )    ,
	CONSTRAINT fk_study_sample_sample_id FOREIGN KEY ( sample_id ) REFERENCES pm.sample( sample_id )
 );
CREATE INDEX idx_study_sample_study_id ON pm.study_sample ( study_id );
CREATE INDEX idx_study_sample_sample_id ON pm.study_sample ( sample_id );

CREATE TABLE pm.template (
	template_id          bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	plate_type_id        bigint  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_template PRIMARY KEY ( template_id ),
	CONSTRAINT uq_template_name UNIQUE ( name ) ,
	CONSTRAINT fk_template_plate_type_id FOREIGN KEY ( plate_type_id ) REFERENCES pm.plate_type( plate_type_id )
 );
CREATE INDEX idx_template_plate_type_id ON pm.template ( plate_type_id );

CREATE TABLE pm.template_barcode_seq (
	template_id          bigint  NOT NULL,
	col                  smallint  NOT NULL,
	row                  smallint  NOT NULL,
	barcode_seq          varchar  ,
	CONSTRAINT fk_template_barcode_seq_template_id FOREIGN KEY ( template_id ) REFERENCES pm.template( template_id )
 );
CREATE INDEX idx_template_barcode_seq_template_id ON pm.template_barcode_seq ( template_id );

CREATE TABLE pm.tm1000_8_tool (
	tm1000_8_tool_id     bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_tm1000_8_tool PRIMARY KEY ( tm1000_8_tool_id ),
	CONSTRAINT uq_tm1000_8_tool_name UNIQUE ( name )
 );

CREATE TABLE pm.tm300_8_tool (
	tm300_8_tool_id      bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_tm300_8_tool PRIMARY KEY ( tm300_8_tool_id ),
	CONSTRAINT uq_tm300_8_tool_name UNIQUE ( name )
 );

CREATE TABLE pm.tm50_8_tool (
	tm50_8_tool_id       bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_tm50_8_tool PRIMARY KEY ( tm50_8_tool_id ),
	CONSTRAINT uq_tm50_8_tool_name UNIQUE ( name )
 );

CREATE TABLE pm.water_lot (
	water_lot_id         bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_water_lot PRIMARY KEY ( water_lot_id ),
	CONSTRAINT uq_water_lot_name UNIQUE ( name )
 );

CREATE TABLE pm.plate (
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
	tm300_8_tool_id      bigint  ,
	tm50_8_tool_id       bigint  ,
	notes                varchar  ,
	CONSTRAINT pk_plate PRIMARY KEY ( plate_id ),
	CONSTRAINT uq_plate_name UNIQUE ( name ) ,
	CONSTRAINT fk_plate_email FOREIGN KEY ( email ) REFERENCES ag.labadmin_users( email )    ,
	CONSTRAINT fk_plate_plate_type_id FOREIGN KEY ( plate_type_id ) REFERENCES pm.plate_type( plate_type_id )    ,
	CONSTRAINT fk_plate_template_id FOREIGN KEY ( template_id ) REFERENCES pm.template( template_id )    ,
	CONSTRAINT fk_plate_extraction_kit_lot_id FOREIGN KEY ( extraction_kit_lot_id ) REFERENCES pm.extraction_kit_lot( extraction_kit_lot_id )    ,
	CONSTRAINT fk_plate_extraction_robot_id FOREIGN KEY ( extraction_robot_id ) REFERENCES pm.extraction_robot( extraction_robot_id )    ,
	CONSTRAINT fk_plate_tm1000_8_tool_id FOREIGN KEY ( tm1000_8_tool_id ) REFERENCES pm.tm1000_8_tool( tm1000_8_tool_id )    ,
	CONSTRAINT fk_plate_master_mix_lot_id FOREIGN KEY ( master_mix_lot_id ) REFERENCES pm.master_mix_lot( master_mix_lot_id )    ,
	CONSTRAINT fk_plate_water_lot_id FOREIGN KEY ( water_lot_id ) REFERENCES pm.water_lot( water_lot_id )    ,
	CONSTRAINT fk_plate_processing_robot_id FOREIGN KEY ( processing_robot_id ) REFERENCES pm.processing_robot( processing_robot_id )    ,
	CONSTRAINT fk_plate_tm300_8_tool_id FOREIGN KEY ( tm300_8_tool_id ) REFERENCES pm.tm300_8_tool( tm300_8_tool_id )    ,
	CONSTRAINT fk_plate_tm50_8_tool_id FOREIGN KEY ( tm50_8_tool_id ) REFERENCES pm.tm50_8_tool( tm50_8_tool_id )
 );
CREATE INDEX idx_plate_email ON pm.plate ( email );
CREATE INDEX idx_plate_plate_type_id ON pm.plate ( plate_type_id );
CREATE INDEX idx_plate_template_id ON pm.plate ( template_id );
CREATE INDEX idx_plate_extraction_kit_lot_id ON pm.plate ( extraction_kit_lot_id );
CREATE INDEX idx_plate_extraction_robot_id ON pm.plate ( extraction_robot_id );
CREATE INDEX idx_plate_tm1000_8_tool_id ON pm.plate ( tm1000_8_tool_id );
CREATE INDEX idx_plate_master_mix_lot_id ON pm.plate ( master_mix_lot_id );
CREATE INDEX idx_plate_water_lot_id ON pm.plate ( water_lot_id );
CREATE INDEX idx_plate_processing_robot_id ON pm.plate ( processing_robot_id );
CREATE INDEX idx_plate_tm300_8_tool_id ON pm.plate ( tm300_8_tool_id );
CREATE INDEX idx_plate_tm50_8_tool_id ON pm.plate ( tm50_8_tool_id );

CREATE TABLE pm.plate_sample (
	plate_id             bigint  NOT NULL,
	col                  smallint  NOT NULL,
	row                  smallint  NOT NULL,
	sample_id            varchar  NOT NULL,
	CONSTRAINT fk_plate_sample_plate_id FOREIGN KEY ( plate_id ) REFERENCES pm.plate( plate_id )    ,
	CONSTRAINT fk_plate_sample_sample_id FOREIGN KEY ( sample_id ) REFERENCES pm.sample( sample_id )
 );
CREATE INDEX idx_plate_sample_plate_id ON pm.plate_sample ( plate_id );
CREATE INDEX idx_plate_sample_sample_id ON pm.plate_sample ( sample_id );

CREATE TABLE pm.run_plate (
	run_id               bigint  NOT NULL,
	plate_id             bigint  NOT NULL,
	CONSTRAINT fk_run_plate_run_id FOREIGN KEY ( run_id ) REFERENCES pm.run( run_id )    ,
	CONSTRAINT fk_run_plate_plate_id FOREIGN KEY ( plate_id ) REFERENCES pm.plate( plate_id )
 );
CREATE INDEX idx_run_plate_run_id ON pm.run_plate ( run_id );
CREATE INDEX idx_run_plate_plate_id ON pm.run_plate ( plate_id );

-- Populate table fields with pre-defined options

INSERT INTO pm.plate_type (name, cols, rows, notes) VALUES ('96-well', 12, 8, 'Standard 96-well plate');

INSERT INTO pm.extraction_robot (name) VALUES ('HOWE_KF1');
INSERT INTO pm.extraction_robot (name) VALUES ('HOWE_KF2');
INSERT INTO pm.extraction_robot (name) VALUES ('HOWE_KF3');
INSERT INTO pm.extraction_robot (name) VALUES ('HOWE_KF4');

INSERT INTO pm.tm1000_8_tool (name) VALUES ('108379Z');

INSERT INTO pm.processing_robot (name) VALUES ('ROBE');
INSERT INTO pm.processing_robot (name) VALUES ('RIKE');
INSERT INTO pm.processing_robot (name) VALUES ('JERE');
INSERT INTO pm.processing_robot (name) VALUES ('CARMEN');

INSERT INTO pm.tm300_8_tool (name) VALUES ('208484Z');
INSERT INTO pm.tm300_8_tool (name) VALUES ('311318B');
INSERT INTO pm.tm300_8_tool (name) VALUES ('109375A');
INSERT INTO pm.tm300_8_tool (name) VALUES ('3076189');

INSERT INTO pm.tm50_8_tool (name) VALUES ('108364Z');
INSERT INTO pm.tm50_8_tool (name) VALUES ('311426B');
INSERT INTO pm.tm50_8_tool (name) VALUES ('311441B');
INSERT INTO pm.tm50_8_tool (name) VALUES ('409172Z');
