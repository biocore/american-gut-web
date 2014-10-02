SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION update_akb (
    barcode_ text,
    moldy_ char,
    overloaded_ char,
    other_ char,
    other_text_ text,
    date_ text
)
 RETURNS VOID AS $body$
BEGIN

    update  ag_kit_barcodes
    set     moldy = moldy_,
            overloaded = overloaded_,
            other = other_,
            other_text = other_text_,
            date_of_last_email = date_
    where   barcode = barcode_;
end;
 /*
begin;
select update_akb('000010860', 'n', 'n', 'y', 'some other text', '07/30/2014');
select * from ag_kit_barcodes where barcode = '000010860';
select update_akb('000010860', null, null, null, null, null);
select * from ag_kit_barcodes where barcode = '000010860';
commit;
*/
 
$body$
LANGUAGE PLPGSQL;




