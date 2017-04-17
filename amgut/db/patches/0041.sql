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

 CREATE TABLE pm.run_pool (
  	run_pool_id          bigserial  NOT NULL,
  	name                 varchar  NOT NULL,
  	volume               real  NOT NULL,
  	notes                varchar  ,
  	CONSTRAINT pk_run_pool PRIMARY KEY ( run_pool_id ),
  	CONSTRAINT idx_run_pool UNIQUE ( name )
 ) ;


CREATE TYPE reagent_type AS ENUM ('MiSeq v3 150 cycle');

CREATE TYPE assay_type AS ENUM ('Kapa Hyper Plus', 'TrueSeq HT');

CREATE TABLE pm.run (
    run_id               bigserial  NOT NULL,
    name                 varchar  NOT NULL,
    email                varchar  ,
    created_on           timestamp  ,
    notes                varchar  ,
    run_pool_id          bigint NOT NULL,
    sequencer            varchar,
    reagent_type         reagent_type NOT NULL,
    reagent_lot          varchar,
    platform             seq_platform,
    instrument_model     seq_instrument_model,
    assay                assay_type,
    fwd_cycles           integer  NOT NULL,
    rev_cycles           integer  NOT NULL,
    CONSTRAINT pk_run PRIMARY KEY ( run_id ),
    CONSTRAINT uq_run_name UNIQUE ( name ) ,
    CONSTRAINT fk_run_labadmin_users FOREIGN KEY ( email ) REFERENCES ag.labadmin_users( email ),
    CONSTRAINT fk_run_run_pool FOREIGN KEY ( run_pool_id ) REFERENCES pm.run_pool( run_pool_id )
 );
CREATE INDEX idx_run_email ON pm.run ( email );
CREATE INDEX idx_run_pool_link ON pm.run ( run_pool_id ) ;

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

CREATE TYPE target_region AS ENUM ('16S', '18S', 'ITS');
CREATE TYPE target_subfragment AS ENUM ('V4');

CREATE TABLE pm.targeted_primer_plate (
    targeted_primer_plate_id   bigserial  NOT NULL,
    name                       varchar  NOT NULL,
    plate_type_id              bigint  NOT NULL,
    notes                      varchar  ,
    linker_primer_sequence     varchar NOT NULL,
    target_gene                target_region NOT NULL,
    target_subfragment         target_subfragment NOT NULL,
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

 CREATE TYPE shotgun_index_type AS ENUM ('iTru7', 'iTru5', 'NEXTflex');

 CREATE TABLE pm.shotgun_index (
	shotgun_index_id     varchar  NOT NULL,
	bases                varchar  NOT NULL,
	shotgun_index        shotgun_index_type  NOT NULL,
	CONSTRAINT idx_shotgun_index PRIMARY KEY ( shotgun_index_id )
 );

 CREATE TABLE pm.shotgun_normalized_plate_well_values (
	shotgun_normalized_plate_id bigint  NOT NULL,
	row                  integer  NOT NULL,
	col                  integer  NOT NULL,
	sample_volume_nl     real  NOT NULL,
	water_volume_nl      real  NOT NULL,
	shotgun_i5_index_id  varchar  ,
	shotgun_i7_index_id  varchar  ,
	i5_i7_index          integer  ,
	qpcr_concentration   real  ,
	qpcr_cp              real  ,
	shotgun_index_aliquot bigint
 );
 CREATE INDEX idx_wgs_normalized_plate_well_values ON pm.shotgun_normalized_plate_well_values ( shotgun_normalized_plate_id );
 CREATE INDEX idx_wgs_normalized_plate_well_values_0 ON pm.shotgun_normalized_plate_well_values ( shotgun_i5_index_id );
 CREATE INDEX idx_wgs_normalized_plate_well_values_1 ON pm.shotgun_normalized_plate_well_values ( shotgun_i7_index_id );
 ALTER TABLE pm.shotgun_normalized_plate_well_values ADD CONSTRAINT fk_wgs_normalized_plate_well_values FOREIGN KEY ( shotgun_normalized_plate_id ) REFERENCES pm.shotgun_normalized_plate( shotgun_normalized_plate_id );
 ALTER TABLE pm.shotgun_normalized_plate_well_values ADD CONSTRAINT fk_wgs_normalized_plate_well_values_i5 FOREIGN KEY ( shotgun_i5_index_id ) REFERENCES pm.shotgun_index( shotgun_index_id );
 ALTER TABLE pm.shotgun_normalized_plate_well_values ADD CONSTRAINT fk_shotgun_normalized_plate_well_values_aliquot FOREIGN KEY ( shotgun_index_aliquot ) REFERENCES pm.shotgun_index_aliquot( shotgun_index_aliquot_id );
 ALTER TABLE pm.shotgun_normalized_plate_well_values ADD CONSTRAINT fk_shotgun_normalized_plate_well_values FOREIGN KEY ( shotgun_i7_index_id ) REFERENCES pm.shotgun_index( shotgun_index_id );

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
    VALUES ('96-well', 12, 8, 'Standard 96-well plate'),
           ('384-well', 24, 16, 'Standard 384-well plate');

INSERT INTO pm.extraction_robot (name)
    VALUES ('HOWE_KF1'), ('HOWE_KF2'), ('HOWE_KF3'), ('HOWE_KF4');

INSERT INTO pm.extraction_tool (name)
    VALUES ('108379Z');

INSERT INTO pm.processing_robot (name)
    VALUES ('ROBE'), ('RIKE'), ('JERE'), ('CARMEN');

INSERT INTO pm.qpcr (name)
    VALUES ('QPCR-KL-1234');

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
INSERT INTO pm.targeted_primer_plate (name, plate_type_id, linker_primer_sequence, target_gene, target_subfragment)
    VALUES ('Primer plate 1', 1, 'GTGTGCCAGCMGCCGCGGTAA', '16S', 'V4'), ('Primer plate 2', 1, 'GTGTGCCAGCMGCCGCGGTAA', '16S', 'V4'),
           ('Primer plate 3', 1, 'GTGTGCCAGCMGCCGCGGTAA', '16S', 'V4'), ('Primer plate 4', 1, 'GTGTGCCAGCMGCCGCGGTAA', '16S', 'V4'),
           ('Primer plate 5', 1, 'GTGTGCCAGCMGCCGCGGTAA', '16S', 'V4'), ('Primer plate 6', 1, 'GTGTGCCAGCMGCCGCGGTAA', '16S', 'V4'),
           ('Primer plate 7', 1, 'GTGTGCCAGCMGCCGCGGTAA', '16S', 'V4'), ('Primer plate 8', 1, 'GTGTGCCAGCMGCCGCGGTAA', '16S', 'V4');

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

-- Add a plate
INSERT INTO pm.plate_reader (name, notes)
    VALUES ('PR1234', 'Standard plate reader');

-- Add a mosquito machine
INSERT INTO pm.mosquito (name, notes)
    VALUES ('Mosquito1', 'Standard mosquito machine');

-- Add shotgun_index valid values
INSERT INTO pm.shotgun_index (shotgun_index_id, bases, shotgun_index)
    VALUES
        ('NEXTflex1', 'ATCTAGCCGGCC', 'NEXTflex'),
        ('NEXTflex2', 'TATCTCTTCCTT', 'NEXTflex'),
        ('NEXTflex3', 'TAGATGCCGTCC', 'NEXTflex'),
        ('NEXTflex4', 'CGCTCCTTCCTT', 'NEXTflex'),
        ('NEXTflex5', 'CGAGCGCCGTCC', 'NEXTflex'),
        ('NEXTflex6', 'TCGAGAGTCCGG', 'NEXTflex'),
        ('NEXTflex7', 'GCTCGGCCGGCC', 'NEXTflex'),
        ('NEXTflex8', 'AGCTCAGTCCGG', 'NEXTflex'),
        ('NEXTflex9', 'ACTGCCGCGTCC', 'NEXTflex'),
        ('NEXTflex10', 'TTACTTCTCCGG', 'NEXTflex'),
        ('NEXTflex11', 'TGACGCGCGGCC', 'NEXTflex'),
        ('NEXTflex12', 'AATGATCTCCGG', 'NEXTflex'),
        ('NEXTflex13', 'AAGCGTACGTCC', 'NEXTflex'),
        ('NEXTflex14', 'TTATCAGTCCTT', 'NEXTflex'),
        ('NEXTflex15', 'GTCATCGCGTCC', 'NEXTflex'),
        ('NEXTflex16', 'CCGTCTCTCCGG', 'NEXTflex'),
        ('NEXTflex17', 'TTCGCTACGTCC', 'NEXTflex'),
        ('NEXTflex18', 'ACGCTCTTCCGG', 'NEXTflex'),
        ('NEXTflex19', 'CAGTACGCGGCC', 'NEXTflex'),
        ('NEXTflex20', 'GTACTGATCCTT', 'NEXTflex'),
        ('NEXTflex21', 'GGATATACGGCC', 'NEXTflex'),
        ('NEXTflex22', 'CATAGCTTCCGG', 'NEXTflex'),
        ('NEXTflex23', 'GAGGCATCGGCC', 'NEXTflex'),
        ('NEXTflex24', 'ATAAGGATCCGG', 'NEXTflex'),
        ('NEXTflex25', 'CTCCGATCGTCC', 'NEXTflex'),
        ('NEXTflex26', 'TATTCGATCCGG', 'NEXTflex'),
        ('NEXTflex27', 'TCTTAATCGTCC', 'NEXTflex'),
        ('NEXTflex28', 'CGCCTGATCCGG', 'NEXTflex'),
        ('NEXTflex29', 'AGAATATCGTCC', 'NEXTflex'),
        ('NEXTflex30', 'GCGGAGATCCGG', 'NEXTflex'),
        ('NEXTflex31', 'CATGGCCGGTCC', 'NEXTflex'),
        ('NEXTflex32', 'GTCACGTACCTT', 'NEXTflex'),
        ('NEXTflex33', 'TGCAACCGGTCC', 'NEXTflex'),
        ('NEXTflex34', 'CCTGTTGACCGG', 'NEXTflex'),
        ('NEXTflex35', 'AGCCCAAGGTCC', 'NEXTflex'),
        ('NEXTflex36', 'GCTTGGTACCGG', 'NEXTflex'),
        ('NEXTflex37', 'TCGGGAAGGTCC', 'NEXTflex'),
        ('NEXTflex38', 'CGAACGTACCGG', 'NEXTflex'),
        ('NEXTflex39', 'GATTTAAGGGCC', 'NEXTflex'),
        ('NEXTflex40', 'AGAACTGACCTT', 'NEXTflex'),
        ('NEXTflex41', 'CCGCCTTGGTCC', 'NEXTflex'),
        ('NEXTflex42', 'TGATGCAACCGG', 'NEXTflex'),
        ('NEXTflex43', 'GGCGGTTGGGCC', 'NEXTflex'),
        ('NEXTflex44', 'ACTACCAACCGG', 'NEXTflex'),
        ('NEXTflex45', 'AATAATTGGTCC', 'NEXTflex'),
        ('NEXTflex46', 'GTCGTCAACCGG', 'NEXTflex'),
        ('NEXTflex47', 'AAATCTCAGGCC', 'NEXTflex'),
        ('NEXTflex48', 'GTGCGCGGCCGG', 'NEXTflex'),
        ('NEXTflex49', 'TTTAGTCAGTCC', 'NEXTflex'),
        ('NEXTflex50', 'CACGCCGGCCGG', 'NEXTflex'),
        ('NEXTflex51', 'CCCGATCAGTCC', 'NEXTflex'),
        ('NEXTflex52', 'TGTATCGGCCGG', 'NEXTflex'),
        ('NEXTflex53', 'CTTTCAGAGTCC', 'NEXTflex'),
        ('NEXTflex54', 'TACCGGCGCCGG', 'NEXTflex'),
        ('NEXTflex55', 'GAAAGAGAGTCC', 'NEXTflex'),
        ('NEXTflex56', 'CTGGCTAGCCTT', 'NEXTflex'),
        ('NEXTflex57', 'AGGGAAGAGGCC', 'NEXTflex'),
        ('NEXTflex58', 'GACCGTAGCCTT', 'NEXTflex'),
        ('NEXTflex59', 'TCCCTAGAGTCC', 'NEXTflex'),
        ('NEXTflex60', 'AGTTATAGCCTT', 'NEXTflex'),
        ('NEXTflex61', 'GCCTCGAAGTCC', 'NEXTflex'),
        ('NEXTflex62', 'CGTCGCGGCCTT', 'NEXTflex'),
        ('NEXTflex63', 'CGGAGGAAGGCC', 'NEXTflex'),
        ('NEXTflex64', 'GCAGCCGGCCTT', 'NEXTflex'),
        ('NEXTflex65', 'TAAGAGAAGTCC', 'NEXTflex'),
        ('NEXTflex66', 'ATGATCGGCCTT', 'NEXTflex'),
        ('NEXTflex67', 'ATTCTGAAGTCC', 'NEXTflex'),
        ('NEXTflex68', 'TACTACGGCCTT', 'NEXTflex'),
        ('NEXTflex69', 'TGGTCCTAGTCC', 'NEXTflex'),
        ('NEXTflex70', 'AACATTAGCCGG', 'NEXTflex'),
        ('NEXTflex71', 'ACCAGCTAGTCC', 'NEXTflex'),
        ('NEXTflex72', 'TTGTATAGCCGG', 'NEXTflex'),
        ('NEXTflex73', 'GTTGACTAGTCC', 'NEXTflex'),
        ('NEXTflex74', 'CCACGTAGCCGG', 'NEXTflex'),
        ('NEXTflex75', 'CAACTCTAGTCC', 'NEXTflex'),
        ('NEXTflex76', 'TGTGCGCGCCTT', 'NEXTflex'),
        ('NEXTflex77', 'GGTACTGTGGCC', 'NEXTflex'),
        ('NEXTflex78', 'AAATTAACCCTT', 'NEXTflex'),
        ('NEXTflex79', 'TTGCATGTGGCC', 'NEXTflex'),
        ('NEXTflex80', 'CCCGGAACCCTT', 'NEXTflex'),
        ('NEXTflex81', 'AACGTTGTGTCC', 'NEXTflex'),
        ('NEXTflex82', 'GGGCCAACCCTT', 'NEXTflex'),
        ('NEXTflex83', 'CACACCATGTCC', 'NEXTflex'),
        ('NEXTflex84', 'TTTGGTTCCCGG', 'NEXTflex'),
        ('NEXTflex85', 'GTGTGCATGTCC', 'NEXTflex'),
        ('NEXTflex86', 'CCCAATTCCCGG', 'NEXTflex'),
        ('NEXTflex87', 'TGTGTCATGTCC', 'NEXTflex'),
        ('NEXTflex88', 'AAACCTTCCCGG', 'NEXTflex'),
        ('NEXTflex89', 'ATGACGTTGTCC', 'NEXTflex'),
        ('NEXTflex90', 'TCCTTAACCCGG', 'NEXTflex'),
        ('NEXTflex91', 'CGTCAGTTGTCC', 'NEXTflex'),
        ('NEXTflex92', 'GAAGGAACCCGG', 'NEXTflex'),
        ('NEXTflex93', 'GCAGTGTTGGCC', 'NEXTflex'),
        ('NEXTflex94', 'CTTCCAACCCGG', 'NEXTflex'),
        ('NEXTflex95', 'GTATGACCAGCC', 'NEXTflex'),
        ('NEXTflex96', 'CCTAAGGTTCGG', 'NEXTflex'),
        ('NEXTflex97', 'TGCGTACCATCC', 'NEXTflex'),
        ('NEXTflex98', 'AAGCCGGTTCGG', 'NEXTflex'),
        ('NEXTflex99', 'ATAACTGCATCC', 'NEXTflex'),
        ('NEXTflex100', 'GAGGGCCTTCGG', 'NEXTflex'),
        ('NEXTflex101', 'TATTGTGCAGCC', 'NEXTflex'),
        ('NEXTflex102', 'AGAAACCTTCGG', 'NEXTflex'),
        ('NEXTflex103', 'CGCCATGCATCC', 'NEXTflex'),
        ('NEXTflex104', 'TCTTTCCTTCGG', 'NEXTflex'),
        ('NEXTflex105', 'GCGGTTGCATCC', 'NEXTflex'),
        ('NEXTflex106', 'ATCCCAATTCTT', 'NEXTflex'),
        ('NEXTflex107', 'TCGACCACAGCC', 'NEXTflex'),
        ('NEXTflex108', 'CTCTTGGTTCTT', 'NEXTflex'),
        ('NEXTflex109', 'AGCTGCACAGCC', 'NEXTflex'),
        ('NEXTflex110', 'TCTCCGGTTCTT', 'NEXTflex'),
        ('NEXTflex111', 'CTAGTCACAGCC', 'NEXTflex'),
        ('NEXTflex112', 'GAGAAGGTTCTT', 'NEXTflex'),
        ('NEXTflex113', 'CCGTGGTCATCC', 'NEXTflex'),
        ('NEXTflex114', 'TGACCAATTCGG', 'NEXTflex'),
        ('NEXTflex115', 'TTACAGTCATCC', 'NEXTflex'),
        ('NEXTflex116', 'CAGTTAATTCGG', 'NEXTflex'),
        ('NEXTflex117', 'AATGTGTCAGCC', 'NEXTflex'),
        ('NEXTflex118', 'TTCAACCTTCTT', 'NEXTflex'),
        ('NEXTflex119', 'GCTTCTCGATCC', 'NEXTflex'),
        ('NEXTflex120', 'ATAATATATCTT', 'NEXTflex'),
        ('NEXTflex121', 'CGAAGTCGATCC', 'NEXTflex'),
        ('NEXTflex122', 'TCGGCCGATCGG', 'NEXTflex'),
        ('NEXTflex123', 'TAGGATCGATCC', 'NEXTflex'),
        ('NEXTflex124', 'CTAATCGATCGG', 'NEXTflex'),
        ('NEXTflex125', 'ATCCTTCGATCC', 'NEXTflex'),
        ('NEXTflex126', 'GATTACGATCGG', 'NEXTflex'),
        ('NEXTflex127', 'TGATCAGGAGCC', 'NEXTflex'),
        ('NEXTflex128', 'CCGCGGCATCGG', 'NEXTflex'),
        ('NEXTflex129', 'ACTAGAGGATCC', 'NEXTflex'),
        ('NEXTflex130', 'GTATATAATCTT', 'NEXTflex'),
        ('NEXTflex131', 'GTCGAAGGAGCC', 'NEXTflex'),
        ('NEXTflex132', 'AATATGCATCGG', 'NEXTflex'),
        ('NEXTflex133', 'CAGCTAGGATCC', 'NEXTflex'),
        ('NEXTflex134', 'TGCGCTAATCTT', 'NEXTflex'),
        ('NEXTflex135', 'TTCAGGAGAGCC', 'NEXTflex'),
        ('NEXTflex136', 'ACGTAATATCGG', 'NEXTflex'),
        ('NEXTflex137', 'CCTGAGAGATCC', 'NEXTflex'),
        ('NEXTflex138', 'TTACGCGATCTT', 'NEXTflex'),
        ('NEXTflex139', 'GGACTGAGATCC', 'NEXTflex'),
        ('NEXTflex140', 'CATGCATATCGG', 'NEXTflex'),
        ('NEXTflex141', 'CTCTCCTGATCC', 'NEXTflex'),
        ('NEXTflex142', 'GATCGGCATCTT', 'NEXTflex'),
        ('NEXTflex143', 'GAGAGCTGAGCC', 'NEXTflex'),
        ('NEXTflex144', 'ATAGCTAATCGG', 'NEXTflex'),
        ('NEXTflex145', 'AGAGACTGATCC', 'NEXTflex'),
        ('NEXTflex146', 'TCGATGCATCTT', 'NEXTflex'),
        ('NEXTflex147', 'TCTCTCTGAGCC', 'NEXTflex'),
        ('NEXTflex148', 'CGCTATAATCGG', 'NEXTflex'),
        ('NEXTflex149', 'TCAGGCCAAGCC', 'NEXTflex'),
        ('NEXTflex150', 'CGGACTGGTCGG', 'NEXTflex'),
        ('NEXTflex151', 'CTGAACCAATCC', 'NEXTflex'),
        ('NEXTflex152', 'GCCTGTGGTCGG', 'NEXTflex'),
        ('NEXTflex153', 'GACTTCCAAGCC', 'NEXTflex'),
        ('NEXTflex154', 'CTTCAGTGTCTT', 'NEXTflex'),
        ('NEXTflex155', 'CCACCGGAATCC', 'NEXTflex'),
        ('NEXTflex156', 'TGGTGACGTCGG', 'NEXTflex'),
        ('NEXTflex157', 'AACAAGGAAGCC', 'NEXTflex'),
        ('NEXTflex158', 'GTTGTACGTCGG', 'NEXTflex'),
        ('NEXTflex159', 'TTGTTGGAATCC', 'NEXTflex'),
        ('NEXTflex160', 'AAACACAGTCTT', 'NEXTflex'),
        ('NEXTflex161', 'ATGGGTTAATCC', 'NEXTflex'),
        ('NEXTflex162', 'GAAACCAGTCGG', 'NEXTflex'),
        ('NEXTflex163', 'GCAAATTAACCC', 'NEXTflex'),
        ('NEXTflex164', 'CTTTGCAGTGGG', 'NEXTflex'),
        ('NEXTflex165', 'TTTGCGCTATCC', 'NEXTflex'),
        ('NEXTflex166', 'CCACTCTCTCTT', 'NEXTflex'),
        ('NEXTflex167', 'AAACGGCTATCC', 'NEXTflex'),
        ('NEXTflex168', 'TGTGAAGCTCGG', 'NEXTflex'),
        ('NEXTflex169', 'GGGTAGCTATCC', 'NEXTflex'),
        ('NEXTflex170', 'AACAGCTCTCTT', 'NEXTflex'),
        ('NEXTflex171', 'CCCATGCTAGCC', 'NEXTflex'),
        ('NEXTflex172', 'TTGTCCTCTCTT', 'NEXTflex'),
        ('NEXTflex173', 'GAAGCCGTATCC', 'NEXTflex'),
        ('NEXTflex174', 'CTGAGGACTCTT', 'NEXTflex'),
        ('NEXTflex175', 'CTTCGCGTAGCC', 'NEXTflex'),
        ('NEXTflex176', 'GACTCGACTCTT', 'NEXTflex'),
        ('NEXTflex177', 'TCCTACGTATCC', 'NEXTflex'),
        ('NEXTflex178', 'AGTCTGACTCTT', 'NEXTflex'),
        ('NEXTflex179', 'ATGGCGCGCTGG', 'NEXTflex'),
        ('NEXTflex180', 'GCCCTCTAGCAA', 'NEXTflex'),
        ('NEXTflex181', 'CGTTAGCGCGGG', 'NEXTflex'),
        ('NEXTflex182', 'TAAAGCTAGCAA', 'NEXTflex'),
        ('NEXTflex183', 'GCAATGCGCTGG', 'NEXTflex'),
        ('NEXTflex184', 'ATTTCCTAGCAA', 'NEXTflex'),
        ('NEXTflex185', 'GGTGCTAGCTGG', 'NEXTflex'),
        ('NEXTflex186', 'CCCAGAGAGCAA', 'NEXTflex'),
        ('NEXTflex187', 'TCAGCATGCTGG', 'NEXTflex'),
        ('NEXTflex188', 'AGGAGTCAGCAA', 'NEXTflex'),
        ('NEXTflex189', 'AGTCGATGCTGG', 'NEXTflex'),
        ('NEXTflex190', 'GAAGATCAGCAA', 'NEXTflex'),
        ('NEXTflex191', 'GACTAATGCTGG', 'NEXTflex'),
        ('NEXTflex192', 'CTTCTTCAGCAA', 'NEXTflex'),
        ('NEXTflex193', 'CTGATATGCTGG', 'NEXTflex'),
        ('NEXTflex194', 'TCCTCTCAGCAA', 'NEXTflex'),
        ('NEXTflex195', 'GAGACACACGGG', 'NEXTflex'),
        ('NEXTflex196', 'CTAGGTTGGCAA', 'NEXTflex'),
        ('NEXTflex197', 'CTCTGACACTGG', 'NEXTflex'),
        ('NEXTflex198', 'TCGAATTGGCAA', 'NEXTflex'),
        ('NEXTflex199', 'AGAGTACACTGG', 'NEXTflex'),
        ('NEXTflex200', 'GATCCTTGGCAA', 'NEXTflex'),
        ('NEXTflex201', 'TTCACTGACGGG', 'NEXTflex'),
        ('NEXTflex202', 'CCGTTAAGGCAA', 'NEXTflex'),
        ('NEXTflex203', 'AAGTGTGACTGG', 'NEXTflex'),
        ('NEXTflex204', 'TTACCAAGGCAA', 'NEXTflex'),
        ('NEXTflex205', 'ATCCAGTACGGG', 'NEXTflex'),
        ('NEXTflex206', 'TATTTCCGGCAA', 'NEXTflex'),
        ('NEXTflex207', 'TAGGTGTACCGG', 'NEXTflex'),
        ('NEXTflex208', 'ATAAACCGGTAA', 'NEXTflex'),
        ('NEXTflex209', 'CTAGAAGTCCGG', 'NEXTflex'),
        ('NEXTflex210', 'GAGATTACGTAA', 'NEXTflex'),
        ('NEXTflex211', 'GATCTAGTCCGG', 'NEXTflex'),
        ('NEXTflex212', 'AGAGCTACGGAA', 'NEXTflex'),
        ('NEXTflex213', 'TTGACCATGTGG', 'NEXTflex'),
        ('NEXTflex214', 'CCCTTGGCCCAA', 'NEXTflex'),
        ('NEXTflex215', 'GCATGACTGTGG', 'NEXTflex'),
        ('NEXTflex216', 'ATTAATTCCCAA', 'NEXTflex'),
        ('NEXTflex217', 'CGTACACTGTGG', 'NEXTflex'),
        ('NEXTflex218', 'GCCGGTTCCCAA', 'NEXTflex'),
        ('NEXTflex219', 'TTTCTCTAGTGG', 'NEXTflex'),
        ('NEXTflex220', 'CCAGCGCGCCAA', 'NEXTflex'),
        ('NEXTflex221', 'AAAGACTAGTGG', 'NEXTflex'),
        ('NEXTflex222', 'TTGATGCGCCAA', 'NEXTflex'),
        ('NEXTflex223', 'GAACTGAAGTGG', 'NEXTflex'),
        ('NEXTflex224', 'AGTGCCGGCCAA', 'NEXTflex'),
        ('NEXTflex225', 'CTTGAGAAGTGG', 'NEXTflex'),
        ('NEXTflex226', 'TCACGCGGCCAA', 'NEXTflex'),
        ('NEXTflex227', 'TCCAGGAAGTGG', 'NEXTflex'),
        ('NEXTflex228', 'CTGTACGGCCAA', 'NEXTflex'),
        ('NEXTflex229', 'AGGTCGAAGTGG', 'NEXTflex'),
        ('NEXTflex230', 'GACATCGGCCAA', 'NEXTflex'),
        ('NEXTflex231', 'CGGCTAGAGTGG', 'NEXTflex'),
        ('NEXTflex232', 'TACGCTAGCCAA', 'NEXTflex'),
        ('NEXTflex233', 'GCCGAAGAGTGG', 'NEXTflex'),
        ('NEXTflex234', 'CGTATTAGCCAA', 'NEXTflex'),
        ('NEXTflex235', 'ATTAGAGAGTGG', 'NEXTflex'),
        ('NEXTflex236', 'GCATATAGCCAA', 'NEXTflex'),
        ('NEXTflex237', 'TAATCAGAGTGG', 'NEXTflex'),
        ('NEXTflex238', 'ATGCGTAGCCAA', 'NEXTflex'),
        ('NEXTflex239', 'ACCCTTCAGTGG', 'NEXTflex'),
        ('NEXTflex240', 'GTGGCATGCCAA', 'NEXTflex'),
        ('NEXTflex241', 'TGGGATCAGTGG', 'NEXTflex'),
        ('NEXTflex242', 'CACCGATGCCAA', 'NEXTflex'),
        ('NEXTflex243', 'CAAAGTCAGTGG', 'NEXTflex'),
        ('NEXTflex244', 'TGTTAATGCCAA', 'NEXTflex'),
        ('NEXTflex245', 'GTTTCTCAGTGG', 'NEXTflex'),
        ('NEXTflex246', 'ACAATATGCCAA', 'NEXTflex'),
        ('NEXTflex247', 'GTAAATTGGTGG', 'NEXTflex'),
        ('NEXTflex248', 'ACTTGACACCAA', 'NEXTflex'),
        ('NEXTflex249', 'ACGGGTTGGTGG', 'NEXTflex'),
        ('NEXTflex250', 'TGAACACACCAA', 'NEXTflex'),
        ('NEXTflex251', 'TGCCCTTGGTGG', 'NEXTflex'),
        ('NEXTflex252', 'CAGGTACACCAA', 'NEXTflex'),
        ('NEXTflex253', 'ATATTAAGGTGG', 'NEXTflex'),
        ('NEXTflex254', 'GCTACTGACCAA', 'NEXTflex'),
        ('NEXTflex255', 'CGCGGAAGGTGG', 'NEXTflex'),
        ('NEXTflex256', 'TAGCATGACCAA', 'NEXTflex'),
        ('NEXTflex257', 'GCGCCAAGGTGG', 'NEXTflex'),
        ('NEXTflex258', 'CGATGTGACCAA', 'NEXTflex'),
        ('NEXTflex259', 'GGCTTCCGGTGG', 'NEXTflex'),
        ('NEXTflex260', 'CCTCAGTACCAA', 'NEXTflex'),
        ('NEXTflex261', 'TTAGGCCGGTGG', 'NEXTflex'),
        ('NEXTflex262', 'AAGACGTACCAA', 'NEXTflex'),
        ('NEXTflex263', 'GCTATATCGTGG', 'NEXTflex'),
        ('NEXTflex264', 'ATATCTCTCCAA', 'NEXTflex'),
        ('NEXTflex265', 'CGATAATCGTGG', 'NEXTflex'),
        ('NEXTflex266', 'TATAGTCTCCAA', 'NEXTflex'),
        ('NEXTflex267', 'TAGCGATCGTGG', 'NEXTflex'),
        ('NEXTflex268', 'CGCGATCTCCAA', 'NEXTflex'),
        ('NEXTflex269', 'ATCGCATCGTGG', 'NEXTflex'),
        ('NEXTflex270', 'GCGCTTCTCCAA', 'NEXTflex'),
        ('NEXTflex271', 'TGAATTACGCGG', 'NEXTflex'),
        ('NEXTflex272', 'CATTCAGTCTAA', 'NEXTflex'),
        ('NEXTflex273', 'GGAAGAGGACGG', 'NEXTflex'),
        ('NEXTflex274', 'ACGGCGCATTCC', 'NEXTflex'),
        ('NEXTflex275', 'CCTTCAGGAGGG', 'NEXTflex'),
        ('NEXTflex276', 'GTAATGCATCCC', 'NEXTflex'),
        ('NEXTflex277', 'GAGCTTCGACGG', 'NEXTflex'),
        ('NEXTflex278', 'CTATAATATTAA', 'NEXTflex'),
        ('NEXTflex279', 'CTCGATCGACGG', 'NEXTflex'),
        ('NEXTflex280', 'TATATCGATGCC', 'NEXTflex'),
        ('NEXTflex281', 'TCTAGTCGATGG', 'NEXTflex'),
        ('NEXTflex282', 'CGCGCCGATCCC', 'NEXTflex'),
        ('NEXTflex283', 'AGATCTCGACGG', 'NEXTflex'),
        ('NEXTflex284', 'GCGCGCGATGCC', 'NEXTflex'),
        ('NEXTflex285', 'GTAGTGTCATGG', 'NEXTflex'),
        ('NEXTflex286', 'CCTCCAATTCCC', 'NEXTflex'),
        ('NEXTflex287', 'CATCAGTCAGGG', 'NEXTflex'),
        ('NEXTflex288', 'GTCTTCCTTCAA', 'NEXTflex'),
        ('NEXTflex289', 'ACGACGTCACGG', 'NEXTflex'),
        ('NEXTflex290', 'TTCTTAATTGCC', 'NEXTflex'),
        ('NEXTflex291', 'TATGTCACATGG', 'NEXTflex'),
        ('NEXTflex292', 'ATCAAGGTTCAA', 'NEXTflex'),
        ('NEXTflex293', 'ATACACACATGG', 'NEXTflex'),
        ('NEXTflex294', 'TAGTTGGTTCAA', 'NEXTflex'),
        ('NEXTflex295', 'AGCGTTGCACGG', 'NEXTflex'),
        ('NEXTflex296', 'GAGCCAATTGAA', 'NEXTflex'),
        ('NEXTflex297', 'TCGCATGCATGG', 'NEXTflex'),
        ('NEXTflex298', 'CTCGGAATTCAA', 'NEXTflex'),
        ('NEXTflex299', 'CTATGTGCACGG', 'NEXTflex'),
        ('NEXTflex300', 'GCTAACCTTTCC', 'NEXTflex'),
        ('NEXTflex301', 'GATACTGCACGG', 'NEXTflex'),
        ('NEXTflex302', 'ATCGGCCTTTCC', 'NEXTflex'),
        ('NEXTflex303', 'CCGGTACCATGG', 'NEXTflex'),
        ('NEXTflex304', 'GTCCCGGTTCCC', 'NEXTflex'),
        ('NEXTflex305', 'AATTGACCACGG', 'NEXTflex'),
        ('NEXTflex306', 'TGAAAGGTTTCC', 'NEXTflex'),
        ('NEXTflex307', 'CCAGTCATGCGG', 'NEXTflex'),
        ('NEXTflex308', 'TTTCCGGCCGAA', 'NEXTflex'),
        ('NEXTflex309', 'CGGCCTTCCCAA', 'NEXTflex'),
        ('NEXTflex310', 'GACGTCATGTTT', 'NEXTflex'),
        ('NEXTflex311', 'ACACACATGTCC', 'NEXTflex'),
        ('NEXTflex312', 'TGGTTGGCCCTT', 'NEXTflex'),
        ('NEXTflex313', 'GCTAATCTGGAA', 'NEXTflex'),
        ('NEXTflex314', 'CTATGCGCCATT', 'NEXTflex'),
        ('NEXTflex315', 'CGATTTCTGAAA', 'NEXTflex'),
        ('NEXTflex316', 'GCGCAATCCGGG', 'NEXTflex'),
        ('NEXTflex317', 'CAGGGAGTGGAA', 'NEXTflex'),
        ('NEXTflex318', 'TGCCATACCAGG', 'NEXTflex'),
        ('NEXTflex319', 'AAGAAGATGGAA', 'NEXTflex'),
        ('NEXTflex320', 'GTAGTATCCATT', 'NEXTflex'),
        ('NEXTflex321', 'TTCTTGATGAAA', 'NEXTflex'),
        ('NEXTflex322', 'ACGACATCCGTT', 'NEXTflex'),
        ('NEXTflex323', 'AGACCCTTGAAA', 'NEXTflex'),
        ('NEXTflex324', 'TATGTTACCGTT', 'NEXTflex'),
        ('NEXTflex325', 'TCTGGCTTGAAA', 'NEXTflex'),
        ('NEXTflex326', 'CGCACTACCGTT', 'NEXTflex'),
        ('NEXTflex327', 'GAGTTCTTGGAA', 'NEXTflex'),
        ('NEXTflex328', 'ATACATACCATT', 'NEXTflex'),
        ('NEXTflex329', 'AGGCCAGCAGAA', 'NEXTflex'),
        ('NEXTflex330', 'TACGTGCTTATT', 'NEXTflex'),
        ('NEXTflex331', 'TCCGGAGCAGAA', 'NEXTflex'),
        ('NEXTflex332', 'ATGCAGCTTATT', 'NEXTflex'),
        ('NEXTflex333', 'GAATTAGCAGAA', 'NEXTflex'),
        ('NEXTflex334', 'CGTACGCTTATT', 'NEXTflex'),
        ('NEXTflex335', 'TAACCGACATAA', 'NEXTflex'),
        ('NEXTflex336', 'AGTGTATTTATT', 'NEXTflex'),
        ('NEXTflex337', 'ATTGGGACAGAA', 'NEXTflex'),
        ('NEXTflex338', 'TCACAATTTATT', 'NEXTflex'),
        ('NEXTflex339', 'GCCAAGACAGAA', 'NEXTflex'),
        ('NEXTflex340', 'CTGTGATTTATT', 'NEXTflex'),
        ('NEXTflex341', 'ATTGCGGTGAAA', 'NEXTflex'),
        ('NEXTflex342', 'GACAGACCCTTT', 'NEXTflex'),
        ('NEXTflex343', 'GATATCTAATTT', 'NEXTflex'),
        ('NEXTflex344', 'ATCGATAGTAAA', 'NEXTflex'),
        ('NEXTflex345', 'TGAGGACTAATT', 'NEXTflex'),
        ('NEXTflex346', 'AATCAGGCTTAA', 'NEXTflex'),
        ('NEXTflex347', 'CAGAAACTATTT', 'NEXTflex'),
        ('NEXTflex348', 'TGCTGTTCTACC', 'NEXTflex'),
        ('NEXTflex349', 'GTCTTACTATTT', 'NEXTflex'),
        ('NEXTflex350', 'CATCATTCTACC', 'NEXTflex'),
        ('NEXTflex351', 'CGACCTGTATTT', 'NEXTflex'),
        ('NEXTflex352', 'GCGTGAACTCCC', 'NEXTflex'),
        ('NEXTflex353', 'GCTGGTGTATTT', 'NEXTflex'),
        ('NEXTflex354', 'CTACACCCTAAA', 'NEXTflex'),
        ('NEXTflex355', 'ATCAATGTATTT', 'NEXTflex'),
        ('NEXTflex356', 'TATGTAACTACC', 'NEXTflex'),
        ('NEXTflex357', 'TAGTTTGTATTT', 'NEXTflex'),
        ('NEXTflex358', 'ATACAAACTCCC', 'NEXTflex'),
        ('NEXTflex359', 'GAGCCCATAATT', 'NEXTflex'),
        ('NEXTflex360', 'CGCGTTTCTTAA', 'NEXTflex'),
        ('NEXTflex361', 'CCTATTACGTCC', 'NEXTflex'),
        ('NEXTflex362', 'GGCGAAGTCCTT', 'NEXTflex'),
        ('NEXTflex363', 'ACGTTCCGGTCC', 'NEXTflex'),
        ('NEXTflex364', 'GGACATGACCGG', 'NEXTflex'),
        ('NEXTflex365', 'GGGCTTCAGGCC', 'NEXTflex'),
        ('NEXTflex366', 'ACATACGGCCGG', 'NEXTflex'),
        ('NEXTflex367', 'CATACACCATCC', 'NEXTflex'),
        ('NEXTflex368', 'GGATTGGTTCGG', 'NEXTflex'),
        ('NEXTflex369', 'GGCACGTCAGCC', 'NEXTflex'),
        ('NEXTflex370', 'ACTGGAATTCGG', 'NEXTflex'),
        ('NEXTflex371', 'AAGTCGAGAGCC', 'NEXTflex'),
        ('NEXTflex372', 'GGCATCGATCTT', 'NEXTflex'),
        ('NEXTflex373', 'GGCAGTCTCTGG', 'NEXTflex'),
        ('NEXTflex374', 'CCTGCATCGCAA', 'NEXTflex'),
        ('NEXTflex375', 'GGGAGCTAGTGG', 'NEXTflex'),
        ('NEXTflex376', 'AACTAGCGCCAA', 'NEXTflex'),
        ('NEXTflex377', 'CCCTCCTAGTGG', 'NEXTflex'),
        ('NEXTflex378', 'GGTCGGCGCCAA', 'NEXTflex'),
        ('NEXTflex379', 'CCGAACCGGTGG', 'NEXTflex'),
        ('NEXTflex380', 'GGAGTGTACCAA', 'NEXTflex'),
        ('NEXTflex381', 'GGCCAACCACGG', 'NEXTflex'),
        ('NEXTflex382', 'ACTTTGGTTGCC', 'NEXTflex'),
        ('NEXTflex383', 'AACTGCATGCGG', 'NEXTflex'),
        ('NEXTflex384', 'GGGAAGGCCTAA', 'NEXTflex'),
        ('iTru5_01_A', 'TTGTCGGT', 'iTru5'),
        ('iTru5_01_B', 'TTGCCACT', 'iTru5'),
        ('iTru5_01_C', 'AGTCTGTG', 'iTru5'),
        ('iTru5_01_D', 'AAGTGTCG', 'iTru5'),
        ('iTru5_01_E', 'CACAAGTC', 'iTru5'),
        ('iTru5_01_F', 'AGTCTCAC', 'iTru5'),
        ('iTru5_01_G', 'CATGGAAC', 'iTru5'),
        ('iTru5_01_H', 'CTCAGCTA', 'iTru5'),
        ('iTru5_02_A', 'TTGCGAAG', 'iTru5'),
        ('iTru5_02_B', 'CATACCAC', 'iTru5'),
        ('iTru5_02_C', 'CTACAGTG', 'iTru5'),
        ('iTru5_02_D', 'TAGCGTCT', 'iTru5'),
        ('iTru5_02_E', 'TGGAGTTG', 'iTru5'),
        ('iTru5_02_F', 'AGCGTGTT', 'iTru5'),
        ('iTru5_02_G', 'ACCATCCA', 'iTru5'),
        ('iTru5_02_H', 'GCTTCGAA', 'iTru5'),
        ('iTru5_03_A', 'GTGGTGTT', 'iTru5'),
        ('iTru5_03_B', 'ACAGCTCA', 'iTru5'),
        ('iTru5_03_C', 'TTCCTGTG', 'iTru5'),
        ('iTru5_03_D', 'GGTTGTCA', 'iTru5'),
        ('iTru5_03_E', 'ACGGAACA', 'iTru5'),
        ('iTru5_03_F', 'TCTCTAGG', 'iTru5'),
        ('iTru5_03_G', 'CGTTATGC', 'iTru5'),
        ('iTru5_03_H', 'AAGCACTG', 'iTru5'),
        ('iTru5_04_A', 'GAGATACG', 'iTru5'),
        ('iTru5_04_B', 'TCTTGACG', 'iTru5'),
        ('iTru5_04_C', 'GTTCATGG', 'iTru5'),
        ('iTru5_04_D', 'GAAGTACC', 'iTru5'),
        ('iTru5_04_E', 'ATAGCGGT', 'iTru5'),
        ('iTru5_04_F', 'ACCTGGAA', 'iTru5'),
        ('iTru5_04_G', 'AGGTTCGA', 'iTru5'),
        ('iTru5_04_H', 'TGGCACTA', 'iTru5'),
        ('iTru5_05_A', 'TTCGTACC', 'iTru5'),
        ('iTru5_05_B', 'CGATGCTT', 'iTru5'),
        ('iTru5_05_C', 'GTATTGGC', 'iTru5'),
        ('iTru5_05_D', 'GCATACAG', 'iTru5'),
        ('iTru5_05_E', 'GTCCTAAG', 'iTru5'),
        ('iTru5_05_F', 'AAGGCTGA', 'iTru5'),
        ('iTru5_05_G', 'TGGCATGT', 'iTru5'),
        ('iTru5_05_H', 'ACTCCATC', 'iTru5'),
        ('iTru5_06_A', 'ATCGATCG', 'iTru5'),
        ('iTru5_06_B', 'CTGGAGTA', 'iTru5'),
        ('iTru5_06_C', 'TGGTAGCT', 'iTru5'),
        ('iTru5_06_D', 'CTTGTCGA', 'iTru5'),
        ('iTru5_06_E', 'CGGTCATA', 'iTru5'),
        ('iTru5_06_F', 'AGTTGGCT', 'iTru5'),
        ('iTru5_06_G', 'GCAAGATC', 'iTru5'),
        ('iTru5_06_H', 'TAACGAGG', 'iTru5'),
        ('iTru5_07_A', 'GGTGTCTT', 'iTru5'),
        ('iTru5_07_B', 'CAGGTATC', 'iTru5'),
        ('iTru5_07_C', 'GTTCGGTT', 'iTru5'),
        ('iTru5_07_D', 'GATTCAGC', 'iTru5'),
        ('iTru5_07_E', 'CACTAGCT', 'iTru5'),
        ('iTru5_07_F', 'TGAGCTAG', 'iTru5'),
        ('iTru5_07_G', 'CGCTTAAC', 'iTru5'),
        ('iTru5_07_H', 'TCCAATCG', 'iTru5'),
        ('iTru5_08_A', 'AGCAGATG', 'iTru5'),
        ('iTru5_08_B', 'GAAGAGGT', 'iTru5'),
        ('iTru5_08_C', 'GTTGCGAT', 'iTru5'),
        ('iTru5_08_D', 'GCACAACT', 'iTru5'),
        ('iTru5_08_E', 'CTTCGTTC', 'iTru5'),
        ('iTru5_08_F', 'TCTCTTCC', 'iTru5'),
        ('iTru5_08_G', 'ACGATGAC', 'iTru5'),
        ('iTru5_08_H', 'TTCGTTGG', 'iTru5'),
        ('iTru5_09_A', 'TCTGAGAG', 'iTru5'),
        ('iTru5_09_B', 'AAGTCCGT', 'iTru5'),
        ('iTru5_09_C', 'ACAGCAAC', 'iTru5'),
        ('iTru5_09_D', 'AGTCGACA', 'iTru5'),
        ('iTru5_09_E', 'GTTAGACG', 'iTru5'),
        ('iTru5_09_F', 'CCAGTGTT', 'iTru5'),
        ('iTru5_09_G', 'GTGTCTGA', 'iTru5'),
        ('iTru5_09_H', 'GTCCTTCT', 'iTru5'),
        ('iTru5_10_A', 'TCAGACGA', 'iTru5'),
        ('iTru5_10_B', 'CACACATG', 'iTru5'),
        ('iTru5_10_C', 'GGACTAGA', 'iTru5'),
        ('iTru5_10_D', 'AGAGCCTT', 'iTru5'),
        ('iTru5_10_E', 'CTCTGGTT', 'iTru5'),
        ('iTru5_10_F', 'GCGATAGT', 'iTru5'),
        ('iTru5_10_G', 'CTTAGGAC', 'iTru5'),
        ('iTru5_10_H', 'AACGGTCA', 'iTru5'),
        ('iTru5_11_A', 'GGCTATTG', 'iTru5'),
        ('iTru5_11_B', 'TTGAGGCA', 'iTru5'),
        ('iTru5_11_C', 'AGTTCGTC', 'iTru5'),
        ('iTru5_11_D', 'CTGTTAGG', 'iTru5'),
        ('iTru5_11_E', 'ATAAGGCG', 'iTru5'),
        ('iTru5_11_F', 'GCTGTTGT', 'iTru5'),
        ('iTru5_11_G', 'CAAGGTCT', 'iTru5'),
        ('iTru5_11_H', 'TCTAACGC', 'iTru5'),
        ('iTru5_12_A', 'GACGAATG', 'iTru5'),
        ('iTru5_12_B', 'GGTCAGAT', 'iTru5'),
        ('iTru5_12_C', 'CGTACGAA', 'iTru5'),
        ('iTru5_12_D', 'CTCGTCTT', 'iTru5'),
        ('iTru5_12_E', 'AGAACGAG', 'iTru5'),
        ('iTru5_12_F', 'AAGCCACA', 'iTru5'),
        ('iTru5_12_G', 'GCATGTCT', 'iTru5'),
        ('iTru5_12_H', 'CTCCTAGA', 'iTru5'),
        ('iTru5_13_A', 'CCTATACC', 'iTru5'),
        ('iTru5_13_B', 'CGTCAATG', 'iTru5'),
        ('iTru5_13_C', 'ACATTGCG', 'iTru5'),
        ('iTru5_13_D', 'TCGTGGAT', 'iTru5'),
        ('iTru5_13_E', 'TTCAGGAG', 'iTru5'),
        ('iTru5_13_F', 'GTCATCGA', 'iTru5'),
        ('iTru5_13_G', 'GAAGGTTC', 'iTru5'),
        ('iTru5_13_H', 'TGTGAAGC', 'iTru5'),
        ('iTru5_14_A', 'TGATCGGA', 'iTru5'),
        ('iTru5_14_B', 'TCATCACC', 'iTru5'),
        ('iTru5_14_C', 'GCCTTGTT', 'iTru5'),
        ('iTru5_14_D', 'CGAACTGT', 'iTru5'),
        ('iTru5_14_E', 'CAGCGATT', 'iTru5'),
        ('iTru5_14_F', 'AGTGTTGG', 'iTru5'),
        ('iTru5_14_G', 'CATGTTCC', 'iTru5'),
        ('iTru5_14_H', 'AACCGAAG', 'iTru5'),
        ('iTru5_15_A', 'TTAGGTCG', 'iTru5'),
        ('iTru5_15_B', 'ACACGGTT', 'iTru5'),
        ('iTru5_15_C', 'GACATGGT', 'iTru5'),
        ('iTru5_15_D', 'CGTCTTGT', 'iTru5'),
        ('iTru5_15_E', 'GCCTATCA', 'iTru5'),
        ('iTru5_15_F', 'CAGTGAAG', 'iTru5'),
        ('iTru5_15_G', 'ACATAGGC', 'iTru5'),
        ('iTru5_15_H', 'GATCCATG', 'iTru5'),
        ('iTru5_16_A', 'GAGATGTC', 'iTru5'),
        ('iTru5_16_B', 'CCAATAGG', 'iTru5'),
        ('iTru5_16_C', 'GCTGGATT', 'iTru5'),
        ('iTru5_16_D', 'ACCACGAT', 'iTru5'),
        ('iTru5_16_E', 'TGACGCAT', 'iTru5'),
        ('iTru5_16_F', 'GAACATCG', 'iTru5'),
        ('iTru5_16_G', 'AGTTACGG', 'iTru5'),
        ('iTru5_16_H', 'CTGTTGAC', 'iTru5'),
        ('iTru5_17_A', 'GATACTGG', 'iTru5'),
        ('iTru5_17_B', 'CCTACTGA', 'iTru5'),
        ('iTru5_17_C', 'CGTTGCAA', 'iTru5'),
        ('iTru5_17_D', 'ACCTGACT', 'iTru5'),
        ('iTru5_17_E', 'GTATGCTG', 'iTru5'),
        ('iTru5_17_F', 'TAACCGGT', 'iTru5'),
        ('iTru5_17_G', 'TTGATCCG', 'iTru5'),
        ('iTru5_17_H', 'CCGGAATT', 'iTru5'),
        ('iTru5_18_A', 'AGAAGCGT', 'iTru5'),
        ('iTru5_18_B', 'ACCGCATA', 'iTru5'),
        ('iTru5_18_C', 'TCGAAGGT', 'iTru5'),
        ('iTru5_18_D', 'GGTTGATG', 'iTru5'),
        ('iTru5_18_E', 'CTGCACTT', 'iTru5'),
        ('iTru5_18_F', 'GCTGTAAG', 'iTru5'),
        ('iTru5_18_G', 'CAATGTGG', 'iTru5'),
        ('iTru5_18_H', 'TATTCGCC', 'iTru5'),
        ('iTru5_19_A', 'TGTGCGTT', 'iTru5'),
        ('iTru5_19_B', 'CTAGGCAT', 'iTru5'),
        ('iTru5_19_C', 'TCCGTATG', 'iTru5'),
        ('iTru5_19_D', 'TAGTGACC', 'iTru5'),
        ('iTru5_19_E', 'CGGAATAC', 'iTru5'),
        ('iTru5_19_F', 'AAGAGCCA', 'iTru5'),
        ('iTru5_19_G', 'CGATAGAG', 'iTru5'),
        ('iTru5_19_H', 'AACCTCCT', 'iTru5'),
        ('iTru5_20_A', 'CGTGATCA', 'iTru5'),
        ('iTru5_20_B', 'ACTGCTAG', 'iTru5'),
        ('iTru5_20_C', 'TATCGGTC', 'iTru5'),
        ('iTru5_20_D', 'TAATGCCG', 'iTru5'),
        ('iTru5_20_E', 'TGGATCAC', 'iTru5'),
        ('iTru5_20_F', 'ACGGTCTT', 'iTru5'),
        ('iTru5_20_G', 'CTGACACA', 'iTru5'),
        ('iTru5_20_H', 'CTCAGAGT', 'iTru5'),
        ('iTru5_21_A', 'TGATACGC', 'iTru5'),
        ('iTru5_21_B', 'GTTGACCT', 'iTru5'),
        ('iTru5_21_C', 'ACCAGCTT', 'iTru5'),
        ('iTru5_21_D', 'GATCGAGT', 'iTru5'),
        ('iTru5_21_E', 'GTGCCATA', 'iTru5'),
        ('iTru5_21_F', 'TGATGTCC', 'iTru5'),
        ('iTru5_21_G', 'TAGTTGCG', 'iTru5'),
        ('iTru5_21_H', 'AAGAAGGC', 'iTru5'),
        ('iTru5_22_A', 'AAGGACAC', 'iTru5'),
        ('iTru5_22_B', 'TCACGTTC', 'iTru5'),
        ('iTru5_22_C', 'TGAGGTGT', 'iTru5'),
        ('iTru5_22_D', 'GGACCTAT', 'iTru5'),
        ('iTru5_22_E', 'CCTATGGT', 'iTru5'),
        ('iTru5_22_F', 'TGCACCAA', 'iTru5'),
        ('iTru5_22_G', 'GTCTGATC', 'iTru5'),
        ('iTru5_22_H', 'ATGGTCCA', 'iTru5'),
        ('iTru5_23_A', 'ACGTTACC', 'iTru5'),
        ('iTru5_23_B', 'CGCATGAT', 'iTru5'),
        ('iTru5_23_C', 'ATACTCCG', 'iTru5'),
        ('iTru5_23_D', 'TGTGACTG', 'iTru5'),
        ('iTru5_23_E', 'GATTGGAG', 'iTru5'),
        ('iTru5_23_F', 'GAACGCTT', 'iTru5'),
        ('iTru5_23_G', 'AGCGGAAT', 'iTru5'),
        ('iTru5_23_H', 'GACTATGC', 'iTru5'),
        ('iTru5_24_A', 'TTCTCTCG', 'iTru5'),
        ('iTru5_24_B', 'ACTCGTTG', 'iTru5'),
        ('iTru5_24_C', 'AAGTCGAG', 'iTru5'),
        ('iTru5_24_D', 'CACCACTA', 'iTru5'),
        ('iTru5_24_E', 'CCGTATCT', 'iTru5'),
        ('iTru5_24_F', 'TGGAGAGT', 'iTru5'),
        ('iTru5_24_G', 'GGAAGGAT', 'iTru5'),
        ('iTru5_24_H', 'CGTGTGTA', 'iTru5'),
        ('iTru7_101_01', 'ACGTTACC', 'iTru7'),
        ('iTru7_101_02', 'CTGTGTTG', 'iTru7'),
        ('iTru7_101_03', 'TGAGGTGT', 'iTru7'),
        ('iTru7_101_04', 'GATCCATG', 'iTru7'),
        ('iTru7_101_05', 'GCCTATCA', 'iTru7'),
        ('iTru7_101_06', 'AACAACCG', 'iTru7'),
        ('iTru7_101_07', 'ACTCGTTG', 'iTru7'),
        ('iTru7_101_08', 'CCTATGGT', 'iTru7'),
        ('iTru7_101_09', 'TGTACACC', 'iTru7'),
        ('iTru7_101_10', 'GTATGCTG', 'iTru7'),
        ('iTru7_101_11', 'TGATGTCC', 'iTru7'),
        ('iTru7_101_12', 'GTCCTTCT', 'iTru7'),
        ('iTru7_102_01', 'ATAAGGCG', 'iTru7'),
        ('iTru7_102_02', 'CTTACCTG', 'iTru7'),
        ('iTru7_102_03', 'CGTTGCAA', 'iTru7'),
        ('iTru7_102_04', 'GATTCAGC', 'iTru7'),
        ('iTru7_102_05', 'TCACGTTC', 'iTru7'),
        ('iTru7_102_06', 'TGTGCGTT', 'iTru7'),
        ('iTru7_102_07', 'TAGTTGCG', 'iTru7'),
        ('iTru7_102_08', 'AAGAGCCA', 'iTru7'),
        ('iTru7_102_09', 'ACAGCTCA', 'iTru7'),
        ('iTru7_102_10', 'GTTAAGGC', 'iTru7'),
        ('iTru7_102_11', 'AAGCCACA', 'iTru7'),
        ('iTru7_102_12', 'ACACGGTT', 'iTru7'),
        ('iTru7_103_01', 'CAGCGATT', 'iTru7'),
        ('iTru7_103_02', 'TAGTGACC', 'iTru7'),
        ('iTru7_103_03', 'CGAGACTA', 'iTru7'),
        ('iTru7_103_04', 'GACATGGT', 'iTru7'),
        ('iTru7_103_05', 'GCATGTCT', 'iTru7'),
        ('iTru7_103_06', 'ACTCCATC', 'iTru7'),
        ('iTru7_103_07', 'TGTGACTG', 'iTru7'),
        ('iTru7_103_08', 'CGAAGAAC', 'iTru7'),
        ('iTru7_103_09', 'GGTGTCTT', 'iTru7'),
        ('iTru7_103_10', 'AAGAAGGC', 'iTru7'),
        ('iTru7_103_11', 'AGGTTCGA', 'iTru7'),
        ('iTru7_103_12', 'CATGTTCC', 'iTru7'),
        ('iTru7_104_01', 'GTGCCATA', 'iTru7'),
        ('iTru7_104_02', 'CCTTGTAG', 'iTru7'),
        ('iTru7_104_03', 'GCTGGATT', 'iTru7'),
        ('iTru7_104_04', 'TAACGAGG', 'iTru7'),
        ('iTru7_104_05', 'ATGGTTGC', 'iTru7'),
        ('iTru7_104_06', 'CCTATACC', 'iTru7'),
        ('iTru7_104_07', 'TTAGGTCG', 'iTru7'),
        ('iTru7_104_08', 'GCAAGATC', 'iTru7'),
        ('iTru7_104_09', 'AGAGCCTT', 'iTru7'),
        ('iTru7_104_10', 'GCAATGGA', 'iTru7'),
        ('iTru7_104_11', 'CTGGAGTA', 'iTru7'),
        ('iTru7_104_12', 'GAACATCG', 'iTru7'),
        ('iTru7_105_01', 'GCACAACT', 'iTru7'),
        ('iTru7_105_02', 'TTCTCTCG', 'iTru7'),
        ('iTru7_105_03', 'AACGGTCA', 'iTru7'),
        ('iTru7_105_04', 'ACAGACCT', 'iTru7'),
        ('iTru7_105_05', 'TCTCTTCC', 'iTru7'),
        ('iTru7_105_06', 'AGTGTTGG', 'iTru7'),
        ('iTru7_105_07', 'TGGCATGT', 'iTru7'),
        ('iTru7_105_08', 'AGAAGCGT', 'iTru7'),
        ('iTru7_105_09', 'AGCGGAAT', 'iTru7'),
        ('iTru7_105_10', 'TAACCGGT', 'iTru7'),
        ('iTru7_105_11', 'CATGGAAC', 'iTru7'),
        ('iTru7_105_12', 'ATGGTCCA', 'iTru7'),
        ('iTru7_106_01', 'CTTCTGAG', 'iTru7'),
        ('iTru7_106_02', 'AACCGAAG', 'iTru7'),
        ('iTru7_106_03', 'TTCGTACC', 'iTru7'),
        ('iTru7_106_04', 'CTGTTAGG', 'iTru7'),
        ('iTru7_106_05', 'CACAAGTC', 'iTru7'),
        ('iTru7_106_06', 'TCTTGACG', 'iTru7'),
        ('iTru7_106_07', 'CGTCTTGT', 'iTru7'),
        ('iTru7_106_08', 'CGTGATCA', 'iTru7'),
        ('iTru7_106_09', 'CCAAGTTG', 'iTru7'),
        ('iTru7_106_10', 'GTACCTTG', 'iTru7'),
        ('iTru7_106_11', 'GACTATGC', 'iTru7'),
        ('iTru7_106_12', 'TGGATCAC', 'iTru7'),
        ('iTru7_107_01', 'CTCTGGTT', 'iTru7'),
        ('iTru7_107_02', 'GTTCATGG', 'iTru7'),
        ('iTru7_107_03', 'GCTGTAAG', 'iTru7'),
        ('iTru7_107_04', 'GTCGAAGA', 'iTru7'),
        ('iTru7_107_05', 'GAGCTCAA', 'iTru7'),
        ('iTru7_107_06', 'TGAACCTG', 'iTru7'),
        ('iTru7_107_07', 'CCGACTAT', 'iTru7'),
        ('iTru7_107_08', 'AGCTAACC', 'iTru7'),
        ('iTru7_107_09', 'GCCTTGTT', 'iTru7'),
        ('iTru7_107_10', 'AACTTGCC', 'iTru7'),
        ('iTru7_107_11', 'CAATGTGG', 'iTru7'),
        ('iTru7_107_12', 'AAGGCTGA', 'iTru7'),
        ('iTru7_108_01', 'TTACCGAG', 'iTru7'),
        ('iTru7_108_02', 'GTCCTAAG', 'iTru7'),
        ('iTru7_108_03', 'GAAGGTTC', 'iTru7'),
        ('iTru7_108_04', 'GAAGAGGT', 'iTru7'),
        ('iTru7_108_05', 'TCTGAGAG', 'iTru7'),
        ('iTru7_108_06', 'ACCGCATA', 'iTru7'),
        ('iTru7_108_07', 'GAAGTACC', 'iTru7'),
        ('iTru7_108_08', 'CAGGTATC', 'iTru7'),
        ('iTru7_108_09', 'TCTCTAGG', 'iTru7'),
        ('iTru7_108_10', 'AAGCACTG', 'iTru7'),
        ('iTru7_108_11', 'CCAAGCAA', 'iTru7'),
        ('iTru7_108_12', 'TGTTCGAG', 'iTru7'),
        ('iTru7_109_01', 'CTCGTCTT', 'iTru7'),
        ('iTru7_109_02', 'CGAACTGT', 'iTru7'),
        ('iTru7_109_03', 'CATTCGGT', 'iTru7'),
        ('iTru7_109_04', 'TCGGTTAC', 'iTru7'),
        ('iTru7_109_05', 'AAGTCGAG', 'iTru7'),
        ('iTru7_109_06', 'TATCGGTC', 'iTru7'),
        ('iTru7_109_07', 'TATTCGCC', 'iTru7'),
        ('iTru7_109_08', 'GTATTGGC', 'iTru7'),
        ('iTru7_109_09', 'AGTCGCTT', 'iTru7'),
        ('iTru7_109_10', 'TGGCACTA', 'iTru7'),
        ('iTru7_109_11', 'GGTTGTCA', 'iTru7'),
        ('iTru7_109_12', 'AACCTCCT', 'iTru7'),
        ('iTru7_110_01', 'ATGACCAG', 'iTru7'),
        ('iTru7_110_02', 'AACCGTTC', 'iTru7'),
        ('iTru7_110_03', 'TCCAATCG', 'iTru7'),
        ('iTru7_110_04', 'CTGCACTT', 'iTru7'),
        ('iTru7_110_05', 'CGCTTAAC', 'iTru7'),
        ('iTru7_110_06', 'CACCACTA', 'iTru7'),
        ('iTru7_110_07', 'ACAGCAAC', 'iTru7'),
        ('iTru7_110_08', 'GGAAGGAT', 'iTru7'),
        ('iTru7_110_09', 'GGCGTTAT', 'iTru7'),
        ('iTru7_110_10', 'CTGTTGAC', 'iTru7'),
        ('iTru7_110_11', 'GTCATCGA', 'iTru7'),
        ('iTru7_110_12', 'TGACTTCG', 'iTru7'),
        ('iTru7_111_01', 'CGATAGAG', 'iTru7'),
        ('iTru7_111_02', 'TTCGTTGG', 'iTru7'),
        ('iTru7_111_03', 'TGGAGAGT', 'iTru7'),
        ('iTru7_111_04', 'TCAGACGA', 'iTru7'),
        ('iTru7_111_05', 'GACGAATG', 'iTru7'),
        ('iTru7_111_06', 'CATGAGGA', 'iTru7'),
        ('iTru7_111_07', 'CGGTTGTT', 'iTru7'),
        ('iTru7_111_08', 'TCCGTATG', 'iTru7'),
        ('iTru7_111_09', 'TGTGGTAC', 'iTru7'),
        ('iTru7_111_10', 'AGAACGAG', 'iTru7'),
        ('iTru7_111_11', 'CTTCGTTC', 'iTru7'),
        ('iTru7_111_12', 'CCAATAGG', 'iTru7'),
        ('iTru7_112_01', 'ACCATCCA', 'iTru7'),
        ('iTru7_112_02', 'CACACATG', 'iTru7'),
        ('iTru7_112_03', 'CTTGTCGA', 'iTru7'),
        ('iTru7_112_04', 'AGTCTCAC', 'iTru7'),
        ('iTru7_112_05', 'AGTTGGCT', 'iTru7'),
        ('iTru7_112_06', 'CCGGAATT', 'iTru7'),
        ('iTru7_112_07', 'CAGTGAAG', 'iTru7'),
        ('iTru7_112_08', 'CCTACTGA', 'iTru7'),
        ('iTru7_112_09', 'TGTGAAGC', 'iTru7'),
        ('iTru7_112_10', 'GTCTGATC', 'iTru7'),
        ('iTru7_112_11', 'TTCAGGAG', 'iTru7'),
        ('iTru7_112_12', 'ACGATGAC', 'iTru7'),
        ('iTru7_113_01', 'CGTTATGC', 'iTru7'),
        ('iTru7_113_02', 'GATACTGG', 'iTru7'),
        ('iTru7_113_03', 'CTACTTGG', 'iTru7'),
        ('iTru7_113_04', 'CATACCAC', 'iTru7'),
        ('iTru7_113_05', 'ACATTGCG', 'iTru7'),
        ('iTru7_113_06', 'TGATCGGA', 'iTru7'),
        ('iTru7_113_07', 'AAGTGTCG', 'iTru7'),
        ('iTru7_113_08', 'GAACGCTT', 'iTru7'),
        ('iTru7_113_09', 'TCAAGGAC', 'iTru7'),
        ('iTru7_113_10', 'TCAACTGG', 'iTru7'),
        ('iTru7_113_11', 'GGTTGATG', 'iTru7'),
        ('iTru7_113_12', 'AAGGACAC', 'iTru7'),
        ('iTru7_114_01', 'TTGATCCG', 'iTru7'),
        ('iTru7_114_02', 'GGTGATTC', 'iTru7'),
        ('iTru7_114_03', 'GATTGCTC', 'iTru7'),
        ('iTru7_114_04', 'ACCTGGAA', 'iTru7'),
        ('iTru7_114_05', 'CATCTACG', 'iTru7'),
        ('iTru7_114_06', 'CCGTATCT', 'iTru7'),
        ('iTru7_114_07', 'CGGAATAC', 'iTru7'),
        ('iTru7_114_08', 'CTCCTAGA', 'iTru7'),
        ('iTru7_114_09', 'TGGTAGCT', 'iTru7'),
        ('iTru7_114_10', 'TCGAAGGT', 'iTru7'),
        ('iTru7_114_11', 'ACATAGGC', 'iTru7'),
        ('iTru7_114_12', 'CTCAGAGT', 'iTru7');

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

CREATE TABLE pm.targeted_plate_well_values (
	targeted_plate_id    bigint  ,
	row                  integer  NOT NULL,
	col                  integer  NOT NULL,
	raw_concentration    real  NOT NULL,
	mod_concentration    real
 );

CREATE INDEX idx_targeted_plate_well_values ON pm.targeted_plate_well_values ( targeted_plate_id );
ALTER TABLE pm.targeted_plate_well_values ADD CONSTRAINT fk_fadfasf_targeted_plate FOREIGN KEY ( targeted_plate_id ) REFERENCES pm.targeted_plate( targeted_plate_id );

