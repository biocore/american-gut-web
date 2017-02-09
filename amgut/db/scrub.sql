-- This script is used to scrub the live American Gut database in order to
-- generate a test database for Travis without personal information but
-- representative of the real world.

-- Function to generate a string with all the different characters present in
-- a column (adapted from: http://dba.stackexchange.com/a/83679)
CREATE FUNCTION retrieve_chars(column_name varchar, table_name varchar) RETURNS varchar AS $$
    DECLARE
        result varchar;
    BEGIN
         EXECUTE format(
            'SELECT string_agg(c, '''') FROM (SELECT DISTINCT regexp_split_to_table(%s, '''') AS c FROM %s) t',
            column_name, table_name)
         INTO result;
         RETURN result;
    END;
$$ language plpgsql;

-- Function to generate random strings of a given length from a given set
-- of characters (adapted from: http://stackoverflow.com/a/3972983/3746629)
CREATE FUNCTION random_string(length integer, source varchar, suffix varchar) RETURNS varchar AS $$
    DECLARE
        result varchar;
        chars text[];
    BEGIN
        chars := regexp_split_to_array(source, '');
        result := suffix;
        FOR i in 1..length LOOP
            result := result || chars[1+random()*(array_length(chars, 1) - 1)];
        END LOOP;
        RETURN result;
    END;
$$ language plpgsql;

-- Function to generate a random latitude or longitude
CREATE FUNCTION random_lat_or_long() RETURNS varchar AS $$
    DECLARE
        result varchar;
        numsource varchar;
    BEGIN
        numsource := '0123456789';
        result := random_string(2, numsource, '') || ',' || random_string(5, numsource, '');
        IF random() < 0.5 THEN
            result := '-' || result;
        END IF;
        RETURN result;
    END;
$$ language plpgsql;

-- Function to generate random emails
CREATE FUNCTION random_email(column_name varchar, table_name varchar) RETURNS varchar AS $$
    DECLARE
        source varchar;
    BEGIN
        source := retrieve_chars(column_name, table_name);
        source := replace(replace(source, '@', ''), '.', '');
        RETURN random_string(10, source, '') || '@' || random_string(5, source, '') || '.' || random_string(3, source, '');
    END;
$$ language plpgsql;

-- Function to generate random dates
CREATE FUNCTION random_date() RETURNS varchar AS $$
    DECLARE
        result varchar;
    BEGIN
        SELECT date(now() - trunc(random()  * 80) * '1 year'::interval - trunc(random() * 12) * '1 month'::interval - trunc(random() * 30) * '1 day'::interval) INTO result;
        RETURN result;
    END
$$ language plpgsql;

-- Create a temp table for storing the zipcodes
CREATE TEMP TABLE allzipcodes ON COMMIT DROP AS
    SELECT DISTINCT zip_code FROM ag.ag_human_survey;

-- We have all the functions that we need, start scrubbing data
DO $do$
DECLARE
    rec         RECORD;
    rec2        RECORD;
    numsource   varchar;
    source      varchar;
    source2     varchar;
    source3     varchar;
    source4     varchar;
    source5     varchar;
    source6     varchar;
    source7     varchar;
    source8     varchar;
    source9     varchar;
    source10    varchar;
    source11    varchar;
    source12    varchar;
    source13    varchar;
    passwd      varchar;
    newname     varchar;
BEGIN
    -- To simplify testing, all the passwords are going to be the same ('test')
    passwd := '$2a$12$rX8UTcDkIj8bwcxZ22iRpebAxblEclT83xBiUIdJGUJGoUfznu1RK';
    numsource := '0123456789';

    -- Table: ag_survey_multiples_backup; Columns: participant_name, item_value
    source := retrieve_chars('participant_name', 'ag.ag_survey_multiples_backup');
    source2 := retrieve_chars('item_value', 'ag.ag_survey_multiples_backup');
    FOR rec IN
        SELECT ag_login_id FROM ag.ag_survey_multiples_backup
    LOOP
        UPDATE ag.ag_survey_multiples_backup
            SET participant_name = random_string(10, source, 'Name - '),
                item_value = random_string(30, source, 'Free text - ')
            WHERE ag_login_id = rec.ag_login_id;
    END LOOP;

    -- Table: ag_handout_kits; Columns: password and verification_code
    source := retrieve_chars('verification_code', 'ag.ag_handout_kits');
    FOR rec IN
        SELECT kit_id FROM ag.ag_handout_kits
    LOOP
        UPDATE ag.ag_handout_kits
            SET password = passwd,
                verification_code = random_string(5, source, '');
    END LOOP;

    -- Table project; Columns: project
    source := retrieve_chars('project', 'barcodes.project');
    FOR rec IN
        SELECT project_id FROM barcodes.project WHERE project != 'American Gut Project'
    LOOP
        UPDATE barcodes.project
            SET project = random_string(10, source, 'Project - ');
    END LOOP;

    -- Table: consent_revoked; Columns: participant_name, participant_email
    source := retrieve_chars('participant_name', 'ag.consent_revoked');
    FOR rec IN
        SELECT ag_login_id FROM ag.consent_revoked
    LOOP
        UPDATE ag.consent_revoked
            SET participant_name = random_string(10, source, 'Name - '),
                participant_email = random_email('participant_email', 'ag.consent_revoked')
            WHERE ag_login_id = rec.ag_login_id;
    END LOOP;

    -- Table: ag_consent; Columns: participant_name, participant_email,
    -- parent_1_name, parent_2_name, assent_obtainer
    source := retrieve_chars('participant_name', 'ag.ag_consent');
    source2 := retrieve_chars('parent_1_name', 'ag.ag_consent');
    source3 := retrieve_chars('parent_2_name', 'ag.ag_consent');
    source4 := retrieve_chars('assent_obtainer', 'ag.ag_consent');
    FOR rec IN
        SELECT ag_login_id, participant_name FROM ag.ag_consent
    LOOP
        UPDATE ag.ag_consent
            SET participant_name = random_string(10, source, 'Name - '),
                participant_email = random_email('participant_email', 'ag.ag_consent'),
                parent_1_name = random_string(10, source, 'Name - '),
                parent_2_name = random_string(10, source, 'Name - '),
                assent_obtainer = random_string(10, source, 'Name - ')
            WHERE ag_login_id = rec.ag_login_id AND participant_name = rec.participant_name;
    END LOOP;

    -- Table: ag_login_surveys; Columns: participant_name
    source := retrieve_chars('participant_name', 'ag.ag_login_surveys');
    FOR rec IN
        SELECT ag_login_id FROM ag.ag_login_surveys
    LOOP
        UPDATE ag.ag_login_surveys
            SET participant_name = random_string(10, source, 'Name - ')
            WHERE ag_login_id = rec.ag_login_id;
    END LOOP;

    -- Table: ag_human_survey; Columns: participant_name, parent_1_name,
    -- parent_2_name, birth_date, phone_num, zip_code, foodallergies_other_text,
    -- race_other, antibiotic_condition, primary_vegetable, primary_carb,
    -- mainfactor_other_1, mainfactor_other_2, mainfactor_other_3,
    -- about_yourself_text, participant_email, participant_name_u
    source := retrieve_chars('participant_name', 'ag.ag_human_survey');
    source2 := retrieve_chars('parent_1_name', 'ag.ag_human_survey');
    source3 := retrieve_chars('parent_2_name', 'ag.ag_human_survey');
    source4 := retrieve_chars('foodallergies_other_text', 'ag.ag_human_survey');
    source5 := retrieve_chars('race_other', 'ag.ag_human_survey');
    source6 := retrieve_chars('antibiotic_condition', 'ag.ag_human_survey');
    source7 := retrieve_chars('primary_vegetable', 'ag.ag_human_survey');
    source8 := retrieve_chars('primary_carb', 'ag.ag_human_survey');
    source9 := retrieve_chars('mainfactor_other_1', 'ag.ag_human_survey');
    source10 := retrieve_chars('mainfactor_other_2', 'ag.ag_human_survey');
    source11 := retrieve_chars('mainfactor_other_3', 'ag.ag_human_survey');
    source12 := retrieve_chars('about_yourself_text', 'ag.ag_human_survey');
    source13 := retrieve_chars('participant_name_u', 'ag.ag_human_survey');
    FOR rec IN
        SELECT ag_login_id, participant_name FROM ag.ag_human_survey
    LOOP
        UPDATE ag.ag_human_survey
            SET participant_name = random_string(10, source, 'Name - '),
                parent_1_name = random_string(10, source2, 'Name - '),
                parent_2_name = random_string(10, source3, 'Name - '),
                birth_date = random_date(),
                phone_num = random_string(10, numsource, ''),
                zip_code = (SELECT zip_code FROM allzipcodes ORDER BY RANDOM() LIMIT 1),
                foodallergies_other_text = random_string(50, source4, 'Free text - '),
                race_other = random_string(20, source5, 'Free text - '),
                antibiotic_condition = random_string(30, source6, 'Free text - '),
                primary_vegetable = random_string(15, source7, 'Free text - '),
                primary_carb = random_string(15, source8, 'Free text - '),
                mainfactor_other_1 = random_string(20, source9, 'Free text - '),
                mainfactor_other_2 = random_string(20, source10, 'Free text - '),
                mainfactor_other_3 = random_string(20, soruce11, 'Free text - '),
                about_yourself_text = random_string(100, source12, 'Free text - '),
                participant_email = random_email('participant_email', 'ag.ag_human_survey'),
                participant_name_u = random_string(10, source13, 'Name - ')
            WHERE ag_login_id = rec.ag_login_id AND participant_name = rec.participant_name;
    END LOOP;

    -- Table: ag_survey_answer; randomize the birth month
    -- Magic number 111: birth month question
    FOR rec IN
        SELECT survey_id FROM ag.survey_answers WHERE survey_question_id = 111
    LOOP
        -- Adapted from http://dba.stackexchange.com/a/55401
        UPDATE ag.survey_answers
            SET response = ('[0:11]={January,February,March,April,May,June,July,August,September,October,November,December}'::text[])[trunc(random()*12)]
            WHERE survey_id = rec.survey_id AND survey_question_id = 111;
    END LOOP;

    -- Table: survey_answers_other; Columns: response
    source := retrieve_chars('response', 'ag.survey_answers_other');
    -- This column is stored in a weird way. It looks like a python list, but
    -- it always have a single element, even if it is an empty string. Thus,
    -- removing those characters that can break this structure
    source := replace(replace(replace(source, '""', ''), '[', ''), ']', '');
    FOR rec IN
        SELECT survey_id, survey_question_id FROM ag.survey_answers_other
    LOOP
        UPDATE ag.survey_answers_other
            SET response = '["' || random_string(20, source, 'Free text - ') || '"]'
            WHERE survey_id = rec.survey_id AND survey_question_id = rec.survey_question_id;
    END LOOP;

    -- Table: ag_participant_exceptions; columns: participant_name
    source := retrieve_chars('participant_name', 'ag.ag_participant_exceptions');
    FOR rec IN
        SELECT ag_login_id FROM ag.ag_participant_exceptions
    LOOP
        UPDATE ag.ag_participant_exceptions
            SET participant_name = random_string(10, source, 'Name - ')
        WHERE ag_login_id = rec.ag_login_id;
    END LOOP;

    -- Table: ag_animal_survey; Columns: participant_name, comments
    source := retrieve_chars('participant_name', 'ag.ag_animal_survey');
    source2 := retrieve_chars('comments', 'ag.ag_animal_survey');
    FOR rec IN
        SELECT ag_login_id, participant_name FROM ag.ag_animal_survey
    LOOP
        UPDATE ag.ag_animal_survey
            SET participant_name = random_string(10, source, 'Name - '),
                comments = random_string(50, source2, 'Free text - ')
            WHERE ag_login_id = rec.ag_login_id AND participant_name = rec.participant_name;
    END LOOP;

    -- Table: ag_login; columns: email, name, address, city, state, zip, latitude, longitude
    source := retrieve_chars('address', 'ag.ag_login');
    source2 := retrieve_chars('city', 'ag.ag_login');
    source3 := retrieve_chars('state', 'ag.ag_login');
    FOR rec IN
        SELECT ag_login_id FROM ag.ag_login
    LOOP
        UPDATE ag.ag_login
            SET email = random_email('email', 'ag.ag_login'),
                name = random_string('name', 'ag.ag_login'),
                address = random_string(4, numsource, '') || random_string(10, source, ' '),
                city = random_string(10, source2, 'City - '),
                state = random_string(10, source3, 'State - '),
                zip = random_string(5, numsource, ''),
                latitude = random_lat_or_long(),
                longitude = random_lat_or_long()
            WHERE ag_login_id = rec.ag_login_id;
    END LOOP;

    -- Table: ag_survey_answer; columns: participant_name, answer
    source := retrieve_chars('participant_name', 'ag.ag_survey_answer');
    source2 := retrieve_chars('answer', 'ag.ag_survey_answer');
    FOR rec IN
        SELECT DISTINCT ag_login_id, participant_name FROM ag.ag_survey_answer
    LOOP
        newname := random_string(10, source, 'Name - ');
        FOR rec2 IN
            SELECT * FROM ag.ag_survey_answer
                WHERE ag_login_id = rec.ag_login_id AND participant_name = rec.participant_name
        LOOP
            UPDATE ag.ag_survey_answer
                SET participant_name = newname,
                    answer = random_string(30, source2, 'Free text - ')
                WHERE ag_login_id = rec2.ag_login_id AND
                      participant_name = rec2.participant_name AND
                      question = rec2.question;
        END LOOP;
    END LOOP;

    -- Table: ag_survey_multiples; Columns: participant_name, item_value
    source := retrieve_chars('participant_name', 'ag.ag_survey_multiples');
    source2 := retrieve_chars('item_value', 'ag.ag_survey_multiples');
    FOR rec IN
        SELECT DISTINCT ag_login_id, participant_name FROM ag.ag_survey_multiples
    LOOP
        newname := random_string(10, source, 'Name - ');
        FOR rec2 IN
            SELECT * FROM ag.ag_survey_multiples
                WHERE ag_login_id = rec.ag_login_id AND participant_name = rec.participant_name
        LOOP
            UPDATE ag.ag_survey_multiples
                SET participant_name = newname,
                    item_value = random_string(10, source2, 'Free text - ')
                WHERE ag_login_id = rec2.ag_login_id AND
                      participant_name = rec2.participant_name AND
                      item_name = rec2.item_name;
        END LOOP;
    END LOOP;

    -- Table: ag_kit; columns: kit_password, kit_verification_code, open_humans_token
    source := retrieve_chars('kit_verification_code', 'ag.ag_kit');
    FOR rec IN
        SELECT ag_kit_id FROM ag.ag_kit
    LOOP
        UPDATE ag.ag_kit
            SET kit_password = passwd,
                kit_verification_code = random_string(5, source, ''),
                open_humans_token = NULL
            WHERE ag_kit_id = rec.ag_kit_id;
    END LOOP;

    --Table: ag_kit_barcodes; columns: notes, other_text
    source := retrieve_chars('notes', 'ag.ag_kit_barcodes');
    source2 := retrieve_chars('other_text', 'ag.ag_kit_barcodes');
    FOR rec IN
        SELECT ag_kit_barcode_id FROM ag.ag_kit_barcodes
    LOOP
        UPDATE ag.ag_kit_barcodes
            SET notes = random_string(50, source, 'Free text - '),
                other_text = random_string(50, source2, 'Free text - ')
            WHERE ag_kit_barcode_id = rec.ag_kit_barcode_id;
    END LOOP;

    -- Table: labadmin_users; columns: email, password
    -- For this table it is easier to drop everybody and add a test user
    DELETE FROM ag.labadmin_users_access;
    DELETE FROM ag.labadmin_users;
    INSERT INTO ag.labadmin_users (email, password) VALUES ('test@foo.bar', passwd);
    -- Magic number 7 -> admin access
    INSERT INTO ag.labadmin_users_access (email, access_id) VALUES ('test@foo.bar', 7);

END $do$;

-- Set this database as a test database
UPDATE ag.settings SET test_environment = 'true';


-- Drop the functions that we created
DROP FUNCTION retrieve_chars(varchar, varchar);
DROP FUNCTION random_string(integer, varchar, varchar);
DROP FUNCTION random_email(varchar, varchar);
DROP FUNCTION random_date();
DROP FUNCTION random_lat_or_long();
