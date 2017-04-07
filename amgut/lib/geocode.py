# from amgut.lib.data_access.ag_data_access import AGDataAccess
import geocoder
import requests

from amgut.lib.data_access.sql_connection import TRN


class GoogleAPILimitExceeded(Exception):
    pass


def geocode_aglogins(ag_login_ids, force=False):
    """ Retriev locations for one or more ag_login_ids and stores results in DB

    Parameters
    ----------
    ag_login_ids : str or [str]
        A single ag_login_id or a list of ag_login_ids for which locations
        should be retrieved.
    force : bool
        If True, locations are retrieved from the geoservice even if we already
        have them in our DB. Useful, if locations needs to be updated.
        Default = False.

    Returns
    -------
    Stats about location lookups: dict {sucessful, cannot_geocode, checked,
    provided}, where
    - provided: is the number of passed ag_login_ids
    - checked: the number of ag_login_ids for which location retrieval was
               executed (sucessful or not). This number might be <= "provided",
               since we do not look-up ag_login_ids which already have
               latitude, longitude, elevation and cannot_geocode=False
               in our DB.
    - sucessful: number of successfully retrieved locations,
                 which is <= "checked"
    - cannot_geocode: number of successfully retrieved locations, which is <=
                      "checked".
    """
    # if only one ag_login_id is passed as a string, we convert it to a one
    # element list to be compatible with the following code.
    if type(ag_login_ids) == str:
        ag_login_ids = [ag_login_ids]

    # check with ag_logins are present in our DB for the given list of
    # ag_login_ids
    sql = """SELECT ag_login_id, address, zip, city, state, country
             FROM ag.ag_login
             WHERE ag_login_id in %s"""
    # skip ag_logins if we already have lat,long,elev in our DB unless we
    # enforce an update
    if force is False:
        sql += """AND (latitude IS NULL
                  OR longitude IS NULL
                  OR elevation IS NULL)"""

    sql_update = """UPDATE ag.ag_login
                    SET latitude = %s,
                        longitude = %s,
                        elevation = %s,
                        cannot_geocode = %s
                    WHERE ag_login_id = %s"""

    stats = {'successful': 0,
             'cannot_geocode': 0,
             'checked': 0,
             'provided': len(ag_login_ids)}

    with TRN:
        TRN.add(sql, [tuple(ag_login_ids)])

        for address in TRN.execute_fetchindex():
            lat, lng, elev, cannot_geocode = None, None, None, None
            # lookup lat,lng by address
            address_str = " ".join([x for x in address[1:]
                                    if x is not None])
            g = geocoder.google(address_str)
            # only continue if we got a valid result
            if g.error is None:
                lat, lng = g.latlng
                # lookup elevation in a second call
                e = geocoder.elevation(g.latlng)
                # only continue if we got a valid result
                if e.error is None:
                    elev = e.elevation
                elif g.error == "OVER_QUERY_LIMIT":
                    raise GoogleAPILimitExceeded()
                else:
                    cannot_geocode = 'Y'
            elif g.error == "OVER_QUERY_LIMIT":
                raise GoogleAPILimitExceeded()
            else:
                cannot_geocode = 'Y'

            if cannot_geocode == 'Y':
                stats['cannot_geocode'] += 1
            else:
                stats['successful'] += 1
            stats['checked'] += 1

            # update the database with results we just obtained
            TRN.add(sql_update,
                    [lat, lng, elev, cannot_geocode, address[0]])
        TRN.execute()

    return stats
