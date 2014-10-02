SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_get_survey_details (
    ag_login_id_ uuid,
    participant_name_ text,
    user_data_ refcursor
)
 RETURNS refcursor AS $body$
BEGIN

    open user_data_ for
        SELECT  cast(ag_login_id as varchar(100)) as ag_login_id,
                participant_name, question, answer
        from    ag_survey_answer
        where   ag_login_id = ag_login_id_ and participant_name = participant_name_;
    return user_data_;
end;
/*
begin;
select ag_get_survey_details(cast ('d8592c747da12135e0408a80115d6401' as uuid), 'foo', 'a'); 
fetch all in a;
commit;
*/
 
$body$
LANGUAGE PLPGSQL;




