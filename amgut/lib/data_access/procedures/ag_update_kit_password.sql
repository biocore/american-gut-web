SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_update_kit_password (
  KIT_ID_ IN text 
, PASS_ IN text 
)  RETURNS VOID AS $body$
BEGIN
  UPDATE AG_KIT  set kit_password = PASS_, pass_reset_code = null
  where supplied_kit_id = KIT_ID_;  
END;
 /*
 lookup old password
begin;
select ag_update_kit_password('test', 'newpass');
select * from ag_kit where supplied_kit_id = 'test';
select ag_update_kit_password('test', 'oldpass');
select * from ag_kit where supplied_kit_id = 'test';
commit;
*/

$body$
LANGUAGE PLPGSQL;




