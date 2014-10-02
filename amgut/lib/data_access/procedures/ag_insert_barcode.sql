SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_insert_barcode (
    ag_kit_id_ uuid, 
    barcode_ text
)
 RETURNS VOID AS $body$
BEGIN
    BEGIN
        insert into barcode (barcode) values (barcode_);
    EXCEPTION
        WHEN OTHERS THEN
            END;
    BEGIN
        insert into project_barcode (project_id, barcode) 
            values (1, barcode_);
    EXCEPTION
        WHEN OTHERS THEN
            END;        
    insert  into ag_kit_barcodes
            (ag_kit_id, barcode, sample_barcode_file)
    values  (ag_kit_id_, barcode_, barcode_ || '.jpg');
  
end;
/*
begin;
select ag_insert_barcode(cast('d8592c74-7da2-2135-e040-8a80115d6401' as uuid) ,'991299');
select * from ag_kit_barcodes where barcode = '991299';
select * from project_barcode where barcode = '991299';
select * from barcode where barcode = '991299';
delete from ag_kit_barcodes where barcode = '991299';
delete from project_barcode where barcode = '991299';
delete from barcode where barcode = '991299';
select * from ag_kit_barcodes where barcode = '991299';
select * from project_barcode where barcode = '991299';
select * from barcode where barcode = '991299';
commit;
*/ 
 
$body$
LANGUAGE PLPGSQL;




