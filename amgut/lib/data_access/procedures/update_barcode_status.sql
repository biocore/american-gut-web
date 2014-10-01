SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION update_barcode_status (
    status_ text,
    postmark_ text,
    scan_date_ text,
    barcode_ text
)
 RETURNS VOID AS $body$
BEGIN

    update  barcode
    set     status = status_,
            sample_postmark_date = postmark_,
            scan_date = scan_date_
    where   barcode = barcode_;
end;
/*
begin;
select update_barcode_status ('Received', '07/27/2014', '07/30/2014', '000010860');
select * from barcode where barcode = '000010860';
select update_barcode_status (null, null, null, '000010860');
select * from barcode where barcode = '000010860';
commit;
*/

 
$body$
LANGUAGE PLPGSQL;


