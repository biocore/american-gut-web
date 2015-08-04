-- Aug 4, 2015
-- Create setup for using barcodes on plates & barcode processing tracking

-- Create table for storing what object the barcode is tracking
CREATE TABLE barcodes.barcode_type (
	barcode_type_id      bigserial  NOT NULL,
	barcode_type         varchar NOT NULL,
	CONSTRAINT pk_barcode_type PRIMARY KEY ( barcode_type_id )
 );
INSERT INTO barcodes.barcode_type (barcode_type) VALUES ('BD BBL CultureSwab 220135');

--link barcode table with new barcode_type table, defaulting to BD swabs as type
ALTER TABLE barcodes.barcode ADD barcode_type_id bigint NOT NULL DEFAULT 1;
COMMENT ON COLUMN barcodes.barcode.barcode_type_id IS 'what type of item this is barcoding (sample tube, plate, etc)';
ALTER TABLE barcodes.barcode ALTER COLUMN barcode_type_id DROP DEFAULT;

CREATE INDEX idx_barcode ON barcodes.barcode ( barcode_type_id );
ALTER TABLE barcodes.barcode ADD CONSTRAINT fk_barcode FOREIGN KEY ( barcode_type_id ) REFERENCES barcodes.barcode_type( barcode_type_id );

-- Add column for tracking what step the barcode is on
ALTER TABLE barcodes.barcode ADD step varchar  NOT NULL;
COMMENT ON COLUMN barcodes.barcode.step IS 'What rough step of the process (Arrived, Extracted, PCR, Sequencing, Sequenced)';

-- Add protocols table
CREATE TABLE barcodes.protocol (
	protocol_id          bigserial  NOT NULL,
	step                 varchar  NOT NULL,
	protocol_shortname   varchar(100)  NOT NULL,
	protocol             text  NOT NULL,
	CONSTRAINT pk_protocol PRIMARY KEY ( protocol_id )
 );

--Change plate_barcode table to track wells
ALTER TABLE barcodes.plate_barcode ALTER COLUMN barcode TYPE varchar;
ALTER TABLE barcodes.plate_barcode ADD well varchar(5)  NOT NULL;

-- Make plates table play nice with new system
ALTER TABLE barcodes.plate ADD protocol_id bigint NOT NULL, ADD barcode varchar NOT NULL, DROP COLUMN plate, DROP COLUMN sequence_date;
CREATE INDEX idx_plate ON barcodes.plate ( protocol_id );
ALTER TABLE barcodes.plate ADD CONSTRAINT fk_plate FOREIGN KEY ( barcode ) REFERENCES barcodes.barcode( barcode );
ALTER TABLE barcodes.plate ADD CONSTRAINT fk_plate_0 FOREIGN KEY ( protocol_id ) REFERENCES barcodes.protocol( protocol_id );