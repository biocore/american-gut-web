SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_get_next_barcode (refcursor)
 RETURNS refcursor AS $body$
 
BEGIN

    open $1 for
        SELECT  barcode_seq.next_barcode
        from    (
                    SELECT  max(cast(barcode as integer)) + 1 as next_barcode
                    from    barcode
                    where   length(barcode) = 9
                            and barcode not like '9%'
                ) as barcode_seq
        order by barcode_seq.next_barcode;
        return $1;

end; 
/* BEGIN;
select ag_get_next_barcode('a');
fetch all in a;
COMMIT;
*/

$body$
LANGUAGE PLPGSQL;




