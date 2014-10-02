SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION set_barcode_proj_type (
  project_ in text
, barcode_ in text 
)  RETURNS VOID AS $body$
DECLARE
 
  project_code bigint;


BEGIN
  select project_id into project_code from project where project = project_;
  update project_barcode set project_id = project_code where barcode = barcode_;
end;
/*
begin;
select set_barcode_proj_type('American Gut Handout kit' , '000000001');
select * from  project_barcode where barcode = '000000001';
select set_barcode_proj_type('American Gut Project' , '000000001');
select * from  project_barcode where barcode = '000000001';
commit;
*/

$body$
LANGUAGE PLPGSQL;




