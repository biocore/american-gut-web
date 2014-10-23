-- Populates the test database
SET search_path TO ag, public;
insert into ag_login (ag_login_id) values ('d8592c74-7da1-2135-e040-8a80115d6401');
insert into ag_kit (ag_kit_id, ag_login_id, supplied_kit_id, swabs_per_kit, kit_password, kit_verified) values ('a47e4a7f-7e23-4984-8c7c-90f3f5196742', 'd8592c74-7da1-2135-e040-8a80115d6401', 'test', 1, '%^&*test', 'y');
insert into barcode (barcode) values ('000000001');
insert into ag_kit_barcodes (ag_kit_id, barcode) values ('a47e4a7f-7e23-4984-8c7c-90f3f5196742', '000000001');