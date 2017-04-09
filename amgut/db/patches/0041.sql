-- March 31, 2017
-- Plate Mapper

-- Create tables

CREATE SCHEMA pm;

CREATE TABLE pm.adapter_aliquot (
    adapter_aliquot_id   bigserial  NOT NULL,
    name                 varchar  NOT NULL,
    notes                varchar  ,
    limit_freeze_thaw_cycles integer  NOT NULL,
    CONSTRAINT pk_adapter_aliquot PRIMARY KEY ( adapter_aliquot_id )
 ) ;

 CREATE TABLE pm.index_aliquot (
 	index_aliquot_id     bigserial  NOT NULL,
 	name                 varchar  NOT NULL,
 	notes                varchar  ,
 	limit_freeze_thaw_cycles bigint  NOT NULL,
 	CONSTRAINT pk_index_aliquot PRIMARY KEY ( index_aliquot_id ),
 	CONSTRAINT idx_index_aliquot UNIQUE ( name )
  ) ;

 CREATE TABLE pm.echo (
     echo_id              bigserial  NOT NULL,
     name                 varchar  NOT NULL,
     notes                varchar  ,
     CONSTRAINT pk_echo PRIMARY KEY ( echo_id ),
     CONSTRAINT idx_echo UNIQUE ( name )
  ) ;

 CREATE TABLE pm.mosquito (
     mosquito_id          bigserial  NOT NULL,
     name                 varchar  NOT NULL,
     notes                varchar  ,
     CONSTRAINT pk_mosquito PRIMARY KEY ( mosquito_id ),
     CONSTRAINT idx_mosquito UNIQUE ( name )
  ) ;

 CREATE TABLE pm.plate_reader (
     plate_reader_id      bigserial  NOT NULL,
     name                 varchar  NOT NULL,
     notes                varchar  ,
     CONSTRAINT pk_plate_reader PRIMARY KEY ( plate_reader_id ),
     CONSTRAINT idx_plate_reader UNIQUE ( name )
  ) ;

 CREATE TABLE pm.qpcr (
     qpcr_id              bigserial  NOT NULL,
     name                 varchar  NOT NULL,
     notes                varchar  ,
     CONSTRAINT pk_qpcr PRIMARY KEY ( qpcr_id ),
     CONSTRAINT idx_qpcr UNIQUE ( name )
  ) ;

CREATE TABLE pm.extraction_kit_lot (
    extraction_kit_lot_id bigserial  NOT NULL,
    name                  varchar  NOT NULL,
    notes                 varchar  ,
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

 CREATE TABLE pm.sequencer (
     sequencer_id         bigserial  NOT NULL,
     platform             varchar  NOT NULL,
     instrument_model     varchar  NOT NULL,
     name                 varchar  NOT NULL,
     CONSTRAINT pk_sequencer PRIMARY KEY ( sequencer_id )
  ) ;

CREATE TABLE pm.run (
    run_id               bigserial  NOT NULL,
    name                 varchar  NOT NULL,
    email                varchar  ,
    created_on           timestamp  ,
    notes                varchar  ,
    sequencer_id         bigint NOT NULL,
    CONSTRAINT pk_run PRIMARY KEY ( run_id ),
    CONSTRAINT uq_run_name UNIQUE ( name ) ,
    CONSTRAINT fk_run_labadmin_users FOREIGN KEY ( email ) REFERENCES ag.labadmin_users( email ),
    CONSTRAINT fk_run_sequencer FOREIGN KEY ( sequencer_id ) REFERENCES pm.sequencer( sequencer_id )
 );
CREATE INDEX idx_run_email ON pm.run ( email );
CREATE INDEX idx_run ON pm.run ( sequencer_id ) ;

CREATE TABLE pm.sample (
    sample_id            varchar  NOT NULL,
    is_blank             bool DEFAULT FALSE NOT NULL,
    details              varchar  ,
    CONSTRAINT pk_sample PRIMARY KEY ( sample_id )
 );

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
    sample_id            varchar,
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
    jira_id              varchar  NOT NULL,
    CONSTRAINT pk_study PRIMARY KEY ( study_id ),
    CONSTRAINT uq_study_title UNIQUE ( title ) ,
    CONSTRAINT uq_jira_id UNIQUE ( jira_id )
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
    col                       smallint  NOT NULL,
    row                       smallint  NOT NULL,
    barcode_sequence          varchar  NOT NULL,
    linker_primer_sequence    varchar NOT NULL,
    CONSTRAINT fk_template_barcode_seq_template_id FOREIGN KEY ( barcode_sequence_plate_id ) REFERENCES pm.barcode_sequence_plate( barcode_sequence_plate_id )
 );
CREATE INDEX idx_barcode_sequence_plate_layout_barcode_sequence_plate_id ON pm.barcode_sequence_plate_layout ( barcode_sequence_plate_id );

CREATE TABLE pm.dna_plate (
    dna_plate_id          bigserial  NOT NULL,
    name                  varchar  NOT NULL,
    email                 varchar  ,
    created_on            timestamp  ,
    sample_plate_id       bigint  NOT NULL,
    extraction_robot_id   bigint  NOT NULL,
    extraction_kit_lot_id bigint  NOT NULL,
    extraction_tool_id    bigint  NOT NULL,
    notes                 varchar  ,
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

CREATE TABLE pm.target_gene_plate (
    target_gene_plate_id bigserial  NOT NULL,
    name                 varchar  NOT NULL,
    email                varchar  NOT NULL,
    created_on           timestamp  NOT NULL,
    dna_plate_id         bigint  NOT NULL,
    barcode_sequence_plate_id bigint  NOT NULL,
    master_mix_lot_id    bigint  NOT NULL,
    tm300_8_tool_id      bigint  NOT NULL,
    tm50_8_tool_id       bigint  NOT NULL,
    water_lot_id         bigint  NOT NULL,
    processing_robot_id  bigint  NOT NULL,
    CONSTRAINT pk_target_gene_plate PRIMARY KEY ( target_gene_plate_id ),
    CONSTRAINT idx_target_gene_plate UNIQUE ( name ),
    CONSTRAINT fk_target_gene_plate FOREIGN KEY ( email ) REFERENCES ag.labadmin_users( email ),
    CONSTRAINT fk_target_gene_plate_dna_plate FOREIGN KEY ( dna_plate_id ) REFERENCES pm.dna_plate( dna_plate_id ),
    CONSTRAINT fk_target_gene_barcode FOREIGN KEY ( barcode_sequence_plate_id ) REFERENCES pm.barcode_sequence_plate( barcode_sequence_plate_id ),
    CONSTRAINT fk_target_gene_master_mix FOREIGN KEY ( master_mix_lot_id ) REFERENCES pm.master_mix_lot( master_mix_lot_id ),
    CONSTRAINT fk_target_gene_tm300_tool FOREIGN KEY ( tm300_8_tool_id ) REFERENCES pm.tm300_8_tool( tm300_8_tool_id ),
    CONSTRAINT fk_target_gene_plate_tm50_8_tool FOREIGN KEY ( tm50_8_tool_id ) REFERENCES pm.tm50_8_tool( tm50_8_tool_id ),
    CONSTRAINT fk_target_gene_plate_water_lot FOREIGN KEY ( water_lot_id ) REFERENCES pm.water_lot( water_lot_id ),
    CONSTRAINT fk_target_gene_plate_robot FOREIGN KEY ( processing_robot_id ) REFERENCES pm.processing_robot( processing_robot_id )
 ) ;
CREATE INDEX idx_target_gene_plate_0 ON pm.target_gene_plate ( email ) ;
CREATE INDEX idx_target_gene_plate_1 ON pm.target_gene_plate ( dna_plate_id ) ;
CREATE INDEX idx_target_gene_plate_2 ON pm.target_gene_plate ( barcode_sequence_plate_id ) ;
CREATE INDEX idx_target_gene_plate_3 ON pm.target_gene_plate ( master_mix_lot_id ) ;
CREATE INDEX idx_target_gene_plate_4 ON pm.target_gene_plate ( tm300_8_tool_id ) ;
CREATE INDEX idx_target_gene_plate_5 ON pm.target_gene_plate ( tm50_8_tool_id ) ;
CREATE INDEX idx_target_gene_plate_6 ON pm.target_gene_plate ( water_lot_id ) ;
CREATE INDEX idx_target_gene_plate_7 ON pm.target_gene_plate ( processing_robot_id ) ;

CREATE TABLE pm.target_gene_pool (
    target_gene_pool_id  bigserial  NOT NULL,
    name                 varchar  NOT NULL,
    CONSTRAINT pk_target_gene_pool PRIMARY KEY ( target_gene_pool_id ),
    CONSTRAINT idx_target_gene_pool UNIQUE ( name )
 ) ;

CREATE TABLE pm.target_gene_pool_plate (
    target_gene_pool_id  bigint  NOT NULL,
    target_gene_plate_id bigint  NOT NULL,
    CONSTRAINT fk_target_gene_pool_plate FOREIGN KEY ( target_gene_pool_id ) REFERENCES pm.target_gene_pool( target_gene_pool_id ),
    CONSTRAINT fk_target_gene_pool_plate_plate FOREIGN KEY ( target_gene_plate_id ) REFERENCES pm.target_gene_plate( target_gene_plate_id )
 ) ;
CREATE INDEX idx_target_gene_pool_plate ON pm.target_gene_pool_plate ( target_gene_pool_id ) ;
CREATE INDEX idx_target_gene_pool_plate_0 ON pm.target_gene_pool_plate ( target_gene_plate_id ) ;

CREATE TABLE pm.whole_genome_plate (
    whole_genome_plate_id       bigserial  NOT NULL,
    name                        varchar  NOT NULL,
    email                       varchar  NOT NULL,
    created_on                  timestamp  NOT NULL,
    processing_robot_id         bigint  NOT NULL,
    plate_type_id               bigint  NOT NULL,
    volume                      real  NOT NULL,
    dna_quantification_date     timestamp  ,
    dna_quantification_email    varchar  ,
    dna_quantification_volume   real  ,
    plate_reader_id             bigint  ,
    CONSTRAINT pk_whole_genome_plate PRIMARY KEY ( whole_genome_plate_id ),
    CONSTRAINT idx_whole_genome_plate UNIQUE ( name ),
    CONSTRAINT fk_whole_genome_plate FOREIGN KEY ( email ) REFERENCES ag.labadmin_users( email ),
    CONSTRAINT fk_whole_genome_plate_prc_robot FOREIGN KEY ( processing_robot_id ) REFERENCES pm.processing_robot( processing_robot_id ),
    CONSTRAINT fk_whole_genome_plate_type FOREIGN KEY ( plate_type_id ) REFERENCES pm.plate_type( plate_type_id ),
    CONSTRAINT fk_whole_genome_plate_email FOREIGN KEY ( dna_quantification_email ) REFERENCES ag.labadmin_users( email ),
    CONSTRAINT fk_whole_genome_plate_reader FOREIGN KEY ( plate_reader_id ) REFERENCES pm.plate_reader( plate_reader_id )
 ) ;
CREATE INDEX idx_whole_genome_plate_0 ON pm.whole_genome_plate ( email ) ;
CREATE INDEX idx_whole_genome_plate_1 ON pm.whole_genome_plate ( processing_robot_id ) ;
CREATE INDEX idx_whole_genome_plate_2 ON pm.whole_genome_plate ( plate_type_id ) ;
CREATE INDEX idx_whole_genome_plate_3 ON pm.whole_genome_plate ( dna_quantification_email ) ;
CREATE INDEX idx_whole_genome_plate_4 ON pm.whole_genome_plate ( plate_reader_id ) ;

CREATE TABLE pm.condensed_plates (
    whole_genome_plate_id  bigint  NOT NULL,
    dna_plate_id           bigint  NOT NULL,
    position               integer  NOT NULL,
    CONSTRAINT idx_condensed_plates PRIMARY KEY ( whole_genome_plate_id, dna_plate_id, position ),
    CONSTRAINT fk_condensed_plates FOREIGN KEY ( whole_genome_plate_id ) REFERENCES pm.whole_genome_plate( whole_genome_plate_id ),
    CONSTRAINT fk_condensed_plates_dna_plate FOREIGN KEY ( dna_plate_id ) REFERENCES pm.dna_plate( dna_plate_id )
 ) ;
CREATE INDEX idx_condensed_plates_0 ON pm.condensed_plates ( whole_genome_plate_id ) ;
CREATE INDEX idx_condensed_plates_1 ON pm.condensed_plates ( dna_plate_id ) ;

CREATE TABLE pm.whole_genome_plate_layout (
    whole_genome_plate_id bigint  NOT NULL,
    sample_id             varchar  ,
    row                   integer  NOT NULL,
    col                   integer  NOT NULL,
    name                  varchar  ,
    notes                 varchar  ,
    dna_concentration     real,
    CONSTRAINT fk_whole_genome_plate_layout FOREIGN KEY ( whole_genome_plate_id ) REFERENCES pm.whole_genome_plate( whole_genome_plate_id ),
    CONSTRAINT fk_whole_genome_plate_layout_sample FOREIGN KEY ( sample_id ) REFERENCES pm.sample( sample_id )
 ) ;
CREATE INDEX idx_whole_genome_plate_layout ON pm.whole_genome_plate_layout ( whole_genome_plate_id ) ;
CREATE INDEX idx_whole_genome_plate_layout_0 ON pm.whole_genome_plate_layout ( sample_id ) ;

CREATE TABLE pm.wgs_library_prep_kit (
    wgs_library_prep_kit_id bigserial  NOT NULL,
    name                 varchar  NOT NULL,
    notes                varchar  ,
    CONSTRAINT pk_wgs_library_prep_kit PRIMARY KEY ( wgs_library_prep_kit_id ),
    CONSTRAINT idx_wgs_library_prep_kit UNIQUE ( name )
 ) ;

 CREATE TABLE pm.wgs_normalized_plate (
     wgs_normalized_plate_id  bigserial  NOT NULL,
     whole_genome_plate_id    bigint  NOT NULL,
     created_on               timestamp  NOT NULL,
     email                    varchar  NOT NULL,
     echo_id                  bigint  NOT NULL,
     lp_date                  timestamp  ,
     lp_email                 varchar  ,
     mosquito                 bigint  ,
     wgs_library_prep_kit_id  bigint  ,
     adapter_aliquot_id       bigint  ,
     qpcr_date                timestamp  ,
     qpcr_email               varchar  ,
     qpcr_std_ladder          varchar  ,
     qpcr_id                  bigint  ,
     CONSTRAINT pk_wgs_normalized_plate PRIMARY KEY ( wgs_normalized_plate_id ),
     CONSTRAINT fk_wgs_normalized_plate FOREIGN KEY ( whole_genome_plate_id ) REFERENCES pm.whole_genome_plate( whole_genome_plate_id ),
     CONSTRAINT fk_wgs_normalized_plate_email FOREIGN KEY ( email ) REFERENCES ag.labadmin_users( email ),
     CONSTRAINT fk_wgs_normalized_plate_echo FOREIGN KEY ( echo_id ) REFERENCES pm.echo( echo_id ),
     CONSTRAINT fk_wgs_normalized_plate_lp_email FOREIGN KEY ( lp_email ) REFERENCES ag.labadmin_users( email ),
     CONSTRAINT fk_wgs_normalized_plate_mosquito FOREIGN KEY ( mosquito ) REFERENCES pm.mosquito( mosquito_id ),
     CONSTRAINT fk_wgs_normalized_plate_kit FOREIGN KEY ( wgs_library_prep_kit_id ) REFERENCES pm.wgs_library_prep_kit( wgs_library_prep_kit_id ),
     CONSTRAINT fk_wgs_normalized_plate_adapter FOREIGN KEY ( adapter_aliquot_id ) REFERENCES pm.adapter_aliquot( adapter_aliquot_id ),
     CONSTRAINT fk_wgs_normalized_plate_qpcr_email FOREIGN KEY ( qpcr_email ) REFERENCES ag.labadmin_users( email ),
     CONSTRAINT fk_wgs_normalized_plate_qpcr FOREIGN KEY ( qpcr_id ) REFERENCES pm.qpcr( qpcr_id )
  ) ;
 CREATE INDEX idx_wgs_normalized_plate ON pm.wgs_normalized_plate ( whole_genome_plate_id ) ;
 CREATE INDEX idx_wgs_normalized_plate_0 ON pm.wgs_normalized_plate ( email ) ;
 CREATE INDEX idx_wgs_normalized_plate_1 ON pm.wgs_normalized_plate ( echo_id ) ;
 CREATE INDEX idx_wgs_normalized_plate_2 ON pm.wgs_normalized_plate ( lp_email ) ;
 CREATE INDEX idx_wgs_normalized_plate_3 ON pm.wgs_normalized_plate ( mosquito ) ;
 CREATE INDEX idx_wgs_normalized_plate_4 ON pm.wgs_normalized_plate ( wgs_library_prep_kit_id ) ;
 CREATE INDEX idx_wgs_normalized_plate_5 ON pm.wgs_normalized_plate ( adapter_aliquot_id ) ;
 CREATE INDEX idx_wgs_normalized_plate_6 ON pm.wgs_normalized_plate ( qpcr_email ) ;
 CREATE INDEX idx_wgs_normalized_plate_7 ON pm.wgs_normalized_plate ( qpcr_id ) ;

 CREATE TABLE pm.i5_index (
     i5_index_id          bigserial  NOT NULL,
     index_aliquot_id     bigint  NOT NULL,
     name                 varchar  NOT NULL,
     row                  integer  NOT NULL,
     col                  integer  NOT NULL,
     CONSTRAINT pk_i5_index PRIMARY KEY ( i5_index_id ),
     CONSTRAINT fk_i5_index_index_aliquot FOREIGN KEY ( index_aliquot_id ) REFERENCES pm.index_aliquot( index_aliquot_id )
  ) ;
 CREATE INDEX idx_i5_index ON pm.i5_index ( index_aliquot_id ) ;

 CREATE TABLE pm.i7_index (
     i7_index_id          bigserial  NOT NULL,
     index_aliquot_id     bigint  NOT NULL,
     name                 varchar  NOT NULL,
     row                  integer  NOT NULL,
     col                  integer  NOT NULL,
     CONSTRAINT pk_i7_index PRIMARY KEY ( i7_index_id ),
     CONSTRAINT fk_i7_index_index_aliquot FOREIGN KEY ( index_aliquot_id ) REFERENCES pm.index_aliquot( index_aliquot_id )
  ) ;
 CREATE INDEX idx_i7_index ON pm.i7_index ( index_aliquot_id ) ;

 CREATE TABLE pm.wgs_normalized_plate_well_values (
     wgs_normalized_plate_id bigint  NOT NULL,
     row                  integer  NOT NULL,
     col                  integer  NOT NULL,
     nl_sample            real  NOT NULL,
     nl_water             real  NOT NULL,
     i5_index_id          bigint  ,
     i7_index_id          bigint  ,
     CONSTRAINT fk_wgs_normalized_plate_well_values FOREIGN KEY ( wgs_normalized_plate_id ) REFERENCES pm.wgs_normalized_plate( wgs_normalized_plate_id ),
     CONSTRAINT fk_wgs_normalized_plate_well_values_i5 FOREIGN KEY ( i5_index_id ) REFERENCES pm.i5_index( i5_index_id ),
     CONSTRAINT fk_wgs_normalized_plate_well_values_i7 FOREIGN KEY ( i7_index_id ) REFERENCES pm.i7_index( i7_index_id )
  ) ;
 CREATE INDEX idx_wgs_normalized_plate_well_values ON pm.wgs_normalized_plate_well_values ( wgs_normalized_plate_id ) ;
 CREATE INDEX idx_wgs_normalized_plate_well_values_0 ON pm.wgs_normalized_plate_well_values ( i5_index_id ) ;
 CREATE INDEX idx_wgs_normalized_plate_well_values_1 ON pm.wgs_normalized_plate_well_values ( i7_index_id ) ;

 CREATE TABLE pm.wgs_pool (
     wgs_pool_id          bigserial  NOT NULL,
     name                 varchar  NOT NULL,
     echo_id              bigint  NOT NULL,
     CONSTRAINT pk_wgs_pool PRIMARY KEY ( wgs_pool_id ),
     CONSTRAINT idx_wgs_pool UNIQUE ( name ),
     CONSTRAINT fk_wgs_pool_echo FOREIGN KEY ( echo_id ) REFERENCES pm.echo( echo_id )
  ) ;
 CREATE INDEX idx_wgs_pool_0 ON pm.wgs_pool ( echo_id ) ;

 CREATE TABLE pm.pool_run (
     run_id               bigint  NOT NULL,
     wgs_pool_id          bigint  ,
     target_gene_pool_id  integer  ,
     notes                varchar ,
     CONSTRAINT fk_pool_run_wgs_pool FOREIGN KEY ( wgs_pool_id ) REFERENCES pm.wgs_pool( wgs_pool_id ),
     CONSTRAINT fk_pool_run_target_gene_pool_tg FOREIGN KEY ( target_gene_pool_id ) REFERENCES pm.target_gene_pool( target_gene_pool_id ),
     CONSTRAINT fk_pool_run_run FOREIGN KEY ( run_id ) REFERENCES pm.run( run_id )
  ) ;
 CREATE INDEX idx_pool_run ON pm.pool_run ( wgs_pool_id ) ;
 CREATE INDEX idx_pool_run_0 ON pm.pool_run ( target_gene_pool_id ) ;
 CREATE INDEX idx_pool_run_1 ON pm.pool_run ( run_id ) ;


 CREATE TABLE pm.wgs_pool_plate (
     wgs_pool_plate_id    bigserial  NOT NULL,
     wgs_pool_id          bigint  NOT NULL,
     wgs_normalized_plate_id bigint  NOT NULL,
     CONSTRAINT pk_wgs_pool_plate PRIMARY KEY ( wgs_pool_plate_id ),
     CONSTRAINT idx_wgs_pool_plate UNIQUE ( wgs_pool_id, wgs_normalized_plate_id ),
     CONSTRAINT fk_wgs_pool_plate_wgs_pool FOREIGN KEY ( wgs_pool_id ) REFERENCES pm.wgs_pool( wgs_pool_id ),
     CONSTRAINT fk_wgs_pool_plate FOREIGN KEY ( wgs_normalized_plate_id ) REFERENCES pm.wgs_normalized_plate( wgs_normalized_plate_id )
  ) ;
 CREATE INDEX idx_wgs_pool_plate_0 ON pm.wgs_pool_plate ( wgs_pool_id ) ;
 CREATE INDEX idx_wgs_pool_plate_1 ON pm.wgs_pool_plate ( wgs_normalized_plate_id ) ;

 CREATE TABLE pm.wgs_pool_plate_well_values (
     wgs_pool_plate_id    bigint  NOT NULL,
     row                  integer  NOT NULL,
     col                  integer  NOT NULL,
     nl_sample            real  NOT NULL,
     CONSTRAINT fk_wgs_pool_plate_well_values FOREIGN KEY ( wgs_pool_plate_id ) REFERENCES pm.wgs_pool_plate( wgs_pool_plate_id )
  ) ;
 CREATE INDEX idx_wgs_pool_plate_well_values ON pm.wgs_pool_plate_well_values ( wgs_pool_plate_id ) ;

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

-- Add the barcode sequence plates
INSERT INTO pm.barcode_sequence_plate (name, plate_type_id)
    VALUES ('Primer plate 1', 1), ('Primer plate 2', 1), ('Primer plate 3', 1),
           ('Primer plate 4', 1), ('Primer plate 5', 1), ('Primer plate 6', 1),
           ('Primer plate 7', 1), ('Primer plate 8', 1);

INSERT INTO pm.barcode_sequence_plate_layout (
        barcode_sequence_plate_id, row, col, linker_primer_sequence, barcode_sequence)
    VALUES
        -- Primer plate 1
        (1, 0, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'AGCCTTCGTCGC'), (1, 0, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'TCCATACCGGAA'), (1, 0, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'AGCCCTGCTACA'),
        (1, 0, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'CCTAACGGTCCA'), (1, 0, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'CGCGCCTTAAAC'), (1, 0, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'TATGGTACCCAG'),
        (1, 0, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'TACAATATCTGT'), (1, 0, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'AATTTAGGTAGG'), (1, 0, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'GACTCAACCAGT'),
        (1, 0, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'GCCTCTACGTCG'), (1, 0, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'ACTACTGAGGAT'), (1, 0, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'AATTCACCTCCT'),
        (1, 1, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'CGTATAAATGCG'), (1, 1, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'ATGCTGCAACAC'), (1, 1, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'ACTCGCTCGCTG'),
        (1, 1, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'TTCCTTAGTAGT'), (1, 1, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'CGTCCGTATGAA'), (1, 1, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'ACGTGAGGAACG'),
        (1, 1, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'GGTTGCCCTGTA'), (1, 1, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'CATATAGCCCGA'), (1, 1, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'GCCTATGAGATC'),
        (1, 1, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'CAAGTGAAGGGA'), (1, 1, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'CACGTTTATTCC'), (1, 1, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'TAATCGGTGCCA'),
        (1, 2, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'TGACTAATGGCC'), (1, 2, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'CGGGACACCCGA'), (1, 2, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'CTGTCTATACTA'),
        (1, 2, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'TATGCCAGAGAT'), (1, 2, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'CGTTTGGAATGA'), (1, 2, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'AAGAACTCATGA'),
        (1, 2, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'TGATATCGTCTT'), (1, 2, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'CGGTGACCTACT'), (1, 2, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'AATGCGCGTATA'),
        (1, 2, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'CTTGATTCTTGA'), (1, 2, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'GAAATCTTGAAG'), (1, 2, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'GAGATACAGTTC'),
        (1, 3, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'GTGGAGTCTCAT'), (1, 3, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'ACCTTACACCTT'), (1, 3, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'TAATCTCGCCGG'),
        (1, 3, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'ATCTAGTGGCAA'), (1, 3, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'ACGCTTAACGAC'), (1, 3, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'TACGGATTATGG'),
        (1, 3, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'ATACATGCAAGA'), (1, 3, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'CTTAGTGCAGAA'), (1, 3, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'AATCTTGCGCCG'),
        (1, 3, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'AGGATCAGGGAA'), (1, 3, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'AATAACTAGGGT'), (1, 3, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'TATTGCAGCAGC'),
        (1, 4, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'TGATGTGCTAAG'), (1, 4, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'GTAGTAGACCAT'), (1, 4, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'AGTAAAGATCGT'),
        (1, 4, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'CTCGCCCTCGCC'), (1, 4, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'TCTCTTTCGACA'), (1, 4, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'ACATACTGAGCA'),
        (1, 4, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'GTTGATACGATG'), (1, 4, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'GTCAACGCTGTC'), (1, 4, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'TGAGACCCTACA'),
        (1, 4, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'ACTTGGTGTAAG'), (1, 4, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'ATTACGTATCAT'), (1, 4, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'CACGCAGTCTAC'),
        (1, 5, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'TGTGCACGCCAT'), (1, 5, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'CCGGACAAGAAG'), (1, 5, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'TTGCTGGACGCT'),
        (1, 5, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'TACTAACGCGGT'), (1, 5, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'GCGATCACACCT'), (1, 5, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'CAAACGCACTAA'),
        (1, 5, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'GAAGAGGGTTGA'), (1, 5, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'TGAGTGGTCTGT'), (1, 5, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'TTACACAAAGGC'),
        (1, 5, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'ACGACGCATTTG'), (1, 5, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'TATCCAAGCGCA'), (1, 5, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'AGAGCCAAGAGC'),
        (1, 6, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'GGTGAGCAAGCA'), (1, 6, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'TAAATATACCCT'), (1, 6, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'TTGCGGACCCTA'),
        (1, 6, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'GTCGTCCAAATG'), (1, 6, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'TGCACAGTCGCT'), (1, 6, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'TTACTGTGGCCG'),
        (1, 6, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'GGTTCATGAACA'), (1, 6, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'TAACAATAATTC'), (1, 6, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'CTTATTAAACGT'),
        (1, 6, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'GCTCGAAGATTC'), (1, 6, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'TATTTGATTGGT'), (1, 6, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'TGTCAAAGTGAC'),
        (1, 7, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'CTATGTATTAGT'), (1, 7, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'ACTCCCGTGTGA'), (1, 7, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'CGGTATAGCAAT'),
        (1, 7, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'GACTCTGCTCAG'), (1, 7, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'GTCATGCTCCAG'), (1, 7, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'TACCGAAGGTAT'),
        (1, 7, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'TGAGTATGAGTA'), (1, 7, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'AATGGTTCAGCA'), (1, 7, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'GAACCAGTACTC'),
        (1, 7, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'CGCACCCATACA'), (1, 7, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'GTGCCATAATCG'), (1, 7, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'ACTCTTACTTAG'),
        -- Primer plate 2
        (2, 0, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'CTACAGGGTCTC'), (2, 0, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'CTTGGAGGCTTA'), (2, 0, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'TATCATATTACG'),
        (2, 0, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'CTATATTATCCG'), (2, 0, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'ACCGAACAATCC'), (2, 0, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'ACGGTACCCTAC'),
        (2, 0, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'TGAGTCATTGAG'), (2, 0, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'ACCTACTTGTCT'), (2, 0, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'ACTGTGACGTCC'),
        (2, 0, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'CTCTGAGGTAAC'), (2, 0, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'CATGTCTTCCAT'), (2, 0, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'AACAGTAAACAA'),
        (2, 1, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'GTTCATTAAACT'), (2, 1, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'GTGCCGGCCGAC'), (2, 1, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'CCTTGACCGATG'),
        (2, 1, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'CAAACTGCGTTG'), (2, 1, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'TCGAGAGTTTGC'), (2, 1, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'CGACACGGAGAA'),
        (2, 1, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'TCCACAGGGTTC'), (2, 1, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'GGAGAACGACAC'), (2, 1, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'CCTACCATTGTT'),
        (2, 1, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'TCCGGCGGGCAA'), (2, 1, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'TAATCCATAATC'), (2, 1, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'CCTCCGTCATGG'),
        (2, 2, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'TTCGATGCCGCA'), (2, 2, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'AGAGGGTGATCG'), (2, 2, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'AGCTCTAGAAAC'),
        (2, 2, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'CTGACACGAATA'), (2, 2, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'GCTGCCCACCTA'), (2, 2, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'GCGTTTGCTAGC'),
        (2, 2, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'AGATCGTGCCTA'), (2, 2, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'AATTAATATGTA'), (2, 2, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'CATTTCGCACTT'),
        (2, 2, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'ACATGATATTCT'), (2, 2, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'GCAACGAACGAG'), (2, 2, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'AGATGTCCGTCA'),
        (2, 3, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'TCGTTATTCAGT'), (2, 3, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'GGATACTCGCAT'), (2, 3, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'AATGTTCAACTT'),
        (2, 3, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'AGCAGTGCGGTG'), (2, 3, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'GCATATGCACTG'), (2, 3, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'CCGGCGACAGAA'),
        (2, 3, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'CCTCACTAGCGA'), (2, 3, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'CTAATCAGAGTG'), (2, 3, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'CTACTCCACGAG'),
        (2, 3, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'TAAGGCATCGCT'), (2, 3, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'AGCGCGGCGAAT'), (2, 3, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'TAGCAGTTGCGT'),
        (2, 4, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'ACTCTGTAATTA'), (2, 4, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'TCATGGCCTCCG'), (2, 4, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'CAATCATAGGTG'),
        (2, 4, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'GTTGGACGAAGG'), (2, 4, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'GTCACTCCGAAC'), (2, 4, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'CGTTCTGGTGGT'),
        (2, 4, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'TAGTTCGGTGAC'), (2, 4, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'TTAATGGATCGG'), (2, 4, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'TCAAGTCCGCAC'),
        (2, 4, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'CACACAAAGTCA'), (2, 4, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'GTCAGGTGCGGC'), (2, 4, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'TTGAACAAGCCA'),
        (2, 5, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'ATATGTTCTCAA'), (2, 5, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'ATGTGCTGCTCG'), (2, 5, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'CCGATAAAGGTT'),
        (2, 5, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'CAGGAACCAGGA'), (2, 5, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'GCATAAACGACT'), (2, 5, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'ATCGTAGTGGTC'),
        (2, 5, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'ACTAAAGCAAAC'), (2, 5, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'TAGGAACTCACC'), (2, 5, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'GTCCGTCCTGGT'),
        (2, 5, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'CGAGGCGAGTCA'), (2, 5, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'TTCCAATACTCA'), (2, 5, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'AACTCAATAGCG'),
        (2, 6, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'TCAGACCAACTG'), (2, 6, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'CCACGAGCAGGC'), (2, 6, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'GCGTGCCCGGCC'),
        (2, 6, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'CAAAGGAGCCCG'), (2, 6, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'TGCGGCGTCAGG'), (2, 6, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'CGCTGTGGATTA'),
        (2, 6, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'CTTGCTCATAAT'), (2, 6, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'ACGACAACGGGC'), (2, 6, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'CTAGCGTGCGTT'),
        (2, 6, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'TAGTCTAAGGGT'), (2, 6, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'GTTTGAAACACG'), (2, 6, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'ACCTCAGTCAAG'),
        (2, 7, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'TCATTAGCGTGG'), (2, 7, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'CGCCGTACTTGC'), (2, 7, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'TAAACCTGGACA'),
        (2, 7, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'CCAACCCAGATC'), (2, 7, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'TTAAGTTAAGTT'), (2, 7, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'AGCCGCGGGTCC'),
        (2, 7, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'GGTAGTTCATAG'), (2, 7, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'CGATGAATATCG'), (2, 7, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'GTTCTAAGGTGA'),
        (2, 7, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'ATGACTAAGATG'), (2, 7, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'TACAGCGCATAC'), (2, 7, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'TGACAGAATCCA'),
        -- Primer plate 3
        (3, 0, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'CCTCGCATGACC'), (3, 0, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'GGCGTAACGGCA'), (3, 0, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'GCGAGGAAGTCC'),
        (3, 0, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'CAAATTCGGGAT'), (3, 0, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'TTGTGTCTCCCT'), (3, 0, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'CAATGTAGACAC'),
        (3, 0, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'AACCACTAACCG'), (3, 0, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'AACTTTCAGGAG'), (3, 0, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'CCAGGACAGGAA'),
        (3, 0, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'GCGCGGCGTTGC'), (3, 0, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'GTCGCTTGCACA'), (3, 0, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'TCCGCCTAGTCG'),
        (3, 1, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'CGCGCAAGTATT'), (3, 1, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'AATACAGACCTG'), (3, 1, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'GGACAAGTGCGA'),
        (3, 1, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'TACGGTCTGGAT'), (3, 1, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'TTCAGTTCGTTA'), (3, 1, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'CCGCGTCTCAAC'),
        (3, 1, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'CCGAGGTATAAT'), (3, 1, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'AGATTCGCTCGA'), (3, 1, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'TTGCCGCTCTGG'),
        (3, 1, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'AGACTTCTCAGG'), (3, 1, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'TCTTGCGGAGTC'), (3, 1, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'CTATCTCCTGTC'),
        (3, 2, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'AAGGCGCTCCTT'), (3, 2, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'GATCTAATCGAG'), (3, 2, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'CTGATGTACACG'),
        (3, 2, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'ACGTATTCGAAG'), (3, 2, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'GACGTTAAGAAT'), (3, 2, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'TGGTGGAGTTTC'),
        (3, 2, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'TTAACAAGGCAA'), (3, 2, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'AACCGCATAAGT'), (3, 2, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'CCACAACGATCA'),
        (3, 2, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'AGTTCTCATTAA'), (3, 2, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'GAGCCATCTGTA'), (3, 2, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'GATATACCAGTG'),
        (3, 3, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'CGCAATGAGGGA'), (3, 3, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'CCGCAGCCGCAG'), (3, 3, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'TGGAGCCTTGTC'),
        (3, 3, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'TTACTTATCCGA'), (3, 3, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'ATGGGACCTTCA'), (3, 3, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'TCCGATAATCGG'),
        (3, 3, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'AAGTCACACACA'), (3, 3, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'GAAGTAGCGAGC'), (3, 3, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'CACCATCTCCGG'),
        (3, 3, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'GTGTCGAGGGCA'), (3, 3, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'TTCCACACGTGG'), (3, 3, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'AGAATCCACCAC'),
        (3, 4, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'ACGGCGTTATGT'), (3, 4, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'GAACCGTGCAGG'), (3, 4, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'ACGTGCCTTAGA'),
        (3, 4, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'AGTTGTAGTCCG'), (3, 4, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'AGGGACTTCAAT'), (3, 4, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'CGGCCAGAAGCA'),
        (3, 4, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'TGGCAGCGAGCC'), (3, 4, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'GTGAATGTTCGA'), (3, 4, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'TATGTTGACGGC'),
        (3, 4, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'AGTGTTTCGGAC'), (3, 4, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'ATTTCCGCTAAT'), (3, 4, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'CAAACCTATGGC'),
        (3, 5, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'CATTTGACGACG'), (3, 5, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'ACTAAGTACCCG'), (3, 5, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'CACCCTTGCGAC'),
        (3, 5, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'GATGCCTAATGA'), (3, 5, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'GTACGTCACTGA'), (3, 5, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'TCGCTACAGATG'),
        (3, 5, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'CCGGCTTATGTG'), (3, 5, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'ATAGTCCTTTAA'), (3, 5, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'TCGAGCCGATCT'),
        (3, 5, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'AGTGCAGGAGCC'), (3, 5, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'GTACTCGAACCA'), (3, 5, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'ATAGGAATAACC'),
        (3, 6, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'GCTGCGTATACC'), (3, 6, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'CTCAGCGGGACG'), (3, 6, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'ATGCCTCGTAAG'),
        (3, 6, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'TTAGTTTGTCAC'), (3, 6, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'CCGGCCGCGTGC'), (3, 6, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'ATTATGATTATG'),
        (3, 6, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'CGAATACTGACA'), (3, 6, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'TCTTATAACGCT'), (3, 6, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'TAAGGTCGATAA'),
        (3, 6, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'GTTGCTGAGTCC'), (3, 6, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'ACACCGCACAAT'), (3, 6, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'CACAACCACAAC'),
        (3, 7, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'GAGAAGCTTATA'), (3, 7, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'GTTAACTTACTA'), (3, 7, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'GTTGTTCTGGGA'),
        (3, 7, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'AGGGTGACTTTA'), (3, 7, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'GCCGCCAGGGTC'), (3, 7, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'GCCACCGCCGGA'),
        (3, 7, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'ACACACCCTGAC'), (3, 7, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'TATAGGCTCCGC'), (3, 7, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'ATAATTGCCGAG'),
        (3, 7, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'CGGAGAGACATG'), (3, 7, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'CAGCCCTACCCA'), (3, 7, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'TCGTTGGGACTA'),
        -- Primer plate 4
        (4, 0, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'TAGGACGGGAGT'), (4, 0, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'AAGTCTTATCTC'), (4, 0, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'TTGCACCGTCGA'),
        (4, 0, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'CTCCGAACAACA'), (4, 0, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'TCTGGCTACGAC'), (4, 0, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'AGTAGTTTCCTT'),
        (4, 0, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'CAGATCCCAACC'), (4, 0, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'GATAGCACTCGT'), (4, 0, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'GTAATTGTAATT'),
        (4, 0, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'TGCTACAGACGT'), (4, 0, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'AGGTGAGTTCTA'), (4, 0, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'AACGATCATAGA'),
        (4, 1, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'GTTTGGCCACAC'), (4, 1, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'GTCCTACACAGC'), (4, 1, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'ATTTACAATTGA'),
        (4, 1, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'CCACTGCCCACC'), (4, 1, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'ATAGTTAGGGCT'), (4, 1, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'GACCCGTTTCGC'),
        (4, 1, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'TGACTGCGTTAG'), (4, 1, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'ACGTTAATATTC'), (4, 1, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'TCTAACGAGTGC'),
        (4, 1, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'GATCCCACGTAC'), (4, 1, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'CCGCCAGCTTTG'), (4, 1, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'TCATCTTGATTG'),
        (4, 2, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'TATATAGTATCC'), (4, 2, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'ACTGTTTACTGT'), (4, 2, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'GTCACGGACATT'),
        (4, 2, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'GAATATACCTGG'), (4, 2, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'GAATCTGACAAC'), (4, 2, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'ATTGCCTTGATT'),
        (4, 2, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'GAGCCCAAAGAG'), (4, 2, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'CCATGTGGCTCC'), (4, 2, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'CGTTCCTTGTTA'),
        (4, 2, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'CGCTAGGATGTT'), (4, 2, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'AGCGGTAGCGGT'), (4, 2, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'GTCAGTATGGCT'),
        (4, 3, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'CATAAGGGAGGC'), (4, 3, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'CAGGCCACTCTC'), (4, 3, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'ACAGTTGTACGC'),
        (4, 3, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'ACCAGAAATGTC'), (4, 3, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'CTCATCATGTTC'), (4, 3, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'TTAGGATTCTAT'),
        (4, 3, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'CAACGAACCATC'), (4, 3, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'ACACGTTTGGGT'), (4, 3, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'CGTCGCAGCCTT'),
        (4, 3, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'CTACTTACATCC'), (4, 3, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'CGCACGTACCTC'), (4, 3, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'GTCCTCGCGACT'),
        (4, 4, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'GTGCAACCAATC'), (4, 4, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'ACCCAAGCGTTA'), (4, 4, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'ACTGGCAAACCT'),
        (4, 4, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'AACACCATCGAC'), (4, 4, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'TTATCCAGTCCT'), (4, 4, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'GTTTATCTTAAG'),
        (4, 4, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'GTTCGCCGCATC'), (4, 4, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'AGACTATTTCAT'), (4, 4, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'AGCGATTCCTCG'),
        (4, 4, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'ACCACCGTAACC'), (4, 4, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'AGGAAGTAACTT'), (4, 4, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'CGTTCGCTAGCC'),
        (4, 5, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'CTCACCTAGGAA'), (4, 5, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'AGATGCAATGAT'), (4, 5, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'GCATTCGGCGTT'),
        (4, 5, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'TCTACATACATA'), (4, 5, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'GAGTCTTGGTAA'), (4, 5, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'CAGTCTAGTACG'),
        (4, 5, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'GTTCGAGTGAAT'), (4, 5, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'AGTCCGAGTTGT'), (4, 5, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'CGTGAGGACCAG'),
        (4, 5, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'CGGTTGGCGGGT'), (4, 5, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'CGATTCCTTAAT'), (4, 5, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'TGCCTGCTCGAC'),
        (4, 6, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'TACTGTACTGTT'), (4, 6, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'TCTCGCACTGGA'), (4, 6, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'ACCAGTGACTCA'),
        (4, 6, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'TGGCGCACGGAC'), (4, 6, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'CATTTACATCAC'), (4, 6, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'GTGGGACTGCGC'),
        (4, 6, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'CGGCCTAAGTTC'), (4, 6, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'GCTGAGCCTTTG'), (4, 6, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'AGAGACGCGTAG'),
        (4, 6, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'CCACCGGGCCGA'), (4, 6, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'AATCCGGTCACC'), (4, 6, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'TCTTACCCATAA'),
        (4, 7, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'CTAGAGCTCCCA'), (4, 7, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'GGTCTTAGCACC'), (4, 7, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'GCCTACTCTCGG'),
        (4, 7, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'ACTGCCCGATAC'), (4, 7, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'TTCTTAACGCCT'), (4, 7, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'CTCCCGAGCTCC'),
        (4, 7, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'TAGACTTCAGAG'), (4, 7, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'ACTTAGACTCTT'), (4, 7, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'GGACCTGGATGG'),
        (4, 7, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'TATGTGCCGGCT'), (4, 7, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'ATACCGTCTTTC'), (4, 7, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'TGTGCTTGTAGG'),
        -- Primer plate 5
        (5, 0, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'ATGTTAGGGAAT'), (5, 0, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'GCTAGTTATGGA'), (5, 0, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'TCATCCGTCGGC'),
        (5, 0, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'ATTTGGCTCTTA'), (5, 0, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'GATCCGGCAGGA'), (5, 0, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'GTTAAGCTGACC'),
        (5, 0, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'CCTATTGCGGCC'), (5, 0, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'CAATAGAATAAG'), (5, 0, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'ACATAGCGGTTC'),
        (5, 0, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'GCGTGGTCATTA'), (5, 0, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'GATTCTTTAGAT'), (5, 0, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'CGGATCTAGTGT'),
        (5, 1, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'AAGTGGCTATCC'), (5, 1, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'ACTAGTTGGACC'), (5, 1, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'GGCTTCGGAGCG'),
        (5, 1, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'CGCGTCAAACTA'), (5, 1, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'CTTCCAACTCAT'), (5, 1, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'GCCTAGCCCAAT'),
        (5, 1, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'GTTAGGGAGCGA'), (5, 1, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'TATACCGCTGCG'), (5, 1, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'CTTACACTGCTT'),
        (5, 1, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'CCTGCACCTGCA'), (5, 1, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'AGGACAAACTAT'), (5, 1, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'ATAACGGTGTAC'),
        (5, 2, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'GTCGTTACCCGC'), (5, 2, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'CGCAAGCCCGCG'), (5, 2, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'CGGTCAATTGAC'),
        (5, 2, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'ATGTTCCTCATC'), (5, 2, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'CGACCTCGCATA'), (5, 2, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'CATTCGTGGCGT'),
        (5, 2, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'AGTACGCAGTCT'), (5, 2, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'CAGTGCACGTCT'), (5, 2, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'ACTCACAGGAAT'),
        (5, 2, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'TGGTGTTTATAT'), (5, 2, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'TCTTCCTAAAGT'), (5, 2, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'GCCCTTCCCGTG'),
        (5, 3, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'AGTATATGTTTC'), (5, 3, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'AGAGCGGAACAA'), (5, 3, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'TCCGCTGCTGAC'),
        (5, 3, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'TCCGTGGTATAG'), (5, 3, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'GTCAGAGTATTG'), (5, 3, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'GCGGTCGGTCAG'),
        (5, 3, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'TATCCTGGTTTC'), (5, 3, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'CTGGTGCTGAAT'), (5, 3, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'GTTGAAGCACCT'),
        (5, 3, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'GTGCGGTTCACT'), (5, 3, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'CTTGTGCGACAA'), (5, 3, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'CACAGTTGAAGT'),
        (5, 4, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'GGCTCGTCGGAG'), (5, 4, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'ACATGGGCGGAA'), (5, 4, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'TGCGCGCCTTCC'),
        (5, 4, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'GTTGGTTGGCAT'), (5, 4, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'GAACGATCATGT'), (5, 4, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'TCAGTCAGATGA'),
        (5, 4, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'CTGGTCTTACGG'), (5, 4, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'ACAAAGGTATCA'), (5, 4, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'GTAAACGACTTG'),
        (5, 4, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'TAGCGCGAACTT'), (5, 4, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'GCGCTTAGAATA'), (5, 4, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'GCAAAGGCCCGC'),
        (5, 5, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'GACATCTGACAC'), (5, 5, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'CTGCGGATATAC'), (5, 5, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'GCGCACACCTTC'),
        (5, 5, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'AACGGGCGACGT'), (5, 5, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'CTCCACATTCCT'), (5, 5, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'CGAACGTCTATG'),
        (5, 5, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'ATGCCGGTAATA'), (5, 5, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'TGAACCCTATGG'), (5, 5, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'TTGGACGTCCAC'),
        (5, 5, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'ATGTAGGCTTAG'), (5, 5, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'AGAGGAGTCGAC'), (5, 5, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'CTCCCACTAGAG'),
        (5, 6, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'AATTTCCTAACA'), (5, 6, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'GTGAGGGCAAGT'), (5, 6, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'CACGAAAGCAGG'),
        (5, 6, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'TACTGAGCCTCG'), (5, 6, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'TCTTCGCAGCAG'), (5, 6, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'CAGTCCCTGCAC'),
        (5, 6, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'ATCAAGATACGC'), (5, 6, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'AATAAGCAATAG'), (5, 6, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'GCACGCGAGCAC'),
        (5, 6, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'GCATTACTGGAC'), (5, 6, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'GTCTCCTCCCTT'), (5, 6, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'AATAGATGCTGA'),
        (5, 7, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'ATAAACGGACAT'), (5, 7, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'ATATTGGCAGCC'), (5, 7, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'CGTGGCTTTCCG'),
        (5, 7, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'GGTGCAGACAGA'), (5, 7, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'CACGCTATTGGA'), (5, 7, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'TGATTTAATTGC'),
        (5, 7, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'CTGAGGCCCTTC'), (5, 7, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'TATGGGTAGCTA'), (5, 7, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'CTTAGGCATGTG'),
        (5, 7, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'TCCGGACTCCTG'), (5, 7, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'AGTATCATATAT'), (5, 7, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'AACGCTTCTTAT'),
        -- Primer plate 6
        (6, 0, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'GTTCGGTGTCCA'), (6, 0, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'CTACCGATTGCG'), (6, 0, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'GAGAGTCCACTT'),
        (6, 0, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'CTAACCTCATAT'), (6, 0, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'AGCTTCGACAGT'), (6, 0, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'GAGAGGGATCAC'),
        (6, 0, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'TGGCCGTTACTG'), (6, 0, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'TTCAGCGATGGT'), (6, 0, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'AAGATCGTACTG'),
        (6, 0, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'ATTTGAAGAGGT'), (6, 0, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'GTCAATTAGTGG'), (6, 0, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'CCTAAGAGCATC'),
        (6, 1, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'GCAAGAATACAT'), (6, 1, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'GGTAATAGAGTT'), (6, 1, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'ATTTGCTTTGCC'),
        (6, 1, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'CTTCGGAGGGAG'), (6, 1, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'TAAGAAACGTCA'), (6, 1, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'TTGCGACAAAGT'),
        (6, 1, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'AGGAACCAGACG'), (6, 1, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'CGTGGTGGGAAC'), (6, 1, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'GTCATTGGGCTA'),
        (6, 1, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'TCTACGGCACGT'), (6, 1, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'AGCCCGCAAAGG'), (6, 1, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'GAGCGCCGAACA'),
        (6, 2, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'CAGGGTAGGGTA'), (6, 2, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'GTAAATTCAGGC'), (6, 2, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'ACCCGGATTTCG'),
        (6, 2, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'GTGACCCTGTCA'), (6, 2, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'AGCAACATTGCA'), (6, 2, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'CAGTGTCATGAA'),
        (6, 2, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'GTTGACCATCGC'), (6, 2, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'AGACACCAATGT'), (6, 2, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'CGCAGATTAGTA'),
        (6, 2, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'TCCTAGGTCCGA'), (6, 2, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'GGCCTATAAGTC'), (6, 2, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'CTCTATTCCACC'),
        (6, 3, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'CTAGTCGCTGGT'), (6, 3, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'AATATCGGGATC'), (6, 3, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'AAGCCTCTACGA'),
        (6, 3, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'GAGAATGGAAAG'), (6, 3, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'GCTTCATTTCTG'), (6, 3, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'CATTCAGTTATA'),
        (6, 3, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'CCAGATATAGCA'), (6, 3, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'TCATACAGCCAG'), (6, 3, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'CTCATATGCTAT'),
        (6, 3, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'CTCTTCTGATCA'), (6, 3, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'CGCGGCGCAGCT'), (6, 3, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'ATGGATAGCTAA'),
        (6, 4, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'AGAAGGCCTTAT'), (6, 4, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'TGGACTCAGCTA'), (6, 4, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'GCGATGGCGATG'),
        (6, 4, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'TAGGAGAGACAG'), (6, 4, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'CAGTAGCGATAT'), (6, 4, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'CCACTCTCTCTA'),
        (6, 4, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'TATCGTTATCGT'), (6, 4, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'ATGTATCAATTA'), (6, 4, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'CAAATGGTCGTC'),
        (6, 4, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'ACACGCGGTTTA'), (6, 4, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'AAGCCGGGTCCG'), (6, 4, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'AGGACGCCAGCA'),
        (6, 5, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'TTGGAACGGCTT'), (6, 5, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'TGTTGCGTTTCT'), (6, 5, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'TTATACGTTGTA'),
        (6, 5, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'GGTGTGAGAAAG'), (6, 5, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'GCCAAGGATAGG'), (6, 5, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'GAACAAAGAGCG'),
        (6, 5, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'ATTCGGTAGTGC'), (6, 5, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'CGCTGGCTTTAG'), (6, 5, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'CAGCTGGTTCAA'),
        (6, 5, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'CTTGAGAAATCG'), (6, 5, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'CGAGGGAAAGTC'), (6, 5, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'GAATGCGTATAA'),
        (6, 6, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'TACCTGTGTCTT'), (6, 6, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'GCTATATCCAGG'), (6, 6, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'CATGATTAAGAG'),
        (6, 6, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'ACCTATGGTGAA'), (6, 6, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'AATCTAACAATT'), (6, 6, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'GTTCCATCGGCC'),
        (6, 6, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'TGACGAGGGCTG'), (6, 6, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'AGACAGTAGGAG'), (6, 6, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'ATAGACACTCCG'),
        (6, 6, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'ACGGCCCTGGAG'), (6, 6, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'CTTCAAGATGGA'), (6, 6, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'CACAATACACCG'),
        (6, 7, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'GATGCGCAGGAC'), (6, 7, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'TGAAAGCGGCGA'), (6, 7, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'AGCACCGGTCTT'),
        (6, 7, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'ACGCCGAGGTAG'), (6, 7, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'CTCACGCAATGC'), (6, 7, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'ATCGTTATATCA'),
        (6, 7, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'TACTTAAACATC'), (6, 7, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'GTGCGAGGACAA'), (6, 7, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'CTTTGATAATAA'),
        (6, 7, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'CATAAATTCTTG'), (6, 7, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'CTGTAAAGGTTG'), (6, 7, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'GGCAGTGTTAAT'),
        -- Primer plate 7
        (7, 0, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'TAGACCGACTCC'), (7, 0, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'TGGAATTCGGCT'), (7, 0, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'GAAGATCTATCG'),
        (7, 0, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'ATCGCCGCCTTG'), (7, 0, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'TAGTGTCGGATC'), (7, 0, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'TCAAGCAATACG'),
        (7, 0, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'AGGGAGCTTCGG'), (7, 0, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'CTGGTAAGTCCA'), (7, 0, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'GGACTTCCAGCT'),
        (7, 0, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'GGAGGAGCAATA'), (7, 0, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'CATGAACAGTGT'), (7, 0, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'TAGGTAACCGAT'),
        (7, 1, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'GGAATCCGATTA'), (7, 1, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'TTCCCACCCATT'), (7, 1, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'GTCCCAGTCCCA'),
        (7, 1, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'AGCCAGTCATAC'), (7, 1, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'GTGTAATGTAGA'), (7, 1, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'ATACTGAGTGAA'),
        (7, 1, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'TGTATGCTTCTA'), (7, 1, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'GAACTCGCTATG'), (7, 1, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'CGATATCAGTAG'),
        (7, 1, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'TCGTAGTAATGG'), (7, 1, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'CGGGTCCTCTTG'), (7, 1, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'GTCGGGCCGGTA'),
        (7, 2, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'TCCGACCCGATC'), (7, 2, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'CCGCATGACCTA'), (7, 2, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'CACTAGACCCAC'),
        (7, 2, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'AGTAATAACAAG'), (7, 2, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'CTTCTTCGCCCT'), (7, 2, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'TACACGCTGATG'),
        (7, 2, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'GACGTCCCTCCA'), (7, 2, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'TATTCTACATGA'), (7, 2, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'GAGGCGCCATAG'),
        (7, 2, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'GCAGAGAGGCTA'), (7, 2, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'CGTTTATCCGTT'), (7, 2, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'GCTAGACACTAC'),
        (7, 3, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'TCACTGCTAGGA'), (7, 3, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'GGTCCTTCCCGA'), (7, 3, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'CGGTAGTTGATC'),
        (7, 3, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'TGGTTTCGAAGA'), (7, 3, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'CCGAAACGGAGC'), (7, 3, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'TCTCCTAGGCGC'),
        (7, 3, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'GTTTGCTCGAGA'), (7, 3, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'TCGATAAGTAAG'), (7, 3, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'AATCTCTATAAC'),
        (7, 3, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'GAGTCCGTTGCT'), (7, 3, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'TAACCACCAACG'), (7, 3, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'TCGTCTGATATT'),
        (7, 4, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'ACATCAGGTCAC'), (7, 4, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'CAGACCGGACGA'), (7, 4, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'AGTTATTCTAGT'),
        (7, 4, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'GTAGGTGCTTAC'), (7, 4, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'GTGGGCGGCCCT'), (7, 4, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'AGTCTTAAAGGA'),
        (7, 4, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'GTCTGACGGTCT'), (7, 4, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'CCATAGGAGGCG'), (7, 4, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'GTGGCGCATGGA'),
        (7, 4, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'CAACTTAATGTT'), (7, 4, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'TAGCGACCTCAC'), (7, 4, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'CCAGCGCTTCAC'),
        (7, 5, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'AGCTATGTATGG'), (7, 5, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'TTCCGAATCGGC'), (7, 5, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'CACATTCTATAA'),
        (7, 5, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'CGGCGATGAAAG'), (7, 5, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'GTTGGGATCCTC'), (7, 5, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'TAATCATGTAAT'),
        (7, 5, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'GAGTTCCATTGG'), (7, 5, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'GCCGCGGGATCA'), (7, 5, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'CGTGTTATGTGG'),
        (7, 5, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'CTGTACTTCTAA'), (7, 5, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'TAGGCATGCTTG'), (7, 5, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'AATAGTCGTGAC'),
        (7, 6, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'AATGACCTCGTG'), (7, 6, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'GCATGTCGAAAT'), (7, 6, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'GCGTTAACCCAA'),
        (7, 6, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'GACCACTGCTGT'), (7, 6, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'TTCACGCGCCCA'), (7, 6, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'TAGGCGGTAGGC'),
        (7, 6, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'ACACTCATTACT'), (7, 6, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'TCTTAAGATTTG'), (7, 6, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'AAGTAGGAAGGA'),
        (7, 6, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'GGCCCTGTGGGC'), (7, 6, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'ATCCATGAGCGT'), (7, 6, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'GAGGCCTCGGGT'),
        (7, 7, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'AAGGGTTAGTCT'), (7, 7, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'ACGCGAACTAAT'), (7, 7, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'TTCGACTAATAT'),
        (7, 7, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'AATCATTTGTAA'), (7, 7, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'TATGCTCTCTCA'), (7, 7, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'TCATTCCACTCA'),
        (7, 7, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'CAGAAATGTGTC'), (7, 7, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'CTTATAGAGAAG'), (7, 7, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'ATGCGCCCGTAT'),
        (7, 7, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'GCATCGTCTGGT'), (7, 7, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'GAGGCAAACGCC'), (7, 7, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'GACTTGGTAAAC'),
        -- Primer plate 8
        (8, 0, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'GCTTATTGCTTA'), (8, 0, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'GACCATGTAGTA'), (8, 0, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'CTTCGCGGATGT'),
        (8, 0, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'TGAGCGCACGCG'), (8, 0, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'CATGAGACTGTA'), (8, 0, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'TTACCCGCACAG'),
        (8, 0, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'AAGATTTGCAGC'), (8, 0, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'AACCGATGTACC'), (8, 0, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'GCCTTACGATAG'),
        (8, 0, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'ACGACCTACGCT'), (8, 0, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'ACGGTGAAAGCG'), (8, 0, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'TGGGACATATCC'),
        (8, 1, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'ATGGCCTGACTA'), (8, 1, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'GCAAGCTGTCTC'), (8, 1, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'ATCACATTCTCC'),
        (8, 1, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'CGAGTATACAAC'), (8, 1, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'CCAGGGACTTCT'), (8, 1, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'ACAAGTGCTGCT'),
        (8, 1, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'CACTCTCCGGCA'), (8, 1, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'ATTAATGAAGCG'), (8, 1, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'ACCGATTAGGTA'),
        (8, 1, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'ATCGATCCACAG'), (8, 1, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'CACCTCCAAGGT'), (8, 1, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'CTAAATACCCTT'),
        (8, 2, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'TCAATGACCGCA'), (8, 2, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'TATCTTCCTGAA'), (8, 2, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'AACGTCCTGTGC'),
        (8, 2, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'TAAGCGTCTCGA'), (8, 2, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'GAGGTATTCTGA'), (8, 2, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'CGTAAGATGCCT'),
        (8, 2, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'GGAGGGTACCGT'), (8, 2, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'TCAAGATCAAGA'), (8, 2, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'TGCAACTTGCAG'),
        (8, 2, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'TACTAGATATTA'), (8, 2, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'TACGTTTGGCGA'), (8, 2, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'GTTGTATTATAC'),
        (8, 3, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'CTTTATGTGTCA'), (8, 3, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'GGTACTGTACCA'), (8, 3, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'AAGGTGGACAAG'),
        (8, 3, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'ACGCTCCCATCG'), (8, 3, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'AGAGCTCCTCTG'), (8, 3, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'GCGTACGGGTGA'),
        (8, 3, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'AAGCGTACATTG'), (8, 3, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'CTGTTACAGCGA'), (8, 3, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'CCGAGTACAATC'),
        (8, 3, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'GGTCTCCTACAG'), (8, 3, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'CTCCTGTCCGGA'), (8, 3, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'AGCCTGGTACCT'),
        (8, 4, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'GGTCGAATTGCT'), (8, 4, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'TCAACTATGTCT'), (8, 4, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'TATAGAAGAATG'),
        (8, 4, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'CTAATATTTGAA'), (8, 4, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'GAGCATTACATG'), (8, 4, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'ATATACCTGCGG'),
        (8, 4, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'CAATATTCAATA'), (8, 4, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'AAGTGCTTGGTA'), (8, 4, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'GCGGAGCACGTC'),
        (8, 4, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'TCCCGCCTACGC'), (8, 4, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'CCTGGTGTCCGT'), (8, 4, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'GGTCCCGAAATT'),
        (8, 5, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'TTACCACATCTA'), (8, 5, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'TGGCATGTTGGT'), (8, 5, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'GTGTGCTAACGT'),
        (8, 5, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'TGAGTTCGGTCC'), (8, 5, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'AGACAAGCTTCC'), (8, 5, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'TATAATCCGAGG'),
        (8, 5, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'ATAAAGAGGAGG'), (8, 5, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'AGTTTGCGAGAT'), (8, 5, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'AAGCTAAAGCTA'),
        (8, 5, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'ACCCTGGGTATC'), (8, 5, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'GGAAGCTTAACT'), (8, 5, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'GACAATTCCGAA'),
        (8, 6, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'ATGCAACTCGAA'), (8, 6, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'ATCATCTCGGCG'), (8, 6, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'GTCTATACATAT'),
        (8, 6, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'CTCAGGAGACTT'), (8, 6, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'CATCCTGAGCAA'), (8, 6, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'GTGACTAGTGAT'),
        (8, 6, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'TCATGTGAACGA'), (8, 6, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'CACTTGCTCTCT'), (8, 6, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'ACAATCCCGAGT'),
        (8, 6, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'GTTCCCAACGGT'), (8, 6, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'ATAATCTAATCC'), (8, 6, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'TAGGTCTAGGTC'),
        (8, 7, 0, 'GTGTGCCAGCMGCCGCGGTAA', 'TTGGTGCCTGTG'), (8, 7, 1,  'GTGTGCCAGCMGCCGCGGTAA', 'ATTGGGACATAA'), (8, 7, 2,  'GTGTGCCAGCMGCCGCGGTAA', 'AGTTCGGCATTG'),
        (8, 7, 3, 'GTGTGCCAGCMGCCGCGGTAA', 'TCTGATCGAGGT'), (8, 7, 4,  'GTGTGCCAGCMGCCGCGGTAA', 'GAATGACGTTTG'), (8, 7, 5,  'GTGTGCCAGCMGCCGCGGTAA', 'GAAGGAAAGTAG'),
        (8, 7, 6, 'GTGTGCCAGCMGCCGCGGTAA', 'AACTGGAACCCT'), (8, 7, 7,  'GTGTGCCAGCMGCCGCGGTAA', 'AGGAATACTCAC'), (8, 7, 8,  'GTGTGCCAGCMGCCGCGGTAA', 'CCATCGACGCTC'),
        (8, 7, 9, 'GTGTGCCAGCMGCCGCGGTAA', 'GTCACCAATCCG'), (8, 7, 10, 'GTGTGCCAGCMGCCGCGGTAA', 'GCCAGGCTTCCT'), (8, 7, 11, 'GTGTGCCAGCMGCCGCGGTAA', 'GCACCAATCTGC');

-- Add some control samples
INSERT INTO pm.sample (sample_id, is_blank, details)
    VALUES ('BLANK', TRUE, NULL);

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
