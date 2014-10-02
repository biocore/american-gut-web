SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_get_participant_samples (
    ag_login_id_ uuid,
    participant_name_ text,
    results_ refcursor
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
        where   (akb.site_sampled IS NOT NULL AND akb.site_sampled::text <> '')
                and ak.ag_login_id = ag_login_id_
                and akb.participant_name = participant_name_;
    return results_;            
end;
/*
begin;
select ag_get_participant_samples(cast ('d8592c747da12135e0408a80115d6401' as uuid), 'foo', 'a'); 
fetch all in a;
commit;
*/
 
$body$
LANGUAGE PLPGSQL;




