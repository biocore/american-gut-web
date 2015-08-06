from __future__ import division

# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

"""
Centralized database access for the American Gut web portal
"""

import urllib
import httplib
import json
import logging

from time import sleep
from random import choice

import psycopg2

from passlib.hash import bcrypt

from amgut.lib.data_access.sql_connection import SQLConnectionHandler
from amgut.lib.config_manager import AMGUT_CONFIG


# character sets for kit id, passwords and verification codes
KIT_ALPHA = "abcdefghjkmnpqrstuvwxyz"  # removed i, l and o for clarity
KIT_PASSWD = '1234567890'
KIT_VERCODE = KIT_PASSWD
KIT_PASSWD_NOZEROS = KIT_PASSWD[0:-1]
KIT_VERCODE_NOZEROS = KIT_PASSWD_NOZEROS


class GoogleAPILimitExceeded(Exception):
    pass


class AGDataAccess(object):
    """Data Access implementation for all the American Gut web portal
    """
    # arbitrary, unique ID and value
    human_sites = ['Stool',
                   'Mouth',
                   'Right hand',
                   'Left hand',
                   'Forehead',
                   'Nares',
                   'Hair',
                   'Tears',
                   'Nasal mucus',
                   'Ear wax',
                   'Vaginal mucus']

    animal_sites = ['Stool',
                    'Mouth',
                    'Nares',
                    'Ears',
                    'Skin',
                    'Fur']

    general_sites = ['Animal Habitat',
                     'Biofilm',
                     'Dust',
                     'Food',
                     'Fermented Food',
                     'Indoor Surface',
                     'Outdoor Surface',
                     'Plant habitat',
                     'Soil',
                     'Sole of shoe',
                     'Water']

    def __init__(self, con=None):
        self.connection = None
        if con is None:
            self._open_connection()
        else:
            self.connection = con
        cur = self.get_cursor()
        cur.execute('set search_path TO ag, barcodes, public')

        self._sql = SQLConnectionHandler(con)

    def __del__(self):
        self.connection.close()

    def get_cursor(self):
        if self.connection.closed:
            self._open_connection()

        return self.connection.cursor()

    def _open_connection(self):
        self.connection = psycopg2.connect(
            user=AMGUT_CONFIG.user, password=AMGUT_CONFIG.password,
            database=AMGUT_CONFIG.database, host=AMGUT_CONFIG.host,
            port=AMGUT_CONFIG.port)

    #####################################
    # Helper Functions
    #####################################

    def _get_col_names_from_cursor(self, cur):
        if cur.description:
            return [x[0] for x in cur.description]
        else:
            return []

    #####################################
    # Users
    #####################################

    def authenticateWebAppUser(self, username, password):
        """ Attempts to validate authenticate the supplied username/password

        Attempt to authenticate the user against the list of users in
        web_app_user table. If successful, a dict with user innformation is
        returned. If not, the function returns False.
        """
        data = self._sql.execute_proc_return_cursor(
            'ag_authenticate_user', [username, password])
        row = data.fetchone()
        col_names = self._get_col_names_from_cursor(data)
        data.close()
        if row:
            results = dict(zip(col_names, row))

            if not bcrypt.verify(password, results['kit_password']):
                return False

            results['ag_login_id'] = str(results['ag_login_id'])

            return results
        else:
            return False

    def addAGLogin(self, email, name, address, city, state, zip_, country):
        clean_email = email.strip().lower()
        sql = "select ag_login_id from ag_login WHERE LOWER(email) = %s"
        cur = self.get_cursor()
        cur.execute(sql, [clean_email])
        ag_login_id = cur.fetchone()
        if not ag_login_id:
            # create the login
            sql = ("INSERT INTO ag_login (email, name, address, city, state, "
                   "zip, country) VALUES (%s, %s, %s, %s, %s, %s, %s) "
                   "RETURNING ag_login_id")
            cur.execute(sql, [clean_email, name, address, city,
                              state, zip_, country])
            ag_login_id = cur.fetchone()
            self.connection.commit()
        return ag_login_id[0]

    def updateAGLogin(self, ag_login_id, email, name, address, city, state,
                      zip, country):
        self.get_cursor().callproc('ag_update_login', [ag_login_id,
                                   email.strip().lower(), name,
                                   address, city, state, zip, country])
        self.connection.commit()

    def getAGSurveyDetails(self, ag_login_id, participant_name):
        results = self._sql.execute_proc_return_cursor('ag_get_survey_details',
                                                       [ag_login_id,
                                                        participant_name])
        rows = results.fetchall()
        col_names = self._get_col_names_from_cursor(results)
        results.close()

        rows = [dict(zip(col_names, row)) for row in rows]

        data = {row['question']: row['answer'] for row in rows
                if row['answer']}

        return data

    # note: only used by the password migration
    def getAGKitsByLogin(self):
        results = self._sql.execute_proc_return_cursor('ag_get_kits_by_login',
                                                       [])
        rows = results.fetchall()
        col_names = self._get_col_names_from_cursor(results)
        results.close()

        return_res = [dict(zip(col_names, row)) for row in rows]

        return return_res

    def getAGBarcodes(self):
        results = self._sql.execute_proc_return_cursor('ag_get_barcodes', [])
        return_res = [row[0] for row in results]
        results.close()
        return return_res

    def getAGBarcodeDetails(self, barcode):
        results = self._sql.execute_proc_return_cursor(
            'ag_get_barcode_details', [barcode])
        barcode_details = results.fetchone()
        col_names = self._get_col_names_from_cursor(results)
        results.close()

        row_dict = {}
        if barcode_details:
            row_dict = dict(zip(col_names, barcode_details))

        return row_dict

    def getAGKitDetails(self, supplied_kit_id):
        results = self._sql.execute_proc_return_cursor('ag_get_kit_details',
                                                       [supplied_kit_id])
        row = results.fetchone()
        col_names = self._get_col_names_from_cursor(results)
        results.close()

        kit_details = {}
        if row:
            kit_details = dict(zip(col_names, row))
        return kit_details

    def getAGHandoutKitDetails(self, supplied_kit_id):
        sql = """SELECT * FROM ag.ag_handout_kits
                 JOIN (SELECT
                    kit_id, array_agg(barcode ORDER BY barcode) AS barcodes,
                    sample_barcode_file FROM ag.ag_handout_barcodes
                    GROUP BY kit_id, sample_barcode_file) AS hb
                 USING (kit_id)
                 WHERE kit_id = %s"""
        cur = self.get_cursor()
        cur.execute(sql, [supplied_kit_id])
        row = cur.fetchone()
        col_names = self._get_col_names_from_cursor(cur)
        cur.close()

        kit_details = dict(zip(col_names, row))

        return kit_details

    def getAGHandoutKitIDsAndPasswords(self):
        sql = "SELECT kit_id, password FROM ag_handout_kits"
        cur = self.get_cursor()
        cur.execute(sql)

        return cur.fetchall()

    def getAGCode(self, passwd_length, type='alpha'):
        if type == 'alpha':
            x = ''.join([choice(KIT_ALPHA)
                for i in range(passwd_length-1)])
            return x
        if type == 'numeric':
            x = ''.join([choice(KIT_PASSWD)
                for i in range(passwd_length-1)])
            return choice(KIT_PASSWD_NOZEROS) + x

    def getNewAGKitId(self):
        def get_used_kit_ids(cursor):
            """Grab in use kit IDs, return set of them
            """
            cursor.execute("select supplied_kit_id from ag_kit")
            kits = set([i[0] for i in cursor.fetchall()])
            return kits

        def make_kit_id(kit_id_length=8):
            kit_id = ''.join([choice(KIT_ALPHA) for i in range(kit_id_length)])
            return kit_id

        cur = self.get_cursor()
        obs_kit_ids = get_used_kit_ids(cur)
        kit_id = make_kit_id(8)
        while kit_id in obs_kit_ids:
            kit_id = make_kit_id(8)

        return kit_id

    def getNextAGBarcode(self):
        results = self._sql.execute_proc_return_cursor('ag_get_next_barcode',
                                                       [])
        next_barcode = results.fetchone()[0]
        text_barcode = '{0}'.format(str(next_barcode))
        # Pad out the barcode until it's 9 digits long
        while len(text_barcode) < 9:
            text_barcode = '0{0}'.format(text_barcode)

        results.close()
        return next_barcode, text_barcode

    def reassignAGBarcode(self, ag_kit_id, barcode):
        self.get_cursor().callproc('ag_reassign_barcode', [ag_kit_id,
                                                           barcode])
        self.connection.commit()

    def addAGKit(self, ag_login_id, kit_id, kit_password, swabs_per_kit,
                 kit_verification_code, printresults='n'):
        """
        Returns
        -------
        int
            1:  success
            -1: insert failed due to IntegrityError

        Notes
        -----
        Whatever is passed as kit_password will be added AS IS. This means you
        must hash the password before passing, if desired.
        """
        try:
            self.get_cursor().callproc('ag_insert_kit',
                                       [ag_login_id, kit_id,
                                        kit_password, swabs_per_kit,
                                        kit_verification_code,
                                        printresults])
            self.connection.commit()
        except psycopg2.IntegrityError:
            logging.exception('Error on skid %s:' % ag_login_id)
            self.connection.rollback()
            return -1
        return 1

    def updateAGKit(self, ag_kit_id, supplied_kit_id, kit_password,
                    swabs_per_kit, kit_verification_code):
        kit_password = bcrypt.encrypt(kit_password)

        self.get_cursor().callproc('ag_update_kit',
                                   [ag_kit_id, supplied_kit_id,
                                    kit_password, swabs_per_kit,
                                    kit_verification_code])
        self.connection.commit()

    def addAGBarcode(self, ag_kit_id, barcode):
        """
        return values
        1:  success
        -1: insert failed due to IntegrityError
        """
        try:
            self.get_cursor().callproc('ag_insert_barcode',
                                       [ag_kit_id, barcode])
            self.connection.commit()
        except psycopg2.IntegrityError:
            logging.exception('Error on barcode %s:' % barcode)
            self.connection.rollback()
            return -1
        return 1

    def updateAGBarcode(self, barcode, ag_kit_id, site_sampled,
                        environment_sampled, sample_date, sample_time,
                        participant_name, notes, refunded, withdrawn):
        self.get_cursor().callproc('ag_update_barcode',
                                   [barcode, ag_kit_id, site_sampled,
                                    environment_sampled,
                                    sample_date, sample_time,
                                    participant_name, notes,
                                    refunded, withdrawn])
        self.connection.commit()

    def registerHandoutKit(self, ag_login_id, supplied_kit_id):
        """
        Returns
        -------
        bool
            True:  success
            False: insert failed due to IntegrityError

        Notes
        -----
        Whatever is passed as kit_password will be added AS IS. This means you
        must hash the password before passing, if desired.
        """
        printresults = self.checkPrintResults(supplied_kit_id)
        if printresults is None:
            printresults = 'n'

        sql = """
            DO $do$
            DECLARE
                k_id uuid;
                bc varchar;
            BEGIN
                INSERT INTO ag_kit
                (ag_login_id, supplied_kit_id, kit_password, swabs_per_kit,
                 kit_verification_code, print_results)
                SELECT '{0}', kit_id, password, swabs_per_kit,
                    verification_code, '{1}'
                    FROM ag_handout_kits WHERE kit_id = %s LIMIT 1
                RETURNING ag_kit_id INTO k_id;
                FOR bc IN
                    SELECT barcode FROM ag_handout_barcodes WHERE kit_id = %s
                LOOP
                    INSERT  INTO ag_kit_barcodes
                        (ag_kit_id, barcode, sample_barcode_file)
                        VALUES (k_id, bc, bc || '.jpg');
                END LOOP;
                DELETE FROM ag_handout_kits WHERE kit_id = %s;
            END $do$;
            """.format(ag_login_id, printresults)

        conn_handler = SQLConnectionHandler()
        try:
            conn_handler.execute(sql, [supplied_kit_id] * 3)
        except psycopg2.IntegrityError:
            logging.exception('Error on skid %s:' % ag_login_id)
            return False
        return True

    def addAGHumanParticipant(self, ag_login_id, participant_name):
        self.get_cursor().callproc('ag_add_participant',
                                   [ag_login_id, participant_name])
        self.connection.commit()

    def addAGAnimalParticipant(self, ag_login_id, participant_name):
        self.get_cursor().callproc('ag_add_animal_participant',
                                   [ag_login_id, participant_name])
        self.connection.commit()

    def addAGSingle(self, ag_login_id, participant_name, field_name,
                    field_value, table_name):
        table = "update %s set %s" % (table_name, field_name)
        sql = table + ("= %s where ag_login_id = %s and "
                       "participant_name = %s")
        self.get_cursor().execute(sql, [field_value, ag_login_id,
                                        participant_name])
        self.connection.commit()

    def deleteAGParticipantSurvey(self, ag_login_id, participant_name):
        # Remove user using old stype DB Schema
        self.get_cursor().callproc('ag_delete_participant',
                                   [ag_login_id, participant_name])
        self.connection.commit()

        # Remove user from new schema
        conn_handler = SQLConnectionHandler()
        sql = ("SELECT survey_id FROM ag_login_surveys WHERE ag_login_id = "
               "%s AND participant_name = %s")
        survey_id = conn_handler.execute_fetchone(
            sql, (ag_login_id, participant_name))[0]

        with conn_handler.get_postgres_cursor() as curr:
            sql = ("DELETE FROM survey_answers WHERE "
                   "survey_id = %s")
            curr.execute(sql, [survey_id])

            sql = ("DELETE FROM survey_answers_other WHERE "
                   "survey_id = %s")
            curr.execute(sql, [survey_id])

            # Reset survey attached to barcode(s)
            sql = ("UPDATE ag_kit_barcodes SET survey_id = NULL WHERE "
                   "survey_id = %s")
            curr.execute(sql, [survey_id])

            sql = "DELETE FROM promoted_survey_ids WHERE survey_id = %s"
            curr.execute(sql, [survey_id])

            # Delete last due to foreign keys
            sql = ("DELETE FROM ag_login_surveys WHERE "
                   "survey_id = %s")
            curr.execute(sql, [survey_id])

            sql = ("DELETE FROM ag_consent WHERE ag_login_id = "
                   "%s AND participant_name = %s")
            curr.execute(sql, [ag_login_id, participant_name])

    def getConsent(self, survey_id):
        conn_handler = SQLConnectionHandler()
        with conn_handler.get_postgres_cursor() as cur:
            cur.execute("""SELECT agc.participant_name,
                                  agc.participant_email,
                                  agc.parent_1_name,
                                  agc.parent_2_name,
                                  agc.is_juvenile,
                                  agc.deceased_parent,
                                  agc.ag_login_id,
                                  agc.date_signed,
                                  agc.assent_obtainer,
                                  agc.age_range,
                                  agl.survey_id
                           FROM ag_consent agc JOIN
                                ag_login_surveys agl
                                USING (ag_login_id, participant_name)
                           WHERE agl.survey_id=%s""", [survey_id])
            colnames = [x[0] for x in cur.description]
            result = cur.fetchone()
            if result:
                result = {k: v for k, v in zip(colnames, result)}
                if 'date_signed' in result:
                    result['date_signed'] = str(result['date_signed'])
                return result

    def addAGGeneralValue(self, ag_login_id, participant_name, field_name,
                          field_value):
        self.get_cursor().callproc('ag_insert_survey_answer',
                                   [ag_login_id, participant_name,
                                    field_name, field_value])
        self.connection.commit()

    def deleteAGGeneralValues(self, ag_login_id, participant_name):
        self.get_cursor().callproc('ag_delete_survey_answer',
                                   [ag_login_id, participant_name])
        self.connection.commit()

    def logParticipantSample(self, ag_login_id, barcode, sample_site,
                             environment_sampled, sample_date, sample_time,
                             participant_name, notes):

        conn_handler = SQLConnectionHandler()
        if sample_site is not None:
            # Get survey id
            sql = ("SELECT survey_id FROM ag_login_surveys WHERE ag_login_id = "
                   "%s AND participant_name = %s")

            survey_id = conn_handler.execute_fetchone(
                sql, (ag_login_id, participant_name))
            if survey_id:
                # remove the list encapulation
                survey_id = survey_id[0]
            else:
                raise RuntimeError("No survey ID for ag_login_id %s and "
                                   "participant name %s" % (ag_login_id,
                                                            participant_name))
        else:
            # otherwise, it is an environmental sample
            survey_id = None

        # Add barcode info
        sql = """update  ag_kit_barcodes
                 set     site_sampled = %s,
                         environment_sampled = %s,
                         sample_date = %s,
                         sample_time = %s,
                         participant_name = %s,
                         notes = %s,
                         survey_id = %s
                 where   barcode = %s"""
        conn_handler.execute(sql, [
            sample_site, environment_sampled, sample_date, sample_time,
            participant_name, notes, survey_id, barcode])
        self.connection.commit()

    def deleteSample(self, barcode, ag_login_id):
        """
        Strictly speaking the ag_login_id isn't needed but it makes it really
        hard to hack the function when you would need to know someone else's
        login id (a GUID) to delete something maliciously
        """
        self.get_cursor().callproc('ag_delete_sample',
                                   [barcode, ag_login_id])
        self.connection.commit()

    def getHumanParticipants(self, ag_login_id):
        conn_handler = SQLConnectionHandler()
        # get people from new survey setup
        sql = """SELECT participant_name from ag.ag_login_surveys
                 JOIN ag.survey_answers USING (survey_id)
                 JOIN ag.group_questions gq USING (survey_question_id)
                 JOIN ag.surveys ags USING (survey_group)
                 WHERE ag_login_id = %s AND ags.survey_id = %s"""
        results = conn_handler.execute_fetchall(sql, [ag_login_id, 1])
        return [row[0] for row in results]

    def is_old_survey(self, survey_id):
        conn_handler = SQLConnectionHandler()
        # check survey exists
        survey_answers = conn_handler.execute_fetchone(
            "SELECT exists(SELECT * FROM survey_answers WHERE survey_id = %s)",
            [survey_id])[0]
        survey_answers_other = conn_handler.execute_fetchone(
            "SELECT exists(SELECT * FROM survey_answers_other WHERE "
            "survey_id = %s)", [survey_id])[0]

        return all((survey_answers is False, survey_answers_other is False))

    def updateVioscreenStatus(self, survey_id, status):
        conn_handler = SQLConnectionHandler()
        sql = ("UPDATE ag_login_surveys SET vioscreen_status = %s WHERE "
               "survey_id = %s")
        conn_handler.execute(sql, (status, survey_id))

    def AGGetBarcodeMetadata(self, barcode):
        results = self._sql.execute_proc_return_cursor(
            'ag_get_barcode_metadata', [barcode])
        rows = results.fetchall()
        col_names = self._get_col_names_from_cursor(results)
        results.close()

        return_res = [dict(zip(col_names, row)) for row in rows]

        return return_res

    def AGGetBarcodeMetadataAnimal(self, barcode):
        results = self._sql.execute_proc_return_cursor(
            'ag_get_barcode_md_animal', [barcode])
        col_names = self._get_col_names_from_cursor(results)
        return_res = [dict(zip(col_names, row)) for row in results]
        results.close()
        return return_res

    def getAnimalParticipants(self, ag_login_id):
        sql = """SELECT participant_name FROM ag_animal_survey
                 WHERE  ag_login_id = %s
                 UNION
                 SELECT participant_name from ag.ag_login_surveys
                 JOIN ag.survey_answers USING (survey_id)
                 JOIN ag.group_questions gq USING (survey_question_id)
                 JOIN ag.surveys ags USING (survey_group)
                 WHERE ag_login_id = %s AND ags.survey_id = %s"""
        conn_handler = SQLConnectionHandler()
        return [row[0] for row in
                conn_handler.execute_fetchall(
                    sql, [ag_login_id, ag_login_id, 2])]

    def getParticipantExceptions(self, ag_login_id):
        results = self._sql.execute_proc_return_cursor(
            'ag_get_participant_exceptions', [ag_login_id])

        return_res = [row[0] for row in results]
        results.close()
        return return_res

    def getParticipantSamples(self, ag_login_id, participant_name):
        results = self._sql.execute_proc_return_cursor(
            'ag_get_participant_samples', [ag_login_id, participant_name])
        rows = results.fetchall()
        col_names = self._get_col_names_from_cursor(results)
        results.close()

        barcodes = [dict(zip(col_names, row)) for row in rows]

        return barcodes

    def getEnvironmentalSamples(self, ag_login_id):
        barcodes = []
        results = self._sql.execute_proc_return_cursor(
            'ag_get_environmental_samples', [ag_login_id])
        rows = results.fetchall()
        col_names = self._get_col_names_from_cursor(results)
        results.close()

        barcodes = [dict(zip(col_names, row)) for row in rows]

        return barcodes

    def getAvailableBarcodes(self, ag_login_id):
        results = self._sql.execute_proc_return_cursor('ag_available_barcodes',
                                                       [ag_login_id])
        return_res = [row[0] for row in results]
        results.close()
        return return_res

    def verifyKit(self, supplied_kit_id):
        """Set the KIT_VERIFIED for the supplied_kit_id to 'y'"""
        self.get_cursor().callproc('ag_verify_kit_status',
                                   [supplied_kit_id])
        self.connection.commit()

    def addGeocodingInfo(self, limit=None, retry=False):
        """Adds latitude, longitude, and elevation to ag_login_table

        Uses the city, state, zip, and country from the database to retrieve
        lat, long, and elevation from the google maps API.

        If any of that information cannot be retrieved, then cannot_geocode
        is set to 'y' in the ag_login table, and it will not be tried again
        on subsequent calls to this function.  Pass retry=True to retry all
        (or maximum of limit) previously failed geocodings.
        """

        # clear previous geocoding attempts if retry is True
        if retry:
            sql = (
                "select cast(ag_login_id as varchar(100))from ag_login "
                "where cannot_geocode = 'y'"
            )
            cursor = self.connection.cursor()
            cursor.execute(sql)
            logins = cursor.fetchall()

            for row in logins:
                ag_login_id = row[0]
                self.updateGeoInfo(ag_login_id, None, None, None, '')

        # get logins that have not been geocoded yet
        sql = (
            'select city, state, zip, country, '
            'cast(ag_login_id as varchar(100))'
            'from ag_login '
            'where elevation is null '
            'and cannot_geocode is null'
        )

        cursor = self.connection.cursor()
        cursor.execute(sql)
        logins = cursor.fetchall()

        row_counter = 0
        for row in logins:
            row_counter += 1
            if limit is not None and row_counter > limit:
                break

            ag_login_id = row[4]
            # Attempt to geocode
            address = '{0} {1} {2} {3}'.format(row[0], row[1], row[2], row[3])
            encoded_address = urllib.urlencode({'address': address})
            url = '/maps/api/geocode/json?{0}&sensor=false'.format(
                encoded_address)

            r = self.getGeocodeJSON(url)

            if r in ('unknown_error', 'not_OK', 'no_results'):
                # Could not geocode, mark it so we don't try next time
                self.updateGeoInfo(ag_login_id, None, None, None, 'y')
                continue
            elif r == 'over_limit':
                # If the reason for failure is merely that we are over the
                # Google API limit, then we should try again next time
                # ... but we should stop hitting their servers, so raise an
                # exception
                raise GoogleAPILimitExceeded("Exceeded Google API limit")

            # Unpack it and write to DB
            lat, lon = r

            encoded_lat_lon = urllib.urlencode(
                {'locations': ','.join(map(str, [lat, lon]))})

            url2 = '/maps/api/elevation/json?{0}&sensor=false'.format(
                encoded_lat_lon)

            r2 = self.getElevationJSON(url2)

            if r2 in ('unknown_error', 'not_OK', 'no_results'):
                # Could not geocode, mark it so we don't try next time
                self.updateGeoInfo(ag_login_id, None, None, None, 'y')
                continue
            elif r2 == 'over_limit':
                # If the reason for failure is merely that we are over the
                # Google API limit, then we should try again next time
                # ... but we should stop hitting their servers, so raise an
                # exception
                raise GoogleAPILimitExceeded("Exceeded Google API limit")

            elevation = r2

            self.updateGeoInfo(ag_login_id, lat, lon, elevation, '')

    def getGeocodeStats(self):
        stat_queries = [
            ("Total Rows",
             "select count(*) from ag_login"),
            ("Cannot Geocode",
             "select count(*) from ag_login where cannot_geocode = 'y'"),
            ("Null Latitude Field",
             "select count(*) from ag_login where latitude is null"),
            ("Null Elevation Field",
             "select count(*) from ag_login where elevation is null")
        ]
        results = []
        for name, sql in stat_queries:
            cur = self.get_cursor()
            cur.execute(sql)
            total = cur.fetchone()[0]
            results.append((name, total))
        return results

    def getMapMarkers(self):
        cur_completed = self.get_cursor()
        cur_ver = self.get_cursor()
        cur_ll = self.get_cursor()

        # fetch all latitide/longitude by kit id
        cur_ll.execute("""SELECT ak.supplied_kit_id, al.latitude, al.longitude
                          FROM ag_login al
                               INNER JOIN ag_kit ak
                               ON ak.ag_login_id=al.ag_login_id
                          WHERE al.latitude IS NOT NULL AND
                                al.longitude IS NOT NULL""")
        ll = {res[0]: (res[1], res[2]) for res in cur_ll.fetchall()}

        # determine all completed kits
        cur_completed.execute("""SELECT ak.supplied_kit_id
                                 FROM ag_kit ak
                                 WHERE (
                                       SELECT  count(*)
                                       FROM ag_kit_barcodes akb
                                       WHERE akb.ag_kit_id = ak.ag_kit_id
                                       ) =
                                       (
                                       SELECT  count(*)
                                       FROM ag_kit_barcodes akb
                                       WHERE akb.ag_kit_id = ak.ag_kit_id AND
                                             akb.site_sampled IS NOT NULL
                                       )""")
        completed = (res[0] for res in cur_completed.fetchall())

        # determine what kit are not verified
        cur_ver.execute("""SELECT supplied_kit_id, kit_verified
                           FROM ag_kit""")
        notverified = (res[0] for res in cur_ver.fetchall() if res[1] == 'n')

        # set green for completed kits
        res = {ll[kid]: '00FF00' for kid in completed if kid in ll}

        # set blue for unverified kits
        res.update({ll[kid]: '00B2FF' for kid in notverified if kid in ll})

        # set yellow for all others
        res.update({v: 'FFFF00' for k, v in ll.items() if v not in res})

        return [[lat, lng, c] for ((lat, lng), c) in res.items()]

    def getGeocodeJSON(self, url):
        conn = httplib.HTTPConnection('maps.googleapis.com')
        success = False
        num_tries = 0
        while num_tries < 2 and not success:
            conn.request('GET', url)
            result = conn.getresponse()

            # Make sure we get an 'OK' status
            if result.status != 200:
                return 'not_OK'

            data = json.loads(result.read())

            # if we're over the query limit, wait 2 seconds and try again,
            # it may just be that we're submitting requests too fast
            if data.get('status', None) == 'OVER_QUERY_LIMIT':
                num_tries += 1
                sleep(2)
            elif 'results' in data:
                success = True
            else:
                return 'unknown_error'

        conn.close()

        # if we got here without getting an unknown_error or succeeding, then
        # we are over the request limit for the 24 hour period
        if not success:
            return 'over_limit'

        # sanity check the data returned by Google and return the lat/lng
        if len(data['results']) == 0:
            return 'no_results'

        geometry = data['results'][0].get('geometry', {})
        location = geometry.get('location', {})
        lat = location.get('lat', {})
        lon = location.get('lng', {})

        if not lat or not lon:
            return 'unknown_error'

        return (lat, lon)

    def getElevationJSON(self, url):
        """Use Google's Maps API to retrieve an elevation

        url should be formatted as described here:
        https://developers.google.com/maps/documentation/elevation
        /#ElevationRequests

        The number of API requests is limited to 2500 per 24 hour period.
        If this function is called and the limit is surpassed, the return value
        will be "over_limit".  Other errors will cause the return value to be
        "unknown_error".  On success, the return value is the elevation of the
        location requested in the url.
        """
        conn = httplib.HTTPConnection('maps.googleapis.com')
        success = False
        num_tries = 0
        while num_tries < 2 and not success:
            conn.request('GET', url)
            result = conn.getresponse()

            # Make sure we get an 'OK' status
            if result.status != 200:
                return 'not_OK'

            data = json.loads(result.read())

            # if we're over the query limit, wait 2 seconds and try again,
            # it may just be that we're submitting requests too fast
            if data.get('status', None) == 'OVER_QUERY_LIMIT':
                num_tries += 1
                sleep(2)
            elif 'results' in data:
                success = True
            else:
                return 'unknown_error'

        conn.close()

        # if we got here without getting an unknown_error or succeeding, then
        # we are over the request limit for the 24 hour period
        if not success:
            return 'over_limit'

        # sanity check the data returned by Google and return the lat/lng
        if len(data['results']) == 0:
            return 'no_results'

        elevation = data['results'][0].get('elevation', {})

        if not elevation:
            return 'unknown_error'

        return elevation

    def updateGeoInfo(self, ag_login_id, lat, lon, elevation, cannot_geocode):
        self.get_cursor().callproc('ag_update_geo_info',
                                   [ag_login_id, lat, lon, elevation,
                                    cannot_geocode])
        self.connection.commit()

    def handoutCheck(self, username, password):
        cursor = self.get_cursor()
        cursor.execute("""SELECT password
                          FROM ag.ag_handout_kits
                          WHERE kit_id=%s""", [username])
        to_check = cursor.fetchone()

        if not to_check:
            return False
        else:
            return bcrypt.verify(password, to_check[0])

    def check_access(self, supplied_kit_id, barcode):
        """Check if the user has access to the barcode

        Parameters
        ----------
        supplied_kit_id : str
            The user's supplied kit ID
        barcode : str
            The barcode to check access for

        Returns
        -------
        boolean
            True if the user can access the barcode, False otherwise
        """
        ag_login_id = self.get_user_for_kit(supplied_kit_id)
        cursor = self.get_cursor()
        cursor.execute("""SELECT EXISTS (
                              SELECT barcode
                              FROM ag.ag_kit JOIN
                                   ag.ag_kit_barcodes USING(ag_kit_id)
                              WHERE ag_login_id = %s AND
                                    barcode = %s)""", [ag_login_id, barcode])
        return cursor.fetchone()[0]

    def updateAGSurvey(self, ag_login_id, participant_name, field, value):
        # Make sure no single quotes get passed as it will break the sql string
        value = str(value).replace("'", "''")
        participant_name = str(participant_name).replace("'", "''")
        table = "update ag_human_survey set %s" % field
        sql = table + "= %s where ag_login_id = %s and participant_name = %s"
        self.get_cursor().execute(sql, [value, ag_login_id,
                                        participant_name])
        self.connection.commit()

    def getAGStats(self):
        # returned tuple consists of:
        # site_sampled, sample_date, sample_time, participant_name,
        #environment_sampled, notes
        results = self._sql.execute_proc_return_cursor('ag_stats', [])
        ag_stats = results.fetchall()
        results.close()
        return ag_stats

    def updateAKB(self, barcode, moldy, overloaded, other, other_text,
                  date_of_last_email):
        """ Update ag_kit_barcodes table.
        """
        self.get_cursor().callproc('update_akb', [barcode, moldy,
                                                  overloaded, other,
                                                  other_text,
                                                  date_of_last_email])
        self.connection.commit()

    def getAGKitIDsByEmail(self, email):
        """Returns a list of kitids based on email

        email is email address of login
        returns a list of kit_id's associated with the email or an empty list
        """
        results = self._sql.execute_proc_return_cursor(
            'ag_get_kit_id_by_email', [email.lower()])
        kit_ids = [row[0] for row in results]
        results.close()
        return kit_ids

    def ag_set_pass_change_code(self, email, kitid, pass_code):
        """updates ag_kit table with the supplied pass_code

        email is email address of participant
        kitid is supplied_kit_kd in the ag_kit table
        pass_code is the password change verfication value
        """
        self.get_cursor().callproc('ag_set_pass_change_code',
                                   [email, kitid, pass_code])
        self.connection.commit()

    def ag_update_kit_password(self, kit_id, password):
        """updates ag_kit table with password

        kit_id is supplied_kit_id in the ag_kit table
        password is the new password
        """
        password = bcrypt.encrypt(password)

        self.get_cursor().callproc('ag_update_kit_password',
                                   [kit_id, password])
        self.connection.commit()

    def ag_update_handout_kit_password(self, kit_id, password):
        """updates ag_handout_kits table with password

        kit_id is kit_id in the ag_handout_kits table
        password is the new password
        """
        password = bcrypt.encrypt(password)

        cursor = self.get_cursor()
        cursor.execute("""UPDATE ag_handout_kits
                          SET password=%s
                          WHERE kit_id=%s""", [password, kit_id])
        self.connection.commit()

    def ag_verify_kit_password_change_code(self, email, kitid, passcode):
        """returns true if it still in the password change window

        email is the email address of the participant
        kitid is the supplied_kit_id in the ag_kit table
        passcode is the password change verification value
        """
        cursor = self.get_cursor()
        cursor.callproc('ag_verify_password_change_code', [email, kitid,
                                                           passcode])
        return cursor.fetchone()[0]

    def getBarcodesByKit(self, kitID):
        """Returns a list of barcodes in a kit

        kitID is the supplied_kit_id from the ag_kit table
        """
        results = self._sql.execute_proc_return_cursor(
            'ag_get_barcodes_by_kit', [kitID])
        barcodes = [row[0] for row in results]
        results.close()
        return barcodes

    def checkPrintResults(self, kit_id):
        results = self._sql.execute_proc_return_cursor('ag_get_print_results',
                                                       [kit_id])
        print_results = results.fetchone()
        results.close()
        if print_results is None:
            return None
        else:
            return print_results[0].strip()

    def get_user_for_kit(self, supplied_kit_id):
        sql = ("select AK.ag_login_id from ag_kit AK "
               "join ag_login AL on AK.ag_login_id = AL.ag_login_id "
               "where AK.supplied_kit_id = %s")
        cursor = self.get_cursor()
        cursor.execute(sql, [supplied_kit_id])
        results = cursor.fetchone()
        if results:
            return results[0]
        else:
            raise RuntimeError("No user ID for kit %s" % supplied_kit_id)

    def get_menu_items(self, supplied_kit_id):
        """Returns information required to populate the menu of the website"""
        ag_login_id = self.get_user_for_kit(supplied_kit_id)
        info = self.getAGKitDetails(supplied_kit_id)

        kit_verified = False
        if info['kit_verified'] == 'y':
            kit_verified = True

        human_samples = {hs: self.getParticipantSamples(ag_login_id, hs)
                         for hs in self.getHumanParticipants(ag_login_id)}
        animal_samples = {ans: self.getParticipantSamples(ag_login_id, ans)
                          for ans in self.getAnimalParticipants(ag_login_id)}
        environmental_samples = self.getEnvironmentalSamples(ag_login_id)

        return (human_samples, animal_samples, environmental_samples,
                kit_verified)

    def check_if_consent_exists(self, ag_login_id, participant_name):
        """Return True if a consent already exists"""
        sql = """select exists(
                    select 1
                    from ag_consent
                    where ag_login_id=%s and
                        participant_name=%s)"""
        cursor = self.get_cursor()
        cursor.execute(sql, (ag_login_id, participant_name))
        return cursor.fetchone()[0]

    def get_user_info(self, supplied_kit_id):
        sql = """SELECT  cast(agl.ag_login_id as varchar(100)) as ag_login_id,
                        agl.email, agl.name, agl.address, agl.city,
                        agl.state, agl.zip, agl.country
                 from    ag_login agl
                        inner join ag_kit agk
                        on agl.ag_login_id = agk.ag_login_id
                 where   agk.supplied_kit_id = %s"""
        cursor = self.get_cursor()
        cursor.execute(sql, [supplied_kit_id])
        row = cursor.fetchone()
        col_names = self._get_col_names_from_cursor(cursor)

        user_data = {}
        if row:
            user_data = dict(zip(col_names, row))
            user_data['ag_login_id'] = str(user_data['ag_login_id'])

        return user_data

    def get_person_info(self, survey_id):
        # get question responses
        info = {'birth_month': 'Unspecified', 'birth_year': 'Unspecified', 'gender': 'Unspecified'}
        sql = ("SELECT q.american, sa.response FROM ag.survey_answers_other "
               " sa JOIN ag.ag_login_surveys ls ON sa.survey_id = ls.survey_id "
               "JOIN ag.survey_question q ON q.survey_question_id = sa.survey_question_id "
               "WHERE sa.survey_id = %s AND q.american IN ('Birth month:','Birth year:','Gender:')")
        cursor = self.get_cursor()
        cursor.execute(sql, [survey_id])
        rows = cursor.fetchall()

        for res in rows:
            value = json.loads(res[1])[0]
            if res[0] == 'Birth month:':
                info['birth_month'] = value
            elif res[0] == 'Birth year:':
                info['birth_year'] = value
            elif res[0] == 'Gender:':
                info['gender'] = value

        # get name from consent form
        sql = ("SELECT c.participant_name FROM ag.ag_consent c JOIN "
               "ag.ag_login_surveys ls ON c.ag_login_id = ls.ag_login_id WHERE "
               "ls.survey_id = %s")
        cursor.execute(sql, [survey_id])
        info["name"] = cursor.fetchone()[0]

        return info

    def get_barcode_results(self, supplied_kit_id):
        """Get the results associated with the login ID of the kit"""
        ag_login_id = self.get_user_for_kit(supplied_kit_id)
        cursor = self.get_cursor()

        sql = """SELECT akb.barcode, akb.participant_name
                 FROM ag_kit_barcodes akb
                 INNER JOIN ag_kit agk USING(ag_kit_id)
                 WHERE agk.ag_login_id = %s AND akb.results_ready = 'Y'"""

        cursor.execute(sql, [ag_login_id])
        results = cursor.fetchall()
        col_names = self._get_col_names_from_cursor(cursor)
        return [dict(zip(col_names, row)) for row in results]

    def search_participant_info(self, term):
        sql = """select   cast(ag_login_id as varchar(100)) as ag_login_id
                 from    ag_login al
                 where   lower(email) like %s or lower(name) like
                 %s or lower(address) like %s"""
        cursor = self.get_cursor()
        liketerm = '%%' + term.lower() + '%%'
        cursor.execute(sql, [liketerm, liketerm, liketerm])
        results = cursor.fetchall()
        cursor.close()
        return [x[0] for x in results]

    def search_kits(self, term):
        sql = """ select  cast(ag_login_id as varchar(100)) as ag_login_id
                 from    ag_kit
                 where   lower(supplied_kit_id) like %s or
                 lower(kit_password) like %s or
                 lower(kit_verification_code) = %s"""
        cursor = self.get_cursor()
        liketerm = '%%' + term.lower() + '%%'
        cursor.execute(sql, [liketerm, liketerm, term])
        results = cursor.fetchall()
        cursor.close()
        return [x[0] for x in results]

    def search_participants(self, term):
        sql = """ select  cast(ag_login_id as varchar(100)) as ag_login_id
                 from    ag_consent
                 where   lower(participant_name) like %s or
                 lower(participant_email) like %s"""
        conn_handler = SQLConnectionHandler()
        liketerm = '%%' + term.lower() + '%%'
        return [x[0] for x in conn_handler.execute_fetchall(
            sql, [liketerm, liketerm])]

    def search_barcodes(self, term):
        sql = """select  cast(ak.ag_login_id as varchar(100)) as ag_login_id
                 from    ag_kit ak
                 inner join ag_kit_barcodes akb
                 on ak.ag_kit_id = akb.ag_kit_id
                 where   barcode like %s or lower(participant_name) like
                 %s or lower(notes) like %s"""
        cursor = self.get_cursor()
        liketerm = '%%' + term.lower() + '%%'
        cursor.execute(sql, [liketerm, liketerm, liketerm])
        results = cursor.fetchall()
        cursor.close()
        return [x[0] for x in results]

    def get_login_info(self, ag_login_id):
        sql = """select  ag_login_id, email, name, address, city, state, zip,
                         country
                 from    ag_login
                 where   ag_login_id = %s"""
        cursor = self.get_cursor()
        cursor.execute(sql, [ag_login_id])
        col_names = [x[0] for x in cursor.description]
        results = [dict(zip(col_names, row)) for row in cursor.fetchall()]
        cursor.close()
        return results

    def get_kit_info_by_login(self, ag_login_id):
        sql = """select  cast(ag_kit_id as varchar(100)) as ag_kit_id,
                        cast(ag_login_id as varchar(100)) as ag_login_id,
                        supplied_kit_id, kit_password, swabs_per_kit,
                        kit_verification_code, kit_verified
                from    ag_kit
                where   ag_login_id = %s"""
        cursor = self.get_cursor()
        cursor.execute(sql, [ag_login_id])
        col_names = [x[0] for x in cursor.description]
        results = [dict(zip(col_names, row)) for row in cursor.fetchall()]
        cursor.close()
        return results

    def get_barcode_info_by_kit_id(self, ag_kit_id):
        sql = """select  cast(ag_kit_barcode_id as varchar(100)) as
                  ag_kit_barcode_id, cast(ag_kit_id as varchar(100)) as
                  ag_kit_id, barcode, sample_date, sample_time, site_sampled,
                  participant_name, environment_sampled, notes, results_ready,
                  withdrawn, refunded
                from    ag_kit_barcodes
                where   ag_kit_id = %s"""
        cursor = self.get_cursor()
        cursor.execute(sql, [ag_kit_id])
        col_names = [x[0] for x in cursor.description]
        results = [dict(zip(col_names, row)) for row in cursor.fetchall()]
        cursor.close()
        return results

    def search_handout_kits(self, term):
        sql = """SELECT kit_id, password, barcode, verification_code
                 FROM ag_handout_kits
                 JOIN (SELECT kit_id, barcode, sample_barcode_file
                    FROM ag.ag_handout_barcodes
                    GROUP BY kit_id, barcode) AS hb USING (kit_id)
                 WHERE kit_id LIKE %s or barcode LIKE %s"""
        cursor = self.get_cursor()
        liketerm = '%%' + term + '%%'
        cursor.execute(sql, [liketerm, liketerm])
        col_names = [x[0] for x in cursor.description]
        results = [dict(zip(col_names, row)) for row in cursor.fetchall()]
        cursor.close()
        return results

    def get_login_by_email(self, email):
        sql = """select name, address, city, state, zip, country, ag_login_id
                 from ag_login where email = %s"""
        cursor = self.get_cursor()
        cursor.execute(sql, [email])
        col_names = self._get_col_names_from_cursor(cursor)
        row = cursor.fetchone()

        login = {}
        if row:
            login = dict(zip(col_names, row))
            login['email'] = email

        return login

    def ag_new_survey_exists(self, barcode):
        """
        Returns metadata for an american gut barcode in the new database
        tables
        """
        sql = "select survey_id from ag_kit_barcodes where barcode = %s"
        cursor = self.connection.cursor()
        cursor.execute(sql, [barcode])
        survey_id = cursor.fetchone()
        return survey_id is not None

#################################################
### GENERAL DATA ACCESS  #######################
################################################
# not sure where these should end up
    def get_barcode_details(self, barcode):
        """
        Returns the genral barcode details for a barcode
        """
        sql = """select  create_date_time, status, scan_date,
                  sample_postmark_date,
                  biomass_remaining, sequencing_status, obsolete
                  from    barcode
                  where barcode = %s"""
        cursor = self.get_cursor()
        cursor.execute(sql, [barcode])
        col_names = [x[0] for x in cursor.description]
        results = [dict(zip(col_names, row)) for row in cursor.fetchall()]
        cursor.close()
        if results:
            return results[0]
        else:
            return {}

    def get_plate_for_barcode(self, barcode):
        """
        Gets the sequencing plates a barcode is on
        """
        sql = """select  p.plate, p.sequence_date
                 from    plate p inner join plate_barcode pb on
                 pb.plate_id = p.plate_id \
                where   pb.barcode = %s"""
        cursor = self.get_cursor()
        cursor.execute(sql, [barcode])
        col_names = [x[0] for x in cursor.description]
        results = [dict(zip(col_names, row)) for row in cursor.fetchall()]
        cursor.close()
        return results

    def getBarcodeProjType(self, barcode):
        """ Get the project type of the barcode.
            Return a tuple of project and project type.
        """
        sql = """select p.project from project p inner join
                 project_barcode pb on (pb.project_id = p.project_id)
                 where pb.barcode = %s"""
        cursor = self.get_cursor()
        cursor.execute(sql, [barcode])
        results = cursor.fetchone()
        proj = results[0]
        #this will get changed to get the project type from the db
        if proj in ('American Gut Project', 'ICU Microbiome', 'Handout Kits',
                    'Office Succession Study',
                    'American Gut Project: Functional Feces',
                    'Down Syndrome Microbiome', 'Beyond Bacteria',
                    'All in the Family', 'American Gut Handout kit',
                    'Personal Genome Project', 'Sleep Study',
                    'Anxiety/Depression cohort', 'Alzheimers Study'):
            proj_type = 'American Gut'
        else:
            proj_type = proj
        return (proj, proj_type)

    def setBarcodeProjType(self, project, barcode):
        """sets the project type of the barcodel

            project is the project name from the project table
            barcode is the barcode
        """
        sql = """update project_barcode set project_id =
                (select project_id from project where project = %s)
                where barcode = %s"""
        result = self.get_cursor()
        cursor = self.get_cursor()
        cursor.execute(sql, [project, barcode])
        self.connection.commit()
        cursor.close()

    def getProjectNames(self):
        """Returns a list of project names
        """
        sql = """select project from project"""
        result = self.get_cursor()
        cursor = self.get_cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        return [x[0] for x in results]

    def updateBarcodeStatus(self, status, postmark, scan_date, barcode,
                            biomass_remaining, sequencing_status, obsolete):
        """ Updates a barcode's status
        """
        sql = """update  barcode
        set     status = %s,
            sample_postmark_date = %s,
            scan_date = %s,
            biomass_remaining = %s,
            sequencing_status = %s,
            obsolete = %s
        where   barcode = %s"""
        cursor = self.get_cursor()
        cursor.execute(sql, [status, postmark, scan_date, biomass_remaining,
                             sequencing_status, obsolete, barcode])
        self.connection.commit()
        cursor.close()

    def get_survey_id(self, ag_login_id, participant_name):
        """Return the survey ID associated with a participant or None"""
        sql = """select survey_id
                 from ag_login_surveys
                 where ag_login_id=%s and participant_name=%s"""
        cursor = self.get_cursor()
        cursor.execute(sql, [ag_login_id, participant_name])
        id_ = cursor.fetchone()

        return id_[0] if id_ else None
