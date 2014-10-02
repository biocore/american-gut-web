SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_insert_kit (
    ag_login_id_ uuid, 
    kit_id_ text, 
    kit_password_ text, 
    swabs_per_kit_ bigint, 
    kit_verification_code_ text,
    print_results_ text
)
 RETURNS VOID AS $body$
BEGIN

  insert    into ag_kit
            (ag_login_id, supplied_kit_id, kit_password, swabs_per_kit, kit_verification_code, print_results)
  values    (ag_login_id_, kit_id_, kit_password_, swabs_per_kit_, kit_verification_code_, print_results_);
 
end;
/*
begin;
select ag_insert_kit(cast('d8592c747da12135e0408a80115d6401' as uuid), 'somekit','pass', 2, 'ver', 'n');
select * from ag_kit where ag_login_id = cast('d8592c747da12135e0408a80115d6401' as uuid);
delete from ag_kit where ag_login_id = cast('d8592c747da12135e0408a80115d6401' as uuid) and supplied_kit_id = 'somekit';
select * from ag_kit where ag_login_id = cast('d8592c747da12135e0408a80115d6401' as uuid);
commit;
*/
$body$
LANGUAGE PLPGSQL;




