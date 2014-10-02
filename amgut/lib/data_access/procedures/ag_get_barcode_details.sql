SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_get_barcode_details (
    barcode_ in text,
    user_data_ refcursor
)
 RETURNS refcursor AS $body$
BEGIN

    open user_data_ for
        SELECT  al.email, 
                cast(akb.ag_kit_barcode_id as varchar(100)), 
                cast(akb.ag_kit_id as varchar(100)), 
                akb.barcode, 
                akb.site_sampled, akb.environment_sampled, akb.sample_date, 
                akb.sample_time, akb.participant_name, akb.notes,
                akb.refunded, akb.withdrawn, akb.moldy, akb.other, 
                akb.other_text, akb.date_of_last_email ,akb.overloaded, al.name,
                b.status
        from    ag_kit_barcodes akb
                inner join ag_kit ak
                on akb.ag_kit_id = ak.ag_kit_id
                inner join ag_login al
                on ak.ag_login_id = al.ag_login_id
                inner join barcode b 
                on akb.barcode = b.barcode
        where   akb.barcode = barcode_;
    return user_data_;

end;
/*
begin;
select ag_get_barcode_details('000010860', 'a');
fetch all in a;
commit;
*/

$body$
LANGUAGE PLPGSQL;




