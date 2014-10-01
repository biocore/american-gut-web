SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_get_human_participants (
    ag_login_id_ uuid,
    results_ in refcursor
)
 RETURNS refcursor AS $body$
BEGIN

    open results_ for
        SELECT  participant_name
        from    ag_human_survey
        where   ag_login_id = ag_login_id_;
    return results_;
end;
 /*
 begin;
select ag_get_human_participants(cast ('d8592c747da12135e0408a80115d6401' as uuid), 'a'); 
fetch all in a;
 commit;
 */
 
$body$
LANGUAGE PLPGSQL;




