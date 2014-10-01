SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION get_project_names ( 
proj_names_ refcursor
) RETURNS refcursor AS $body$
BEGIN
  open proj_names_ for 
    SELECT project from project;
  return proj_names_;
end;
/*
begin;
select get_project_names('a');
fetch all in a;
commit;
*/

$body$
LANGUAGE PLPGSQL;




