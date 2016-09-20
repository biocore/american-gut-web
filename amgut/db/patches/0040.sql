-- Sep. 20, 2016
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

CREATE TABLE pm.extraction_tool (
	extraction_tool_id   bigserial  NOT NULL,
	name                 varchar  NOT NULL,
	notes                varchar  ,
	CONSTRAINT idx_extraction_tool PRIMARY KEY ( extraction_tool_id ),
	CONSTRAINT idx_extraction_tool_0 UNIQUE ( name )
 );

COMMENT ON TABLE pm.extraction_tool IS 'tm1000_8 tools';

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
	CONSTRAINT pk_protocol PRIMARY KEY ( protocol_id )
 );

CREATE TABLE pm.run (
	run_id               bigint  NOT NULL,
	name                 varchar  NOT NULL,
	email                varchar  NOT NULL,
	creation_timestamp   timestamp  ,
	CONSTRAINT pk_run_0 PRIMARY KEY ( run_id ),
	CONSTRAINT fk_run_labadmin_users FOREIGN KEY ( email ) REFERENCES ag.labadmin_users( email )
 );

CREATE INDEX idx_run ON pm.run ( email );

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
	creation_timestamp   timestamp  ,
	notes                varchar  ,
	plate_type_id        bigint  NOT NULL,
	CONSTRAINT pk_sample_plate PRIMARY KEY ( sample_plate_id ),
	CONSTRAINT idx_sample_plate UNIQUE ( name ) ,
	CONSTRAINT fk_sample_plate_labadmin_users FOREIGN KEY ( email ) REFERENCES ag.labadmin_users( email )    ,
	CONSTRAINT fk_sample_plate_plate_type FOREIGN KEY ( plate_type_id ) REFERENCES pm.plate_type( plate_type_id )
 );

CREATE INDEX idx_sample_plate_0 ON pm.sample_plate ( email );

CREATE INDEX idx_sample_plate_1 ON pm.sample_plate ( plate_type_id );

COMMENT ON TABLE pm.sample_plate IS 'Holds the information about the initial plate that the wet lab creates.';

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

CREATE TABLE pm.dna_plate (
	dna_plate_id         bigint  NOT NULL,
	name                 varchar  NOT NULL,
	email                varchar  ,
	creation_timestamp   timestamp  ,
	sample_plate_id      bigint  NOT NULL,
	notes                varchar  ,
	extraction_robot_id  bigint  NOT NULL,
	extraction_kit_lot_id bigint  NOT NULL,
	extraction_tool_id   bigint  NOT NULL,
	CONSTRAINT pk_dna_plate PRIMARY KEY ( dna_plate_id ),
	CONSTRAINT idx_dna_plate UNIQUE ( name ) ,
	CONSTRAINT fk_dna_plate_labadmin_users FOREIGN KEY ( email ) REFERENCES ag.labadmin_users( email )    ,
	CONSTRAINT fk_dna_plate_sample_plate FOREIGN KEY ( sample_plate_id ) REFERENCES pm.sample_plate( sample_plate_id )    ,
	CONSTRAINT fk_dna_plate_extraction_robot FOREIGN KEY ( extraction_robot_id ) REFERENCES pm.extraction_robot( extraction_robot_id )    ,
	CONSTRAINT fk_dna_plate FOREIGN KEY ( extraction_kit_lot_id ) REFERENCES pm.extraction_kit_lot( extraction_kit_lot_id )    ,
	CONSTRAINT fk_dna_plate_extraction_tool FOREIGN KEY ( extraction_tool_id ) REFERENCES pm.extraction_tool( extraction_tool_id )
 );

CREATE INDEX idx_dna_plate ON pm.dna_plate ( email );

CREATE INDEX idx_dna_plate_0 ON pm.dna_plate ( sample_plate_id );

CREATE INDEX idx_dna_plate_1 ON pm.dna_plate ( extraction_robot_id );

CREATE INDEX idx_dna_plate_2 ON pm.dna_plate ( extraction_kit_lot_id );

CREATE INDEX idx_dna_plate_3 ON pm.dna_plate ( extraction_tool_id );

CREATE TABLE pm.plate_map (
	sample_plate_id      bigint  NOT NULL,
	sample_id            varchar  NOT NULL,
	col                  integer  NOT NULL,
	row                  varchar  NOT NULL,
	name                 varchar  ,
	notes                varchar  ,
	CONSTRAINT idx_plate_map_0 PRIMARY KEY ( sample_plate_id, sample_id, col, row ),
	CONSTRAINT fk_plate_map_sample_plate FOREIGN KEY ( sample_plate_id ) REFERENCES pm.sample_plate( sample_plate_id )    ,
	CONSTRAINT fk_plate_map_sample FOREIGN KEY ( sample_id ) REFERENCES pm.sample( sample_id )
 );

CREATE INDEX idx_plate_map ON pm.plate_map ( sample_plate_id );

CREATE INDEX idx_plate_map ON pm.plate_map ( sample_id );

COMMENT ON COLUMN pm.plate_map.name IS 'The name of the sample in this plate in case that needs to be changed (e.g. if the sample has been plated twice)';

CREATE TABLE pm.protocol_target_gene (
	protocol_target_gene_id bigserial  NOT NULL,
	template_id          bigint  ,
	master_mix_lot_id    bigint  ,
	water_lot_id         bigint  ,
	tm300_8_tool_id      bigint  ,
	tm50_8_tool_id       bigint  ,
	processing_robot_id  bigint  ,
	CONSTRAINT pk_protocol_target_gene PRIMARY KEY ( protocol_target_gene_id ),
	CONSTRAINT fk_protocol_target_gene FOREIGN KEY ( template_id ) REFERENCES pm.template( template_id )    ,
	CONSTRAINT fk_protocol_target_gene_mm FOREIGN KEY ( master_mix_lot_id ) REFERENCES pm.master_mix_lot( master_mix_lot_id )    ,
	CONSTRAINT fk_protocol_target_gene_wl FOREIGN KEY ( water_lot_id ) REFERENCES pm.water_lot( water_lot_id )    ,
	CONSTRAINT fk_protocol_target_gene_tm300 FOREIGN KEY ( tm300_8_tool_id ) REFERENCES pm.tm300_8_tool( tm300_8_tool_id )    ,
	CONSTRAINT fk_protocol_target_gene_tm50 FOREIGN KEY ( tm50_8_tool_id ) REFERENCES pm.tm50_8_tool( tm50_8_tool_id )    ,
	CONSTRAINT fk_protocol_target_gene_robot FOREIGN KEY ( processing_robot_id ) REFERENCES pm.processing_robot( processing_robot_id )
 );

CREATE INDEX idx_protocol_target_gene ON pm.protocol_target_gene ( template_id );

CREATE INDEX idx_protocol_target_gene_0 ON pm.protocol_target_gene ( master_mix_lot_id );

CREATE INDEX idx_protocol_target_gene_1 ON pm.protocol_target_gene ( water_lot_id );

CREATE INDEX idx_protocol_target_gene_2 ON pm.protocol_target_gene ( tm300_8_tool_id );

CREATE INDEX idx_protocol_target_gene_3 ON pm.protocol_target_gene ( tm50_8_tool_id );

CREATE INDEX idx_protocol_target_gene_4 ON pm.protocol_target_gene ( processing_robot_id );

CREATE TABLE pm.protocol_plate (
	protocol_plate_id    bigint  NOT NULL,
	name                 varchar  NOT NULL,
	email                varchar  NOT NULL,
	creation_timestamp   timestamp  ,
	dna_plate_id         bigint  NOT NULL,
	notes                varchar  ,
	protocol_id          bigint  NOT NULL,
	protocol_target_gene_id bigint  ,
	CONSTRAINT pk_protocol_plate PRIMARY KEY ( protocol_plate_id ),
	CONSTRAINT idx_protocol_plate UNIQUE ( name ) ,
	CONSTRAINT fk_protocol_plate FOREIGN KEY ( email ) REFERENCES ag.labadmin_users( email )    ,
	CONSTRAINT fk_protocol_plate_dna_plate FOREIGN KEY ( dna_plate_id ) REFERENCES pm.dna_plate( dna_plate_id )    ,
	CONSTRAINT fk_protocol_plate_protocol FOREIGN KEY ( protocol_id ) REFERENCES pm.protocol( protocol_id )    ,
	CONSTRAINT fk_protocol_plate_ptg FOREIGN KEY ( protocol_target_gene_id ) REFERENCES pm.protocol_target_gene( protocol_target_gene_id )
 );

CREATE INDEX idx_protocol_plate ON pm.protocol_plate ( email );

CREATE INDEX idx_protocol_plate ON pm.protocol_plate ( dna_plate_id );

CREATE INDEX idx_protocol_plate_0 ON pm.protocol_plate ( protocol_id );

CREATE INDEX idx_protocol_plate_1 ON pm.protocol_plate ( protocol_target_gene_id );

CREATE TABLE pm.run_protocol_plate (
	run_id               bigint  NOT NULL,
	protocol_plate_id    bigint  NOT NULL,
	CONSTRAINT idx_run_protocol_plate_0 PRIMARY KEY ( run_id, protocol_plate_id ),
	CONSTRAINT fk_run_protocol_plate_run FOREIGN KEY ( run_id ) REFERENCES pm.run( run_id )    ,
	CONSTRAINT fk_run_protocol_plate FOREIGN KEY ( protocol_plate_id ) REFERENCES pm.protocol_plate( protocol_plate_id )
 );

CREATE INDEX idx_run_protocol_plate ON pm.run_protocol_plate ( run_id );

CREATE INDEX idx_run_protocol_plate ON pm.run_protocol_plate ( protocol_plate_id );
