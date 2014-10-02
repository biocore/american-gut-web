SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_update_login (
    ag_login_id_ uuid,
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

    update  ag_login
    set     email = email_,
            name = name_,
            address = address_,
            city = city_,
            state = state_,
            zip = zip_,
            country = country_
    where   ag_login_id = ag_login_id_;
end;
 /*
begin;
select ag_update_login(cast('d8592c747da12135e0408a80115d6401' as uuid), 'chagned@chaged.com', '','add', 'city', 'state', 'zip', 'USA');
select * from ag_login where ag_login_id = cast('d8592c747da12135e0408a80115d6401' as uuid);
select ag_update_login(cast('d8592c747da12135e0408a80115d6401' as uuid), 'test@microbio.me', 'Test','Test', 'Boulder', 'CO', '80303', 'United States');
select * from ag_login where ag_login_id = cast('d8592c747da12135e0408a80115d6401' as uuid);
)
commit;
*/
 
$body$
LANGUAGE PLPGSQL;




