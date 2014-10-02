SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_get_barcodes (
    user_data_ refcursor
)
 RETURNS refcursor AS $body$
BEGIN

    open user_data_ for
        SELECT  barcode
        from    ag_kit_barcodes
        order by barcode;
    return user_data_;
end;
/*
begin;
select ag_get_barcodes('a');
fetch all in a;
commit;
*/ 
 
$body$
LANGUAGE PLPGSQL;




