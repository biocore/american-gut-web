SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_is_handout (
    kit_id_ text,
    password_ text
)
 RETURNS char AS $body$
DECLARE
    is_handout_ char;
    cnt bigint;

BEGIN

    is_handout_ := 'n';

    select  count(*) into cnt
    from    ag_handout_kits
    where   kit_id = kit_id_
            and password = password_;
            
    if (cnt > 0)
    then
        is_handout_ := 'y';
    end if;   
    return is_handout_; 

end;
 /*
 begin;
 select ag_is_handout('test', 'wrongpass');
 commit;
 */
 
$body$
LANGUAGE PLPGSQL;




