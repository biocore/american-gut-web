SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_reassign_barcode (
    ag_kit_id_ uuid,
    barcode_ text
)
 RETURNS VOID AS $body$
BEGIN

    update  ag_kit_barcodes
    set     ag_kit_id = ag_kit_id_
    where   barcode = barcode_;
end;
/*
begin;
test = "d8592c74-7da2-2135-e040-8a80115d6401"
1111 = "dbd466b5-651b-bfb2-e040-8a80115d6775"
select ag_reassign_barcode(cast ('dbd466b5-651b-bfb2-e040-8a80115d6775' as uuid), '000010860');
select ag_get_barcodes_by_kit('1111', 'a');
fetch all in a;
select ag_reassign_barcode(cast ('d8592c74-7da2-2135-e040-8a80115d6401' as uuid), '000010860');
select ag_get_barcodes_by_kit('test', 'a');
fetch all in a;
commit;
*/ 
 
$body$
LANGUAGE PLPGSQL;




