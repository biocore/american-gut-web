SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_get_environmental_samples (
    ag_login_id_ uuid,
    results_ in refcursor
)
 RETURNS refcursor AS $body$
BEGIN

    open results_ for
        SELECT  akb.barcode, akb.site_sampled, akb.sample_date, akb.sample_time, 
                akb.notes, b.status
        from    ag_kit_barcodes akb
                inner join barcode b
                on akb.barcode = b.barcode
                inner join ag_kit ak 
                on akb.ag_kit_id = ak.ag_kit_id 
        where   (akb.environment_sampled IS NOT NULL AND akb.environment_sampled::text <> '')
                and ak.ag_login_id = ag_login_id_;
    return results_;     
end;
 /*
 begin;
select ag_get_environmental_samples(cast ('d8592c747da12135e0408a80115d6401' as uuid), 'a'); 
fetch all in a;
 commit;
 */
 
$body$
LANGUAGE PLPGSQL;




