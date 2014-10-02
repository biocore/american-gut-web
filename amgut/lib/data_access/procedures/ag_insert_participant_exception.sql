SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_insert_participant_exception (
    ag_login_id_ uuid,
    participant_name_ text
)
 RETURNS VOID AS $body$
BEGIN

  insert    into ag_participant_exceptions
            (ag_login_id, participant_name)
  values    (ag_login_id_, participant_name_);
end;
/*
begin;
select ag_insert_participant_exception(cast('d8592c747da12135e0408a80115d6401' as uuid), 'random kid');
select * from ag_participant_exceptions where ag_login_id = cast('d8592c747da12135e0408a80115d6401' as uuid);
delete from ag_participant_exceptions where  ag_login_id = cast('d8592c747da12135e0408a80115d6401' as uuid) and participant_name = 'random kid';
select * from ag_participant_exceptions where ag_login_id = cast('d8592c747da12135e0408a80115d6401' as uuid); 
commit;
*/
 
$body$
LANGUAGE PLPGSQL;




