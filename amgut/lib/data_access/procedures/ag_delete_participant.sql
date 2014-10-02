SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_delete_participant (
    ag_login_id_ uuid,
    participant_name_ text
)
 RETURNS VOID AS $body$
BEGIN

    -- Remove the backup log
    delete from  ag_survey_answer
    where   ag_login_id = ag_login_id_
            and participant_name = participant_name_;
    
    -- Remove the multiple answers
    delete from  ag_survey_multiples
    where   ag_login_id = ag_login_id_
            and participant_name = participant_name_;
    -- Remove the participant/survey/consent
    delete from  ag_human_survey
    where   ag_login_id = ag_login_id_
            and participant_name = participant_name_;
    -- Remove the participant/survey/consent if they are an animal
    delete from  ag_animal_survey
    where   ag_login_id = ag_login_id_
            and participant_name = participant_name_;
end;
 /*begin;
 insert into ag_human_survey (ag_login_id, participant_name) values (cast ('d8592c747da12135e0408a80115d6401' as uuid), 'sp_test');
select ag_delete_participant(cast ('d8592c747da12135e0408a80115d6401' as uuid), 'sp_test');
select ag_get_human_participants(cast('d8592c747da12135e0408a80115d6401' as uuid), 'a'); 
fetch all in a;
*/
 
$body$
LANGUAGE PLPGSQL;




