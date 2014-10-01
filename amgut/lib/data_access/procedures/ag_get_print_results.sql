SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_get_print_results (
   kit_id_  text,
   results_ refcursor
) RETURNS refcursor AS $body$
BEGIN
  open results_ for 
  SELECT print_results from ag_handout_kits 
  where kit_id = kit_id_;
  return results_;
end;
/*
begin;
select ag_get_print_results('PGP_KBXvt', 'a');
fetch all in a;
commit;
*/

$body$
LANGUAGE PLPGSQL;




