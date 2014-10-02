SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_check_barcode_status (
    barcode_ in text,
    barcode_status_ refcursor
)
 RETURNS refcursor AS $body$
BEGIN

    open barcode_status_ for
        SELECT  akb.site_sampled, akb.sample_date, akb.sample_time,
                akb.moldy, akb.overloaded, akb.other, akb.other_text, akb.date_of_last_email,
                barcode.status, barcode.scan_date, barcode.sample_postmark_date,
                al.email, al.name
        from    ag_kit_barcodes akb
                inner join ag_kit ak
                on akb.ag_kit_id = ak.ag_kit_id
                inner join ag_login al
                on ak.ag_login_id = al.ag_login_id
                inner join barcode
                on akb.barcode = barcode.barcode
        where   akb.barcode = barcode_;
        return barcode_status_;
end;
/*
begin;
select ag_check_barcode_status('000001056', 'a');
fetch all in a;
coomit;
*/
 
$body$
LANGUAGE PLPGSQL;




