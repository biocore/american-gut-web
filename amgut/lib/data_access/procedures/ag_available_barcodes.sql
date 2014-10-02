SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_available_barcodes (
    ag_login_id_ uuid,
    results_ in out refcursor
)
 RETURNS refcursor AS $body$
BEGIN

    open results_ for
        SELECT  akb.barcode 
        from    ag_kit_barcodes akb 
                inner join ag_kit ak 
                on akb.ag_kit_id = ak.ag_kit_id 
        where   ak.ag_login_id = ag_login_id_
                and ak.kit_verified = 'y'
                and coalesce(akb.sample_date::text, '') = '';

end;
 
 
$body$
LANGUAGE PLPGSQL;
/*
BEGIN;
select ag_available_barcodes(cast ('d8592c747da12135e0408a80115d6401' as uuid), 'a'); 
fetch all in a;
COMMIT;
*/




