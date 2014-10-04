CREATE OR REPLACE FUNCTION uuid_generate_v4()
 RETURNS uuid
 LANGUAGE c
 STRICT
AS '$libdir/uuid-ossp', $function$uuid_generate_v4$function$
