-- August 25, 2015
-- Add EBI expected country names to database

--Update country names from google
ALTER TABLE ag.iso_country_lookup DROP CONSTRAINT fk_iso_country_lookup;
UPDATE ag.iso_country_lookup SET country = 'North Korea' WHERE country = 'Korea, Democratic People''s Republic of';
UPDATE ag.iso_country_lookup SET country = 'Moldova' WHERE country = 'Moldova, Republic of';
UPDATE ag.iso_country_lookup SET country = 'Federated States of Micronesia' WHERE country = 'Micronesia, Federated States of';
UPDATE ag.iso_country_lookup SET country = 'Pitcairn Islands' WHERE country = 'Pitcairn';
UPDATE ag.iso_country_lookup SET country = 'Russia' WHERE country = 'Russian Federation';
UPDATE ag.iso_country_lookup SET country = 'South Korea' WHERE country = 'Korea, Republic of';
UPDATE ag.iso_country_lookup SET country = 'Syria' WHERE country = 'Syrian Arab Republic';
UPDATE ag.iso_country_lookup SET country = 'Taiwan' WHERE country = 'Taiwan, Province of China';
UPDATE ag.iso_country_lookup SET country = 'Tanzania' WHERE country = 'Tanzania, United Republic of';
UPDATE ag.iso_country_lookup SET country = 'U.S. Virgin Islands' WHERE country = 'Virgin Islands, U.S.';
UPDATE ag.iso_country_lookup SET country = 'Brunei' WHERE country = 'Brunei Darussalam';
UPDATE ag.iso_country_lookup SET country = 'Democratic Republic of the Congo' WHERE country = 'Congo, The Democratic Republic of The';
UPDATE ag.iso_country_lookup SET country = 'Falkland Islands (Islas Malvinas)' WHERE country = 'Falkland Islands (Malvinas)';
UPDATE ag.iso_country_lookup SET country = 'French Southern and Antarctic Lands' WHERE country = 'French Southern Territories';
UPDATE ag.iso_country_lookup SET country = 'Iran' WHERE country = 'Iran, Islamic Republic of';
UPDATE ag.iso_country_lookup SET country = 'Laos' WHERE country = 'Lao People''s Democratic Republic';
UPDATE ag.iso_country_lookup SET country = 'Libya' WHERE country = 'Libyan Arab Jamahiriya';
UPDATE ag.iso_country_lookup SET country = 'Macau' WHERE country = 'Macao';
UPDATE ag.iso_country_lookup SET country = 'Macedonia' WHERE country = 'Macedonia, The Former Yugoslav Republic of';
UPDATE ag.iso_country_lookup SET country = 'Tanzania' WHERE country = 'The United Republic of Tanzania';

-- Add EBI country name column and populate it
ALTER TABLE ag.iso_country_lookup ADD COLUMN EBI varchar;
UPDATE ag.iso_country_lookup SET EBI = country;

-- Alter only countries as needed
UPDATE ag.iso_country_lookup SET EBI = 'Cocos Islands' WHERE country = 'Cocos (Keeling) Islands';
UPDATE ag.iso_country_lookup SET EBI = 'Macedonia' WHERE country = 'Macedonia (FYROM)';
UPDATE ag.iso_country_lookup SET EBI = 'Micronesia' WHERE country = 'Federated States of Micronesia';
UPDATE ag.iso_country_lookup SET EBI = 'Republic of the Congo' WHERE country = 'Congo';
UPDATE ag.iso_country_lookup SET EBI = 'Svalbard' WHERE country = 'Svalbard and Jan Mayen';
UPDATE ag.iso_country_lookup SET EBI = 'USA' WHERE country = 'United States';
UPDATE ag.iso_country_lookup SET EBI = 'Virgin Islands' WHERE country = 'U.S. Virgin Islands';