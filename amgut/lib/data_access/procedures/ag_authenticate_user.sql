SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_authenticate_user (
  ag_kit_id_ in text,
  kit_password_ in text,
  user_data in out refcursor
)
 RETURNS refcursor AS $body$
BEGIN

  open user_data for
    SELECT  cast(agl.ag_login_id as varchar(100)) as ag_login_id, 
            agl.email, agl.name, agl.address, agl.city,
            agl.state, agl.zip, agl.country
    from    ag_login agl
            inner join ag_kit agk
            on agl.ag_login_id = agk.ag_login_id
    where   agk.supplied_kit_id = ag_kit_id_
            and agk.kit_password = kit_password_;

end;
/*BEGIN;
emte4531=# select ag_authenticate_user('DctkP', 'z077$Wcz', 'a');
select all in a;
COMMIT;
*/

 
$body$
LANGUAGE PLPGSQL;




