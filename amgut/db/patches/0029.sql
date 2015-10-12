-- October 12, 2015
-- Add tables needed to track plate maps and create prep templates

ALTER TABLE barcodes.plate DROP COLUMN plate_id;
ALTER TABLE barcodes.plate DROP COLUMN plate;
ALTER TABLE barcodes.plate DROP COLUMN sequence_date;
ALTER TABLE barcodes.plate DROP CONSTRAINT plate_pkey;
DROP TABLE barcodes.plate_barcode CASCADE;
ALTER TABLE barcodes.plate ADD barcode varchar  NOT NULL;
ALTER TABLE barcodes.plate ADD nickname varchar(50)  NOT NULL;
ALTER TABLE barcodes.plate ADD project_id varchar(20)  NOT NULL;
ALTER TABLE barcodes.plate ADD protocol bigint  NOT NULL;
ALTER TABLE barcodes.plate ADD ext_robot bigint  NOT NULL;
COMMENT ON COLUMN barcodes.plate.ext_robot IS 'Extraction robot used for this plate';
ALTER TABLE barcodes.plate ADD ext_robot_tool varchar  NOT NULL;
COMMENT ON COLUMN barcodes.plate.ext_robot_tool IS 'Extraction robot pipette head used';
ALTER TABLE barcodes.plate ADD kf_robot bigint  NOT NULL;
COMMENT ON COLUMN barcodes.plate.kf_robot IS 'kingifsher robot used for extracton';
ALTER TABLE barcodes.plate ADD ext_kit_lot bigint  NOT NULL;
COMMENT ON COLUMN barcodes.plate.ext_kit_lot IS 'Extraction kit lot number';
ALTER TABLE barcodes.plate ADD person bigint  NOT NULL;
COMMENT ON COLUMN barcodes.plate.person IS 'Person running the extraction';
ALTER TABLE barcodes.plate ADD finalized bool DEFAULT 'F' NOT NULL;
COMMENT ON COLUMN barcodes.plate.finalized IS 'Whether the plate map is complete or still being filled.';
ALTER TABLE barcodes.plate ADD creation_timestamp timestamp DEFAULT current_date NOT NULL;
ALTER TABLE barcodes.plate ADD finalized_timestamp timestamp  ;
ALTER TABLE barcodes.plate ADD CONSTRAINT plate_pkey PRIMARY KEY ( barcode ) ;

CREATE INDEX idx_plate ON barcodes.plate ( project_id ) ;
CREATE INDEX idx_plate_0 ON barcodes.plate ( ext_robot ) ;
CREATE INDEX idx_plate_1 ON barcodes.plate ( kf_robot ) ;
CREATE INDEX idx_plate_2 ON barcodes.plate ( ext_kit_lot ) ;
CREATE INDEX idx_plate_3 ON barcodes.plate ( protocol ) ;
CREATE INDEX idx_plate_4 ON barcodes.plate ( person ) ;
ALTER TABLE barcodes.plate ADD CONSTRAINT fk_plate FOREIGN KEY ( barcode ) REFERENCES barcodes.barcode( barcode )    ;
ALTER TABLE barcodes.plate ADD CONSTRAINT fk_plate_0 FOREIGN KEY ( project_id ) REFERENCES barcodes.project( project_id )    ;
ALTER TABLE barcodes.plate ADD CONSTRAINT fk_plate_1 FOREIGN KEY ( ext_robot ) REFERENCES barcodes.robots( robot_id )    ;
ALTER TABLE barcodes.plate ADD CONSTRAINT fk_plate_2 FOREIGN KEY ( kf_robot ) REFERENCES barcodes.robots( robot_id )    ;
ALTER TABLE barcodes.plate ADD CONSTRAINT fk_plate_3 FOREIGN KEY ( ext_kit_lot ) REFERENCES barcodes.lot( lot_id )    ;
ALTER TABLE barcodes.plate ADD CONSTRAINT fk_plate_4 FOREIGN KEY ( protocol ) REFERENCES barcodes.protocol( protocol_id )    ;
ALTER TABLE barcodes.plate ADD CONSTRAINT fk_plate_5 FOREIGN KEY ( person ) REFERENCES barcodes.person( person_id )    ;

CREATE TABLE barcodes.lot ( 
	lot_id               bigserial  NOT NULL,
	lot_type             varchar  NOT NULL,
	lot                  varchar  NOT NULL,
	date_added           date DEFAULT current_date NOT NULL,
	CONSTRAINT pk_lots PRIMARY KEY ( lot_id )
 ) ;

CREATE TABLE barcodes.person ( 
	person_id            bigint  NOT NULL,
	name                 varchar(100)  NOT NULL,
	email                varchar  NOT NULL,
	date_added           date DEFAULT current_date NOT NULL,
	CONSTRAINT pk_person PRIMARY KEY ( person_id )
 ) ;

CREATE TABLE barcodes.plate_sample ( 
	barcode              bigint  NOT NULL,
	well                 varchar(3)  NOT NULL,
	sample               varchar  NOT NULL,
	CONSTRAINT pkey_plate_barcode_1 PRIMARY KEY ( barcode, well )
 ) ;

CREATE INDEX idx_plate_barcode ON barcodes.plate_sample ( well ) ;

CREATE INDEX idx_plate_barcode_0 ON barcodes.plate_sample ( barcode ) ;

CREATE TABLE barcodes.protocol ( 
	protocol_id          bigserial  NOT NULL,
	protocol_name        varchar(100)  NOT NULL,
	template_dna         integer  NOT NULL,
	CONSTRAINT pk_protocol PRIMARY KEY ( protocol_id )
 ) ;

COMMENT ON COLUMN barcodes.protocol.template_dna IS 'Template DNA added, in uL';

CREATE TABLE barcodes.robots ( 
	robot_id             bigserial  NOT NULL,
	robot_type           varchar  NOT NULL,
	robot_name           varchar(100)  NOT NULL,
	date_added           date DEFAULT current_date NOT NULL,
	CONSTRAINT pk_robots PRIMARY KEY ( robot_id )
 ) ;

CREATE TABLE barcodes.pcr_plate ( 
	barcode              varchar  NOT NULL,
	nickname             varchar(100)  NOT NULL,
	protocol             bigint  NOT NULL,
	"primer plate"       integer  NOT NULL,
	primer_plate_lot     bigint  NOT NULL,
	amplicon             varchar  NOT NULL,
	master_mix_lot       bigint  NOT NULL,
	water_lot            bigint  NOT NULL,
	pcr_robot            bigint  NOT NULL,
	"300_8_tool"         bigint  NOT NULL,
	"50_8_tool"          bigint  NOT NULL,
	person               bigint  NOT NULL,
	pcr_created          timestamp DEFAULT current_timestamp NOT NULL,
	CONSTRAINT pkey_pcr_plate PRIMARY KEY ( barcode, nickname )
 ) ;

CREATE INDEX idx_pcr_plate ON barcodes.pcr_plate ( barcode ) ;
CREATE INDEX idx_pcr_plate_0 ON barcodes.pcr_plate ( pcr_robot ) ;
CREATE INDEX idx_pcr_plate_1 ON barcodes.pcr_plate ( primer_plate_lot ) ;
CREATE INDEX idx_pcr_plate_2 ON barcodes.pcr_plate ( master_mix_lot ) ;
CREATE INDEX idx_pcr_plate_3 ON barcodes.pcr_plate ( water_lot ) ;
CREATE INDEX idx_pcr_plate_4 ON barcodes.pcr_plate ( protocol ) ;
CREATE INDEX idx_pcr_plate_5 ON barcodes.pcr_plate ( person ) ;
COMMENT ON COLUMN barcodes.pcr_plate."300_8_tool" IS '300uL pipette head used';
COMMENT ON COLUMN barcodes.pcr_plate."50_8_tool" IS '50uL pipette head used';
ALTER TABLE barcodes.barcode ALTER COLUMN barcode TYPE varchar;
ALTER TABLE barcodes.plate_sample ADD CONSTRAINT fk_plate_barcode_0 FOREIGN KEY ( barcode ) REFERENCES barcodes.plate( barcode )    ;
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate FOREIGN KEY ( barcode ) REFERENCES barcodes.plate( barcode )    ;
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate_0 FOREIGN KEY ( pcr_robot ) REFERENCES barcodes.robots( robot_id )    ;
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate_1 FOREIGN KEY ( primer_plate_lot ) REFERENCES barcodes.lot( lot_id )    ;
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate_2 FOREIGN KEY ( master_mix_lot ) REFERENCES barcodes.lot( lot_id )    ;
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate_3 FOREIGN KEY ( water_lot ) REFERENCES barcodes.lot( lot_id )    ;
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate_4 FOREIGN KEY ( protocol ) REFERENCES barcodes.protocol( protocol_id )    ;
ALTER TABLE barcodes.pcr_plate ADD CONSTRAINT fk_pcr_plate_5 FOREIGN KEY ( person ) REFERENCES barcodes.person( person_id )    ;
