SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_get_logins (
    user_data_ refcursor
)
 RETURNS refcursor AS $body$
BEGIN

    open user_data_ for
        SELECT  cast(ag_login_id as varchar(100)) as ag_login_id, 
                lower(email) as email, name
        from    ag_login
        order by lower(email);
    return user_data_;
end;
/*
begin;
select ag_get_logins('a');
fetch all in a;
commit;
*/

$body$
LANGUAGE PLPGSQL;




