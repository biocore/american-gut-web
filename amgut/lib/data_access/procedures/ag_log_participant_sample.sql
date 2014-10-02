SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_log_participant_sample (
    barcode_ text,
    sample_site_ text,
    environment_sampled_ text,
    sample_date_ text,
    sample_time_ text,
    participant_name_ text,
    notes_ text
)
 RETURNS VOID AS $body$
BEGIN

    update  ag_kit_barcodes
    set     site_sampled = sample_site_,
            environment_sampled = environment_sampled_,
            sample_date = sample_date_,
            sample_time = sample_time_,
            participant_name = participant_name_,
            notes = notes_
    where   barcode = barcode_;
end;
/*
begin;
select ag_log_participant_sample('000010860', 'Stool', '', '07/29/2014', '09:30 AM', 'Emily', 'no notes');
select * from ag_kit_barcodes where barcode = ('000010860');
select ag_delete_sample ('000010860', cast('d8592c747da12135e0408a80115d6401' as uuid));
select * from ag_kit_barcodes where barcode = '000010860';
commit;
*/
 
$body$
LANGUAGE PLPGSQL;




