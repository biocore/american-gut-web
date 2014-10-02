SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_add_participant (
    ag_login_id_ uuid,
    participant_name_ text
)
 RETURNS VOID AS $body$
BEGIN
  -- new code written by Emily 
    BEGIN
        insert into ag_human_survey (ag_login_id, participant_name) 
        values (ag_login_id_, participant_name_);
    EXCEPTION
        WHEN OTHERS THEN 
            END;
end;
 /*
 begin;
 select ag_add_participant(cast ('d8592c747da12135e0408a80115d6401' as uuid), 'sp_test');
 select ag_get_human_participants(cast('d8592c747da12135e0408a80115d6401' as uuid), 'a'); 
fetch all in a;
delete from ag_human_survey where ag_login_id = cast ('d8592c747da12135e0408a80115d6401' as uuid) and participant_name ='sp_test';
 commit;
 */
 
$body$
LANGUAGE PLPGSQL;




