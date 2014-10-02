SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_get_barcodes_by_login (
    ag_login_id_ in uuid,
    user_data_ refcursor
)
 RETURNS refcursor AS $body$
BEGIN

    open user_data_ for
        SELECT  al.email, akb.ag_kit_barcode_id, akb.ag_kit_id, akb.barcode, 
                akb.site_sampled, akb.environment_sampled, akb.sample_date, 
                akb.sample_time, akb.participant_name, akb.notes
        from    ag_kit_barcodes akb
                inner join ag_kit ak
                on akb.ag_kit_id = ak.ag_kit_id
                inner join ag_login al
                on ak.ag_login_id = al.ag_login_id
        where   ak.ag_login_id = ag_login_id_;
    return user_data_;

end;
 /*
 begin;
select ag_get_barcodes_by_login(cast ('d8592c747da12135e0408a80115d6401' as uuid), 'a'); 
fetch all in a;
 commit;
 */
 
$body$
LANGUAGE PLPGSQL;




