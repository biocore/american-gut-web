-- create a table to support the persistent buffer for scanned samples in
-- labadmin
CREATE TABLE barcodes.project_qiita_buffer (
    barcode varchar,
    pushed_to_qiita char default 'N',
    CONSTRAINT pk_project_qiita_buffer PRIMARY KEY (barcode),
    CONSTRAINT fk_project_qiita_buffer FOREIGN KEY (barcode) REFERENCES barcodes.barcode(barcode)
);
