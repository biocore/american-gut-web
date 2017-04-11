-- March 31, 2017
-- Plate Mapper

-- Create tables

CREATE SCHEMA pm;

CREATE TABLE pm.shotgun_adapter_aliquot (
    shotgun_adapter_aliquot_id   bigserial  NOT NULL,
    name                 varchar  NOT NULL,
    notes                varchar  ,
    limit_freeze_thaw_cycles integer  NOT NULL,
    CONSTRAINT pk_shotgun_adapter_aliquot PRIMARY KEY ( shotgun_adapter_aliquot_id ),
    CONSTRAINT idx_adapter_aliquot UNIQUE ( name )
 ) ;

 CREATE TABLE pm.shotgun_index_aliquot (
 	shotgun_index_aliquot_id     bigserial  NOT NULL,
 	name                         varchar  NOT NULL,
 	notes                        varchar  ,
 	limit_freeze_thaw_cycles     bigint  NOT NULL,
 	CONSTRAINT pk_shotgun_index_aliquot PRIMARY KEY ( shotgun_index_aliquot_id ),
 	CONSTRAINT idx_shotgun_index_aliquot UNIQUE ( name )
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

CREATE TYPE seq_platform AS ENUM ('Illumina');
CREATE TYPE seq_instrument_model AS ENUM ('MiSeq', 'HiSeq 2500', 'HiSeq 4000');

 CREATE TABLE pm.sequencer (
     sequencer_id         bigserial  NOT NULL,
     platform             seq_platform  NOT NULL,
     instrument_model     seq_instrument_model  NOT NULL,
     name                 varchar  NOT NULL,
     CONSTRAINT pk_sequencer PRIMARY KEY ( sequencer_id )
  ) ;

 CREATE TABLE pm.run_pool (
  	run_pool_id          bigserial  NOT NULL,
  	name                 varchar  NOT NULL,
  	volume               real  NOT NULL,
  	notes                varchar  ,
  	CONSTRAINT pk_run_pool PRIMARY KEY ( run_pool_id ),
  	CONSTRAINT idx_run_pool UNIQUE ( name )
 ) ;


 CREATE TYPE reagent_type AS ENUM ('MiSeq v3 150 cycle');

 CREATE TABLE pm.reagent_kit_lot (
 	reagent_kit_lot_id   bigserial  NOT NULL,
 	name                 varchar  NOT NULL,
 	notes                varchar  ,
 	reagent_kit_type     reagent_type  NOT NULL,
 	CONSTRAINT pk_reagent_kit_lot PRIMARY KEY ( reagent_kit_lot_id ),
 	CONSTRAINT idx_reagent_kit_lot UNIQUE ( name )
  ) ;

CREATE TABLE pm.run (
    run_id               bigserial  NOT NULL,
    name                 varchar  NOT NULL,
    email                varchar  ,
    created_on           timestamp  ,
    notes                varchar  ,
    sequencer_id         bigint NOT NULL,
    run_pool_id          bigint NOT NULL,
    reagent_kit_lot_id   bigint NOT NULL,
    CONSTRAINT pk_run PRIMARY KEY ( run_id ),
    CONSTRAINT uq_run_name UNIQUE ( name ) ,
    CONSTRAINT fk_run_labadmin_users FOREIGN KEY ( email ) REFERENCES ag.labadmin_users( email ),
    CONSTRAINT fk_run_sequencer FOREIGN KEY ( sequencer_id ) REFERENCES pm.sequencer( sequencer_id ),
    CONSTRAINT fk_run_run_pool FOREIGN KEY ( run_pool_id ) REFERENCES pm.run_pool( run_pool_id ),
    CONSTRAINT fk_run_reagent_kit_lot FOREIGN KEY ( reagent_kit_lot_id ) REFERENCES pm.reagent_kit_lot( reagent_kit_lot_id )
 );
CREATE INDEX idx_run_email ON pm.run ( email );
CREATE INDEX idx_run ON pm.run ( sequencer_id ) ;
CREATE INDEX idx_run_pool_link ON pm.run ( run_pool_id ) ;
CREATE INDEX idx_run_reagent ON pm.run ( reagent_kit_lot_id ) ;

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
    discarded            bool NOT NULL DEFAULT false,
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

CREATE TYPE target_region AS ENUM ('16S V4', '18S', 'ITS');

CREATE TABLE pm.targeted_primer_plate (
    targeted_primer_plate_id   bigserial  NOT NULL,
    name                       varchar  NOT NULL,
    plate_type_id              bigint  NOT NULL,
    notes                      varchar  ,
    linker_primer_sequence     varchar NOT NULL,
    target_gene_region         target_region NOT NULL,
    CONSTRAINT pk_targeted_primer_plate PRIMARY KEY ( targeted_primer_plate_id ),
    CONSTRAINT uq_targeted_primer_plate_name UNIQUE ( name ) ,
    CONSTRAINT fk_template_plate_type_id FOREIGN KEY ( plate_type_id ) REFERENCES pm.plate_type( plate_type_id )
 );
CREATE INDEX idx_targeted_primer_plate_plate_type_id ON pm.targeted_primer_plate ( plate_type_id );

CREATE TABLE pm.targeted_primer_plate_layout (
    targeted_primer_plate_id  bigint  NOT NULL,
    col                       smallint  NOT NULL,
    row                       smallint  NOT NULL,
    barcode_sequence          varchar  NOT NULL,
    CONSTRAINT fk_template_barcode_seq_template_id FOREIGN KEY ( targeted_primer_plate_id ) REFERENCES pm.targeted_primer_plate( targeted_primer_plate_id )
 );
CREATE INDEX idx_targeted_primer_plate_layout_targeted_primer_plate_id ON pm.targeted_primer_plate_layout ( targeted_primer_plate_id );

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

CREATE TABLE pm.dna_plate_well_values (
	dna_plate_id         bigint  NOT NULL,
	row                  integer  NOT NULL,
	col                  integer  NOT NULL,
	dna_concentration    real  NOT NULL,
    CONSTRAINT fk_dna_plate_well_values FOREIGN KEY ( dna_plate_id ) REFERENCES pm.dna_plate( dna_plate_id )
 ) ;
CREATE INDEX idx_dna_plate_well_values ON pm.dna_plate_well_values ( dna_plate_id ) ;

CREATE TABLE pm.targeted_plate (
    targeted_plate_id         bigserial  NOT NULL,
    name                      varchar  NOT NULL,
    email                     varchar  NOT NULL,
    created_on                timestamp  NOT NULL,
    dna_plate_id              bigint  NOT NULL,
    targeted_primer_plate_id  bigint  NOT NULL,
    master_mix_lot_id         bigint  NOT NULL,
    tm300_8_tool_id           bigint  NOT NULL,
    tm50_8_tool_id            bigint  NOT NULL,
    water_lot_id              bigint  NOT NULL,
    processing_robot_id       bigint  NOT NULL,
    discarded                 bool DEFAULT false NOT NULL,
    CONSTRAINT pk_targeted_plate PRIMARY KEY ( targeted_plate_id ),
    CONSTRAINT idx_targeted_plate UNIQUE ( name ),
    CONSTRAINT fk_targeted_plate FOREIGN KEY ( email ) REFERENCES ag.labadmin_users( email ),
    CONSTRAINT fk_targeted_plate_dna_plate FOREIGN KEY ( dna_plate_id ) REFERENCES pm.dna_plate( dna_plate_id ),
    CONSTRAINT fk_target_gene_barcode FOREIGN KEY ( targeted_primer_plate_id ) REFERENCES pm.targeted_primer_plate( targeted_primer_plate_id ),
    CONSTRAINT fk_target_gene_master_mix FOREIGN KEY ( master_mix_lot_id ) REFERENCES pm.master_mix_lot( master_mix_lot_id ),
    CONSTRAINT fk_target_gene_tm300_tool FOREIGN KEY ( tm300_8_tool_id ) REFERENCES pm.tm300_8_tool( tm300_8_tool_id ),
    CONSTRAINT fk_targeted_plate_tm50_8_tool FOREIGN KEY ( tm50_8_tool_id ) REFERENCES pm.tm50_8_tool( tm50_8_tool_id ),
    CONSTRAINT fk_targeted_plate_water_lot FOREIGN KEY ( water_lot_id ) REFERENCES pm.water_lot( water_lot_id ),
    CONSTRAINT fk_targeted_plate_robot FOREIGN KEY ( processing_robot_id ) REFERENCES pm.processing_robot( processing_robot_id )
 ) ;
CREATE INDEX idx_targeted_plate_0 ON pm.targeted_plate ( email ) ;
CREATE INDEX idx_targeted_plate_1 ON pm.targeted_plate ( dna_plate_id ) ;
CREATE INDEX idx_targeted_plate_2 ON pm.targeted_plate ( targeted_primer_plate_id ) ;
CREATE INDEX idx_targeted_plate_3 ON pm.targeted_plate ( master_mix_lot_id ) ;
CREATE INDEX idx_targeted_plate_4 ON pm.targeted_plate ( tm300_8_tool_id ) ;
CREATE INDEX idx_targeted_plate_5 ON pm.targeted_plate ( tm50_8_tool_id ) ;
CREATE INDEX idx_targeted_plate_6 ON pm.targeted_plate ( water_lot_id ) ;
CREATE INDEX idx_targeted_plate_7 ON pm.targeted_plate ( processing_robot_id ) ;

CREATE TABLE pm.targeted_pool (
    targeted_pool_id     bigserial  NOT NULL,
    name                 varchar  NOT NULL,
    targeted_plate_id    bigint NOT NULL,
    volume               real NOT NULL,
    discarded            bool DEFAULT false NOT NULL,
    CONSTRAINT pk_targeted_pool PRIMARY KEY ( targeted_pool_id ),
    CONSTRAINT idx_targeted_pool UNIQUE ( name ),
    CONSTRAINT fk_target_gene_pool FOREIGN KEY ( targeted_plate_id ) REFERENCES pm.targeted_plate( targeted_plate_id )
 ) ;
 CREATE INDEX idx_target_gene_pool_0 ON pm.targeted_pool ( targeted_plate_id ) ;

CREATE TABLE pm.shotgun_plate (
    shotgun_plate_id            bigserial  NOT NULL,
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
    CONSTRAINT pk_shotgun_plate PRIMARY KEY ( shotgun_plate_id ),
    CONSTRAINT idx_shotgun_plate UNIQUE ( name ),
    CONSTRAINT fk_shotgun_plate FOREIGN KEY ( email ) REFERENCES ag.labadmin_users( email ),
    CONSTRAINT fk_shotgun_plate_prc_robot FOREIGN KEY ( processing_robot_id ) REFERENCES pm.processing_robot( processing_robot_id ),
    CONSTRAINT fk_shotgun_plate_type FOREIGN KEY ( plate_type_id ) REFERENCES pm.plate_type( plate_type_id ),
    CONSTRAINT fk_shotgun_plate_email FOREIGN KEY ( dna_quantification_email ) REFERENCES ag.labadmin_users( email ),
    CONSTRAINT fk_shotgun_plate_reader FOREIGN KEY ( plate_reader_id ) REFERENCES pm.plate_reader( plate_reader_id )
 ) ;
CREATE INDEX idx_shotgun_plate_0 ON pm.shotgun_plate ( email ) ;
CREATE INDEX idx_shotgun_plate_1 ON pm.shotgun_plate ( processing_robot_id ) ;
CREATE INDEX idx_shotgun_plate_2 ON pm.shotgun_plate ( plate_type_id ) ;
CREATE INDEX idx_shotgun_plate_3 ON pm.shotgun_plate ( dna_quantification_email ) ;
CREATE INDEX idx_shotgun_plate_4 ON pm.shotgun_plate ( plate_reader_id ) ;

CREATE TABLE pm.condensed_plates (
    shotgun_plate_id  bigint  NOT NULL,
    dna_plate_id           bigint  NOT NULL,
    position               integer  NOT NULL,
    CONSTRAINT idx_condensed_plates PRIMARY KEY ( shotgun_plate_id, dna_plate_id, position ),
    CONSTRAINT fk_condensed_plates FOREIGN KEY ( shotgun_plate_id ) REFERENCES pm.shotgun_plate( shotgun_plate_id ),
    CONSTRAINT fk_condensed_plates_dna_plate FOREIGN KEY ( dna_plate_id ) REFERENCES pm.dna_plate( dna_plate_id )
 ) ;
CREATE INDEX idx_condensed_plates_0 ON pm.condensed_plates ( shotgun_plate_id ) ;
CREATE INDEX idx_condensed_plates_1 ON pm.condensed_plates ( dna_plate_id ) ;

CREATE TABLE pm.shotgun_plate_layout (
    shotgun_plate_id bigint  NOT NULL,
    sample_id             varchar  NOT NULL,
    row                   integer  NOT NULL,
    col                   integer  NOT NULL,
    name                  varchar  ,
    notes                 varchar  ,
    dna_concentration     real,
    CONSTRAINT fk_shotgun_plate_layout FOREIGN KEY ( shotgun_plate_id ) REFERENCES pm.shotgun_plate( shotgun_plate_id ),
    CONSTRAINT fk_shotgun_plate_layout_sample FOREIGN KEY ( sample_id ) REFERENCES pm.sample( sample_id )
 ) ;
CREATE INDEX idx_shotgun_plate_layout ON pm.shotgun_plate_layout ( shotgun_plate_id ) ;
CREATE INDEX idx_shotgun_plate_layout_0 ON pm.shotgun_plate_layout ( sample_id ) ;

CREATE TABLE pm.shotgun_library_prep_kit (
    shotgun_library_prep_kit_id   bigserial  NOT NULL,
    name                          varchar  NOT NULL,
    notes                         varchar  ,
    CONSTRAINT pk_shotgun_library_prep_kit PRIMARY KEY ( shotgun_library_prep_kit_id ),
    CONSTRAINT idx_shotgun_library_prep_kit UNIQUE ( name )
 ) ;

 CREATE TABLE pm.shotgun_normalized_plate (
     shotgun_normalized_plate_id   bigserial  NOT NULL,
     shotgun_plate_id              bigint  NOT NULL,
     created_on                    timestamp  NOT NULL,
     email                         varchar  NOT NULL,
     echo_id                       bigint  NOT NULL,
     lp_date                       timestamp  ,
     lp_email                      varchar  ,
     mosquito                      bigint  ,
     shotgun_library_prep_kit_id   bigint  ,
     shotgun_adapter_aliquot_id    bigint  ,
     qpcr_date                     timestamp  ,
     qpcr_email                    varchar  ,
     qpcr_std_ladder               varchar  ,
     qpcr_id                       bigint  ,
     discarded                     bool DEFAULT 'False' NOT NULL,
     CONSTRAINT pk_shotgun_normalized_plate PRIMARY KEY ( shotgun_normalized_plate_id ),
     CONSTRAINT fk_shotgun_normalized_plate FOREIGN KEY ( shotgun_plate_id ) REFERENCES pm.shotgun_plate( shotgun_plate_id ),
     CONSTRAINT fk_shotgun_normalized_plate_email FOREIGN KEY ( email ) REFERENCES ag.labadmin_users( email ),
     CONSTRAINT fk_shotgun_normalized_plate_echo FOREIGN KEY ( echo_id ) REFERENCES pm.echo( echo_id ),
     CONSTRAINT fk_shotgun_normalized_plate_lp_email FOREIGN KEY ( lp_email ) REFERENCES ag.labadmin_users( email ),
     CONSTRAINT fk_shotgun_normalized_plate_mosquito FOREIGN KEY ( mosquito ) REFERENCES pm.mosquito( mosquito_id ),
     CONSTRAINT fk_shotgun_normalized_plate_kit FOREIGN KEY ( shotgun_library_prep_kit_id ) REFERENCES pm.shotgun_library_prep_kit( shotgun_library_prep_kit_id ),
     CONSTRAINT fk_shotgun_normalized_plate_adapter FOREIGN KEY ( shotgun_adapter_aliquot_id ) REFERENCES pm.shotgun_adapter_aliquot( shotgun_adapter_aliquot_id ),
     CONSTRAINT fk_shotgun_normalized_plate_qpcr_email FOREIGN KEY ( qpcr_email ) REFERENCES ag.labadmin_users( email ),
     CONSTRAINT fk_shotgun_normalized_plate_qpcr FOREIGN KEY ( qpcr_id ) REFERENCES pm.qpcr( qpcr_id )
  ) ;
 CREATE INDEX idx_shotgun_normalized_plate ON pm.shotgun_normalized_plate ( shotgun_plate_id ) ;
 CREATE INDEX idx_shotgun_normalized_plate_0 ON pm.shotgun_normalized_plate ( email ) ;
 CREATE INDEX idx_shotgun_normalized_plate_1 ON pm.shotgun_normalized_plate ( echo_id ) ;
 CREATE INDEX idx_shotgun_normalized_plate_2 ON pm.shotgun_normalized_plate ( lp_email ) ;
 CREATE INDEX idx_shotgun_normalized_plate_3 ON pm.shotgun_normalized_plate ( mosquito ) ;
 CREATE INDEX idx_shotgun_normalized_plate_4 ON pm.shotgun_normalized_plate ( shotgun_library_prep_kit_id ) ;
 CREATE INDEX idx_shotgun_normalized_plate_5 ON pm.shotgun_normalized_plate ( shotgun_adapter_aliquot_id ) ;
 CREATE INDEX idx_shotgun_normalized_plate_6 ON pm.shotgun_normalized_plate ( qpcr_email ) ;
 CREATE INDEX idx_shotgun_normalized_plate_7 ON pm.shotgun_normalized_plate ( qpcr_id ) ;

 CREATE TABLE pm.shotgun_i5_index (
     shotgun_i5_index_id          bigserial  NOT NULL,
     shotgun_index_aliquot_id     bigint  NOT NULL,
     name                         varchar  NOT NULL,
     row                          integer  NOT NULL,
     col                          integer  NOT NULL,
     CONSTRAINT pk_shotgun_i5_index PRIMARY KEY ( shotgun_i5_index_id ),
     CONSTRAINT fk_shotgun_i5_index_shotgun_index_aliquot FOREIGN KEY ( shotgun_index_aliquot_id ) REFERENCES pm.shotgun_index_aliquot( shotgun_index_aliquot_id )
  ) ;
 CREATE INDEX idx_shotgun_i5_index ON pm.shotgun_i5_index ( shotgun_index_aliquot_id ) ;

 CREATE TABLE pm.shotgun_i7_index (
     shotgun_i7_index_id          bigserial  NOT NULL,
     shotgun_index_aliquot_id     bigint  NOT NULL,
     name                 varchar  NOT NULL,
     row                  integer  NOT NULL,
     col                  integer  NOT NULL,
     CONSTRAINT pk_shotgun_i7_index PRIMARY KEY ( shotgun_i7_index_id ),
     CONSTRAINT fk_shotgun_i7_index_shotgun_index_aliquot FOREIGN KEY ( shotgun_index_aliquot_id ) REFERENCES pm.shotgun_index_aliquot( shotgun_index_aliquot_id )
  ) ;
 CREATE INDEX idx_shotgun_i7_index ON pm.shotgun_i7_index ( shotgun_index_aliquot_id ) ;

 CREATE TABLE pm.shotgun_normalized_plate_well_values (
     shotgun_normalized_plate_id  bigint  NOT NULL,
     row                          integer  NOT NULL,
     col                          integer  NOT NULL,
     sample_volume_nl             real  NOT NULL,
     water_volume_nl              real  NOT NULL,
     shotgun_i5_index_id          bigint  ,
     shotgun_i7_index_id          bigint  ,
     CONSTRAINT fk_shotgun_normalized_plate_well_values FOREIGN KEY ( shotgun_normalized_plate_id ) REFERENCES pm.shotgun_normalized_plate( shotgun_normalized_plate_id ),
     CONSTRAINT fk_shotgun_normalized_plate_well_values_i5 FOREIGN KEY ( shotgun_i5_index_id ) REFERENCES pm.shotgun_i5_index( shotgun_i5_index_id ),
     CONSTRAINT fk_shotgun_normalized_plate_well_values_i7 FOREIGN KEY ( shotgun_i7_index_id ) REFERENCES pm.shotgun_i7_index( shotgun_i7_index_id )
  ) ;
 CREATE INDEX idx_shotgun_normalized_plate_well_values ON pm.shotgun_normalized_plate_well_values ( shotgun_normalized_plate_id ) ;
 CREATE INDEX idx_shotgun_normalized_plate_well_values_0 ON pm.shotgun_normalized_plate_well_values ( shotgun_i5_index_id ) ;
 CREATE INDEX idx_shotgun_normalized_plate_well_values_1 ON pm.shotgun_normalized_plate_well_values ( shotgun_i7_index_id ) ;

 CREATE TABLE pm.shotgun_pool (
     shotgun_pool_id          bigserial  NOT NULL,
     name                     varchar  NOT NULL,
     echo_id                  bigint  NOT NULL,
     discarded                bool NOT NULL DEFAULT false,
     CONSTRAINT pk_shotgun_pool PRIMARY KEY ( shotgun_pool_id ),
     CONSTRAINT idx_shotgun_pool UNIQUE ( name ),
     CONSTRAINT fk_shotgun_pool_echo FOREIGN KEY ( echo_id ) REFERENCES pm.echo( echo_id )
  ) ;
 CREATE INDEX idx_shotgun_pool_0 ON pm.shotgun_pool ( echo_id ) ;

 CREATE TABLE pm.protocol_run_pool (
     run_pool_id               bigint  NOT NULL,
     shotgun_pool_id           bigint  ,
     targeted_pool_id          bigint  ,
     percentage                real ,
     CONSTRAINT fk_protocol_run_pool_shotgun_pool FOREIGN KEY ( shotgun_pool_id ) REFERENCES pm.shotgun_pool( shotgun_pool_id ),
     CONSTRAINT fk_protocol_run_pool_targeted_pool_tg FOREIGN KEY ( targeted_pool_id ) REFERENCES pm.targeted_pool( targeted_pool_id ),
     CONSTRAINT fk_protocol_run_pool_run_pool FOREIGN KEY ( run_pool_id ) REFERENCES pm.run_pool( run_pool_id )
  ) ;
 CREATE INDEX idx_protocol_run_pool ON pm.protocol_run_pool ( shotgun_pool_id ) ;
 CREATE INDEX idx_protocol_run_pool_0 ON pm.protocol_run_pool ( targeted_pool_id ) ;
 CREATE INDEX idx_protocol_run_pool_1 ON pm.protocol_run_pool ( run_pool_id ) ;


 CREATE TABLE pm.shotgun_pool_plate (
     shotgun_pool_plate_id    bigserial  NOT NULL,
     shotgun_pool_id          bigint  NOT NULL,
     shotgun_normalized_plate_id bigint  NOT NULL,
     CONSTRAINT pk_shotgun_pool_plate PRIMARY KEY ( shotgun_pool_plate_id ),
     CONSTRAINT idx_shotgun_pool_plate UNIQUE ( shotgun_pool_id, shotgun_normalized_plate_id ),
     CONSTRAINT fk_shotgun_pool_plate_shotgun_pool FOREIGN KEY ( shotgun_pool_id ) REFERENCES pm.shotgun_pool( shotgun_pool_id ),
     CONSTRAINT fk_shotgun_pool_plate FOREIGN KEY ( shotgun_normalized_plate_id ) REFERENCES pm.shotgun_normalized_plate( shotgun_normalized_plate_id )
  ) ;
 CREATE INDEX idx_shotgun_pool_plate_0 ON pm.shotgun_pool_plate ( shotgun_pool_id ) ;
 CREATE INDEX idx_shotgun_pool_plate_1 ON pm.shotgun_pool_plate ( shotgun_normalized_plate_id ) ;

 CREATE TABLE pm.shotgun_pool_plate_well_values (
     shotgun_pool_plate_id    bigint  NOT NULL,
     row                      integer  NOT NULL,
     col                      integer  NOT NULL,
     sample_volume_nl         real  NOT NULL,
     CONSTRAINT fk_shotgun_pool_plate_well_values FOREIGN KEY ( shotgun_pool_plate_id ) REFERENCES pm.shotgun_pool_plate( shotgun_pool_plate_id )
  ) ;
 CREATE INDEX idx_shotgun_pool_plate_well_values ON pm.shotgun_pool_plate_well_values ( shotgun_pool_plate_id ) ;

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
INSERT INTO pm.targeted_primer_plate (name, plate_type_id, linker_primer_sequence, target_gene_region)
    VALUES ('Primer plate 1', 1, 'GTGTGCCAGCMGCCGCGGTAA', '16S V4'), ('Primer plate 2', 1, 'GTGTGCCAGCMGCCGCGGTAA', '16S V4'),
           ('Primer plate 3', 1, 'GTGTGCCAGCMGCCGCGGTAA', '16S V4'), ('Primer plate 4', 1, 'GTGTGCCAGCMGCCGCGGTAA', '16S V4'),
           ('Primer plate 5', 1, 'GTGTGCCAGCMGCCGCGGTAA', '16S V4'), ('Primer plate 6', 1, 'GTGTGCCAGCMGCCGCGGTAA', '16S V4'),
           ('Primer plate 7', 1, 'GTGTGCCAGCMGCCGCGGTAA', '16S V4'), ('Primer plate 8', 1, 'GTGTGCCAGCMGCCGCGGTAA', '16S V4');

INSERT INTO pm.targeted_primer_plate_layout (
        targeted_primer_plate_id, row, col, barcode_sequence)
    VALUES
        -- Primer plate 1
        (1, 0, 0, 'AGCCTTCGTCGC'), (1, 0, 1,  'TCCATACCGGAA'), (1, 0, 2,  'AGCCCTGCTACA'),
        (1, 0, 3, 'CCTAACGGTCCA'), (1, 0, 4,  'CGCGCCTTAAAC'), (1, 0, 5,  'TATGGTACCCAG'),
        (1, 0, 6, 'TACAATATCTGT'), (1, 0, 7,  'AATTTAGGTAGG'), (1, 0, 8,  'GACTCAACCAGT'),
        (1, 0, 9, 'GCCTCTACGTCG'), (1, 0, 10, 'ACTACTGAGGAT'), (1, 0, 11, 'AATTCACCTCCT'),
        (1, 1, 0, 'CGTATAAATGCG'), (1, 1, 1,  'ATGCTGCAACAC'), (1, 1, 2,  'ACTCGCTCGCTG'),
        (1, 1, 3, 'TTCCTTAGTAGT'), (1, 1, 4,  'CGTCCGTATGAA'), (1, 1, 5,  'ACGTGAGGAACG'),
        (1, 1, 6, 'GGTTGCCCTGTA'), (1, 1, 7,  'CATATAGCCCGA'), (1, 1, 8,  'GCCTATGAGATC'),
        (1, 1, 9, 'CAAGTGAAGGGA'), (1, 1, 10, 'CACGTTTATTCC'), (1, 1, 11, 'TAATCGGTGCCA'),
        (1, 2, 0, 'TGACTAATGGCC'), (1, 2, 1,  'CGGGACACCCGA'), (1, 2, 2,  'CTGTCTATACTA'),
        (1, 2, 3, 'TATGCCAGAGAT'), (1, 2, 4,  'CGTTTGGAATGA'), (1, 2, 5,  'AAGAACTCATGA'),
        (1, 2, 6, 'TGATATCGTCTT'), (1, 2, 7,  'CGGTGACCTACT'), (1, 2, 8,  'AATGCGCGTATA'),
        (1, 2, 9, 'CTTGATTCTTGA'), (1, 2, 10, 'GAAATCTTGAAG'), (1, 2, 11, 'GAGATACAGTTC'),
        (1, 3, 0, 'GTGGAGTCTCAT'), (1, 3, 1,  'ACCTTACACCTT'), (1, 3, 2,  'TAATCTCGCCGG'),
        (1, 3, 3, 'ATCTAGTGGCAA'), (1, 3, 4,  'ACGCTTAACGAC'), (1, 3, 5,  'TACGGATTATGG'),
        (1, 3, 6, 'ATACATGCAAGA'), (1, 3, 7,  'CTTAGTGCAGAA'), (1, 3, 8,  'AATCTTGCGCCG'),
        (1, 3, 9, 'AGGATCAGGGAA'), (1, 3, 10, 'AATAACTAGGGT'), (1, 3, 11, 'TATTGCAGCAGC'),
        (1, 4, 0, 'TGATGTGCTAAG'), (1, 4, 1,  'GTAGTAGACCAT'), (1, 4, 2,  'AGTAAAGATCGT'),
        (1, 4, 3, 'CTCGCCCTCGCC'), (1, 4, 4,  'TCTCTTTCGACA'), (1, 4, 5,  'ACATACTGAGCA'),
        (1, 4, 6, 'GTTGATACGATG'), (1, 4, 7,  'GTCAACGCTGTC'), (1, 4, 8,  'TGAGACCCTACA'),
        (1, 4, 9, 'ACTTGGTGTAAG'), (1, 4, 10, 'ATTACGTATCAT'), (1, 4, 11, 'CACGCAGTCTAC'),
        (1, 5, 0, 'TGTGCACGCCAT'), (1, 5, 1,  'CCGGACAAGAAG'), (1, 5, 2,  'TTGCTGGACGCT'),
        (1, 5, 3, 'TACTAACGCGGT'), (1, 5, 4,  'GCGATCACACCT'), (1, 5, 5,  'CAAACGCACTAA'),
        (1, 5, 6, 'GAAGAGGGTTGA'), (1, 5, 7,  'TGAGTGGTCTGT'), (1, 5, 8,  'TTACACAAAGGC'),
        (1, 5, 9, 'ACGACGCATTTG'), (1, 5, 10, 'TATCCAAGCGCA'), (1, 5, 11, 'AGAGCCAAGAGC'),
        (1, 6, 0, 'GGTGAGCAAGCA'), (1, 6, 1,  'TAAATATACCCT'), (1, 6, 2,  'TTGCGGACCCTA'),
        (1, 6, 3, 'GTCGTCCAAATG'), (1, 6, 4,  'TGCACAGTCGCT'), (1, 6, 5,  'TTACTGTGGCCG'),
        (1, 6, 6, 'GGTTCATGAACA'), (1, 6, 7,  'TAACAATAATTC'), (1, 6, 8,  'CTTATTAAACGT'),
        (1, 6, 9, 'GCTCGAAGATTC'), (1, 6, 10, 'TATTTGATTGGT'), (1, 6, 11, 'TGTCAAAGTGAC'),
        (1, 7, 0, 'CTATGTATTAGT'), (1, 7, 1,  'ACTCCCGTGTGA'), (1, 7, 2,  'CGGTATAGCAAT'),
        (1, 7, 3, 'GACTCTGCTCAG'), (1, 7, 4,  'GTCATGCTCCAG'), (1, 7, 5,  'TACCGAAGGTAT'),
        (1, 7, 6, 'TGAGTATGAGTA'), (1, 7, 7,  'AATGGTTCAGCA'), (1, 7, 8,  'GAACCAGTACTC'),
        (1, 7, 9, 'CGCACCCATACA'), (1, 7, 10, 'GTGCCATAATCG'), (1, 7, 11, 'ACTCTTACTTAG'),
        -- Primer plate 2
        (2, 0, 0, 'CTACAGGGTCTC'), (2, 0, 1,  'CTTGGAGGCTTA'), (2, 0, 2,  'TATCATATTACG'),
        (2, 0, 3, 'CTATATTATCCG'), (2, 0, 4,  'ACCGAACAATCC'), (2, 0, 5,  'ACGGTACCCTAC'),
        (2, 0, 6, 'TGAGTCATTGAG'), (2, 0, 7,  'ACCTACTTGTCT'), (2, 0, 8,  'ACTGTGACGTCC'),
        (2, 0, 9, 'CTCTGAGGTAAC'), (2, 0, 10, 'CATGTCTTCCAT'), (2, 0, 11, 'AACAGTAAACAA'),
        (2, 1, 0, 'GTTCATTAAACT'), (2, 1, 1,  'GTGCCGGCCGAC'), (2, 1, 2,  'CCTTGACCGATG'),
        (2, 1, 3, 'CAAACTGCGTTG'), (2, 1, 4,  'TCGAGAGTTTGC'), (2, 1, 5,  'CGACACGGAGAA'),
        (2, 1, 6, 'TCCACAGGGTTC'), (2, 1, 7,  'GGAGAACGACAC'), (2, 1, 8,  'CCTACCATTGTT'),
        (2, 1, 9, 'TCCGGCGGGCAA'), (2, 1, 10, 'TAATCCATAATC'), (2, 1, 11, 'CCTCCGTCATGG'),
        (2, 2, 0, 'TTCGATGCCGCA'), (2, 2, 1,  'AGAGGGTGATCG'), (2, 2, 2,  'AGCTCTAGAAAC'),
        (2, 2, 3, 'CTGACACGAATA'), (2, 2, 4,  'GCTGCCCACCTA'), (2, 2, 5,  'GCGTTTGCTAGC'),
        (2, 2, 6, 'AGATCGTGCCTA'), (2, 2, 7,  'AATTAATATGTA'), (2, 2, 8,  'CATTTCGCACTT'),
        (2, 2, 9, 'ACATGATATTCT'), (2, 2, 10, 'GCAACGAACGAG'), (2, 2, 11, 'AGATGTCCGTCA'),
        (2, 3, 0, 'TCGTTATTCAGT'), (2, 3, 1,  'GGATACTCGCAT'), (2, 3, 2,  'AATGTTCAACTT'),
        (2, 3, 3, 'AGCAGTGCGGTG'), (2, 3, 4,  'GCATATGCACTG'), (2, 3, 5,  'CCGGCGACAGAA'),
        (2, 3, 6, 'CCTCACTAGCGA'), (2, 3, 7,  'CTAATCAGAGTG'), (2, 3, 8,  'CTACTCCACGAG'),
        (2, 3, 9, 'TAAGGCATCGCT'), (2, 3, 10, 'AGCGCGGCGAAT'), (2, 3, 11, 'TAGCAGTTGCGT'),
        (2, 4, 0, 'ACTCTGTAATTA'), (2, 4, 1,  'TCATGGCCTCCG'), (2, 4, 2,  'CAATCATAGGTG'),
        (2, 4, 3, 'GTTGGACGAAGG'), (2, 4, 4,  'GTCACTCCGAAC'), (2, 4, 5,  'CGTTCTGGTGGT'),
        (2, 4, 6, 'TAGTTCGGTGAC'), (2, 4, 7,  'TTAATGGATCGG'), (2, 4, 8,  'TCAAGTCCGCAC'),
        (2, 4, 9, 'CACACAAAGTCA'), (2, 4, 10, 'GTCAGGTGCGGC'), (2, 4, 11, 'TTGAACAAGCCA'),
        (2, 5, 0, 'ATATGTTCTCAA'), (2, 5, 1,  'ATGTGCTGCTCG'), (2, 5, 2,  'CCGATAAAGGTT'),
        (2, 5, 3, 'CAGGAACCAGGA'), (2, 5, 4,  'GCATAAACGACT'), (2, 5, 5,  'ATCGTAGTGGTC'),
        (2, 5, 6, 'ACTAAAGCAAAC'), (2, 5, 7,  'TAGGAACTCACC'), (2, 5, 8,  'GTCCGTCCTGGT'),
        (2, 5, 9, 'CGAGGCGAGTCA'), (2, 5, 10, 'TTCCAATACTCA'), (2, 5, 11, 'AACTCAATAGCG'),
        (2, 6, 0, 'TCAGACCAACTG'), (2, 6, 1,  'CCACGAGCAGGC'), (2, 6, 2,  'GCGTGCCCGGCC'),
        (2, 6, 3, 'CAAAGGAGCCCG'), (2, 6, 4,  'TGCGGCGTCAGG'), (2, 6, 5,  'CGCTGTGGATTA'),
        (2, 6, 6, 'CTTGCTCATAAT'), (2, 6, 7,  'ACGACAACGGGC'), (2, 6, 8,  'CTAGCGTGCGTT'),
        (2, 6, 9, 'TAGTCTAAGGGT'), (2, 6, 10, 'GTTTGAAACACG'), (2, 6, 11, 'ACCTCAGTCAAG'),
        (2, 7, 0, 'TCATTAGCGTGG'), (2, 7, 1,  'CGCCGTACTTGC'), (2, 7, 2,  'TAAACCTGGACA'),
        (2, 7, 3, 'CCAACCCAGATC'), (2, 7, 4,  'TTAAGTTAAGTT'), (2, 7, 5,  'AGCCGCGGGTCC'),
        (2, 7, 6, 'GGTAGTTCATAG'), (2, 7, 7,  'CGATGAATATCG'), (2, 7, 8,  'GTTCTAAGGTGA'),
        (2, 7, 9, 'ATGACTAAGATG'), (2, 7, 10, 'TACAGCGCATAC'), (2, 7, 11, 'TGACAGAATCCA'),
        -- Primer plate 3
        (3, 0, 0, 'CCTCGCATGACC'), (3, 0, 1,  'GGCGTAACGGCA'), (3, 0, 2,  'GCGAGGAAGTCC'),
        (3, 0, 3, 'CAAATTCGGGAT'), (3, 0, 4,  'TTGTGTCTCCCT'), (3, 0, 5,  'CAATGTAGACAC'),
        (3, 0, 6, 'AACCACTAACCG'), (3, 0, 7,  'AACTTTCAGGAG'), (3, 0, 8,  'CCAGGACAGGAA'),
        (3, 0, 9, 'GCGCGGCGTTGC'), (3, 0, 10, 'GTCGCTTGCACA'), (3, 0, 11, 'TCCGCCTAGTCG'),
        (3, 1, 0, 'CGCGCAAGTATT'), (3, 1, 1,  'AATACAGACCTG'), (3, 1, 2,  'GGACAAGTGCGA'),
        (3, 1, 3, 'TACGGTCTGGAT'), (3, 1, 4,  'TTCAGTTCGTTA'), (3, 1, 5,  'CCGCGTCTCAAC'),
        (3, 1, 6, 'CCGAGGTATAAT'), (3, 1, 7,  'AGATTCGCTCGA'), (3, 1, 8,  'TTGCCGCTCTGG'),
        (3, 1, 9, 'AGACTTCTCAGG'), (3, 1, 10, 'TCTTGCGGAGTC'), (3, 1, 11, 'CTATCTCCTGTC'),
        (3, 2, 0, 'AAGGCGCTCCTT'), (3, 2, 1,  'GATCTAATCGAG'), (3, 2, 2,  'CTGATGTACACG'),
        (3, 2, 3, 'ACGTATTCGAAG'), (3, 2, 4,  'GACGTTAAGAAT'), (3, 2, 5,  'TGGTGGAGTTTC'),
        (3, 2, 6, 'TTAACAAGGCAA'), (3, 2, 7,  'AACCGCATAAGT'), (3, 2, 8,  'CCACAACGATCA'),
        (3, 2, 9, 'AGTTCTCATTAA'), (3, 2, 10, 'GAGCCATCTGTA'), (3, 2, 11, 'GATATACCAGTG'),
        (3, 3, 0, 'CGCAATGAGGGA'), (3, 3, 1,  'CCGCAGCCGCAG'), (3, 3, 2,  'TGGAGCCTTGTC'),
        (3, 3, 3, 'TTACTTATCCGA'), (3, 3, 4,  'ATGGGACCTTCA'), (3, 3, 5,  'TCCGATAATCGG'),
        (3, 3, 6, 'AAGTCACACACA'), (3, 3, 7,  'GAAGTAGCGAGC'), (3, 3, 8,  'CACCATCTCCGG'),
        (3, 3, 9, 'GTGTCGAGGGCA'), (3, 3, 10, 'TTCCACACGTGG'), (3, 3, 11, 'AGAATCCACCAC'),
        (3, 4, 0, 'ACGGCGTTATGT'), (3, 4, 1,  'GAACCGTGCAGG'), (3, 4, 2,  'ACGTGCCTTAGA'),
        (3, 4, 3, 'AGTTGTAGTCCG'), (3, 4, 4,  'AGGGACTTCAAT'), (3, 4, 5,  'CGGCCAGAAGCA'),
        (3, 4, 6, 'TGGCAGCGAGCC'), (3, 4, 7,  'GTGAATGTTCGA'), (3, 4, 8,  'TATGTTGACGGC'),
        (3, 4, 9, 'AGTGTTTCGGAC'), (3, 4, 10, 'ATTTCCGCTAAT'), (3, 4, 11, 'CAAACCTATGGC'),
        (3, 5, 0, 'CATTTGACGACG'), (3, 5, 1,  'ACTAAGTACCCG'), (3, 5, 2,  'CACCCTTGCGAC'),
        (3, 5, 3, 'GATGCCTAATGA'), (3, 5, 4,  'GTACGTCACTGA'), (3, 5, 5,  'TCGCTACAGATG'),
        (3, 5, 6, 'CCGGCTTATGTG'), (3, 5, 7,  'ATAGTCCTTTAA'), (3, 5, 8,  'TCGAGCCGATCT'),
        (3, 5, 9, 'AGTGCAGGAGCC'), (3, 5, 10, 'GTACTCGAACCA'), (3, 5, 11, 'ATAGGAATAACC'),
        (3, 6, 0, 'GCTGCGTATACC'), (3, 6, 1,  'CTCAGCGGGACG'), (3, 6, 2,  'ATGCCTCGTAAG'),
        (3, 6, 3, 'TTAGTTTGTCAC'), (3, 6, 4,  'CCGGCCGCGTGC'), (3, 6, 5,  'ATTATGATTATG'),
        (3, 6, 6, 'CGAATACTGACA'), (3, 6, 7,  'TCTTATAACGCT'), (3, 6, 8,  'TAAGGTCGATAA'),
        (3, 6, 9, 'GTTGCTGAGTCC'), (3, 6, 10, 'ACACCGCACAAT'), (3, 6, 11, 'CACAACCACAAC'),
        (3, 7, 0, 'GAGAAGCTTATA'), (3, 7, 1,  'GTTAACTTACTA'), (3, 7, 2,  'GTTGTTCTGGGA'),
        (3, 7, 3, 'AGGGTGACTTTA'), (3, 7, 4,  'GCCGCCAGGGTC'), (3, 7, 5,  'GCCACCGCCGGA'),
        (3, 7, 6, 'ACACACCCTGAC'), (3, 7, 7,  'TATAGGCTCCGC'), (3, 7, 8,  'ATAATTGCCGAG'),
        (3, 7, 9, 'CGGAGAGACATG'), (3, 7, 10, 'CAGCCCTACCCA'), (3, 7, 11, 'TCGTTGGGACTA'),
        -- Primer plate 4
        (4, 0, 0, 'TAGGACGGGAGT'), (4, 0, 1,  'AAGTCTTATCTC'), (4, 0, 2,  'TTGCACCGTCGA'),
        (4, 0, 3, 'CTCCGAACAACA'), (4, 0, 4,  'TCTGGCTACGAC'), (4, 0, 5,  'AGTAGTTTCCTT'),
        (4, 0, 6, 'CAGATCCCAACC'), (4, 0, 7,  'GATAGCACTCGT'), (4, 0, 8,  'GTAATTGTAATT'),
        (4, 0, 9, 'TGCTACAGACGT'), (4, 0, 10, 'AGGTGAGTTCTA'), (4, 0, 11, 'AACGATCATAGA'),
        (4, 1, 0, 'GTTTGGCCACAC'), (4, 1, 1,  'GTCCTACACAGC'), (4, 1, 2,  'ATTTACAATTGA'),
        (4, 1, 3, 'CCACTGCCCACC'), (4, 1, 4,  'ATAGTTAGGGCT'), (4, 1, 5,  'GACCCGTTTCGC'),
        (4, 1, 6, 'TGACTGCGTTAG'), (4, 1, 7,  'ACGTTAATATTC'), (4, 1, 8,  'TCTAACGAGTGC'),
        (4, 1, 9, 'GATCCCACGTAC'), (4, 1, 10, 'CCGCCAGCTTTG'), (4, 1, 11, 'TCATCTTGATTG'),
        (4, 2, 0, 'TATATAGTATCC'), (4, 2, 1,  'ACTGTTTACTGT'), (4, 2, 2,  'GTCACGGACATT'),
        (4, 2, 3, 'GAATATACCTGG'), (4, 2, 4,  'GAATCTGACAAC'), (4, 2, 5,  'ATTGCCTTGATT'),
        (4, 2, 6, 'GAGCCCAAAGAG'), (4, 2, 7,  'CCATGTGGCTCC'), (4, 2, 8,  'CGTTCCTTGTTA'),
        (4, 2, 9, 'CGCTAGGATGTT'), (4, 2, 10, 'AGCGGTAGCGGT'), (4, 2, 11, 'GTCAGTATGGCT'),
        (4, 3, 0, 'CATAAGGGAGGC'), (4, 3, 1,  'CAGGCCACTCTC'), (4, 3, 2,  'ACAGTTGTACGC'),
        (4, 3, 3, 'ACCAGAAATGTC'), (4, 3, 4,  'CTCATCATGTTC'), (4, 3, 5,  'TTAGGATTCTAT'),
        (4, 3, 6, 'CAACGAACCATC'), (4, 3, 7,  'ACACGTTTGGGT'), (4, 3, 8,  'CGTCGCAGCCTT'),
        (4, 3, 9, 'CTACTTACATCC'), (4, 3, 10, 'CGCACGTACCTC'), (4, 3, 11, 'GTCCTCGCGACT'),
        (4, 4, 0, 'GTGCAACCAATC'), (4, 4, 1,  'ACCCAAGCGTTA'), (4, 4, 2,  'ACTGGCAAACCT'),
        (4, 4, 3, 'AACACCATCGAC'), (4, 4, 4,  'TTATCCAGTCCT'), (4, 4, 5,  'GTTTATCTTAAG'),
        (4, 4, 6, 'GTTCGCCGCATC'), (4, 4, 7,  'AGACTATTTCAT'), (4, 4, 8,  'AGCGATTCCTCG'),
        (4, 4, 9, 'ACCACCGTAACC'), (4, 4, 10, 'AGGAAGTAACTT'), (4, 4, 11, 'CGTTCGCTAGCC'),
        (4, 5, 0, 'CTCACCTAGGAA'), (4, 5, 1,  'AGATGCAATGAT'), (4, 5, 2,  'GCATTCGGCGTT'),
        (4, 5, 3, 'TCTACATACATA'), (4, 5, 4,  'GAGTCTTGGTAA'), (4, 5, 5,  'CAGTCTAGTACG'),
        (4, 5, 6, 'GTTCGAGTGAAT'), (4, 5, 7,  'AGTCCGAGTTGT'), (4, 5, 8,  'CGTGAGGACCAG'),
        (4, 5, 9, 'CGGTTGGCGGGT'), (4, 5, 10, 'CGATTCCTTAAT'), (4, 5, 11, 'TGCCTGCTCGAC'),
        (4, 6, 0, 'TACTGTACTGTT'), (4, 6, 1,  'TCTCGCACTGGA'), (4, 6, 2,  'ACCAGTGACTCA'),
        (4, 6, 3, 'TGGCGCACGGAC'), (4, 6, 4,  'CATTTACATCAC'), (4, 6, 5,  'GTGGGACTGCGC'),
        (4, 6, 6, 'CGGCCTAAGTTC'), (4, 6, 7,  'GCTGAGCCTTTG'), (4, 6, 8,  'AGAGACGCGTAG'),
        (4, 6, 9, 'CCACCGGGCCGA'), (4, 6, 10, 'AATCCGGTCACC'), (4, 6, 11, 'TCTTACCCATAA'),
        (4, 7, 0, 'CTAGAGCTCCCA'), (4, 7, 1,  'GGTCTTAGCACC'), (4, 7, 2,  'GCCTACTCTCGG'),
        (4, 7, 3, 'ACTGCCCGATAC'), (4, 7, 4,  'TTCTTAACGCCT'), (4, 7, 5,  'CTCCCGAGCTCC'),
        (4, 7, 6, 'TAGACTTCAGAG'), (4, 7, 7,  'ACTTAGACTCTT'), (4, 7, 8,  'GGACCTGGATGG'),
        (4, 7, 9, 'TATGTGCCGGCT'), (4, 7, 10, 'ATACCGTCTTTC'), (4, 7, 11, 'TGTGCTTGTAGG'),
        -- Primer plate 5
        (5, 0, 0, 'ATGTTAGGGAAT'), (5, 0, 1,  'GCTAGTTATGGA'), (5, 0, 2,  'TCATCCGTCGGC'),
        (5, 0, 3, 'ATTTGGCTCTTA'), (5, 0, 4,  'GATCCGGCAGGA'), (5, 0, 5,  'GTTAAGCTGACC'),
        (5, 0, 6, 'CCTATTGCGGCC'), (5, 0, 7,  'CAATAGAATAAG'), (5, 0, 8,  'ACATAGCGGTTC'),
        (5, 0, 9, 'GCGTGGTCATTA'), (5, 0, 10, 'GATTCTTTAGAT'), (5, 0, 11, 'CGGATCTAGTGT'),
        (5, 1, 0, 'AAGTGGCTATCC'), (5, 1, 1,  'ACTAGTTGGACC'), (5, 1, 2,  'GGCTTCGGAGCG'),
        (5, 1, 3, 'CGCGTCAAACTA'), (5, 1, 4,  'CTTCCAACTCAT'), (5, 1, 5,  'GCCTAGCCCAAT'),
        (5, 1, 6, 'GTTAGGGAGCGA'), (5, 1, 7,  'TATACCGCTGCG'), (5, 1, 8,  'CTTACACTGCTT'),
        (5, 1, 9, 'CCTGCACCTGCA'), (5, 1, 10, 'AGGACAAACTAT'), (5, 1, 11, 'ATAACGGTGTAC'),
        (5, 2, 0, 'GTCGTTACCCGC'), (5, 2, 1,  'CGCAAGCCCGCG'), (5, 2, 2,  'CGGTCAATTGAC'),
        (5, 2, 3, 'ATGTTCCTCATC'), (5, 2, 4,  'CGACCTCGCATA'), (5, 2, 5,  'CATTCGTGGCGT'),
        (5, 2, 6, 'AGTACGCAGTCT'), (5, 2, 7,  'CAGTGCACGTCT'), (5, 2, 8,  'ACTCACAGGAAT'),
        (5, 2, 9, 'TGGTGTTTATAT'), (5, 2, 10, 'TCTTCCTAAAGT'), (5, 2, 11, 'GCCCTTCCCGTG'),
        (5, 3, 0, 'AGTATATGTTTC'), (5, 3, 1,  'AGAGCGGAACAA'), (5, 3, 2,  'TCCGCTGCTGAC'),
        (5, 3, 3, 'TCCGTGGTATAG'), (5, 3, 4,  'GTCAGAGTATTG'), (5, 3, 5,  'GCGGTCGGTCAG'),
        (5, 3, 6, 'TATCCTGGTTTC'), (5, 3, 7,  'CTGGTGCTGAAT'), (5, 3, 8,  'GTTGAAGCACCT'),
        (5, 3, 9, 'GTGCGGTTCACT'), (5, 3, 10, 'CTTGTGCGACAA'), (5, 3, 11, 'CACAGTTGAAGT'),
        (5, 4, 0, 'GGCTCGTCGGAG'), (5, 4, 1,  'ACATGGGCGGAA'), (5, 4, 2,  'TGCGCGCCTTCC'),
        (5, 4, 3, 'GTTGGTTGGCAT'), (5, 4, 4,  'GAACGATCATGT'), (5, 4, 5,  'TCAGTCAGATGA'),
        (5, 4, 6, 'CTGGTCTTACGG'), (5, 4, 7,  'ACAAAGGTATCA'), (5, 4, 8,  'GTAAACGACTTG'),
        (5, 4, 9, 'TAGCGCGAACTT'), (5, 4, 10, 'GCGCTTAGAATA'), (5, 4, 11, 'GCAAAGGCCCGC'),
        (5, 5, 0, 'GACATCTGACAC'), (5, 5, 1,  'CTGCGGATATAC'), (5, 5, 2,  'GCGCACACCTTC'),
        (5, 5, 3, 'AACGGGCGACGT'), (5, 5, 4,  'CTCCACATTCCT'), (5, 5, 5,  'CGAACGTCTATG'),
        (5, 5, 6, 'ATGCCGGTAATA'), (5, 5, 7,  'TGAACCCTATGG'), (5, 5, 8,  'TTGGACGTCCAC'),
        (5, 5, 9, 'ATGTAGGCTTAG'), (5, 5, 10, 'AGAGGAGTCGAC'), (5, 5, 11, 'CTCCCACTAGAG'),
        (5, 6, 0, 'AATTTCCTAACA'), (5, 6, 1,  'GTGAGGGCAAGT'), (5, 6, 2,  'CACGAAAGCAGG'),
        (5, 6, 3, 'TACTGAGCCTCG'), (5, 6, 4,  'TCTTCGCAGCAG'), (5, 6, 5,  'CAGTCCCTGCAC'),
        (5, 6, 6, 'ATCAAGATACGC'), (5, 6, 7,  'AATAAGCAATAG'), (5, 6, 8,  'GCACGCGAGCAC'),
        (5, 6, 9, 'GCATTACTGGAC'), (5, 6, 10, 'GTCTCCTCCCTT'), (5, 6, 11, 'AATAGATGCTGA'),
        (5, 7, 0, 'ATAAACGGACAT'), (5, 7, 1,  'ATATTGGCAGCC'), (5, 7, 2,  'CGTGGCTTTCCG'),
        (5, 7, 3, 'GGTGCAGACAGA'), (5, 7, 4,  'CACGCTATTGGA'), (5, 7, 5,  'TGATTTAATTGC'),
        (5, 7, 6, 'CTGAGGCCCTTC'), (5, 7, 7,  'TATGGGTAGCTA'), (5, 7, 8,  'CTTAGGCATGTG'),
        (5, 7, 9, 'TCCGGACTCCTG'), (5, 7, 10, 'AGTATCATATAT'), (5, 7, 11, 'AACGCTTCTTAT'),
        -- Primer plate 6
        (6, 0, 0, 'GTTCGGTGTCCA'), (6, 0, 1,  'CTACCGATTGCG'), (6, 0, 2,  'GAGAGTCCACTT'),
        (6, 0, 3, 'CTAACCTCATAT'), (6, 0, 4,  'AGCTTCGACAGT'), (6, 0, 5,  'GAGAGGGATCAC'),
        (6, 0, 6, 'TGGCCGTTACTG'), (6, 0, 7,  'TTCAGCGATGGT'), (6, 0, 8,  'AAGATCGTACTG'),
        (6, 0, 9, 'ATTTGAAGAGGT'), (6, 0, 10, 'GTCAATTAGTGG'), (6, 0, 11, 'CCTAAGAGCATC'),
        (6, 1, 0, 'GCAAGAATACAT'), (6, 1, 1,  'GGTAATAGAGTT'), (6, 1, 2,  'ATTTGCTTTGCC'),
        (6, 1, 3, 'CTTCGGAGGGAG'), (6, 1, 4,  'TAAGAAACGTCA'), (6, 1, 5,  'TTGCGACAAAGT'),
        (6, 1, 6, 'AGGAACCAGACG'), (6, 1, 7,  'CGTGGTGGGAAC'), (6, 1, 8,  'GTCATTGGGCTA'),
        (6, 1, 9, 'TCTACGGCACGT'), (6, 1, 10, 'AGCCCGCAAAGG'), (6, 1, 11, 'GAGCGCCGAACA'),
        (6, 2, 0, 'CAGGGTAGGGTA'), (6, 2, 1,  'GTAAATTCAGGC'), (6, 2, 2,  'ACCCGGATTTCG'),
        (6, 2, 3, 'GTGACCCTGTCA'), (6, 2, 4,  'AGCAACATTGCA'), (6, 2, 5,  'CAGTGTCATGAA'),
        (6, 2, 6, 'GTTGACCATCGC'), (6, 2, 7,  'AGACACCAATGT'), (6, 2, 8,  'CGCAGATTAGTA'),
        (6, 2, 9, 'TCCTAGGTCCGA'), (6, 2, 10, 'GGCCTATAAGTC'), (6, 2, 11, 'CTCTATTCCACC'),
        (6, 3, 0, 'CTAGTCGCTGGT'), (6, 3, 1,  'AATATCGGGATC'), (6, 3, 2,  'AAGCCTCTACGA'),
        (6, 3, 3, 'GAGAATGGAAAG'), (6, 3, 4,  'GCTTCATTTCTG'), (6, 3, 5,  'CATTCAGTTATA'),
        (6, 3, 6, 'CCAGATATAGCA'), (6, 3, 7,  'TCATACAGCCAG'), (6, 3, 8,  'CTCATATGCTAT'),
        (6, 3, 9, 'CTCTTCTGATCA'), (6, 3, 10, 'CGCGGCGCAGCT'), (6, 3, 11, 'ATGGATAGCTAA'),
        (6, 4, 0, 'AGAAGGCCTTAT'), (6, 4, 1,  'TGGACTCAGCTA'), (6, 4, 2,  'GCGATGGCGATG'),
        (6, 4, 3, 'TAGGAGAGACAG'), (6, 4, 4,  'CAGTAGCGATAT'), (6, 4, 5,  'CCACTCTCTCTA'),
        (6, 4, 6, 'TATCGTTATCGT'), (6, 4, 7,  'ATGTATCAATTA'), (6, 4, 8,  'CAAATGGTCGTC'),
        (6, 4, 9, 'ACACGCGGTTTA'), (6, 4, 10, 'AAGCCGGGTCCG'), (6, 4, 11, 'AGGACGCCAGCA'),
        (6, 5, 0, 'TTGGAACGGCTT'), (6, 5, 1,  'TGTTGCGTTTCT'), (6, 5, 2,  'TTATACGTTGTA'),
        (6, 5, 3, 'GGTGTGAGAAAG'), (6, 5, 4,  'GCCAAGGATAGG'), (6, 5, 5,  'GAACAAAGAGCG'),
        (6, 5, 6, 'ATTCGGTAGTGC'), (6, 5, 7,  'CGCTGGCTTTAG'), (6, 5, 8,  'CAGCTGGTTCAA'),
        (6, 5, 9, 'CTTGAGAAATCG'), (6, 5, 10, 'CGAGGGAAAGTC'), (6, 5, 11, 'GAATGCGTATAA'),
        (6, 6, 0, 'TACCTGTGTCTT'), (6, 6, 1,  'GCTATATCCAGG'), (6, 6, 2,  'CATGATTAAGAG'),
        (6, 6, 3, 'ACCTATGGTGAA'), (6, 6, 4,  'AATCTAACAATT'), (6, 6, 5,  'GTTCCATCGGCC'),
        (6, 6, 6, 'TGACGAGGGCTG'), (6, 6, 7,  'AGACAGTAGGAG'), (6, 6, 8,  'ATAGACACTCCG'),
        (6, 6, 9, 'ACGGCCCTGGAG'), (6, 6, 10, 'CTTCAAGATGGA'), (6, 6, 11, 'CACAATACACCG'),
        (6, 7, 0, 'GATGCGCAGGAC'), (6, 7, 1,  'TGAAAGCGGCGA'), (6, 7, 2,  'AGCACCGGTCTT'),
        (6, 7, 3, 'ACGCCGAGGTAG'), (6, 7, 4,  'CTCACGCAATGC'), (6, 7, 5,  'ATCGTTATATCA'),
        (6, 7, 6, 'TACTTAAACATC'), (6, 7, 7,  'GTGCGAGGACAA'), (6, 7, 8,  'CTTTGATAATAA'),
        (6, 7, 9, 'CATAAATTCTTG'), (6, 7, 10, 'CTGTAAAGGTTG'), (6, 7, 11, 'GGCAGTGTTAAT'),
        -- Primer plate 7
        (7, 0, 0, 'TAGACCGACTCC'), (7, 0, 1,  'TGGAATTCGGCT'), (7, 0, 2,  'GAAGATCTATCG'),
        (7, 0, 3, 'ATCGCCGCCTTG'), (7, 0, 4,  'TAGTGTCGGATC'), (7, 0, 5,  'TCAAGCAATACG'),
        (7, 0, 6, 'AGGGAGCTTCGG'), (7, 0, 7,  'CTGGTAAGTCCA'), (7, 0, 8,  'GGACTTCCAGCT'),
        (7, 0, 9, 'GGAGGAGCAATA'), (7, 0, 10, 'CATGAACAGTGT'), (7, 0, 11, 'TAGGTAACCGAT'),
        (7, 1, 0, 'GGAATCCGATTA'), (7, 1, 1,  'TTCCCACCCATT'), (7, 1, 2,  'GTCCCAGTCCCA'),
        (7, 1, 3, 'AGCCAGTCATAC'), (7, 1, 4,  'GTGTAATGTAGA'), (7, 1, 5,  'ATACTGAGTGAA'),
        (7, 1, 6, 'TGTATGCTTCTA'), (7, 1, 7,  'GAACTCGCTATG'), (7, 1, 8,  'CGATATCAGTAG'),
        (7, 1, 9, 'TCGTAGTAATGG'), (7, 1, 10, 'CGGGTCCTCTTG'), (7, 1, 11, 'GTCGGGCCGGTA'),
        (7, 2, 0, 'TCCGACCCGATC'), (7, 2, 1,  'CCGCATGACCTA'), (7, 2, 2,  'CACTAGACCCAC'),
        (7, 2, 3, 'AGTAATAACAAG'), (7, 2, 4,  'CTTCTTCGCCCT'), (7, 2, 5,  'TACACGCTGATG'),
        (7, 2, 6, 'GACGTCCCTCCA'), (7, 2, 7,  'TATTCTACATGA'), (7, 2, 8,  'GAGGCGCCATAG'),
        (7, 2, 9, 'GCAGAGAGGCTA'), (7, 2, 10, 'CGTTTATCCGTT'), (7, 2, 11, 'GCTAGACACTAC'),
        (7, 3, 0, 'TCACTGCTAGGA'), (7, 3, 1,  'GGTCCTTCCCGA'), (7, 3, 2,  'CGGTAGTTGATC'),
        (7, 3, 3, 'TGGTTTCGAAGA'), (7, 3, 4,  'CCGAAACGGAGC'), (7, 3, 5,  'TCTCCTAGGCGC'),
        (7, 3, 6, 'GTTTGCTCGAGA'), (7, 3, 7,  'TCGATAAGTAAG'), (7, 3, 8,  'AATCTCTATAAC'),
        (7, 3, 9, 'GAGTCCGTTGCT'), (7, 3, 10, 'TAACCACCAACG'), (7, 3, 11, 'TCGTCTGATATT'),
        (7, 4, 0, 'ACATCAGGTCAC'), (7, 4, 1,  'CAGACCGGACGA'), (7, 4, 2,  'AGTTATTCTAGT'),
        (7, 4, 3, 'GTAGGTGCTTAC'), (7, 4, 4,  'GTGGGCGGCCCT'), (7, 4, 5,  'AGTCTTAAAGGA'),
        (7, 4, 6, 'GTCTGACGGTCT'), (7, 4, 7,  'CCATAGGAGGCG'), (7, 4, 8,  'GTGGCGCATGGA'),
        (7, 4, 9, 'CAACTTAATGTT'), (7, 4, 10, 'TAGCGACCTCAC'), (7, 4, 11, 'CCAGCGCTTCAC'),
        (7, 5, 0, 'AGCTATGTATGG'), (7, 5, 1,  'TTCCGAATCGGC'), (7, 5, 2,  'CACATTCTATAA'),
        (7, 5, 3, 'CGGCGATGAAAG'), (7, 5, 4,  'GTTGGGATCCTC'), (7, 5, 5,  'TAATCATGTAAT'),
        (7, 5, 6, 'GAGTTCCATTGG'), (7, 5, 7,  'GCCGCGGGATCA'), (7, 5, 8,  'CGTGTTATGTGG'),
        (7, 5, 9, 'CTGTACTTCTAA'), (7, 5, 10, 'TAGGCATGCTTG'), (7, 5, 11, 'AATAGTCGTGAC'),
        (7, 6, 0, 'AATGACCTCGTG'), (7, 6, 1,  'GCATGTCGAAAT'), (7, 6, 2,  'GCGTTAACCCAA'),
        (7, 6, 3, 'GACCACTGCTGT'), (7, 6, 4,  'TTCACGCGCCCA'), (7, 6, 5,  'TAGGCGGTAGGC'),
        (7, 6, 6, 'ACACTCATTACT'), (7, 6, 7,  'TCTTAAGATTTG'), (7, 6, 8,  'AAGTAGGAAGGA'),
        (7, 6, 9, 'GGCCCTGTGGGC'), (7, 6, 10, 'ATCCATGAGCGT'), (7, 6, 11, 'GAGGCCTCGGGT'),
        (7, 7, 0, 'AAGGGTTAGTCT'), (7, 7, 1,  'ACGCGAACTAAT'), (7, 7, 2,  'TTCGACTAATAT'),
        (7, 7, 3, 'AATCATTTGTAA'), (7, 7, 4,  'TATGCTCTCTCA'), (7, 7, 5,  'TCATTCCACTCA'),
        (7, 7, 6, 'CAGAAATGTGTC'), (7, 7, 7,  'CTTATAGAGAAG'), (7, 7, 8,  'ATGCGCCCGTAT'),
        (7, 7, 9, 'GCATCGTCTGGT'), (7, 7, 10, 'GAGGCAAACGCC'), (7, 7, 11, 'GACTTGGTAAAC'),
        -- Primer plate 8
        (8, 0, 0, 'GCTTATTGCTTA'), (8, 0, 1,  'GACCATGTAGTA'), (8, 0, 2,  'CTTCGCGGATGT'),
        (8, 0, 3, 'TGAGCGCACGCG'), (8, 0, 4,  'CATGAGACTGTA'), (8, 0, 5,  'TTACCCGCACAG'),
        (8, 0, 6, 'AAGATTTGCAGC'), (8, 0, 7,  'AACCGATGTACC'), (8, 0, 8,  'GCCTTACGATAG'),
        (8, 0, 9, 'ACGACCTACGCT'), (8, 0, 10, 'ACGGTGAAAGCG'), (8, 0, 11, 'TGGGACATATCC'),
        (8, 1, 0, 'ATGGCCTGACTA'), (8, 1, 1,  'GCAAGCTGTCTC'), (8, 1, 2,  'ATCACATTCTCC'),
        (8, 1, 3, 'CGAGTATACAAC'), (8, 1, 4,  'CCAGGGACTTCT'), (8, 1, 5,  'ACAAGTGCTGCT'),
        (8, 1, 6, 'CACTCTCCGGCA'), (8, 1, 7,  'ATTAATGAAGCG'), (8, 1, 8,  'ACCGATTAGGTA'),
        (8, 1, 9, 'ATCGATCCACAG'), (8, 1, 10, 'CACCTCCAAGGT'), (8, 1, 11, 'CTAAATACCCTT'),
        (8, 2, 0, 'TCAATGACCGCA'), (8, 2, 1,  'TATCTTCCTGAA'), (8, 2, 2,  'AACGTCCTGTGC'),
        (8, 2, 3, 'TAAGCGTCTCGA'), (8, 2, 4,  'GAGGTATTCTGA'), (8, 2, 5,  'CGTAAGATGCCT'),
        (8, 2, 6, 'GGAGGGTACCGT'), (8, 2, 7,  'TCAAGATCAAGA'), (8, 2, 8,  'TGCAACTTGCAG'),
        (8, 2, 9, 'TACTAGATATTA'), (8, 2, 10, 'TACGTTTGGCGA'), (8, 2, 11, 'GTTGTATTATAC'),
        (8, 3, 0, 'CTTTATGTGTCA'), (8, 3, 1,  'GGTACTGTACCA'), (8, 3, 2,  'AAGGTGGACAAG'),
        (8, 3, 3, 'ACGCTCCCATCG'), (8, 3, 4,  'AGAGCTCCTCTG'), (8, 3, 5,  'GCGTACGGGTGA'),
        (8, 3, 6, 'AAGCGTACATTG'), (8, 3, 7,  'CTGTTACAGCGA'), (8, 3, 8,  'CCGAGTACAATC'),
        (8, 3, 9, 'GGTCTCCTACAG'), (8, 3, 10, 'CTCCTGTCCGGA'), (8, 3, 11, 'AGCCTGGTACCT'),
        (8, 4, 0, 'GGTCGAATTGCT'), (8, 4, 1,  'TCAACTATGTCT'), (8, 4, 2,  'TATAGAAGAATG'),
        (8, 4, 3, 'CTAATATTTGAA'), (8, 4, 4,  'GAGCATTACATG'), (8, 4, 5,  'ATATACCTGCGG'),
        (8, 4, 6, 'CAATATTCAATA'), (8, 4, 7,  'AAGTGCTTGGTA'), (8, 4, 8,  'GCGGAGCACGTC'),
        (8, 4, 9, 'TCCCGCCTACGC'), (8, 4, 10, 'CCTGGTGTCCGT'), (8, 4, 11, 'GGTCCCGAAATT'),
        (8, 5, 0, 'TTACCACATCTA'), (8, 5, 1,  'TGGCATGTTGGT'), (8, 5, 2,  'GTGTGCTAACGT'),
        (8, 5, 3, 'TGAGTTCGGTCC'), (8, 5, 4,  'AGACAAGCTTCC'), (8, 5, 5,  'TATAATCCGAGG'),
        (8, 5, 6, 'ATAAAGAGGAGG'), (8, 5, 7,  'AGTTTGCGAGAT'), (8, 5, 8,  'AAGCTAAAGCTA'),
        (8, 5, 9, 'ACCCTGGGTATC'), (8, 5, 10, 'GGAAGCTTAACT'), (8, 5, 11, 'GACAATTCCGAA'),
        (8, 6, 0, 'ATGCAACTCGAA'), (8, 6, 1,  'ATCATCTCGGCG'), (8, 6, 2,  'GTCTATACATAT'),
        (8, 6, 3, 'CTCAGGAGACTT'), (8, 6, 4,  'CATCCTGAGCAA'), (8, 6, 5,  'GTGACTAGTGAT'),
        (8, 6, 6, 'TCATGTGAACGA'), (8, 6, 7,  'CACTTGCTCTCT'), (8, 6, 8,  'ACAATCCCGAGT'),
        (8, 6, 9, 'GTTCCCAACGGT'), (8, 6, 10, 'ATAATCTAATCC'), (8, 6, 11, 'TAGGTCTAGGTC'),
        (8, 7, 0, 'TTGGTGCCTGTG'), (8, 7, 1,  'ATTGGGACATAA'), (8, 7, 2,  'AGTTCGGCATTG'),
        (8, 7, 3, 'TCTGATCGAGGT'), (8, 7, 4,  'GAATGACGTTTG'), (8, 7, 5,  'GAAGGAAAGTAG'),
        (8, 7, 6, 'AACTGGAACCCT'), (8, 7, 7,  'AGGAATACTCAC'), (8, 7, 8,  'CCATCGACGCTC'),
        (8, 7, 9, 'GTCACCAATCCG'), (8, 7, 10, 'GCCAGGCTTCCT'), (8, 7, 11, 'GCACCAATCTGC');

-- Add some control samples
INSERT INTO pm.sample (sample_id, is_blank, details)
    VALUES ('BLANK', TRUE, NULL),
           ('SWAB', TRUE, NULL),
           ('PCRCONTROL', TRUE, NULL);

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
