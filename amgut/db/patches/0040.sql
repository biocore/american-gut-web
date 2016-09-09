-- Sep. 9, 2016
-- Plate Mapper test 01

SET search_path TO ag;

-- Create new tables

CREATE TABLE extraction_kit_lot (
	extraction_kit_lot_id bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	description          varchar  ,
	CONSTRAINT pk_extraction_kit_lot PRIMARY KEY ( extraction_kit_lot_id ),
	CONSTRAINT uq_extraction_kit_lot_name UNIQUE ( name )
 );

CREATE TABLE extraction_robot (
	extraction_robot_id  bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	description          varchar  ,
	CONSTRAINT pk_extraction_robot PRIMARY KEY ( extraction_robot_id ),
	CONSTRAINT uq_extraction_robot_name UNIQUE ( name )
 );

CREATE TABLE master_mix_lot (
	master_mix_lot_id    bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	description          varchar  ,
	CONSTRAINT pk_master_mix_lot PRIMARY KEY ( master_mix_lot_id ),
	CONSTRAINT uq_master_mix_lot_name UNIQUE ( name )
 );

CREATE TABLE plate_type (
	plate_type_id        bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	cols                 smallint  NOT NULL,
	rows                 smallint  NOT NULL,
	description          varchar  ,
	CONSTRAINT pk_plate_type PRIMARY KEY ( plate_type_id ),
	CONSTRAINT uq_plate_type_name UNIQUE ( name )
 );

CREATE TABLE processing_robot (
	processing_robot_id  bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	description          varchar  ,
	CONSTRAINT pk_processing_robot PRIMARY KEY ( processing_robot_id ),
	CONSTRAINT uq_processing_robot_name UNIQUE ( name )
 );

CREATE TABLE run (
	run_id               bigserial  NOT NULL,
	run_date             date  ,
	description          varchar  ,
	CONSTRAINT pk_run PRIMARY KEY ( run_id )
 );

CREATE TABLE sample (
	sample_id            varchar  NOT NULL,
	barcode              varchar  ,
	description          varchar  ,
	CONSTRAINT pk_sample PRIMARY KEY ( sample_id ),
	CONSTRAINT fk_sample_barcode FOREIGN KEY ( barcode ) REFERENCES barcodes.barcode( barcode )
 );
CREATE INDEX idx_sample_barcode ON sample ( barcode );

CREATE TABLE study (
	study_id             bigint  NOT NULL,
	description          varchar  ,
	CONSTRAINT pk_study PRIMARY KEY ( study_id )
 );
COMMENT ON COLUMN study.study_id IS 'positive if Qiita study ID, negative if others';

CREATE TABLE study_sample (
	study_id             bigint  NOT NULL,
	sample_id            varchar  NOT NULL,
	CONSTRAINT fk_study_sample_study_id FOREIGN KEY ( study_id ) REFERENCES study( study_id )    ,
	CONSTRAINT fk_study_sample_sample_id FOREIGN KEY ( sample_id ) REFERENCES sample( sample_id )
 );
CREATE INDEX idx_study_sample_study_id ON study_sample ( study_id );
CREATE INDEX idx_study_sample_sample_id ON study_sample ( sample_id );

CREATE TABLE template (
	template_id          bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	plate_type_id        bigint  NOT NULL,
	description          varchar  ,
	CONSTRAINT pk_plate_template PRIMARY KEY ( template_id ),
	CONSTRAINT uq_template_name UNIQUE ( name ) ,
	CONSTRAINT fk_plate_template_plate_type FOREIGN KEY ( plate_type_id ) REFERENCES plate_type( plate_type_id )
 );
CREATE INDEX idx_plate_template ON template ( plate_type_id );

CREATE TABLE template_barcode_sequence (
	template_id          bigint  NOT NULL,
	col                  smallint  NOT NULL,
	row                  smallint  NOT NULL,
	barcode_sequence     varchar  ,
	CONSTRAINT fk_plate_temp_barseq FOREIGN KEY ( template_id ) REFERENCES template( template_id )
 );
CREATE INDEX idx_plate_temp_barseq ON template_barcode_sequence ( template_id );

CREATE TABLE tm1000_8_tool (
	tm1000_8_tool_id     bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	description          varchar  ,
	CONSTRAINT pk_tm1000_8_tool PRIMARY KEY ( tm1000_8_tool_id ),
	CONSTRAINT uq_tm1000_8_tool_name UNIQUE ( name )
 );

CREATE TABLE tm300_8_tool (
	tm300_8_tool_id      bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	description          varchar  ,
	CONSTRAINT pk_tm300_8_tool PRIMARY KEY ( tm300_8_tool_id ),
	CONSTRAINT uq_tm300_8_tool UNIQUE ( name )
 );

CREATE TABLE tm50_8_tool (
	tm50_8_tool_id       bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	description          varchar  ,
	CONSTRAINT pk_tm50_8_tool PRIMARY KEY ( tm50_8_tool_id ),
	CONSTRAINT uq_tm50_8_tool_name UNIQUE ( name )
 );

CREATE TABLE water_lot (
	water_lot_id         bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	description          varchar  ,
	CONSTRAINT pk_water_lot PRIMARY KEY ( water_lot_id ),
	CONSTRAINT uq_water_lot_name UNIQUE ( name )
 );

CREATE TABLE plate (
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
	description          varchar  ,
	CONSTRAINT pk_plate PRIMARY KEY ( plate_id ),
	CONSTRAINT uq_plate_name UNIQUE ( name ) ,
	CONSTRAINT fk_plate_plate_type FOREIGN KEY ( plate_type_id ) REFERENCES plate_type( plate_type_id )    ,
	CONSTRAINT fk_plate_template FOREIGN KEY ( template_id ) REFERENCES template( template_id )    ,
	CONSTRAINT fk_plate_labadmin_users FOREIGN KEY ( email ) REFERENCES labadmin_users( email )    ,
	CONSTRAINT fk_plate_extraction_kit_lot FOREIGN KEY ( extraction_kit_lot_id ) REFERENCES extraction_kit_lot( extraction_kit_lot_id )    ,
	CONSTRAINT fk_plate_extraction_robot FOREIGN KEY ( extraction_robot_id ) REFERENCES extraction_robot( extraction_robot_id )    ,
	CONSTRAINT fk_plate_tm1000_8_tool FOREIGN KEY ( tm1000_8_tool_id ) REFERENCES tm1000_8_tool( tm1000_8_tool_id )    ,
	CONSTRAINT fk_plate_master_mix_lot FOREIGN KEY ( master_mix_lot_id ) REFERENCES master_mix_lot( master_mix_lot_id )    ,
	CONSTRAINT fk_plate_water_lot FOREIGN KEY ( water_lot_id ) REFERENCES water_lot( water_lot_id )    ,
	CONSTRAINT fk_plate_processing_robot FOREIGN KEY ( processing_robot_id ) REFERENCES processing_robot( processing_robot_id )    ,
	CONSTRAINT fk_plate_tm300_8_tool FOREIGN KEY ( tm300_8_tool_id ) REFERENCES tm300_8_tool( tm300_8_tool_id )    ,
	CONSTRAINT fk_plate_tm50_8_tool FOREIGN KEY ( tm50_8_tool_id ) REFERENCES tm50_8_tool( tm50_8_tool_id )
 );
CREATE INDEX idx_plate_plate_type_id ON plate ( plate_type_id );
CREATE INDEX idx_plate_template_id ON plate ( template_id );
CREATE INDEX idx_plate_tm300_8_tool_id ON plate ( tm300_8_tool_id );
CREATE INDEX idx_plate_email ON plate ( email );
CREATE INDEX idx_plate_extraction_kit_lot_id ON plate ( extraction_kit_lot_id );
CREATE INDEX idx_plate_extraction_robot_id ON plate ( extraction_robot_id );
CREATE INDEX idx_plate_tm1000_8_tool_id ON plate ( tm1000_8_tool_id );
CREATE INDEX idx_plate_master_mix_lot_id ON plate ( master_mix_lot_id );
CREATE INDEX idx_plate_water_lot_id ON plate ( water_lot_id );
CREATE INDEX idx_plate_processing_robot_id ON plate ( processing_robot_id );
CREATE INDEX idx_plate_tm50_8_tool_id ON plate ( tm50_8_tool_id );

CREATE TABLE plate_sample (
	plate_id             bigint  NOT NULL,
	col                  smallint  NOT NULL,
	row                  smallint  NOT NULL,
	sample_id            varchar  NOT NULL,
	CONSTRAINT fk_plate_sample_plate_id FOREIGN KEY ( plate_id ) REFERENCES plate( plate_id )    ,
	CONSTRAINT fk_plate_sample_sample_id FOREIGN KEY ( sample_id ) REFERENCES sample( sample_id )
 );
CREATE INDEX idx_plate_sample_plate_id ON plate_sample ( plate_id );
CREATE INDEX idx_plate_sample_sample_id ON plate_sample ( sample_id );

CREATE TABLE run_plate (
	run_id               bigint  NOT NULL,
	plate_id             bigint  NOT NULL,
	CONSTRAINT fk_run_plate_run_id FOREIGN KEY ( run_id ) REFERENCES run( run_id )    ,
	CONSTRAINT fk_run_plate_plate_id FOREIGN KEY ( plate_id ) REFERENCES plate( plate_id )
 );
CREATE INDEX idx_run_plate_run_id ON run_plate ( run_id );
CREATE INDEX idx_run_plate_plate_id ON run_plate ( plate_id );

-- Populate table fields with pre-defined options

INSERT INTO plate_type (name, cols, rows, description) VALUES ('96-well', 12, 8, 'standard 96-well plate');

INSERT INTO extraction_robot (name) VALUES ('HOWE_KF1');
INSERT INTO extraction_robot (name) VALUES ('HOWE_KF2');
INSERT INTO extraction_robot (name) VALUES ('HOWE_KF3');
INSERT INTO extraction_robot (name) VALUES ('HOWE_KF4');

INSERT INTO tm1000_8_tool (name) VALUES ('108379Z');

INSERT INTO processing_robot (name) VALUES ('ROBE');
INSERT INTO processing_robot (name) VALUES ('RIKE');
INSERT INTO processing_robot (name) VALUES ('JERE');
INSERT INTO processing_robot (name) VALUES ('CARMEN');

INSERT INTO tm300_8_tool (name) VALUES ('208484Z');
INSERT INTO tm300_8_tool (name) VALUES ('311318B');
INSERT INTO tm300_8_tool (name) VALUES ('109375A');
INSERT INTO tm300_8_tool (name) VALUES ('3076189');

INSERT INTO tm50_8_tool (name) VALUES ('108364Z');
INSERT INTO tm50_8_tool (name) VALUES ('311426B');
INSERT INTO tm50_8_tool (name) VALUES ('311441B');
INSERT INTO tm50_8_tool (name) VALUES ('409172Z');
