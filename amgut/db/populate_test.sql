-- Populates the test database
SET search_path TO ag, public;

INSERT INTO ag_login (ag_login_id) VALUES ('d8592c74-7da1-2135-e040-8a80115d6401');

-- the password for test acconut is '%^&*test'
INSERT INTO ag_kit (
  ag_kit_id, ag_login_id, supplied_kit_id, swabs_per_kit, kit_password,
  kit_verified
) VALUES (
  'a47e4a7f-7e23-4984-8c7c-90f3f5196742',
  'd8592c74-7da1-2135-e040-8a80115d6401', 'test', 1,
  '$2a$12$pKAKSEwg3U6gFXtjRYbeyOgmmCPlPqoY1LTeQdsokR50sQUfS9Nhe', 'y'
);

INSERT INTO barcode (barcode) VALUES ('000000001');

INSERT INTO ag_kit_barcodes (ag_kit_id, barcode) VALUES (
  'a47e4a7f-7e23-4984-8c7c-90f3f5196742', '000000001'
);
