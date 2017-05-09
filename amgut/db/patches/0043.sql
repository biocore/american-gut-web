-- see previous patch: this removes the misleading column since data are now stored in source_barcodes_surveys
-- remove incomplete information from other table:
ALTER TABLE ag.ag_kit_barcodes DROP COLUMN survey_id;
