SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_update_kit (
    ag_kit_id_ uuid,
    supplied_kit_id_ text, 
    kit_password_ text, 
    swabs_per_kit_ bigint, 
    kit_verification_code_ text
)
 RETURNS VOID AS $body$
BEGIN

    update  ag_kit
    set     supplied_kit_id = supplied_kit_id_,
            kit_password = kit_password_,
            swabs_per_kit = swabs_per_kit_,
            kit_verification_code = kit_verification_code_
    where   ag_kit_id = ag_kit_id_; 

end;
 /*
 look up oldpassword!!!
begin;
select ag_update_kit (cast('d8592c74-7da2-2135-e040-8a80115d6401' as uuid), 'test22', 'newpass', 24, 'ver');
select * from ag_kit where ag_kit_id = 'd8592c74-7da2-2135-e040-8a80115d6401';
select ag_update_kit (cast('d8592c74-7da2-2135-e040-8a80115d6401' as uuid), 'test', 'oldpass', 1, 'test');
select * from ag_kit where ag_kit_id = 'd8592c74-7da2-2135-e040-8a80115d6401';
commit;
*/
 
$body$
LANGUAGE PLPGSQL;




