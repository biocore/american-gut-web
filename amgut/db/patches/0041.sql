-- March 31, 2017
-- Plate Mapper

-- Create tables

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

CREATE TABLE pm.extraction_tool (
	extraction_tool_id   bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_extraction_tool PRIMARY KEY ( extraction_tool_id ),
	CONSTRAINT uq_extraction_tool_name UNIQUE ( name )
 );
COMMENT ON TABLE pm.extraction_tool IS 'TM1000-8 tools';

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

CREATE TABLE pm.protocol (
	protocol_id          bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	CONSTRAINT pk_protocol PRIMARY KEY ( protocol_id ),
	CONSTRAINT uq_protocol_name UNIQUE ( name )
 );

CREATE TABLE pm.run (
	run_id               bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	email                varchar  ,
	created_on           timestamp  ,
	notes                varchar  ,
	CONSTRAINT pk_run PRIMARY KEY ( run_id ),
	CONSTRAINT uq_run_name UNIQUE ( name ) ,
	CONSTRAINT fk_run_labadmin_users FOREIGN KEY ( email ) REFERENCES ag.labadmin_users( email )
 );
CREATE INDEX idx_run_email ON pm.run ( email );

CREATE TABLE pm.sample (
	sample_id            varchar  NOT NULL,
	is_blank             bool DEFAULT FALSE NOT NULL,
	barcode              varchar  ,
	notes                varchar  ,
	CONSTRAINT pk_sample PRIMARY KEY ( sample_id ),
	CONSTRAINT fk_sample_barcode FOREIGN KEY ( barcode ) REFERENCES barcodes.barcode( barcode )
 );
CREATE INDEX idx_sample_barcode ON pm.sample ( barcode );

CREATE TABLE pm.sample_plate (
	sample_plate_id      bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	email                varchar  ,
	created_on           timestamp  ,
	plate_type_id        bigint  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_sample_plate PRIMARY KEY ( sample_plate_id ),
	CONSTRAINT uq_sample_plate_name UNIQUE ( name ) ,
	CONSTRAINT fk_sample_plate_labadmin_users FOREIGN KEY ( email ) REFERENCES ag.labadmin_users( email )    ,
	CONSTRAINT fk_sample_plate_plate_type FOREIGN KEY ( plate_type_id ) REFERENCES pm.plate_type( plate_type_id )
 );
CREATE INDEX idx_sample_plate_email ON pm.sample_plate ( email );
CREATE INDEX idx_sample_plate_plate_type_id ON pm.sample_plate ( plate_type_id );
COMMENT ON TABLE pm.sample_plate IS 'Holds the information about the initial plate that the wet lab creates.';

CREATE TABLE pm.sample_plate_layout (
	sample_plate_id      bigint  NOT NULL,
	sample_id            varchar  NOT NULL,
	col                  smallint  NOT NULL,
	row                  smallint  NOT NULL,
	name                 varchar  ,
	notes                varchar  ,
	CONSTRAINT fk_plate_map_sample_plate FOREIGN KEY ( sample_plate_id ) REFERENCES pm.sample_plate( sample_plate_id )    ,
	CONSTRAINT fk_plate_map_sample FOREIGN KEY ( sample_id ) REFERENCES pm.sample( sample_id )
 );
CREATE INDEX idx_sample_plate_layout_sample_plate_id ON pm.sample_plate_layout ( sample_plate_id );
CREATE INDEX idx_sample_plate_layout_sample_id ON pm.sample_plate_layout ( sample_id );
COMMENT ON COLUMN pm.sample_plate_layout.name IS 'The name of the sample in this plate in case that needs to be changed (e.g. if the sample has been plated twice)';

CREATE TABLE pm.study (
	study_id             bigint   NOT NULL,
	title                varchar  NOT NULL,
	alias                varchar  NOT NULL,
    jira_key			 varchar  NOT NULL,
	CONSTRAINT pk_study PRIMARY KEY ( study_id ),
	CONSTRAINT uq_study_title UNIQUE ( title ) ,
	CONSTRAINT uq_jira_key UNIQUE ( jira_key )
 );

CREATE TABLE pm.study_sample (
	study_id             bigint  NOT NULL,
	sample_id            varchar  NOT NULL,
	CONSTRAINT fk_study_sample_study_id FOREIGN KEY ( study_id ) REFERENCES pm.study( study_id )    ,
	CONSTRAINT fk_study_sample_sample_id FOREIGN KEY ( sample_id ) REFERENCES pm.sample( sample_id )
 );
CREATE INDEX idx_study_sample_study_id ON pm.study_sample ( study_id );
CREATE INDEX idx_study_sample_sample_id ON pm.study_sample ( sample_id );

CREATE TABLE pm.sample_plate_study (
	sample_plate_id		bigint NOT NULL,
	study_id			bigint NOT NULL,
	CONSTRAINT fk_sample_plate_study FOREIGN KEY ( sample_plate_id ) REFERENCES pm.sample_plate( sample_plate_id ),
	CONSTRAINT fk_sample_plate_study_study FOREIGN KEY ( study_id ) REFERENCES pm.study( study_id )
 );
CREATE INDEX idx_sample_plate_study_sample_plate ON pm.sample_plate_study ( sample_plate_id ) ;
CREATE INDEX idx_sample_plate_study_study_id ON pm.sample_plate_study ( study_id ) ;

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

CREATE TABLE pm.barcode_sequence_plate (
	barcode_sequence_plate_id bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	plate_type_id        bigint  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_barcode_sequence_plate PRIMARY KEY ( barcode_sequence_plate_id ),
	CONSTRAINT uq_barcode_sequence_plate_name UNIQUE ( name ) ,
	CONSTRAINT fk_template_plate_type_id FOREIGN KEY ( plate_type_id ) REFERENCES pm.plate_type( plate_type_id )
 );
CREATE INDEX idx_barcode_sequence_plate_plate_type_id ON pm.barcode_sequence_plate ( plate_type_id );

CREATE TABLE pm.barcode_sequence_plate_layout (
	barcode_sequence_plate_id bigint  NOT NULL,
	col                  smallint  NOT NULL,
	row                  smallint  NOT NULL,
	barcode_sequence     varchar  ,
	CONSTRAINT fk_template_barcode_seq_template_id FOREIGN KEY ( barcode_sequence_plate_id ) REFERENCES pm.barcode_sequence_plate( barcode_sequence_plate_id )
 );
CREATE INDEX idx_barcode_sequence_plate_layout_barcode_sequence_plate_id ON pm.barcode_sequence_plate_layout ( barcode_sequence_plate_id );

CREATE TABLE pm.dna_plate (
	dna_plate_id         bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	email                varchar  ,
	created_on           timestamp  ,
	sample_plate_id      bigint  NOT NULL,
	extraction_robot_id  bigint  NOT NULL,
	extraction_kit_lot_id bigint  NOT NULL,
	extraction_tool_id   bigint  NOT NULL,
	notes                varchar  ,
	CONSTRAINT pk_dna_plate PRIMARY KEY ( dna_plate_id ),
	CONSTRAINT uq_dna_plate_name UNIQUE ( name ) ,
	CONSTRAINT fk_dna_plate_labadmin_users FOREIGN KEY ( email ) REFERENCES ag.labadmin_users( email )    ,
	CONSTRAINT fk_dna_plate_sample_plate FOREIGN KEY ( sample_plate_id ) REFERENCES pm.sample_plate( sample_plate_id )    ,
	CONSTRAINT fk_dna_plate_extraction_robot FOREIGN KEY ( extraction_robot_id ) REFERENCES pm.extraction_robot( extraction_robot_id )    ,
	CONSTRAINT fk_dna_plate FOREIGN KEY ( extraction_kit_lot_id ) REFERENCES pm.extraction_kit_lot( extraction_kit_lot_id )    ,
	CONSTRAINT fk_dna_plate_extraction_tool FOREIGN KEY ( extraction_tool_id ) REFERENCES pm.extraction_tool( extraction_tool_id )
 );
CREATE INDEX idx_dna_plate_email ON pm.dna_plate ( email );
CREATE INDEX idx_dna_plate_sample_plate_id ON pm.dna_plate ( sample_plate_id );
CREATE INDEX idx_dna_plate_extraction_robot_id ON pm.dna_plate ( extraction_robot_id );
CREATE INDEX idx_dna_plate_extraction_kit_lot_id ON pm.dna_plate ( extraction_kit_lot_id );
CREATE INDEX idx_dna_plate_extraction_tool_id ON pm.dna_plate ( extraction_tool_id );

CREATE TABLE pm.protocol_targeted (
	protocol_targeted_id bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	updated_on           timestamp DEFAULT current_timestamp NOT NULL,
	barcode_sequence_plate_id bigint  ,
	master_mix_lot_id    bigint  ,
	water_lot_id         bigint  ,
	tm300_8_tool_id      bigint  ,
	tm50_8_tool_id       bigint  ,
	processing_robot_id  bigint  ,
	CONSTRAINT pk_protocol_targeted PRIMARY KEY ( protocol_targeted_id ),
	CONSTRAINT fk_protocol_targeted FOREIGN KEY ( barcode_sequence_plate_id ) REFERENCES pm.barcode_sequence_plate( barcode_sequence_plate_id )    ,
	CONSTRAINT fk_protocol_targeted_mm FOREIGN KEY ( master_mix_lot_id ) REFERENCES pm.master_mix_lot( master_mix_lot_id )    ,
	CONSTRAINT fk_protocol_targeted_wl FOREIGN KEY ( water_lot_id ) REFERENCES pm.water_lot( water_lot_id )    ,
	CONSTRAINT fk_protocol_targeted_tm300 FOREIGN KEY ( tm300_8_tool_id ) REFERENCES pm.tm300_8_tool( tm300_8_tool_id )    ,
	CONSTRAINT fk_protocol_targeted_tm50 FOREIGN KEY ( tm50_8_tool_id ) REFERENCES pm.tm50_8_tool( tm50_8_tool_id )    ,
	CONSTRAINT fk_protocol_targeted_robot FOREIGN KEY ( processing_robot_id ) REFERENCES pm.processing_robot( processing_robot_id )
 );
CREATE INDEX idx_protocol_targeted_barcode_sequence_plate_id ON pm.protocol_targeted ( barcode_sequence_plate_id );
CREATE INDEX idx_protocol_targeted_master_mix_lot_id ON pm.protocol_targeted ( master_mix_lot_id );
CREATE INDEX idx_protocol_targeted_water_lot_id ON pm.protocol_targeted ( water_lot_id );
CREATE INDEX idx_protocol_targeted_tm300_8_tool_id ON pm.protocol_targeted ( tm300_8_tool_id );
CREATE INDEX idx_protocol_targeted_tm50_8_tool_id ON pm.protocol_targeted ( tm50_8_tool_id );
CREATE INDEX idx_protocol_targeted_processing_robot_id ON pm.protocol_targeted ( processing_robot_id );

CREATE TABLE pm.library_plate (
	library_plate_id     bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	email                varchar  ,
	created_on           timestamp  ,
	dna_plate_id         bigint  NOT NULL,
	protocol_id          bigint  NOT NULL,
	protocol_targeted_id bigint  ,
	notes                varchar  ,
	CONSTRAINT pk_library_plate PRIMARY KEY ( library_plate_id ),
	CONSTRAINT uq_library_plate_name UNIQUE ( name ) ,
	CONSTRAINT fk_library_plate FOREIGN KEY ( email ) REFERENCES ag.labadmin_users( email )    ,
	CONSTRAINT fk_library_plate_dna_plate FOREIGN KEY ( dna_plate_id ) REFERENCES pm.dna_plate( dna_plate_id )    ,
	CONSTRAINT fk_library_plate_protocol FOREIGN KEY ( protocol_id ) REFERENCES pm.protocol( protocol_id )    ,
	CONSTRAINT fk_library_plate_ptg FOREIGN KEY ( protocol_targeted_id ) REFERENCES pm.protocol_targeted( protocol_targeted_id )
 );
CREATE INDEX idx_library_plate_email ON pm.library_plate ( email );
CREATE INDEX idx_library_plate_dna_plate_id ON pm.library_plate ( dna_plate_id );
CREATE INDEX idx_library_plate_protocol_id ON pm.library_plate ( protocol_id );
CREATE INDEX idx_library_plate_protocol_targeted_id ON pm.library_plate ( protocol_targeted_id );

CREATE TABLE pm.run_library_plate (
	run_id               bigint  NOT NULL,
	library_plate_id     bigint  NOT NULL,
	CONSTRAINT fk_run_library_plate_run FOREIGN KEY ( run_id ) REFERENCES pm.run( run_id )    ,
	CONSTRAINT fk_run_library_plate FOREIGN KEY ( library_plate_id ) REFERENCES pm.library_plate( library_plate_id )
 );
CREATE INDEX idx_run_library_plate_run_id ON pm.run_library_plate ( run_id );
CREATE INDEX idx_run_library_plate_library_plate_id ON pm.run_library_plate ( library_plate_id );

-- Add options for properties

INSERT INTO pm.plate_type (name, cols, rows, notes)
		VALUES ('96-well', 12, 8, 'Standard 96-well plate');

INSERT INTO pm.extraction_robot (name)
		VALUES ('HOWE_KF1'), ('HOWE_KF2'), ('HOWE_KF3'), ('HOWE_KF4');

INSERT INTO pm.extraction_tool (name)
		VALUES ('108379Z');

INSERT INTO pm.processing_robot (name)
		VALUES ('ROBE'), ('RIKE'), ('JERE'), ('CARMEN');

INSERT INTO pm.tm300_8_tool (name)
		VALUES ('208484Z'), ('311318B'), ('109375A'), ('3076189');

INSERT INTO pm.tm50_8_tool (name)
		VALUES ('108364Z'), ('311426B'), ('311441B'), ('409172Z');

INSERT INTO pm.extraction_kit_lot (name)
		VALUES ('PM16B11');

INSERT INTO pm.master_mix_lot (name)
		VALUES ('14459');

INSERT INTO pm.water_lot (name)
		VALUES ('RNBD9959');

-- Drop these unused tables
DROP TABLE barcodes.plate_barcode;
DROP TABLE barcodes.plate;

-- The table sample_plate_study is creating a loop on the database in a way
-- that you can get the samples that belong to a study through two different
-- paths: (1) through the study_sample table, and (2) sample_plate_study ->
-- sample_plate -> sample_plate_layout -> sample -> study_sample
-- This loop is required because we know which studies are being plated before
-- we actually start plating. However, it will be a lack of integrity if a
-- sample being plated does not belong to a study linked to the plate. Add
-- a trigger that will check for this entigrity. This should not happen when
-- using the interface, but it doesn't harm to be a bit paranoic :-)
CREATE FUNCTION pm.plate_sample_test() RETURNS trigger AS $plate_sample_test$
BEGIN
	-- Check that the sample being plated actually belongs to a study
	-- linked to the plate
	IF (SELECT study_id FROM pm.study_sample WHERE sample_id = NEW.sample_id) NOT IN (SELECT DISTINCT study_id FROM pm.sample_plate_study WHERE sample_plate_id = NEW.sample_plate_id) THEN
		RAISE EXCEPTION 'Sample % does not belong to a study being plated in %', NEW.sample_id, NEW.sample_plate_id;
	END IF;
	RETURN NEW;
END;
$plate_sample_test$ LANGUAGE plpgsql;

CREATE TRIGGER plate_sample_test BEFORE INSERT OR UPDATE ON pm.sample_plate_layout
	FOR EACH ROW EXECUTE PROCEDURE pm.plate_sample_test();
