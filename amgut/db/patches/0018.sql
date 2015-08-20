-- August 19, 2015
-- Convert date and time columns from varchar to proper formats

ALTER TABLE ag.ag_kit_barcodes
ALTER COLUMN sample_time TYPE time without time zone
USING CASE
    WHEN trim(both ' ' FROM sample_time) ~ '00\:[0-9]{2} {0,1}(AM|aM|Am|am)' THEN
        to_timestamp(trim(both ' pPaAmM' FROM sample_time), '12:MI am')
    WHEN trim(both ' ' FROM sample_time) ~ '(1[3-9]|2[0-3])\:.*' THEN
        to_timestamp(trim(both ' pPaAmM' FROM sample_time), 'HH24:MI')
    WHEN trim(both ' ' FROM sample_time) ~ '[0-9]{1,2}\:[0-9]{2} {0,1}(AM|aM|Am|am)' THEN
        to_timestamp(trim(both ' pPaAmM' FROM sample_time), 'HH:MI am')
    WHEN trim(both ' ' FROM sample_time) ~ '[0-9]{1,2}\:[0-9]{2} {0,1}(PM|pM|Pm|pm)' THEN
        to_timestamp(trim(both ' pPaAmM' FROM sample_time), 'HH:MI pm')
    WHEN trim(both ' ' FROM sample_time) ~ '[0-9]{1,2}\.[0-9]{2} {0,1}(AM|aM|Am|am)' THEN
        to_timestamp(trim(both ' pPaAmM' FROM sample_time), 'HH.MI am')
    WHEN trim(both ' ' FROM sample_time) ~ '[0-9]{1,2}\.[0-9]{2} {0,1}(PM|pM|Pm|pm)' THEN
        to_timestamp(trim(both ' pPaAmM' FROM sample_time), 'HH.MI pm')
    ELSE
        NULL
END;

ALTER TABLE ag.ag_kit_barcodes
ALTER COLUMN sample_date TYPE date
USING CASE
    WHEN trim(both ' ' FROM sample_date) ~ '[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}' THEN
        to_timestamp(trim(both ' ' FROM sample_date), 'MM/DD/YYYY')
    WHEN trim(both ' ' FROM sample_date) ~ '[0-9]{1,2}/[0-9]{1,2}/[0-9]{2}' THEN
        to_timestamp(trim(both ' ' FROM sample_date), 'MM/DD/YY')
    ELSE
        NULL
END;

ALTER TABLE ag.ag_kit_barcodes
ALTER COLUMN date_of_last_email TYPE date
USING CASE
    WHEN trim(both ' ' FROM date_of_last_email) ~ '[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}' THEN
        to_timestamp(trim(both ' ' FROM date_of_last_email), 'MM/DD/YYYY')
    WHEN trim(both ' ' FROM date_of_last_email) ~ '[0-9]{1,2}/[0-9]{1,2}/[0-9]{2}' THEN
        to_timestamp(trim(both ' ' FROM date_of_last_email), 'MM/DD/YY')
    ELSE
        NULL
END;

ALTER TABLE barcodes.barcode
ALTER COLUMN scan_date TYPE date
USING CASE
    WHEN trim(both ' ' FROM scan_date) ~ '[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}' THEN
        to_timestamp(left(scan_date,10), 'MM/DD/YYYY')
    WHEN trim(both ' ' FROM scan_date) ~ '[0-9]{1,2}/[0-9]{1,2}/[0-9]{2}' THEN
        to_timestamp(left(scan_date,8), 'MM/DD/YY')
    ELSE
        NULL
END;

ALTER TABLE barcodes.barcode
ALTER COLUMN sample_postmark_date TYPE date
USING CASE
    WHEN trim(both ' ' FROM sample_postmark_date) ~ '[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}' THEN
        to_timestamp(left(sample_postmark_date,10), 'MM/DD/YYYY')
    WHEN trim(both ' ' FROM sample_postmark_date) ~ '[0-9]{1,2}/[0-9]{1,2}/[0-9]{2}' THEN
        to_timestamp(left(sample_postmark_date,8), 'MM/DD/YY')
    ELSE
        NULL
END;

-- Make sure all barcodes in AG kits are assigned to AG project
DO $do$
DECLARE
    pid integer;
BEGIN
    pid := (SELECT project_id FROM barcodes.project WHERE project = 'American Gut Project');
    INSERT INTO barcodes.project_barcode (project_id, barcode)
        SELECT pid, barcode FROM (ag.ag_kit_barcodes akb
        FULL OUTER JOIN ag.ag_handout_barcodes ahb USING (barcode))
        LEFT JOIN barcodes.project_barcode pb USING (barcode)
        WHERE project_id IS NULL;
END $do$;
