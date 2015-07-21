CREATE SCHEMA barcodes;

ALTER TABLE ag.barcode SET SCHEMA barcodes;
ALTER TABLE ag.project SET SCHEMA barcodes;
ALTER TABLE ag.project_barcode SET SCHEMA barcodes;
ALTER TABLE ag.plate SET SCHEMA barcodes;
ALTER TABLE ag.barcode_exceptions SET SCHEMA barcodes;
ALTER TABLE ag.plate_barcode SET SCHEMA barcodes;