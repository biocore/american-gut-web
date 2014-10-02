SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_update_barcode (
    barcode_ in text,
    ag_kit_id_ in uuid, 
    site_sampled_ in text, 
    environment_sampled_ in text, 
    sample_date_ in text, 
    sample_time_ in text, 
    participant_name_ in text, 
    notes_ in text,
    refunded_ in text, 
    withdrawn_ in text
)
 RETURNS VOID AS $body$
BEGIN

    update  ag_kit_barcodes
    set     ag_kit_id = ag_kit_id_,
            site_sampled = site_sampled_,
            environment_sampled = environment_sampled_,
            sample_date = sample_date_,
            sample_time = sample_time_,
            participant_name = participant_name_,
            notes = notes_,
            refunded = refunded_,
            withdrawn = withdrawn_
    where   barcode = barcode_; 

end;
/*
begin;
select ag_update_barcode('000010860', cast ('d8592c74-7da2-2135-e040-8a80115d6401' as uuid), 'Stool', '', '07/30/2014', '9:30 AM', 'test', '');
select * from ag_kit_barcodes where barcode = '000010860';
select ag_update_barcode('000010860', cast ('d8592c74-7da2-2135-e040-8a80115d6401' as uuid), '', '', '', '', '', '');
select * from ag_kit_barcodes where barcode = '000010860';
commit;
*/
 
 
$body$
LANGUAGE PLPGSQL;




