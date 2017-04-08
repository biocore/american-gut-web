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
    col                  smallint  NOT NULL,
    row                  smallint  NOT NULL,
    barcode_sequence     varchar  ,
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
CREATE INDEX idx_target_gene_plate ON pm.target_gene_plate ( email ) ;
CREATE INDEX idx_target_gene_plate_0 ON pm.target_gene_plate ( dna_plate_id ) ;
CREATE INDEX idx_target_gene_plate_1 ON pm.target_gene_plate ( barcode_sequence_plate_id ) ;
CREATE INDEX idx_target_gene_plate_2 ON pm.target_gene_plate ( master_mix_lot_id ) ;
CREATE INDEX idx_target_gene_plate_3 ON pm.target_gene_plate ( tm300_8_tool_id ) ;
CREATE INDEX idx_target_gene_plate_4 ON pm.target_gene_plate ( tm50_8_tool_id ) ;
CREATE INDEX idx_target_gene_plate_5 ON pm.target_gene_plate ( water_lot_id ) ;
CREATE INDEX idx_target_gene_plate_6 ON pm.target_gene_plate ( processing_robot_id ) ;

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
    CONSTRAINT idx_whole_genome_plate UNIQUE ( name )
    CONSTRAINT fk_whole_genome_plate FOREIGN KEY ( email ) REFERENCES ag.labadmin_users( email ),
    CONSTRAINT fk_whole_genome_plate_prc_robot FOREIGN KEY ( processing_robot_id ) REFERENCES pm.processing_robot( processing_robot_id ),
    CONSTRAINT fk_whole_genome_plate_type FOREIGN KEY ( plate_type_id ) REFERENCES pm.plate_type( plate_type_id ),
    CONSTRAINT fk_whole_genome_plate_email FOREIGN KEY ( dna_quantification_email ) REFERENCES ag.labadmin_users( email ),
    CONSTRAINT fk_whole_genome_plate_reader FOREIGN KEY ( plate_reader_id ) REFERENCES pm.plate_reader( plate_reader_id )
 ) ;
CREATE INDEX idx_whole_genome_plate ON pm.whole_genome_plate ( email ) ;
CREATE INDEX idx_whole_genome_plate_0 ON pm.whole_genome_plate ( processing_robot_id ) ;
CREATE INDEX idx_whole_genome_plate_1 ON pm.whole_genome_plate ( plate_type_id ) ;
CREATE INDEX idx_whole_genome_plate_2 ON pm.whole_genome_plate ( dna_quantification_email ) ;
CREATE INDEX idx_whole_genome_plate_3 ON pm.whole_genome_plate ( plate_reader_id ) ;

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
     email                    varchar  NOT NULL,
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

 CREATE TABLE pm.i5_index (
     i5_index_id          bigserial  NOT NULL,
     index_aliquot_id     bigint  NOT NULL,
     name                 varchar  NOT NULL,
     row                  integer  NOT NULL,
     col                  integer  NOT NULL,
     CONSTRAINT pk_i5_index PRIMARY KEY ( i5_index_id )
  ) ;
 CREATE INDEX idx_i5_index ON pm.i5_index ( index_aliquot_id ) ;

 CREATE TABLE pm.i7_index (
     i7_index_id          bigserial  NOT NULL,
     index_aliquot_id     bigint  NOT NULL,
     name                 varchar  NOT NULL,
     row                  integer  NOT NULL,
     col                  integer  NOT NULL,
     CONSTRAINT pk_i7_index PRIMARY KEY ( i7_index_id )
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
     CONSTRAINT fk_pool_run_run FOREIGN KEY ( run_id ) REFERENCES pm.run( run_id ),
  ) ;
 CREATE INDEX idx_pool_run ON pm.pool_run ( wgs_pool_id ) ;
 CREATE INDEX idx_pool_run_0 ON pm.pool_run ( target_gene_pool_id ) ;
 CREATE INDEX idx_pool_run_1 ON pm.pool_run ( run_id ) ;


 CREATE TABLE pm.wgs_pool_plate (
     wgs_pool_plate_id    bigserial  NOT NULL,
     wgs_pool_id          bigint  NOT NULL,
     wgs_normalized_plate_id bigint  NOT NULL,
     CONSTRAINT pk_wgs_pool_plate PRIMARY KEY ( wgs_pool_plate_id ),
     CONSTRAINT idx_wgs_pool_plate_0 UNIQUE ( wgs_pool_id, wgs_normalized_plate_id ),
     CONSTRAINT fk_wgs_pool_plate_wgs_pool FOREIGN KEY ( wgs_pool_id ) REFERENCES pm.wgs_pool( wgs_pool_id ),
     CONSTRAINT fk_wgs_pool_plate FOREIGN KEY ( wgs_normalized_plate_id ) REFERENCES pm.wgs_normalized_plate( wgs_normalized_plate_id )
  ) ;
 CREATE INDEX idx_wgs_pool_plate ON pm.wgs_pool_plate ( wgs_pool_id ) ;
 CREATE INDEX idx_wgs_pool_plate_0 ON pm.wgs_pool_plate ( wgs_normalized_plate_id ) ;

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
