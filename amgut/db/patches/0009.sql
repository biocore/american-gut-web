--Create pet survey in database
----------------------------------------------------------
-- survey_group
----------------------------------------------------------
INSERT INTO survey_group (group_order, american, british) VALUES (-2, 'Pet Information', 'Pet Information');

----------------------------------------------------------
-- surveys
----------------------------------------------------------
INSERT INTO surveys (survey_id, survey_group) VALUES (1, -2);

----------------------------------------------------------
-- survey_question
----------------------------------------------------------
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES (127, 'NAME', 'Name', 'Name');
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES (128, 'ANIMAL_TYPE', 'Animal type', 'Animal type');
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES (129, 'ANIMAL_ORIGIN', 'Origin', 'Origin');
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES (130, 'ANIMAL_AGE', 'Age', 'Age');
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES (131, 'ANIMAL_GENDER','Gender', 'Gender');
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES (132, 'SETTING', 'Setting', 'Setting');
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES (133, 'WEIGHT_CAT', 'Weight category', 'Weight category');
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES (134, 'DIET', 'Diet classification', 'Diet classification');
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES (135, 'FOOD_SOURCE', 'Food source', 'Food source');
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES (136, 'FOOD_TYPE', 'Food type', 'Food type');
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES (137, 'FOOD_SPECIAL', 'Food special attributes', 'Food special attributes');
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES (138, 'LIVING_STATUS', 'Living status', 'Living status');
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES (139, 'OTHER_ANIMALS', 'Add any pets that the current animal lives with', 'Add any pets that the current animal lives with');
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES (140, 'HUMANS', 'Add the age and gender of any humans that the current animal lives with', 'Add the age and gender of any humans that the current animal lives with');
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES (141, 'HOURS_OUTSIDE', 'Hours spent outside', 'Hours spent outside');
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES (142, 'TOILET_WATER_ACCESS', 'Toilet water access', 'Toilet water access');
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES (143, 'COPROPHAGE', 'Coprophage', 'Coprophage');
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES (144, 'ANIMAL_FREE_TEXT', 'Please write anything else about this animal that you think might affect its microorganisms.', 'Please write anything else about this animal that you think might affect its microorganisms.');

----------------------------------------------------------
-- group_questions
----------------------------------------------------------

INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-2, 127, 0);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-2, 128, 1);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-2, 129, 2);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-2, 130, 3);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-2, 131, 4);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-2, 132, 5);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-2, 133, 6);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-2, 134, 7);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-2, 135, 8);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-2, 136, 9);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-2, 137, 10);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-2, 138, 11);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-2, 139, 12);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-2, 140, 13);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-2, 141, 14);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-2, 142, 15);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-2, 143, 16);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-2, 144, 17);


----------------------------------------------------------
-- survey_question_response_type
----------------------------------------------------------
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (127, 'STRING');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (128, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (129, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (130, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (131, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (132, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (133, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (134, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (135, 'MULTIPLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (136, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (137, 'MULTIPLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (138, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (139, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (140, 'STRING');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (141, 'STRING');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (142, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (143, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (144, 'TEXT');

----------------------------------------------------------
-- survey_response
----------------------------------------------------------
-- animal types
INSERT INTO survey_response (american, british) VALUES ('Dog', 'Dog');
INSERT INTO survey_response (american, british) VALUES ('Cat', 'Cat');
INSERT INTO survey_response (american, british) VALUES ('Small Mammal', 'Small Mammal');
INSERT INTO survey_response (american, british) VALUES ('Large Mammal', 'Large Mammal');
INSERT INTO survey_response (american, british) VALUES ('Fish', 'Fish');
INSERT INTO survey_response (american, british) VALUES ('Bird', 'Bird');
INSERT INTO survey_response (american, british) VALUES ('Reptile', 'Reptile');
INSERT INTO survey_response (american, british) VALUES ('Amphibian', 'Amphibian');
-- animal origin
INSERT INTO survey_response (american, british) VALUES ('Breeder', 'Breeder');
INSERT INTO survey_response (american, british) VALUES ('Shelter', 'Shelter');
INSERT INTO survey_response (american, british) VALUES ('Home', 'Home');
INSERT INTO survey_response (american, british) VALUES ('Wild', 'Wild');
-- living settings
INSERT INTO survey_response (american, british) VALUES ('Urban', 'Urban');
INSERT INTO survey_response (american, british) VALUES ('Suburban', 'Suburban');
INSERT INTO survey_response (american, british) VALUES ('Rural', 'Rural');
-- size of animal
INSERT INTO survey_response (american, british) VALUES ('Underweight', 'Underweight');
INSERT INTO survey_response (american, british) VALUES ('Skinny', 'Skinny');
INSERT INTO survey_response (american, british) VALUES ('Normal', 'Normal');
INSERT INTO survey_response (american, british) VALUES ('Chubby', 'Chubby');
INSERT INTO survey_response (american, british) VALUES ('Overweight', 'Overweight');
-- Diet type
INSERT INTO survey_response (american, british) VALUES ('Carnivore', 'Carnivore');
INSERT INTO survey_response (american, british) VALUES ('Herbivore', 'Herbivore');
-- Food Source
INSERT INTO survey_response (american, british) VALUES ('Pet store food', 'Pet store food');
INSERT INTO survey_response (american, british) VALUES ('Human food', 'Human food');
INSERT INTO survey_response (american, british) VALUES ('Wild food', 'Wild food');
-- Food Type
INSERT INTO survey_response (american, british) VALUES ('Dry', 'Dry');
INSERT INTO survey_response (american, british) VALUES ('Wet', 'Wet');
-- Food special attributes
INSERT INTO survey_response (american, british) VALUES ('Organic', 'Organic');
INSERT INTO survey_response (american, british) VALUES ('Grain free', 'Grain free');
--Living Status
INSERT INTO survey_response (american, british) VALUES ('Lives alone with humans', 'Lives alone with humans');
INSERT INTO survey_response (american, british) VALUES ('Lives alone no/limited humans (shelter)', 'Lives alone no/limited humans (shelter)');
INSERT INTO survey_response (american, british) VALUES ('Lives with other animals and humans', 'Lives with other animals and humans');
INSERT INTO survey_response (american, british) VALUES ('Lives with other animals/limited humans', 'Lives with other animals/limited humans');
-- Outside time
INSERT INTO survey_response (american, british) VALUES ('Less than 2', 'Less than 2');
INSERT INTO survey_response (american, british) VALUES ('2-4', '2-4');
INSERT INTO survey_response (american, british) VALUES ('4-8', '4-8');
INSERT INTO survey_response (american, british) VALUES ('8+', '8+');

INSERT INTO survey_response (american, british) VALUES ('Regular', 'Regular');
INSERT INTO survey_response (american, british) VALUES ('Sometimes', 'Sometimes');

INSERT INTO survey_response (american, british) VALUES ('High', 'High');
INSERT INTO survey_response (american, british) VALUES ('Moderate', 'Moderate');
INSERT INTO survey_response (american, british) VALUES ('Low', 'Low');

----------------------------------------------------------
-- survey_question_response
----------------------------------------------------------
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (128, 'Dog', 0);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (128, 'Cat', 1);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (128, 'Small Mammal', 2);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (128, 'Large Mammal', 3);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (128, 'Fish', 4);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (128, 'Bird', 5);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (128, 'Reptile', 6);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (128, 'Amphibian', 7);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (128, 'Other', 8);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (129, 'Breeder', 0);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (129, 'Shelter', 1);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (129, 'Home', 2);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (129, 'Wild', 3);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (131, 'Male', 0);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (131, 'Female', 1);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (132, 'Urban', 0);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (132, 'Suburban', 1);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (132, 'Rural', 2);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (133, 'Underweight', 0);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (133, 'Skinny', 1);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (133, 'Normal', 2);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (133, 'Chubby', 3);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (133, 'Overweight', 4);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (134, 'Carnivore', 0);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (134, 'Omnivore', 1);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (134, 'Herbivore', 2);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (135, 'Pet store food', 0);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (135, 'Human food', 1);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (135, 'Wild food', 2);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (136, 'Dry', 0);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (136, 'Wet', 1);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (136, 'Both', 2);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (137, 'Organic', 0);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (137, 'Grain free', 1);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (138, 'Lives alone with humans', 0);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (138, 'Lives alone no/limited humans (shelter)', 1);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (138, 'Lives with other animals and humans', 2);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (138, 'Lives with other animals/limited humans', 3);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (139, 'Dog', 0);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (139, 'Cat', 1);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (139, 'Small Mammal', 2);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (139, 'Large Mammal', 3);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (139, 'Fish', 4);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (139, 'Bird', 5);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (139, 'Reptile', 6);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (139, 'Amphibian', 7);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (139, 'Other', 8);


INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (141, 'None', 0);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (141, 'Less than 2', 1);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (141, '2-4', 2);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (141, '4-8', 3);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (141, '8+', 4);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (142, 'Regular', 0);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (142, 'Sometimes', 1);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (142, 'Never', 2);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (143, 'High', 0);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (143, 'Moderate', 1);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (143, 'Low', 2);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (143, 'Never', 3);
----------------------------------------------------------
-- survey_question_triggers
----------------------------------------------------------
