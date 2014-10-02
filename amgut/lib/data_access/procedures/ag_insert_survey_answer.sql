SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_insert_survey_answer (
  ag_login_id_ uuid,
  participant_name_ in text,
  question_ in text,
  answer_ in text
)
 RETURNS VOID AS $body$
BEGIN

  insert into ag_survey_answer
  (ag_login_id, participant_name, question, answer)

  values
  (ag_login_id_, participant_name_, question_, answer_);
end;
/*
begin;
select ag_insert_survey_answer(cast('d8592c747da12135e0408a80115d6401' as uuid), 'test', 'badquest', 'badans');
select * from ag_survey_answer where question = 'badquest';
delete from ag_survey_answer where ag_login_id = cast('d8592c747da12135e0408a80115d6401' as uuid) and participant_name = 'test' and question = 'badquest';
select * from ag_survey_answer where question = 'badquest';
commit;
*/
 
 
$body$
LANGUAGE PLPGSQL;




