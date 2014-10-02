SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_delete_survey_answer (
  ag_login_id_ uuid,
  participant_name_ in text
)
 RETURNS VOID AS $body$
BEGIN
  delete from ag_survey_answer
  where ag_login_id = ag_login_id_ and participant_name = participant_name_;
end;
 /*
 begin;
 insert into ag_survey_answer(ag_login_id, participant_name, question, answer) values (cast('d8592c747da12135e0408a80115d6401' as uuid), 'Emily2', 'race','Caucasian'), (cast('d8592c747da12135e0408a80115d6401' as uuid), 'Emily2', 'cat', 'yes');
select * from ag_survey_answer where ag_login_id = cast('d8592c747da12135e0408a80115d6401' as uuid) and participant_name = 'Emily2';
select ag_delete_survey_answer(cast('d8592c747da12135e0408a80115d6401' as uuid), 'Emily2');
select * from ag_survey_answer where ag_login_id = cast('d8592c747da12135e0408a80115d6401' as uuid) and participant_name = 'Emily2';
 commit;
 */
 
$body$
LANGUAGE PLPGSQL;




