SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_update_geo_info (
    ag_login_id_ uuid,
    lat_ double precision,
    lon_ double precision,
    elevation_ double precision,
    cannot_geocode_ char
)
 RETURNS VOID AS $body$
BEGIN

    update  ag_login
    set     latitude = lat_,
            longitude = lon_,
            elevation = elevation_,
            cannot_geocode = cannot_geocode_
    where   ag_login_id = ag_login_id_;

end;
 /*
 lat = 40.0005378
 long = -105.2077798
 elevation = 1619.83715820312
 begin;
select ag_update_geo_info(cast('d8592c747da12135e0408a80115d6401' as uuid), 54.2, 32.64, 200.535633, 'n');
select * from ag_login where ag_login_id = cast('d8592c747da12135e0408a80115d6401' as uuid);
select ag_update_geo_info(cast('d8592c747da12135e0408a80115d6401' as uuid), 40.0005378, -105.2077798, 1619.83715820312, null);
select * from ag_login where ag_login_id = cast('d8592c747da12135e0408a80115d6401' as uuid);
 commit;
 */
 
$body$
LANGUAGE PLPGSQL;




