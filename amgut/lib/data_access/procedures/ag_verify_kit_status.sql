SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_verify_kit_status (
  -- define the input to this procedure
  supplied_kit_id_ IN text
)
 RETURNS VOID AS $body$
BEGIN
  UPDATE AG_KIT
  SET KIT_VERIFIED='y'
  WHERE SUPPLIED_KIT_ID=supplied_kit_id_;
end;
 /*
begin;
update ag_kit set kit_verified = 'n' where supplied_kit_id = 'test';
select ag_verify_kit_status('test');
select * from ag_kit where supplied_kit_id = 'test';
commit;
*/
 
$body$
LANGUAGE PLPGSQL;




