/* 23 April 2015
Make use of the zipcodes table. Need to relax constraints on the table
to allow NULLs on some columns. Also remove constraints on varchar lengths.
Add elevation column, and update with existing information from ag_login
table. Then, drop latitude, longitude, and elevation columns from ag_login
table to avoid data duplication.

Adam Robbins-Pianka

*/

DROP INDEX ag.ix_zipcode_lat;

DROP INDEX ag.ix_zipcode_long;

ALTER TABLE ag.zipcodes ADD elevation float8  ;

ALTER TABLE ag.zipcodes ALTER COLUMN zipcode TYPE varchar;

ALTER TABLE ag.zipcodes ALTER COLUMN state TYPE varchar;

ALTER TABLE ag.zipcodes ALTER COLUMN state DROP NOT NULL;

ALTER TABLE ag.zipcodes ALTER COLUMN fips_regions TYPE varchar;

ALTER TABLE ag.zipcodes ALTER COLUMN fips_regions DROP NOT NULL;

ALTER TABLE ag.zipcodes ALTER COLUMN city TYPE varchar;

ALTER TABLE ag.zipcodes ALTER COLUMN city DROP NOT NULL;

ALTER TABLE ag.zipcodes ALTER COLUMN latitude DROP NOT NULL;

ALTER TABLE ag.zipcodes ALTER COLUMN longitude DROP NOT NULL;

UPDATE ag.zipcodes
SET elevation = al.elevation
FROM ag.ag_login al
WHERE zipcode = al.zip;

ALTER TABLE ag.ag_login DROP LATITUDE;

ALTER TABLE ag.ag_login DROP LONGITUDE;

ALTER TABLE ag.ag_login DROP ELEVATION;
