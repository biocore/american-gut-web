SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_get_barcodes_by_kit (
  supplied_kit_id_ in text 
, results_  refcursor
)  RETURNS refcursor AS $body$
BEGIN
  open results_ for 
    SELECT b.barcode from ag_kit_barcodes b inner join ag_kit k on k.ag_kit_id =b.ag_kit_id 
      where k.supplied_kit_id = supplied_kit_id_;
  return results_;
       
end ;
/*
begin;
select ag_get_barcodes_by_kit('test', 'a');
fetch all in a;
commit;
*/

$body$
LANGUAGE PLPGSQL;




