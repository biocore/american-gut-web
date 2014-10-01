SET client_encoding TO 'UTF8';


CREATE OR REPLACE FUNCTION ag_get_map_markers (
    results_ in refcursor
)
 RETURNS refcursor AS $body$
BEGIN
    -- PERFORM was replaced with select by Emily this needs tested
    -- Highest priority: completed
    insert  into ag_map_markers
            (zipcode, latitude, longitude, marker_color, order_by)
    select agl.zip, agl.latitude, agl.longitude, '00FF00', 0
    from    ag_login agl
    where   (
                SELECT  count(*)
                from    ag_kit_barcodes akb
                        inner join ag_kit ak
                        on akb.ag_kit_id = ak.ag_kit_id
                where   ak.ag_login_id = agl.ag_login_id
            ) =
            (
                SELECT  count(*)
                from    ag_kit_barcodes akb
                        inner join ag_kit ak
                        on akb.ag_kit_id = ak.ag_kit_id
                where   ak.ag_login_id = agl.ag_login_id
                        and (akb.site_sampled IS NOT NULL AND akb.site_sampled::text <> '')
            );
    
    -- Second priority: verified
    insert  into ag_map_markers
            (zipcode, latitude, longitude, marker_color, order_by)
    select  agl.zip, agl.latitude, agl.longitude, 'FFFF00', 1
    from    ag_login agl
            left join ag_map_markers mm
            on agl.zip = mm.zipcode
    where   (
                SELECT  count(*)
                from    ag_kit ak
                where   ak.ag_login_id = agl.ag_login_id
                        and kit_verified = 'y'
            ) > 0
            and coalesce(mm.zipcode::text, '') = '';
            
    -- Finally, existing participants
    insert  into ag_map_markers
            (zipcode, latitude, longitude, marker_color, order_by)
    select  agl.zip, agl.latitude, agl.longitude, '00B2FF', 2
    from    ag_login agl
            left join ag_map_markers mm
            on agl.zip = mm.zipcode
    where   coalesce(mm.zipcode::text, '') = '';

    open results_ for
        SELECT  zipcode, latitude, longitude, marker_color
        from    ag_map_markers
        order by order_by desc;
    return results_;
end;
 /*
 begin;
 select ag_get_map_markers('a');
 fetch all in a;
 commit;
 */
 
$body$
LANGUAGE PLPGSQL;





