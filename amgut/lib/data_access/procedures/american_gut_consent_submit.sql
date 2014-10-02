SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION american_gut_consent_submit (
  participant_name_ in text,
  contact_code_ in text,
  is_7_to_13_ in text,
  parent_1_name_ in text,
  parent_2_name_ in text,
  parent_1_code_ in text,
  parent_2_code_ in text,
  deceased_parent_ in text
)
 RETURNS VOID AS $body$
BEGIN

    insert  into american_gut_consent  
            (participant_name, contact_code,is_7_to_13, parent_1_name,
            parent_2_name, parent_1_code, parent_2_code, deceased_parent)
    values  (participant_name_, contact_code_,is_7_to_13_, parent_1_name_,
            parent_2_name_, parent_1_code_, parent_2_code_, deceased_parent_);

end;
/*
begin;
select american_gut_consent_submit('testkid', 'test', 'n', 'test', 'test','','','n');
select * from american_gut_consent where participant_name = 'testkid';
delete from american_gut_consent where participant_name = 'testkid';
select * from american_gut_consent where participant_name = 'testkid';
commit;
*/

$body$
LANGUAGE PLPGSQL;



