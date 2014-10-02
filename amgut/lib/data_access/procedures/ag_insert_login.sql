SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_insert_login (
    email_ text, 
    name_ text, 
    address_ text, 
    city_ text, 
    state_ text, 
    zip_ text, 
    country_ text
)
 RETURNS VOID AS $body$
BEGIN

  insert    into ag_login
            (email, name, address, city, state, zip, country)
  values    (email_, name_, address_, city_, state_, zip_, country_);
  

end;
/*
begin;
select ag_insert_login('deleteme@no.no', 'testkit', 'testaddr', 'testcity', 'teststate', 'testzip', 'testcountry' )
select * from ag_login where email = 'deleteme@no.no';
delete from ag_login where email = 'deleteme@no.no';
select * from ag_login where email = 'deleteme@no.no';
commit;
*/
 
 
$body$
LANGUAGE PLPGSQL;




