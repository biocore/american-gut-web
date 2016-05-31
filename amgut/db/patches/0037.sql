-- May 31, 2016
-- Add surfer and fermeted foods questionnaires

----------------------------------------------------------
-- survey_group
----------------------------------------------------------
INSERT INTO survey_group (group_order, american, british) VALUES (-3, 'Fermented Foods', 'Fermented Foods');
INSERT INTO survey_group (group_order, american, british) VALUES (-4, 'Surfers', 'Surfers');

----------------------------------------------------------
-- surveys
----------------------------------------------------------
INSERT INTO surveys (survey_id, survey_group) VALUES (3, -3);
INSERT INTO surveys (survey_id, survey_group) VALUES (4, -4);

----------------------------------------------------------
-- survey_question
----------------------------------------------------------
-- Fermented
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES
(164, 'FERMENTED_FREQUENCY', 'How often do you consume one or more servings of fermented vegetables or plant products a day in an average week? (1 serving = ½ cup sauerkraut, kimchi or fermented vegetable or 1 cup of kombucha)', 'How often do you consume one or more servings of fermented vegetables or plant products a day in an average week? (1 serving = ½ cup sauerkraut, kimchi or fermented vegetable or 1 cup of kombucha)'),
(165, 'FERMENTED_INCREASED', 'Excluding beer, wine, and alcohol, I have significantly increased (i.e. more than doubled) my intake of fermented foods in frequency or quantity within the last ____.', 'Excluding beer, wine, and alcohol, I have significantly increased (i.e. more than doubled) my intake of fermented foods in frequency or quantity within the last ____.'),
(166, 'FERMENTED_CONSUMED', 'Which of the following fermented foods/beverages do you consume more than once a week? Check all that apply.', 'Which of the following fermented foods/beverages do you consume more than once a week? Check all that apply.'),
(167, 'FERMENTED_CONSUMED_OTHER', 'Write in any consumed foods that are not listed under "Other"', 'Write in any consumed foods that are not listed under "Other"'),
(168, 'FERMENTED_PRODUCE_PERSONAL', 'Do you produce any of the following fermented foods/beverages at home for personal consumption? Check all that apply.', 'Do you produce any of the following fermented foods/beverages at home for personal consumption? Check all that apply.'),
(169, 'FERMENTED_PRODUCE_PERSONAL_OTHER', 'Write in any presonally produced foods that are not listed under "Other"', 'Write in any presonally produced foods that are not listed under "Other"'),
(170, 'FERMENTED_PRODUCE_COMMERCIAL', 'Do you produce any of the following fermented foods/beverages for commercial purposes? Check all that apply.', 'Do you produce any of the following fermented foods/beverages for commercial purposes? Check all that apply.'),
(171, 'FERMENTED_PRODUCE_COMMERCIAL_OTHER', 'Write in any commercially produced foods that are not listed under "Other"', 'Write in any commercially produced foods that are not listed under "Other"'),
(172, 'FERMENTED_OTHER', 'Volunteer more information about this activity.', 'Volunteer more information about this activity.');
-- Surfers
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES
(173, 'SURF_LOCAL_BREAK', 'Where is your local surf break?', 'Where is your local surf break?'),
(174, 'SURF_LOAL_BREAK_FREQUENCY', 'How often do you surf your local wave?', 'How often do you surf your local wave?'),
(175, 'SURF_FREQUENCY', 'How often do you surf?', 'How often do you surf?'),
(176, 'SURF_TRAVEL_FREQUENCY', 'How often do you travel to other surf breaks?', 'How often do you travel to other surf breaks?'),
(177, 'SURF_TRAVEL_DISTANCE', 'How far do you travel away from this beach between sessions (home/work/travel)?', 'How far do you travel away from this beach between sessions (home/work/travel)?'),
(178, 'SURF_WEETSUIT', 'What type of wetsuit do you use?', 'What type of wetsuit do you use?'),
(179, 'SURF_SUNSCREEN', 'What type of sunscreen do you use?', 'What type of sunscreen do you use?'),
(180, 'SURF_SUNSCREEN_FREQUENCY', 'How often do you use sunscreen?', 'How often do you use sunscreen?'),
(181, 'SURF_SHOWER_FREQUENCY', 'How often do you shower after surfing?', 'How often do you shower after surfing?'),
(182, 'SURF_STANCE', 'What stance are you?', 'What stance are you?'),
(183, 'SURF_BOARD_TYPE', 'What type of surfboard do you prefer?', 'What type of surfboard do you prefer?'),
(184, 'SURF_WAX', 'What type of wax do you use?', 'What type of wax do you use?');

----------------------------------------------------------
-- group_questions
----------------------------------------------------------
--Fermented
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-3, 164, 0);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-3, 165, 1);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-3, 166, 2);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-3, 167, 3);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-3, 168, 4);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-3, 169, 5);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-3, 170, 6);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-3, 171, 7);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-3, 172, 8);
--Surfers
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-4, 173, 0);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-4, 174, 1);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-4, 175, 2);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-4, 176, 3);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-4, 177, 4);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-4, 178, 5);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-4, 179, 6);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-4, 180, 7);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-4, 181, 8);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-4, 182, 9);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-4, 183, 10);
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES (-4, 184, 11);

----------------------------------------------------------
-- survey_question_response_type
----------------------------------------------------------
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (164, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (165, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (166, 'MULTIPLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (167, 'TEXT');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (168, 'MULTIPLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (169, 'TEXT');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (170, 'MULTIPLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (171, 'TEXT');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (172, 'TEXT');

INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (173, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (174, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (175, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (176, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (177, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (178, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (179, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (180, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (181, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (182, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (183, 'SINGLE');
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES (184, 'SINGLE');

----------------------------------------------------------
-- survey_response
----------------------------------------------------------
INSERT INTO survey_response (american, british) VALUES
('I have not increased my intake', 'I have not increased my intake'),
('Kimchi', 'Kimchi'),
('Sauerkraut', 'Sauerkraut'),
('Fermented beans/Miso/Natto', 'Fermented beans/Miso/Natto'),
('Pickled vegetables', 'Pickled vegetables'),
('Tempeh', 'Tempeh'),
('Fermented tofu', 'Fermented tofu'),
('Kefir (water)', 'Kefir (water)'),
('Kefir (milk)', 'Kefir (milk)'),
('Cottage cheese', 'Cottage cheese'),
('Yogurt/lassi', 'Yogurt/lassi'),
('Sour cream/crème fraiche', 'Sour cream/crème fraiche'),
('Fermented fish', 'Fermented fish'),
('Fish sauce', 'Fish sauce'),
('Fermented bread/sourdough/injera', 'Fermented bread/sourdough/injera'),
('Kombucha', 'Kombucha'),
('Chicha', 'Chicha'),
('Beer', 'Beer'),
('Cider', 'Cider'),
('Wine', 'Wine'),
('Mead', 'Mead');

INSERT INTO survey_response (american, british) VALUES
('Point Loma/Ocean Beach, San Diego, California, USA', 'Point Loma/Ocean Beach, San Diego, California, USA'),
('La Jolla, San Diego, California, USA', 'La Jolla, San Diego, California, USA'),
('Encinitas, California, USA', 'Encinitas, California, USA'),
('Southern California, USA', 'Southern California, USA'),
('Central California, USA', 'Central California, USA'),
('Northern, California', 'Northern, California'),
('Pacific Northwest, USA', 'Pacific Northwest, USA'),
('Hawaii, USA', 'Hawaii, USA'),
('Northeast, USA', 'Northeast, USA'),
('Southeast, USA', 'Southeast, USA'),
('South America', 'South America'),
('Europe', 'Europe'),
('Africa', 'Africa'),
('Southeast Asia', 'Southeast Asia'),
('Asia', 'Asia');

INSERT INTO survey_response (american, british) VALUES
('Multiple times a day', 'Multiple times a day'),
('Multiple times a week', 'Multiple times a week'),
('Once a week', 'Once a week'),
('Multiple times a month', 'Multiple times a month');

INSERT INTO survey_response (american, british) VALUES
('<1 km', '<1 km'),
('5-10km', '5-10km'),
('>10km', '>10km');

INSERT INTO survey_response (american, british) VALUES
('<1mm', '<1mm'),
('2-3mm', '2-3mm'),
('3-4mm', '3-4mm'),
('4-5mm', '4-5mm');

INSERT INTO survey_response (american, british) VALUES
('<SPF25', '<SPF25'),
('SPF 25-50', 'SPF 25-50'),
('SPF 50+', 'SPF 50+');

INSERT INTO survey_response (american, british) VALUES
('Every time I surf', 'Every time I surf'),
('Frequently', 'Frequently'),
('Rarely', 'Rarely');

INSERT INTO survey_response (american, british) VALUES
('Natural', 'Natural'),
('Goofy Foot', 'Goofy Foot'),
('Prone', 'Prone');

INSERT INTO survey_response (american, british) VALUES
('Longboard', 'Longboard'),
('Shortboard', 'Shortboard'),
('Bodyboard', 'Bodyboard'),
('No Board', 'No Board'),
('No preference', 'No preference');

INSERT INTO survey_response (american, british) VALUES
('Sex Wax', 'Sex Wax'),
('Sticky Bumps', 'Sticky Bumps'),
('Mrs. Palmers', 'Mrs. Palmers'),
('Bubble Gum', 'Bubble Gum'),
('Famous', 'Famous');

----------------------------------------------------------
-- survey_response
----------------------------------------------------------
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(164, 'Unspecified', 0),
(164, 'Never', 1),
(164, 'Rarely (a few times/month)', 2),
(164, 'Occasionally (1-2 times/week)', 3),
(164, 'Regularly (3-5 times/week)', 4),
(164, 'Daily', 5);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(165, 'Unspecified', 0),
(165, 'Week', 1),
(165, 'Month', 2),
(165, '6 months', 3),
(165, 'Year', 4),
(165, 'I have not increased my intake', 5);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(166, 'Kimchi', 0),
(166, 'Sauerkraut', 1),
(166, 'Fermented beans/Miso/Natto', 2),
(166, 'Pickled vegetables', 3),
(166, 'Tempeh', 4),
(166, 'Fermented tofu', 5),
(166, 'Kefir (water)', 6),
(166, 'Kefir (milk)', 7),
(166, 'Cottage cheese', 8),
(166, 'Yogurt/lassi', 9),
(166, 'Sour cream/crème fraiche', 10),
(166, 'Fermented fish', 11),
(166, 'Fish sauce', 12),
(166, 'Fermented bread/sourdough/injera', 13),
(166, 'Kombucha', 14),
(166, 'Chicha', 15),
(166, 'Beer', 16),
(166, 'Cider', 17),
(166, 'Wine', 18),
(166, 'Mead', 19),
(166, 'Other', 20);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(168, 'Kimchi', 0),
(168, 'Sauerkraut', 1),
(168, 'Fermented beans/Miso/Natto', 2),
(168, 'Pickled vegetables', 3),
(168, 'Tempeh', 4),
(168, 'Fermented tofu', 5),
(168, 'Kefir (water)', 6),
(168, 'Kefir (milk)', 7),
(168, 'Cottage cheese', 8),
(168, 'Yogurt/lassi', 9),
(168, 'Sour cream/crème fraiche', 10),
(168, 'Fermented fish', 11),
(168, 'Fish sauce', 12),
(168, 'Fermented bread/sourdough/injera', 13),
(168, 'Kombucha', 14),
(168, 'Chicha', 15),
(168, 'Beer', 16),
(168, 'Cider', 17),
(168, 'Wine', 18),
(168, 'Mead', 19),
(168, 'Other', 20);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(170, 'Kimchi', 0),
(170, 'Sauerkraut', 1),
(170, 'Fermented beans/Miso/Natto', 2),
(170, 'Pickled vegetables', 3),
(170, 'Tempeh', 4),
(170, 'Fermented tofu', 5),
(170, 'Kefir (water)', 6),
(170, 'Kefir (milk)', 7),
(170, 'Cottage cheese', 8),
(170, 'Yogurt/lassi', 9),
(170, 'Sour cream/crème fraiche', 10),
(170, 'Fermented fish', 11),
(170, 'Fish sauce', 12),
(170, 'Fermented bread/sourdough/injera', 13),
(170, 'Kombucha', 14),
(170, 'Chicha', 15),
(170, 'Beer', 16),
(170, 'Cider', 17),
(170, 'Wine', 18),
(170, 'Mead', 19),
(170, 'Other', 20);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(173, 'Point Loma/Ocean Beach, San Diego, California, USA', 0),
(173, 'La Jolla, San Diego, California, USA', 1),
(173, 'Encinitas, California, USA', 2),
(173, 'Southern California, USA', 3),
(173, 'Central California, USA', 4),
(173, 'Northern, California', 5),
(173, 'Pacific Northwest, USA', 6),
(173, 'Hawaii, USA', 7),
(173, 'Northeast, USA', 8),
(173, 'Southeast, USA', 9),
(173, 'South America', 10),
(173, 'Europe', 11),
(173, 'Africa', 12),
(173, 'Australia', 13),
(173, 'New Zealand', 14),
(173, 'Southeast Asia', 15),
(173, 'Asia', 16),
(173, 'Other', 17);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(174, 'Multiple times a day', 0),
(174, 'Once a day', 1),
(174, 'Multiple times a week', 2),
(174, 'Once a week', 3),
(174, 'Multiple times a month', 4);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(175, 'Multiple times a day', 0),
(175, 'Once a day', 1),
(175, 'Multiple times a week', 2),
(175, 'Once a week', 3),
(175, 'Multiple times a month', 4);


INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(176, 'Multiple times a day', 0),
(176, 'Once a day', 1),
(176, 'Multiple times a week', 2),
(176, 'Once a week', 3),
(176, 'Multiple times a month', 4);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(177, '<1 km', 0),
(177, '5-10km', 1),
(177, '>10km', 2);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(178, 'None', 0),
(178, '<1mm', 1),
(178, '2-3mm', 2),
(178, '3-4mm', 3),
(178, '4-5mm', 4);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(179, '<SPF25', 0),
(179, 'SPF 25-50', 1),
(179, 'SPF 50+', 2),
(179, 'Other', 3);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(180, 'Every time I surf', 0),
(180, 'Frequently', 1),
(180, 'Rarely', 2),
(180, 'Never', 3);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(181, 'Every time I surf', 0),
(181, 'Frequently', 1),
(181, 'Rarely', 2),
(181, 'Never', 3);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(182, 'Natural', 0),
(182, 'Goofy Foot', 1),
(182, 'Prone', 2);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(183, 'Longboard', 0),
(183, 'Shortboard', 1),
(183, 'Bodyboard', 2),
(183, 'No Board', 3),
(183, 'No preference', 4);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(184, 'Sex Wax', 0),
(184, 'Sticky Bumps', 1),
(184, 'Mrs. Palmers', 2),
(184, 'Bubble Gum', 3),
(184, 'Famous', 4),
(184, 'Other', 5);

----------------------------------------------------------
-- survey_question_triggers
----------------------------------------------------------
INSERT INTO survey_question_triggers (survey_question_id, triggered_question, triggering_response) VALUES (166, 167, 'Other');
INSERT INTO survey_question_triggers (survey_question_id, triggered_question, triggering_response) VALUES (168, 169, 'Other');
INSERT INTO survey_question_triggers (survey_question_id, triggered_question, triggering_response) VALUES (170, 171, 'Other');


