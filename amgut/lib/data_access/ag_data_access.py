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
        sql = """SELECT  cast(ag_login_id as varchar(100)) as ag_login_id,
                  email, name, address, city,
                  state, zip, country,kit_password
                FROM ag_login
            INNER JOIN ag_kit USING (ag_login_id)
            WHERE agk.supplied_kit_id = %s"""
        row = self._sql.execute_fetchone(sql, [username])
        if row:
            results = dict(row)

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

    def getAGBarcodeDetails(self, barcode):
        sql = """SELECT  email,
                    cast(ag_kit_barcode_id as varchar(100)),
                    cast(ag_kit_id as varchar(100)),
                    barcode, site_sampled, environment_sampled, sample_date,
                    sample_time, participant_name, notes, refunded, withdrawn,
                    moldy, other, other_text, date_of_last_email ,overloaded,
                    name, status
                  FROM ag_kit_barcodes
                  INNER JOIN ag_kit USING (ag_kit_id)
                  INNER JOIN ag_login USING (ag_login_id)
                  INNER JOIN barcode USING (barcode)
                  WHERE barcode = %s"""
        row = self._sql.execute_fetchone(sql, [barcode])

        row_dict = {}
        if row:
            row_dict = dict(row)
        return row_dict

    def getAGKitDetails(self, supplied_kit_id):
        sql = """SELECT cast(ag_kit_id as varchar(100)),
                    supplied_kit_id, kit_password, swabs_per_kit, kit_verified,
                    kit_verification_code, verification_email_sent
                 FROM ag_kit
                 WHERE supplied_kit_id = %s"""
        row = self._sql.execute_fetchone(sql, [supplied_kit_id])

        kit_details = {}
        if row:
            kit_details = dict(row)
        return kit_details

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

    def getAnimalParticipants(self, ag_login_id):
        sql = """SELECT participant_name from ag.ag_login_surveys
                 JOIN ag.survey_answers USING (survey_id)
                 JOIN ag.group_questions gq USING (survey_question_id)
                 JOIN ag.surveys ags USING (survey_group)
                 WHERE ag_login_id = %s AND ags.survey_id = %s"""
        conn_handler = SQLConnectionHandler()
        return [row[0] for row in
                conn_handler.execute_fetchall(
                    sql, [ag_login_id, 2])]

    def getParticipantSamples(self, ag_login_id, participant_name):
        sql = """SELECT  barcode, site_sampled, sample_date, sample_time,
                    notes, status
                 FROM ag_kit_barcodes akb
                 INNER JOIN barcode USING (barcode)
                 INNER JOIN ag_kit ak USING (ag_kit_id)
                 WHERE (site_sampled IS NOT NULL AND site_sampled::text <> '')
                 AND ag_login_id = %s AND participant_name = %s"""

        conn_handler = SQLConnectionHandler()
        rows = conn_handler.execute_fetchall(
            sql, [ag_login_id, participant_name])
        barcodes = [dict(row) for row in rows]

        return barcodes

    def getEnvironmentalSamples(self, ag_login_id):
        sql = """SELECT  barcode, site_sampled, sample_date, sample_time,
                    notes, status
                 FROM ag_kit_barcodes
                 INNER JOIN barcode USING (barcode)
                 INNER JOIN ag_kit USING(ag_kit_id)
                 WHERE (environment_sampled IS NOT NULL AND
                    environment_sampled::text <> '')
                    AND ag_login_id = %s"""
        rows = self._sql.execute_fetchall(sql, [ag_login_id])
        barcodes = [dict(row) for row in rows]

        return barcodes

    def getAvailableBarcodes(self, ag_login_id):
        sql = """SELECT barcode
                 FROM ag_kit_barcodes
                 INNER JOIN ag_kit USING (ag_kit_id)
                 WHERE coalesce(sample_date::text, '') = ''
                 AND kit_verified = 'y' AND ag_login_id = %s"""
        results = self._sql.execute_fetchall(sql, [ag_login_id])
        return [row[0] for row in results]

    def verifyKit(self, supplied_kit_id):
        """Set the KIT_VERIFIED for the supplied_kit_id to 'y'"""
        sql = """UPDATE AG_KIT
                 SET kit_verified='y'
                 WHERE supplied_kit_id=%s"""
        self._sql.execute(sql, [supplied_kit_id])

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

    def getAGKitIDsByEmail(self, email):
        """Returns a list of kitids based on email

        email is email address of login
        returns a list of kit_id's associated with the email or an empty list
        """
        sql = """SELECT  supplied_kit_id
                 FROM ag_kit
                 INNER JOIN ag_login USING (ag_login_id)
                 WHERE email = %s"""
        return [row[0] for row in self._sql.execute_fetchall(
            sql, [email.lower()])]

    def ag_set_pass_change_code(self, email, kitid, pass_code):
        """updates ag_kit table with the supplied pass_code

        email is email address of participant
        kitid is supplied_kit_id in the ag_kit table
        pass_code is the password change verfication value
        """
        sql = """UPDATE ag_kit
                 SET pass_reset_code = %s,
                     pass_reset_time = clock_timestamp() + interval '2' hour
                 WHERE supplied_kit_id = %s AND ag_login_id in
                     (SELECT ag_login_id FROM ag_login WHERE email = %s)"""
        self._sql.execute(sql, [pass_code, kitid, email])

    def ag_update_kit_password(self, kit_id, password):
        """updates ag_kit table with password

        kit_id is supplied_kit_id in the ag_kit table
        password is the new password
        """
        password = bcrypt.encrypt(password)

        sql = """UPDATE AG_KIT
                 SET kit_password = %s, pass_reset_code = NULL
                 WHERE supplied_kit_id = %s"""
        self.connection.commit(sql, [password, kit_id])

    def ag_verify_kit_password_change_code(self, email, kitid, passcode):
        """returns true if it still in the password change window

        email is the email address of the participant
        kitid is the supplied_kit_id in the ag_kit table
        passcode is the password change verification value
        """
        sql = """SELECT EXISTS(SELECT pass_reset_time
                 FROM ag.ag_kit
                 INNER JOIN ag.ag_login USING (ag_login_id)
                 WHERE pass_reset_code = %s and email = %s
                 AND supplied_kit_id = %s
                 AND NOW() < pass_reset_time)"""
        return self._sql.execute_fetchone(sql, [passcode, email, kitid])[0]

    def getBarcodesByKit(self, kitid):
        """Returns a list of barcodes in a kit

        kitid is the supplied_kit_id from the ag_kit table
        """
        sql = """SELECT barcode
                 FROM ag_kit_barcodes
                 INNER JOIN ag_kit USING (ag_kit_id)
                 WHERE supplied_kit_id = %s"""
        results = self._sql.execute_fetchall(sql, [kitid])
        return [row[0] for row in results]

    def checkPrintResults(self, kit_id):
        sql = "SELECT print_results FROM ag_handout_kits WHERE kit_id = %s"
        results = self._sql.execute_fetchone(sql, [kit_id])
        if results is None:
            return None
        else:
            return results[0].strip()

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

#################################################
### GENERAL DATA ACCESS  #######################
################################################
# not sure where these should end up

    def get_survey_id(self, ag_login_id, participant_name):
        """Return the survey ID associated with a participant or None"""
        sql = """select survey_id
                 from ag_login_surveys
                 where ag_login_id=%s and participant_name=%s"""
        cursor = self.get_cursor()
        cursor.execute(sql, [ag_login_id, participant_name])
        id_ = cursor.fetchone()

        return id_[0] if id_ else None
