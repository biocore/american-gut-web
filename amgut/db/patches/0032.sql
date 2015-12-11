-- Dec 10, 2015
-- Add new questions to the human survey

----------------------------------------------------------
-- survey_question
----------------------------------------------------------
INSERT INTO survey_question (survey_question_id, question_shortname, american, british) VALUES
(148, 'country_residence', 'Country of residence:', 'Country of residence:'),
(149, 'pets_other', 'Do you have any other pet(s)?', 'Do you have any other pet(s)?'),
(150, 'pets_other_freetext', 'Please list pets', 'Please list pets'),
(152, 'stool_quality', 'Describe the quality of your bowel movements. Use the chart below as a reference:<br/><img src="/static/img/bristol_stool.jpg">', 'Describe the quality of your bowel movements. Use the chart below as a reference:<br/><img src="/static/img/bristol_stool.jpg">'),
(153, 'mental_illness', 'Have you ever been diagnosed mental health illness?', 'Have you ever been diagnosed mental health illness?'),
(154, 'mental_illness_type', 'Please select which disorder(s) from the following list:', 'Please select which disorder(s) from the following list:'),
(155, 'diabetes_type', 'which type of diabetes?', 'which type of diabetes?'),
(156, 'vivid_dreams', 'Do you have vivid and/or frightening dreams?', 'Do you have vivid and/or frightening dreams?'),
(157, 'artificial_sweeteners', 'Consume diet beverages with artificial sweeteners?', 'Consume diet beverages with artificial sweeteners?');

--Retire question 97 (Old mental health question specific to depression, etc)
UPDATE survey_question SET retired = true WHERE survey_question_id = 97;

----------------------------------------------------------
-- group_questions
----------------------------------------------------------
-- make column float instaead of int so can put new questions in without changing all indices
ALTER TABLE group_questions ALTER COLUMN display_index TYPE FLOAT(1);
-- Put plants question in proper place and unhide
UPDATE group_questions SET survey_group = 4, display_index = 16.5 WHERE survey_question_id = 146;
UPDATE survey_question SET retired = false WHERE survey_question_id = 146;

--Add rest of new questions to groups
INSERT INTO group_questions (survey_group, survey_question_id, display_index) VALUES
(-1, 148, 9), (1, 149, 5.2), (1, 150, 5.4), (3, 152, 11.5), (3, 153, 18.2), (3, 154, 18.4),
(3, 155, 16.5), (0, 156, 4.5), (4, 157, 6.5);

----------------------------------------------------------
-- survey_question_response_type
----------------------------------------------------------
INSERT INTO survey_question_response_type (survey_question_id, survey_response_type) VALUES
(148, 'SINGLE'), (149, 'SINGLE'), (150, 'TEXT'), (152, 'SINGLE'), (153, 'SINGLE'),
(154, 'MULTIPLE'), (155, 'SINGLE'), (156, 'SINGLE'), (157, 'SINGLE');

----------------------------------------------------------
-- survey_response
----------------------------------------------------------
INSERT INTO survey_response (american, british) VALUES
('2+ times/day', '2+ times/day'),
('1-2 times/day', '1-2 times/day'),
('Once a day', 'Once a day'),
('I tend to be constipated (have difficulty passing stool) - Type 1 and 2', 'I tend to be constipated (have difficulty passing stool) - Type 1 and 2'),
('I tend to have diarrhea (watery stool) - Type 5, 6 and 7', 'I tend to have diarrhea (watery stool) - Type 5, 6 and 7'),
('I tend to have normal formed stool - Type 3 and 4', 'I tend to have normal formed stool - Type 3 and 4'),
('Depression', 'Depression'),
('Bipolar disorder', 'Bipolar disorder'),
('PTSD (post-traumatic stress disorder)', 'PTSD (post-traumatic stress disorder)'),
('Schizophrenia', 'Schizophrenia'),
('Anorexia nervosa', 'Anorexia nervosa'),
('Bulimia nervosa', 'Bulimia nervosa'),
('Substance abuse', 'Substance abuse'),
('Prediabetes', 'Prediabetes'),
('Type I diabetes', 'Type I diabetes'),
('Type II diabetes', 'Type II diabetes'),
('Gestational diabetes', 'Gestational diabetes');

----------------------------------------------------------
-- survey_question_response
----------------------------------------------------------
-- country of residence
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Unspecified', 0);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Afghanistan', 1);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Aland Islands', 2);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Albania', 3);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Algeria', 4);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'American Samoa', 5);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Andorra', 6);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Angola', 7);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Anguilla', 8);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Antarctica', 9);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Antigua and Barbuda', 10);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Argentina', 11);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Armenia', 12);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Aruba', 13);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Australia', 14);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Austria', 15);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Azerbaijan', 16);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Bahamas', 17);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Bahrain', 18);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Bangladesh', 19);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Barbados', 20);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Belarus', 21);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Belgium', 22);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Belize', 23);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Benin', 24);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Bermuda', 25);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Bhutan', 26);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Bolivia', 27);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Bosnia and Herzegovina', 28);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Botswana', 29);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Bouvet Island', 30);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Brazil', 31);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'British Indian Ocean Territory', 32);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Brunei Darussalam', 33);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Bulgaria', 34);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Burkina Faso', 35);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Burundi', 36);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Cambodia', 37);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Cameroon', 38);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Canada', 39);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Cape Verde', 40);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Cayman Islands', 41);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Central African Republic', 42);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Chad', 43);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Chile', 44);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'China', 45);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Christmas Island', 46);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Cocos (Keeling) Islands', 47);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Colombia', 48);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Comoros', 49);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Congo', 50);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Congo, The Democratic Republic of The', 51);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Cook Islands', 52);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Costa Rica', 53);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Cote D''ivoire', 54);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Croatia', 55);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Cuba', 56);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Cyprus', 57);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Czech Republic', 58);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Denmark', 59);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Djibouti', 60);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Dominica', 61);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Dominican Republic', 62);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Ecuador', 63);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Egypt', 64);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'El Salvador', 65);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Equatorial Guinea', 66);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Eritrea', 67);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Estonia', 68);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Ethiopia', 69);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Falkland Islands (Malvinas)', 70);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Faroe Islands', 71);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Fiji', 72);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Finland', 73);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'France', 74);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'French Guiana', 75);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'French Polynesia', 76);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'French Southern Territories', 77);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Gabon', 78);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Gambia', 79);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Georgia', 80);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Germany', 81);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Ghana', 82);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Gibraltar', 83);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Greece', 84);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Greenland', 85);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Grenada', 86);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Guadeloupe', 87);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Guam', 88);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Guatemala', 89);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Guernsey', 90);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Guinea', 91);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Guinea-bissau', 92);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Guyana', 93);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Haiti', 94);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Heard Island and Mcdonald Islands', 95);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Holy See (Vatican City State)', 96);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Honduras', 97);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Hong Kong', 98);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Hungary', 99);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Iceland', 100);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'India', 101);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Indonesia', 102);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Iran, Islamic Republic of', 103);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Iraq', 104);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Ireland', 105);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Isle of Man', 106);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Israel', 107);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Italy', 108);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Jamaica', 109);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Japan', 110);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Jersey', 111);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Jordan', 112);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Kazakhstan', 113);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Kenya', 114);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Kiribati', 115);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Korea, Democratic People''s Republic of', 116);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Korea, Republic of', 117);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Kuwait', 118);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Kyrgyzstan', 119);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Lao People''s Democratic Republic', 120);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Latvia', 121);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Lebanon', 122);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Lesotho', 123);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Liberia', 124);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Libyan Arab Jamahiriya', 125);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Liechtenstein', 126);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Lithuania', 127);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Luxembourg', 128);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Macao', 129);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Macedonia, The Former Yugoslav Republic of', 130);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Madagascar', 131);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Malawi', 132);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Malaysia', 133);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Maldives', 134);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Mali', 135);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Malta', 136);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Marshall Islands', 137);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Martinique', 138);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Mauritania', 139);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Mauritius', 140);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Mayotte', 141);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Mexico', 142);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Micronesia, Federated States of', 143);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Moldova, Republic of', 144);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Monaco', 145);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Mongolia', 146);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Montenegro', 147);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Montserrat', 148);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Morocco', 149);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Mozambique', 150);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Myanmar', 151);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Namibia', 152);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Nauru', 153);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Nepal', 154);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Netherlands', 155);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Netherlands Antilles', 156);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'New Caledonia', 157);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'New Zealand', 158);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Nicaragua', 159);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Niger', 160);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Nigeria', 161);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Niue', 162);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Norfolk Island', 163);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Northern Mariana Islands', 164);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Norway', 165);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Oman', 166);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Pakistan', 167);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Palau', 168);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Palestinian Territory, Occupied', 169);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Panama', 170);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Papua New Guinea', 171);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Paraguay', 172);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Peru', 173);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Philippines', 174);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Pitcairn', 175);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Poland', 176);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Portugal', 177);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Puerto Rico', 178);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Qatar', 179);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Reunion', 180);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Romania', 181);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Russian Federation', 182);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Rwanda', 183);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Saint Helena', 184);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Saint Kitts and Nevis', 185);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Saint Lucia', 186);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Saint Pierre and Miquelon', 187);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Saint Vincent and The Grenadines', 188);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Samoa', 189);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'San Marino', 190);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Sao Tome and Principe', 191);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Saudi Arabia', 192);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Senegal', 193);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Serbia', 194);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Seychelles', 195);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Sierra Leone', 196);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Singapore', 197);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Slovakia', 198);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Slovenia', 199);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Solomon Islands', 200);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Somalia', 201);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'South Africa', 202);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'South Georgia and The South Sandwich Islands', 203);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Spain', 204);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Sri Lanka', 205);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Sudan', 206);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Suriname', 207);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Svalbard and Jan Mayen', 208);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Swaziland', 209);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Sweden', 210);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Switzerland', 211);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Syrian Arab Republic', 212);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Taiwan, Province of China', 213);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Tajikistan', 214);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Tanzania, United Republic of', 215);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Thailand', 216);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Timor-leste', 217);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Togo', 218);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Tokelau', 219);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Tonga', 220);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Trinidad and Tobago', 221);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Tunisia', 222);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Turkey', 223);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Turkmenistan', 224);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Turks and Caicos Islands', 225);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Tuvalu', 226);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Uganda', 227);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Ukraine', 228);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'United Arab Emirates', 229);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'United Kingdom', 230);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'United States', 231);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'United States Minor Outlying Islands', 232);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Uruguay', 233);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Uzbekistan', 234);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Vanuatu', 235);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Venezuela', 236);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Viet Nam', 237);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Virgin Islands, British', 238);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Virgin Islands, U.S.', 239);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Wallis and Futuna', 240);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Western Sahara', 241);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Yemen', 242);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Zambia', 243);
INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES (148, 'Zimbabwe', 244);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(149, 'Unspecified', 0), (149, 'Yes', 1), (149, 'No', 2);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(152, 'Unspecified', 0),
(152, 'I tend to be constipated (have difficulty passing stool) - Type 1 and 2', 1),
(152, 'I tend to have diarrhea (watery stool) - Type 5, 6 and 7', 2),
(152, 'I tend to have normal formed stool - Type 3 and 4', 3);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(153, 'Unspecified', 0), (153, 'Yes', 1), (153, 'No', 2);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(154, 'Unspecified', 0),
(154, 'Depression', 1),
(154, 'Bipolar disorder', 2),
(154, 'PTSD (post-traumatic stress disorder)', 3),
(154, 'Schizophrenia', 4),
(154, 'Anorexia nervosa', 5),
(154, 'Bulimia nervosa', 6),
(154, 'Substance abuse', 7);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(155, 'Unspecified', 0),
(155, 'Type I diabetes', 1),
(155, 'Type II diabetes', 2),
(155, 'Gestational diabetes', 3);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(156, 'Unspecified', 0),
(156, 'Never', 1),
(156, 'Rarely (a few times/month)', 2),
(156, 'Occasionally (1-2 times/week)', 3),
(156, 'Regularly (3-5 times/week)', 4),
(156, 'Daily', 5);

INSERT INTO survey_question_response (survey_question_id, response, display_index) VALUES
(157, 'Unspecified', 0),
(157, 'Never', 1),
(157, 'Rarely (a few times/month)', 2),
(157, 'Occasionally (1-2 times/week)', 3),
(157, 'Regularly (3-5 times/week)', 4),
(157, 'Daily', 5);

---------------------------------------------------------
-- survey_question_triggers
----------------------------------------------------------
-- Other pets
INSERT INTO survey_question_triggers (survey_question_id, triggered_question, triggering_response) VALUES (149, 150, 'Yes');
-- Mental Illness
INSERT INTO survey_question_triggers (survey_question_id, triggered_question, triggering_response) VALUES (153, 154, 'Yes');
-- Diabetes type
INSERT INTO survey_question_triggers (survey_question_id, triggered_question, triggering_response) VALUES
(82, 155, 'Diagnosed by a medical professional (doctor, physician assistant)'),
(82, 155, 'Diagnosed by an alternative medicine practitioner'),
(82, 155, 'Self-diagnosed');
