DROP TABLE barcodes.plate CASCADE;
DROP TABLE barcodes.plate_barcode CASCADE;

ALTER TABLE ag.ag_kit_barcodes
    ADD status varchar  ,
    ADD sample_postmark_date date  ,
    ADD scan_date            date  ,
    ADD biomass_remaining    bool DEFAULT 'T' NOT NULL,
    ADD sequencing_status    varchar;

ALTER TABLE barcodes.project ADD description varchar;
ALTER TABLE barcodes.project ADD pi bigint;
COMMENT ON COLUMN barcodes.project.pi IS 'primary investigator on the study';
ALTER TABLE barcodes.project ADD contact_person bigint;
ALTER TABLE barcodes.project ADD created_on timestamp DEFAULT current_timestamp NOT NULL;
ALTER TABLE barcodes.project ALTER COLUMN project SET NOT NULL;

CREATE TABLE barcodes.companies ( 
    company              varchar  NOT NULL,
    contact              varchar  ,
    CONSTRAINT pk_companies PRIMARY KEY ( company )
 ) ;

CREATE TABLE barcodes.instrument_type ( 
    instrument_type      varchar  NOT NULL,
    description          varchar  NOT NULL,
    company              varchar  NOT NULL,
    model                varchar  NOT NULL,
    part_number          varchar  NOT NULL,
    CONSTRAINT pk_instrument_type PRIMARY KEY ( instrument_type )
 ) ;

CREATE INDEX idx_instrument_type ON barcodes.instrument_type ( company ) ;
ALTER TABLE barcodes.instrument_type ADD CONSTRAINT fk_instrument_type FOREIGN KEY ( company ) REFERENCES barcodes.companies( company )    ;

CREATE TABLE barcodes.people ( 
    person_id            bigserial  NOT NULL,
    name                 varchar(100)  NOT NULL,
    email                varchar  NOT NULL,
    address              varchar(100)  ,
    affiliation          varchar  ,
    phone                varchar(20)  ,
    CONSTRAINT pk_people PRIMARY KEY ( person_id )
 ) ;

CREATE TABLE barcodes.peripheral_type ( 
    peripheral_type      varchar  NOT NULL,
    description          varchar  NOT NULL,
    company              varchar  NOT NULL,
    model                varchar  NOT NULL,
    part_number          varchar  NOT NULL,
    CONSTRAINT pk_peripherals_type PRIMARY KEY ( peripheral_type )
 ) ;

CREATE INDEX idx_peripheral_type ON barcodes.peripheral_type ( company ) ;
ALTER TABLE barcodes.peripheral_type ADD CONSTRAINT fk_peripheral_type FOREIGN KEY ( company ) REFERENCES barcodes.companies( company )    ;


CREATE TABLE barcodes.plates ( 
    plate_barcode        varchar  NOT NULL,
    plate_name           varchar(100)  NOT NULL,
    created_on           timestamp DEFAULT current_timestamp NOT NULL,
    finalized            bool DEFAULT 'F' NOT NULL,
    person_id            bigint  NOT NULL,
    CONSTRAINT idx_plates UNIQUE ( plate_barcode ) ,
    CONSTRAINT pk_plates PRIMARY KEY ( plate_barcode )
 ) ;
CREATE INDEX idx_plates_0 ON barcodes.plates ( person_id ) ;
COMMENT ON COLUMN barcodes.plates.person_id IS 'Who plated the samples';
ALTER TABLE barcodes.plates ADD CONSTRAINT fk_plates FOREIGN KEY ( plate_barcode ) REFERENCES barcodes.barcode( barcode )    ;
ALTER TABLE barcodes.plates ADD CONSTRAINT fk_plates_0 FOREIGN KEY ( person_id ) REFERENCES barcodes.people( person_id )    ;

CREATE TABLE barcodes.primers ( 
    primer_id            bigserial  NOT NULL,
    primer_name          varchar  ,
    company              varchar  NOT NULL,
    linker               varchar  NOT NULL,
    fwd_primer           varchar  NOT NULL,
    rev_primer           varchar  NOT NULL,
    barcodes             json  NOT NULL,
    CONSTRAINT pk_primers PRIMARY KEY ( primer_id )
 ) ;

CREATE TABLE barcodes.primers_lots ( 
    primer_id            bigint  NOT NULL,
    lot_number           varchar  ,
    created_on           timestamp DEFAULT current_timestamp NOT NULL,
    person_id            bigint  NOT NULL,
    CONSTRAINT pk_primers_lots UNIQUE ( lot_number ) 
 ) ;
CREATE INDEX idx_primers_lots ON barcodes.primers_lots ( primer_id ) ;
ALTER TABLE barcodes.primers_lots ADD CONSTRAINT fk_primers_lots FOREIGN KEY ( primer_id ) REFERENCES barcodes.primers( primer_id )    ;

CREATE TABLE barcodes.protocols ( 
    protocol_id          bigserial  NOT NULL,
    name                 varchar(100)  ,
    description          varchar  NOT NULL,
    created_on           timestamp DEFAULT current_timestamp NOT NULL,
    person_id            bigint  NOT NULL,
    CONSTRAINT pk_protocols PRIMARY KEY ( protocol_id )
 ) ;
CREATE INDEX idx_protocols ON barcodes.protocols ( person_id ) ;
ALTER TABLE barcodes.protocols ADD CONSTRAINT fk_protocols FOREIGN KEY ( person_id ) REFERENCES barcodes.people( person_id )    ;

CREATE TABLE barcodes.protocol_tree ( 
    parent_id            bigint  NOT NULL,
    child_id             bigint  NOT NULL,
    CONSTRAINT idx_protocol_tree PRIMARY KEY ( parent_id, child_id )
 );
CREATE INDEX idx_protocol_tree_0 ON barcodes.protocol_tree ( parent_id );
CREATE INDEX idx_protocol_tree_1 ON barcodes.protocol_tree ( child_id );
ALTER TABLE barcodes.protocol_tree ADD CONSTRAINT fk_protocol_tree FOREIGN KEY ( parent_id ) REFERENCES barcodes.protocols( protocol_id );
ALTER TABLE barcodes.protocol_tree ADD CONSTRAINT fk_protocol_tree_0 FOREIGN KEY ( child_id ) REFERENCES barcodes.protocols( protocol_id );

CREATE TABLE barcodes.reagent_type ( 
    reagent_type         varchar  NOT NULL,
    description          varchar  NOT NULL,
    CONSTRAINT pk_reagent_type PRIMARY KEY ( reagent_type )
 ) ;

CREATE TABLE barcodes.reagents ( 
    reagent_id           bigserial  NOT NULL,
    reagent_type         varchar  NOT NULL,
    company              varchar  NOT NULL,
    name                 varchar(100)  NOT NULL,
    product_number       varchar  NOT NULL,
    created_on           timestamp DEFAULT current_timestamp NOT NULL,
    person_id            bigint  NOT NULL,
    other_information    json  ,
    CONSTRAINT pk_reagents PRIMARY KEY ( reagent_id )
 ) ;
CREATE INDEX idx_reagents ON barcodes.reagents ( company ) ;
CREATE INDEX idx_reagents_0 ON barcodes.reagents ( reagent_type ) ;
CREATE INDEX idx_reagents_1 ON barcodes.reagents ( person_id ) ;
COMMENT ON COLUMN barcodes.reagents.name IS 'Product name of the reagent';
COMMENT ON COLUMN barcodes.reagents.other_information IS 'Other INVARIANT information about the reagent needed for the prep template';
ALTER TABLE barcodes.reagents ADD CONSTRAINT fk_reagents FOREIGN KEY ( company ) REFERENCES barcodes.companies( company )    ;
ALTER TABLE barcodes.reagents ADD CONSTRAINT fk_reagents_0 FOREIGN KEY ( reagent_type ) REFERENCES barcodes.reagent_type( reagent_type )    ;
ALTER TABLE barcodes.reagents ADD CONSTRAINT fk_reagents_1 FOREIGN KEY ( person_id ) REFERENCES barcodes.people( person_id )    ;

CREATE TABLE barcodes.run ( 
    run_id               bigserial  NOT NULL,
    name                 varchar(100)  NOT NULL,
    created_on           timestamp DEFAULT current_timestamp NOT NULL,
    created_by           bigint  NOT NULL,
    finalized            bool DEFAULT 'F' NOT NULL,
    finalized_on         timestamp  ,
    finalized_by         bigint  ,
    CONSTRAINT idx_run_0 UNIQUE ( name ) ,
    CONSTRAINT pk_run PRIMARY KEY ( run_id )
 );
CREATE INDEX idx_run ON barcodes.run ( finalized_by );
COMMENT ON TABLE barcodes.run IS 'Full run, equivalent to a multi-lane sequencing run';
ALTER TABLE barcodes.run ADD CONSTRAINT fk_run FOREIGN KEY ( finalized_by ) REFERENCES barcodes.people( person_id );

CREATE TABLE barcodes.samples ( 
    sample_id            bigserial  NOT NULL,
    external_name        varchar(100)  NOT NULL,
    barcode              varchar  ,
    project_id           bigint  NOT NULL,
    sample_type          varchar  NOT NULL,
    biomass_remaining    bool DEFAULT 'T' NOT NULL,
    created_on           timestamp DEFAULT current_timestamp NOT NULL,
    created_by           bigint  NOT NULL,
    last_scanned         timestamp DEFAULT current_timestamp NOT NULL,
    last_scanned_by      bigint  NOT NULL,
    status               varchar(10) DEFAULT 'Entered' NOT NULL,
    CONSTRAINT pk_samples PRIMARY KEY ( sample_id )
 ) ;
CREATE INDEX idx_samples ON barcodes.samples ( barcode ) ;
CREATE INDEX idx_samples_0 ON barcodes.samples ( project_id ) ;
CREATE INDEX idx_samples_1 ON barcodes.samples ( last_scanned_by ) ;
CREATE INDEX idx_samples_2 ON barcodes.samples ( created_by ) ;
COMMENT ON COLUMN barcodes.samples.sample_type IS 'The type of sample collected (stool, soil, etc)';
COMMENT ON COLUMN barcodes.samples.last_scanned_by IS 'Pereson who last scanned the barcode';
ALTER TABLE barcodes.samples ADD CONSTRAINT fk_samples FOREIGN KEY ( barcode ) REFERENCES barcodes.barcode( barcode )    ;
ALTER TABLE barcodes.samples ADD CONSTRAINT fk_samples_1 FOREIGN KEY ( last_scanned_by ) REFERENCES barcodes.people( person_id )    ;
ALTER TABLE barcodes.samples ADD CONSTRAINT fk_samples_2 FOREIGN KEY ( created_by ) REFERENCES barcodes.people( person_id )    ;
ALTER TABLE barcodes.samples ADD CONSTRAINT fk_samples_0 FOREIGN KEY ( project_id ) REFERENCES barcodes.project( project_id )    ;

CREATE TABLE barcodes.steps ( 
    step_id              bigserial  NOT NULL,
    name                 varchar(100)  NOT NULL,
    description          varchar  NOT NULL,
    created_on           timestamp DEFAULT current_timestamp NOT NULL,
    person_id            bigint  NOT NULL,
    CONSTRAINT pk_steps PRIMARY KEY ( step_id )
 ) ;
CREATE INDEX idx_steps ON barcodes.steps ( person_id ) ;
ALTER TABLE barcodes.steps ADD CONSTRAINT fk_steps FOREIGN KEY ( person_id ) REFERENCES barcodes.people( person_id )    ;

CREATE TABLE barcodes.steps_instruments ( 
    step_id              bigint  NOT NULL,
    instrument_type      varchar  NOT NULL,
    CONSTRAINT idx_steps_instruments_0 PRIMARY KEY ( step_id, instrument_type )
 ) ;
CREATE INDEX idx_steps_instruments ON barcodes.steps_instruments ( instrument_type ) ;
ALTER TABLE barcodes.steps_instruments ADD CONSTRAINT fk_steps_instruments FOREIGN KEY ( step_id ) REFERENCES barcodes.steps( step_id )    ;
ALTER TABLE barcodes.steps_instruments ADD CONSTRAINT fk_steps_instruments_0 FOREIGN KEY ( instrument_type ) REFERENCES barcodes.instrument_type( instrument_type )    ;

CREATE TABLE barcodes.steps_peripherals ( 
    step_id              bigint  NOT NULL,
    peripheral_type      varchar  NOT NULL,
    CONSTRAINT idx_steps_peripherals_1 PRIMARY KEY ( step_id, peripheral_type )
 ) ;
CREATE INDEX idx_steps_peripherals ON barcodes.steps_peripherals ( step_id ) ;
CREATE INDEX idx_steps_peripherals_0 ON barcodes.steps_peripherals ( peripheral_type ) ;
ALTER TABLE barcodes.steps_peripherals ADD CONSTRAINT fk_steps_peripherals FOREIGN KEY ( step_id ) REFERENCES barcodes.steps( step_id )    ;
ALTER TABLE barcodes.steps_peripherals ADD CONSTRAINT fk_steps_peripherals_0 FOREIGN KEY ( peripheral_type ) REFERENCES barcodes.peripheral_type( peripheral_type )    ;

CREATE TABLE barcodes.steps_primers ( 
    step_id              bigint  NOT NULL,
    primer_id            bigint  NOT NULL,
    CONSTRAINT idx_steps_primers PRIMARY KEY ( step_id, primer_id )
 ) ;
CREATE INDEX idx_steps_primers_0 ON barcodes.steps_primers ( step_id ) ;
CREATE INDEX idx_steps_primers_1 ON barcodes.steps_primers ( primer_id ) ;
ALTER TABLE barcodes.steps_primers ADD CONSTRAINT fk_steps_primers FOREIGN KEY ( step_id ) REFERENCES barcodes.steps( step_id )    ;
ALTER TABLE barcodes.steps_primers ADD CONSTRAINT fk_steps_primers_0 FOREIGN KEY ( primer_id ) REFERENCES barcodes.primers( primer_id )    ;

CREATE TABLE barcodes.steps_reagents ( 
    step_id              integer  NOT NULL,
    reagent_id           integer  NOT NULL,
    CONSTRAINT idx_steps_reagents PRIMARY KEY ( step_id, reagent_id )
 ) ;
CREATE INDEX idx_steps_reagents_0 ON barcodes.steps_reagents ( step_id ) ;
CREATE INDEX idx_steps_reagents_1 ON barcodes.steps_reagents ( reagent_id ) ;
ALTER TABLE barcodes.steps_reagents ADD CONSTRAINT fk_steps_reagents FOREIGN KEY ( step_id ) REFERENCES barcodes.steps( step_id )    ;
ALTER TABLE barcodes.steps_reagents ADD CONSTRAINT fk_steps_reagents_0 FOREIGN KEY ( reagent_id ) REFERENCES barcodes.reagents( reagent_id )    ;

CREATE TABLE barcodes.users ( 
    username             varchar  NOT NULL,
    pass                 varchar(36)  NOT NULL,
    person_id            integer  NOT NULL,
    "access"             char(1)  NOT NULL,
    created_on           timestamp DEFAULT current_timestamp NOT NULL,
    CONSTRAINT pk_users PRIMARY KEY ( username )
 ) ;
CREATE INDEX idx_users ON barcodes.users ( person_id ) ;
COMMENT ON COLUMN barcodes.users."access" IS 'What access the user is allowed';
ALTER TABLE barcodes.users ADD CONSTRAINT fk_users FOREIGN KEY ( person_id ) REFERENCES barcodes.people( person_id )    ;

CREATE TABLE barcodes.instruments ( 
    instrument_id        varchar  NOT NULL,
    instrument_type      varchar  NOT NULL,
    created_on           timestamp DEFAULT current_timestamp NOT NULL,
    person_id            bigint  NOT NULL,
    CONSTRAINT idx_instruments PRIMARY KEY ( instrument_id, instrument_type ),
    CONSTRAINT pk_instruments UNIQUE ( instrument_id ) 
 ) ;
CREATE INDEX idx_instruments_0 ON barcodes.instruments ( instrument_type ) ;
CREATE INDEX idx_instruments_1 ON barcodes.instruments ( person_id ) ;
COMMENT ON COLUMN barcodes.instruments.instrument_id IS 'serial number of the instrument';
ALTER TABLE barcodes.instruments ADD CONSTRAINT fk_instruments_0 FOREIGN KEY ( instrument_type ) REFERENCES barcodes.instrument_type( instrument_type )    ;
ALTER TABLE barcodes.instruments ADD CONSTRAINT fk_instruments_1 FOREIGN KEY ( person_id ) REFERENCES barcodes.people( person_id )    ;

CREATE TABLE barcodes.instruments_reagents ( 
    instrument_type_id   varchar  NOT NULL,
    reagent_id           bigint  NOT NULL,
    CONSTRAINT idx_instruments_reagents PRIMARY KEY ( instrument_type_id, reagent_id )
 ) ;
CREATE INDEX idx_instruments_reagents_0 ON barcodes.instruments_reagents ( instrument_type_id ) ;
CREATE INDEX idx_instruments_reagents_1 ON barcodes.instruments_reagents ( reagent_id ) ;
ALTER TABLE barcodes.instruments_reagents ADD CONSTRAINT fk_instruments_reagents_0 FOREIGN KEY ( reagent_id ) REFERENCES barcodes.reagents( reagent_id )    ;
ALTER TABLE barcodes.instruments_reagents ADD CONSTRAINT fk_instruments_reagents FOREIGN KEY ( instrument_type_id ) REFERENCES barcodes.instrument_type( instrument_type )    ;

CREATE TABLE barcodes.peripherals ( 
    peripheral_id        varchar  NOT NULL,
    instrument_type      varchar  NOT NULL,
    peripheral_type      varchar  NOT NULL,
    created_on           timestamp DEFAULT current_timestamp NOT NULL,
    person_id            bigint  NOT NULL,
    CONSTRAINT idx_peripherals_0 UNIQUE ( peripheral_id, instrument_type ) ,
    CONSTRAINT idx_peripherals_3 PRIMARY KEY ( peripheral_id, peripheral_type ),
    CONSTRAINT pk_peripherals UNIQUE ( peripheral_id ) 
 ) ;
CREATE INDEX idx_peripherals_1 ON barcodes.peripherals ( peripheral_type ) ;
CREATE INDEX idx_peripherals_2 ON barcodes.peripherals ( person_id ) ;
CREATE INDEX idx_peripherals ON barcodes.peripherals ( instrument_type ) ;
COMMENT ON COLUMN barcodes.peripherals.instrument_type IS 'The instrument this attaches to';
ALTER TABLE barcodes.peripherals ADD CONSTRAINT fk_peripherals_1 FOREIGN KEY ( peripheral_type ) REFERENCES barcodes.peripheral_type( peripheral_type )    ;
ALTER TABLE barcodes.peripherals ADD CONSTRAINT fk_peripherals_2 FOREIGN KEY ( person_id ) REFERENCES barcodes.people( person_id )    ;
ALTER TABLE barcodes.peripherals ADD CONSTRAINT fk_peripherals_0 FOREIGN KEY ( instrument_type ) REFERENCES barcodes.instrument_type( instrument_type )    ;

CREATE TABLE barcodes.plates_samples ( 
    plate_barcode        varchar  NOT NULL,
    sample_id            bigint  NOT NULL,
    well                 varchar(3)  NOT NULL,
    CONSTRAINT idx_plate_samples PRIMARY KEY ( plate_barcode, sample_id )
 ) ;
CREATE INDEX idx_plate_samples_0 ON barcodes.plates_samples ( sample_id ) ;
CREATE INDEX idx_plate_samples_1 ON barcodes.plates_samples ( plate_barcode ) ;
ALTER TABLE barcodes.plates_samples ADD CONSTRAINT fk_plate_samples FOREIGN KEY ( sample_id ) REFERENCES barcodes.samples( sample_id )    ;
ALTER TABLE barcodes.plates_samples ADD CONSTRAINT fk_plate_samples_0 FOREIGN KEY ( plate_barcode ) REFERENCES barcodes.plates( plate_barcode )    ;

CREATE TABLE barcodes.pool ( 
    pool_id              bigserial  NOT NULL,
    run_id               bigint  ,
    name                 varchar(100)  NOT NULL,
    created_on           timestamp DEFAULT current_timestamp NOT NULL,
    created_by           bigint  NOT NULL,
    finalized            bool DEFAULT 'F' NOT NULL,
    finalized_on         timestamp  ,
    finalized_by         bigint  NOT NULL,
    CONSTRAINT idx_pool_2 UNIQUE ( name ) ,
    CONSTRAINT pk_pool PRIMARY KEY ( pool_id )
 );
CREATE INDEX idx_pool ON barcodes.pool ( run_id );
CREATE INDEX idx_pool_0 ON barcodes.pool ( created_by );
CREATE INDEX idx_pool_1 ON barcodes.pool ( finalized_by );
COMMENT ON TABLE barcodes.pool IS 'Pool of samples, equivalent to a single lane for sequencing';
ALTER TABLE barcodes.pool ADD CONSTRAINT fk_pool FOREIGN KEY ( run_id ) REFERENCES barcodes.run( run_id );
ALTER TABLE barcodes.pool ADD CONSTRAINT fk_pool_0 FOREIGN KEY ( created_by ) REFERENCES barcodes.people( person_id );
ALTER TABLE barcodes.pool ADD CONSTRAINT fk_pool_1 FOREIGN KEY ( finalized_by ) REFERENCES barcodes.people( person_id );

CREATE TABLE barcodes.protocol_settings ( 
    protocol_settings_id bigserial  NOT NULL,
    protocol_id          integer  ,
    sample_id            bigint  ,
    plate_barcode        varchar  ,
    created_on           timestamp DEFAULT current_timestamp NOT NULL,
    created_by           bigint  NOT NULL,
    finalized_on         timestamp  ,
    finalized_by         bigint  ,
    CONSTRAINT pk_protocol_runs PRIMARY KEY ( protocol_settings_id )
 ) ;
CREATE INDEX idx_protocol_runs ON barcodes.protocol_settings ( created_by ) ;
CREATE INDEX idx_protocol_runs_0 ON barcodes.protocol_settings ( finalized_by ) ;
CREATE INDEX idx_protocol_runs_1 ON barcodes.protocol_settings ( plate_barcode ) ;
CREATE INDEX idx_protocol_runs_2 ON barcodes.protocol_settings ( sample_id ) ;
ALTER TABLE barcodes.protocol_settings ADD CONSTRAINT fk_protocol_runs FOREIGN KEY ( created_by ) REFERENCES barcodes.people( person_id )    ;
ALTER TABLE barcodes.protocol_settings ADD CONSTRAINT fk_protocol_runs_0 FOREIGN KEY ( finalized_by ) REFERENCES barcodes.people( person_id )    ;
ALTER TABLE barcodes.protocol_settings ADD CONSTRAINT fk_protocol_runs_1 FOREIGN KEY ( plate_barcode ) REFERENCES barcodes.plates( plate_barcode )    ;
ALTER TABLE barcodes.protocol_settings ADD CONSTRAINT fk_protocol_runs_2 FOREIGN KEY ( sample_id ) REFERENCES barcodes.samples( sample_id )    ;

CREATE TABLE barcodes.protocols_steps ( 
    protocol_id          bigint  NOT NULL,
    step_id              bigint  NOT NULL,
    step_order           integer  NOT NULL,
    CONSTRAINT idx_protocols_steps PRIMARY KEY ( protocol_id, step_id )
 ) ;
CREATE INDEX idx_protocols_steps_0 ON barcodes.protocols_steps ( protocol_id ) ;
CREATE INDEX idx_protocols_steps_1 ON barcodes.protocols_steps ( step_id ) ;
ALTER TABLE barcodes.protocols_steps ADD CONSTRAINT fk_protocols_steps FOREIGN KEY ( protocol_id ) REFERENCES barcodes.protocols( protocol_id )    ;
ALTER TABLE barcodes.protocols_steps ADD CONSTRAINT fk_protocols_steps_0 FOREIGN KEY ( step_id ) REFERENCES barcodes.steps( step_id )    ;

CREATE TABLE barcodes.reagent_lots ( 
    reagent_id           bigserial  NOT NULL,
    lot_number           varchar  NOT NULL,
    created_on           timestamp  ,
    person_id            bigint  NOT NULL,
    CONSTRAINT idx_lots PRIMARY KEY ( reagent_id, lot_number )
 ) ;
CREATE INDEX idx_reagent_lots ON barcodes.reagent_lots ( reagent_id ) ;
CREATE INDEX idx_reagent_lots_0 ON barcodes.reagent_lots ( person_id ) ;
ALTER TABLE barcodes.reagent_lots ADD CONSTRAINT fk_reagent_lots FOREIGN KEY ( reagent_id ) REFERENCES barcodes.reagents( reagent_id )    ;
ALTER TABLE barcodes.reagent_lots ADD CONSTRAINT fk_reagent_lots_0 FOREIGN KEY ( person_id ) REFERENCES barcodes.people( person_id )    ;

CREATE TABLE barcodes.step_settings ( 
    step_settings_id     bigserial  NOT NULL,
    protocol_run_id      bigint  NOT NULL,
    step_id              integer  NOT NULL,
    CONSTRAINT idx_run_settings UNIQUE ( protocol_run_id, step_settings_id ) ,
    CONSTRAINT pk_run_settings PRIMARY KEY ( step_settings_id )
 ) ;
CREATE INDEX idx_run_settings_0 ON barcodes.step_settings ( protocol_run_id ) ;
ALTER TABLE barcodes.step_settings ADD CONSTRAINT fk_run_settings FOREIGN KEY ( protocol_run_id ) REFERENCES barcodes.protocol_settings( protocol_settings_id )    ;

CREATE TABLE barcodes.pool_samples ( 
    pool_id              bigint  NOT NULL,
    protocol_run_id      bigint  NOT NULL
 ) ;
CREATE INDEX idx_pool_samples ON barcodes.pool_samples ( pool_id ) ;
CREATE INDEX idx_pool_samples_0 ON barcodes.pool_samples ( protocol_run_id ) ;
ALTER TABLE barcodes.pool_samples ADD CONSTRAINT fk_pool_samples FOREIGN KEY ( pool_id ) REFERENCES barcodes.pool( pool_id )    ;
ALTER TABLE barcodes.pool_samples ADD CONSTRAINT fk_pool_samples_0 FOREIGN KEY ( protocol_run_id ) REFERENCES barcodes.protocol_settings( protocol_settings_id )    ;

CREATE TABLE barcodes.settings_instruments ( 
    step_settings_id     bigint  NOT NULL,
    instrument_id        varchar(100)  
 ) ;
CREATE INDEX idx_settings_instruments ON barcodes.settings_instruments ( step_settings_id ) ;
CREATE INDEX idx_settings_instruments_0 ON barcodes.settings_instruments ( instrument_id ) ;
ALTER TABLE barcodes.settings_instruments ADD CONSTRAINT fk_settings_instruments FOREIGN KEY ( step_settings_id ) REFERENCES barcodes.step_settings( step_settings_id )    ;
ALTER TABLE barcodes.settings_instruments ADD CONSTRAINT fk_settings_instruments_0 FOREIGN KEY ( instrument_id ) REFERENCES barcodes.instruments( instrument_id )    ;

CREATE TABLE barcodes.settings_peripherals ( 
    step_settings_id     integer  ,
    peripheral_id        varchar  NOT NULL
 ) ;
CREATE INDEX idx_settings_peripherals ON barcodes.settings_peripherals ( peripheral_id ) ;
CREATE INDEX idx_settings_peripherals_0 ON barcodes.settings_peripherals ( step_settings_id ) ;
ALTER TABLE barcodes.settings_peripherals ADD CONSTRAINT fk_settings_peripherals FOREIGN KEY ( peripheral_id ) REFERENCES barcodes.peripherals( peripheral_id )    ;
ALTER TABLE barcodes.settings_peripherals ADD CONSTRAINT fk_settings_peripherals_0 FOREIGN KEY ( step_settings_id ) REFERENCES barcodes.step_settings( step_settings_id )    ;

CREATE TABLE barcodes.settings_primers ( 
    step_settings_id     bigint  NOT NULL,
    primer_id            bigint  NOT NULL,
    lot_number           varchar  NOT NULL
 ) ;
CREATE INDEX idx_settings_primers ON barcodes.settings_primers ( step_settings_id ) ;
CREATE INDEX idx_settings_primers_0 ON barcodes.settings_primers ( primer_id ) ;
CREATE INDEX idx_settings_primers_1 ON barcodes.settings_primers ( lot_number ) ;
ALTER TABLE barcodes.settings_primers ADD CONSTRAINT fk_settings_primers FOREIGN KEY ( step_settings_id ) REFERENCES barcodes.step_settings( step_settings_id )    ;
ALTER TABLE barcodes.settings_primers ADD CONSTRAINT fk_settings_primers_0 FOREIGN KEY ( primer_id ) REFERENCES barcodes.primers( primer_id )    ;
ALTER TABLE barcodes.settings_primers ADD CONSTRAINT fk_settings_primers_1 FOREIGN KEY ( lot_number ) REFERENCES barcodes.primers_lots( lot_number )    ;

CREATE TABLE barcodes.settings_reagents ( 
    step_settings_id     bigint  NOT NULL,
    reagent_id           bigint  NOT NULL,
    lot_number           varchar  NOT NULL
 ) ;
CREATE INDEX idx_settings_reagents ON barcodes.settings_reagents ( step_settings_id ) ;
ALTER TABLE barcodes.settings_reagents ADD CONSTRAINT fk_settings_reagents FOREIGN KEY ( step_settings_id ) REFERENCES barcodes.step_settings( step_settings_id )    ;

UPDATE ag.ag_kit_barcodes
SET status = barcodes.barcode.status,
  scan_date = barcodes.barcode.scan_date,
  sample_postmark_date = barcodes.barcode.sample_postmark_date,
  biomass_remaining = CASE barcodes.barcode.biomass_remaining::boolean
                     WHEN NOT NULL THEN  barcodes.barcode.biomass_remaining::boolean
                     ELSE 'Y'
                     END,
  sequencing_status = barcodes.barcode.sequencing_status
FROM barcodes.barcode
WHERE barcodes.barcode.barcode = ag.ag_kit_barcodes.barcode;

ALTER TABLE barcodes.barcode DROP COLUMN status;
ALTER TABLE barcodes.barcode DROP COLUMN scan_date;
ALTER TABLE barcodes.barcode DROP COLUMN sample_postmark_date;
ALTER TABLE barcodes.barcode DROP COLUMN biomass_remaining;
ALTER TABLE barcodes.barcode DROP COLUMN sequencing_status;

