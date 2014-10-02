SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_get_kit_id_by_email (
      email_ in text,
      user_data_ refcursor
) RETURNS refcursor AS $body$
BEGIN
     open user_data_ for
         SELECT  k.supplied_kit_id 
         from ag_kit k 
              inner join ag_login l 
              on k.ag_login_id = l.ag_login_id 
         where l.email = email_; 
    return user_data_;
END;
/*
begin;
select ag_get_kit_id_by_email('ejteravest@gmail.com', 'a');
fetch all in a;
commit;
*/
 
$body$
LANGUAGE PLPGSQL;




