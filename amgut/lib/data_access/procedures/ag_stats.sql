SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_stats (
    results_ refcursor
)
 RETURNS refcursor AS $body$
BEGIN
    
    open results_ for
        SELECT  ' General stats - Total surveys: ', count(*)
        from    ag_human_survey
        union
        SELECT  ' General stats - Total Kits: ', count(*)
        from    ag_kit
        union
        SELECT  ' General stats: Total barcodes: ', count(*)
        from    ag_kit_barcodes
        union
        SELECT  ' General stats - average age: ', avg((current_date - to_date(birth_date, 'MM/DD/YYYY')) / 365.0) as avg_age
        from    ag_human_survey
        where   (birth_date IS NOT NULL AND birth_date::text <> '')
        union
        SELECT  ' General stats: Avg. height: ', avg(cast(height_in as numeric))
        from    ag_human_survey
        where   (height_in IS NOT NULL AND height_in::text <> '')
                and cast(height_in as numeric) > 30
        union
        SELECT  'Diet type - Vegetarians:', count(diet_type)
        from    ag_human_survey
        where   diet_type = 'Vegetarian'
        union
        SELECT  'Diet type - Vegetarian but eat seafood: ', count(diet_type)
        from    ag_human_survey
        where   diet_type = 'Vegetarian but eat seafood'
        union
        SELECT  'Diet type - Omnivore but no red meat: ', count(diet_type)
        from    ag_human_survey
        where   diet_type = 'Omnivore but no red meat'
        union
        SELECT  'Diet type - Omnivore: ', count(diet_type)
        from    ag_human_survey
        where   diet_type = 'Omnivore'
        union
        SELECT  'Diet type - Vegan: ', count(diet_type)
        from    ag_human_survey
        where   diet_type = 'Vegan'
        union
        SELECT  'Diet type - Did not answer: ', count(diet_type)
        from    ag_human_survey
        where   coalesce(diet_type::text, '') = ''
        union
        SELECT  'Gender - Female: ', count(*)
        from    ag_human_survey
        where   gender = 'Female'
        union
        SELECT  'Gender - Male: ', count(*)
        from    ag_human_survey
        where   gender = 'Male'
        union
        SELECT  'BMI - Underweight: ', count(*)
        from    ag_human_survey
        where   (weight_lbs IS NOT NULL AND weight_lbs::text <> '')
                and cast(weight_lbs as numeric) > 50
                and (height_in IS NOT NULL AND height_in::text <> '')
                and cast(height_in as numeric) > 30
                and (cast(weight_lbs as numeric) / ((cast(height_in as numeric) * cast(height_in as numeric)))) * 703 < 18.5
        union
        SELECT  'BMI - Normal: ', count(*)
        from    ag_human_survey
        where   (weight_lbs IS NOT NULL AND weight_lbs::text <> '')
                and cast(weight_lbs as numeric) > 50
                and (height_in IS NOT NULL AND height_in::text <> '')
                and cast(height_in as numeric) > 30
                and (cast(weight_lbs as numeric) / ((cast(height_in as numeric) * cast(height_in as numeric)))) * 703 between 18.5 and 24.9
        union
        SELECT  'BMI - Overweight: ', count(*)
        from    ag_human_survey
        where   (weight_lbs IS NOT NULL AND weight_lbs::text <> '')
                and cast(weight_lbs as numeric) > 50
                and (height_in IS NOT NULL AND height_in::text <> '')
                and cast(height_in  as numeric) > 30
                and (cast(weight_lbs as numeric) / ((cast(height_in as numeric) * cast(height_in as numeric)))) * 703 between 25 and 29.9
        union
        SELECT  'BMI - Obesity: ', count(*)
        from    ag_human_survey
        where   (weight_lbs IS NOT NULL AND weight_lbs::text <> '')
                and cast(weight_lbs as numeric) > 50
                and (height_in IS NOT NULL AND height_in::text <> '')
                and cast(height_in as numeric) > 30
                and (cast(weight_lbs as numeric) / ((cast(height_in as numeric) * cast(height_in as numeric)))) * 703 > 30
        union
        SELECT  'Antibiotic - Did not answer: ', count(*)
        from    ag_human_survey
        where   coalesce(antibiotic_select::text, '') = ''
        
        union
        SELECT  'Antibiotic - In the past week: ', count(*)
        from    ag_human_survey
        where   antibiotic_select = 'In the past week'
        union
        SELECT  'Antibiotic - In the past year: ', count(*)
        from    ag_human_survey
        where   antibiotic_select = 'In the past year'
        union
        SELECT  'Antibiotic - Not in the last year: ', count(*)
        from    ag_human_survey
        where   antibiotic_select = 'Not in the last year'
        union
        SELECT  'Antibiotic - In the past month: ', count(*)
        from    ag_human_survey
        where   antibiotic_select = 'In the past month'
        union
        SELECT  'Antibiotic - In the past 6 months: ', count(*)
        from    ag_human_survey
        where   antibiotic_select = 'In the past 6 months';
    return results_;
end;
/*
being;
select ag_stats('a');
fetch all in a;
commit;
*/

$body$
LANGUAGE PLPGSQL;




