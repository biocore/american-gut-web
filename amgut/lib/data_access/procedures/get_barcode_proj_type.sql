SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION get_barcode_proj_type (
   barcode_ text,
   proj_type_ refcursor
)
 RETURNS refcursor AS $body$
BEGIN

    open proj_type_ for
        SELECT  p.project
        from    project_barcode pb
                inner join project p
                on pb.project_id = p.project_id
        where   pb.barcode = barcode_;
    return proj_type_;
end;
/*
begin;
select get_barcode_proj_type('000001516', 'a');
fetch all in a;
commit;
*/
 
$body$
LANGUAGE PLPGSQL;




