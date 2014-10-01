SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_verify_password_change_code (
   email_ text,
   kitid_ text,
   pass_code_ text
)
 RETURNS integer AS $body$
DECLARE
    results_ refcursor;
    current_time_ timestamp(6) := clock_timestamp();
    is_valid_ integer;  
    rec RECORD;
   

BEGIN
open results_ for
select k.PASS_RESET_TIME
from ag_kit k inner join ag_login l on l.AG_LOGIN_ID = k.AG_LOGIN_ID
        where k.PASS_RESET_CODE = pass_code_ and l.EMAIL = email_  and k.SUPPLIED_KIT_ID = kitid_;
Fetch results_ into rec;
IF NOT FOUND THEN 
    is_valid_ = 0;
ELSE
    IF (current_time_ < cast(rec.PASS_RESET_TIME as timestamp)) then
        is_valid_ = 1;
    ELSE
        is_valid_ = 0;
    END IF;
END IF;
return is_valid_;

end;
 
/*
begin;
select  ag_verify_password_change_code('test@microbio.me', 'test', '123456789');
commit;
*/
 
 
$body$
LANGUAGE PLPGSQL;



--Do we actually use this table?  There are only 13 rows and none of
--the data makes any sense
