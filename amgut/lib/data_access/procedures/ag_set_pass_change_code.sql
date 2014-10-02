SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_set_pass_change_code (
  email_ in text, 
  kit_id_ in text,  
  pass_code_ in text
)  RETURNS VOID AS $body$
BEGIN
  update ag_kit set pass_reset_code = pass_code_, pass_reset_time = clock_timestamp() + interval '2' hour where
     supplied_kit_id = kit_id_ and ag_login_id in (select ag_login_id from ag_login where email = email_);
end;


/*
select ag_set_pass_change_code('test@microbio.me','test', '123456789');

execute ag_set_pass_change_code('test@microbio.me','test', '123456789');
*/
 
 
$body$
LANGUAGE PLPGSQL;




