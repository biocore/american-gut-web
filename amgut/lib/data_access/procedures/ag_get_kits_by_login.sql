SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_get_kits_by_login (
    user_data_ refcursor
)
 RETURNS refcursor AS $body$
BEGIN

    open user_data_ for
        SELECT  lower(al.email) as email, ak.supplied_kit_id, 
                cast(ak.ag_kit_id as varchar(100)) as ag_kit_id
        from    ag_login al
                inner join ag_kit ak
                on al.ag_login_id = ak.ag_login_id
        order by lower(al.email), ak.supplied_kit_id;
    return user_data_;
end;
/*
begin;
select ag_get_kits_by_login ('a');
fetch all in a;
commit;
*/
 
$body$
LANGUAGE PLPGSQL;




