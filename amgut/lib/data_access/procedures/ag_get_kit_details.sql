SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_get_kit_details (
    supplied_kit_id_ IN text,
    result_ refcursor
)
 RETURNS refcursor AS $body$
BEGIN

    open result_ for
    SELECT
        cast(ag_kit_id as varchar(100)),
        supplied_kit_id,
        kit_password,
        swabs_per_kit,
        kit_verification_code,
        kit_verified,
        verification_email_sent
    from
        ag_kit
    where
        supplied_kit_id = supplied_kit_id_;
    return result_;
end;
/*
begin;
select ag_get_kit_details('test', 'a');
fetch all in a;
commit;
*/
 
$body$
LANGUAGE PLPGSQL;




