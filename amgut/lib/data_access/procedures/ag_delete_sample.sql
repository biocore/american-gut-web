SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_delete_sample (
    barcode_ text,
    ag_login_id_ uuid
)
 RETURNS VOID AS $body$
BEGIN

    -- Delete the associated samples
    update  ag_kit_barcodes
    set     participant_name = null,
            site_sampled = null,
            sample_time = null,
            sample_date = null,
            environment_sampled = null,
            notes = ''
    where   barcode in
            (
                SELECT  akb.barcode
                from    ag_kit_barcodes akb
                        inner join ag_kit ak
                        on akb.ag_kit_id = ak.ag_kit_id
                where   ak.ag_login_id = ag_login_id_
                        and akb.barcode = barcode_
            );
            
    update  barcode
    set     status = ''
    where   barcode = barcode_;
end;
/*
begin;
update ag_kit_barcodes set site_sampled = 'Stool', sample_date = '07/30/2014', participant_name = 'test', sample_time = '9:30 AM' where barcode = '000010860';
select * from ag_kit_barcodes where barcode = '000010860';
select ag_delete_sample ('000010860', cast('d8592c747da12135e0408a80115d6401' as uuid));
select * from ag_kit_barcodes where barcode = '000010860';
commit;
*/ 

$body$
LANGUAGE PLPGSQL;




