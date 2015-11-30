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

import logging
from uuid import UUID

import psycopg2
from passlib.hash import bcrypt

from amgut.lib.data_access.sql_connection import TRN


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

    #####################################
    # Users
    #####################################

    def authenticateWebAppUser(self, username, password):
        """ Attempts to validate authenticate the supplied username/password

        Attempt to authenticate the user against the list of users in
        web_app_user table. If successful, a dict with user innformation is
        returned. If not, the function returns False.
        """
        with TRN:
            sql = """SELECT  cast(ag_login_id as varchar(100)) as ag_login_id,
                      email, name, address, city,
                      state, zip, country,kit_password
                    FROM ag_login
                INNER JOIN ag_kit USING (ag_login_id)
                WHERE supplied_kit_id = %s"""
            TRN.add(sql, [username])
            row = TRN.execute_fetchindex()
            if not row:
                return False

            results = dict(row[0])

            if not bcrypt.verify(password, results['kit_password']):
                return False
            results['ag_login_id'] = str(results['ag_login_id'])

            return results

    def check_login_exists(self, email):
        """Checks if email for login already exists on system

        Parameters
        ----------
        email : str
            Email for user to check

        Returns
        -------
        ag_login_id or None
            If exists, returns ag_login_id, else returns None
        """
        with TRN:
            clean_email = email.strip().lower()
            sql = "SELECT ag_login_id FROM ag_login WHERE LOWER(email) = %s"
            TRN.add(sql, [clean_email])
            value = TRN.execute_fetchindex()
            if value:
                value = value[0][0]
            return None if value == [] else value

    def addAGLogin(self, email, name, address, city, state, zip_, country):
        """Adds a new login or returns the login_id if email already exists

        Parameters
        ----------
        email : str
            Email to register for user
        name : str
            Name to register for user
        address : str
            Street address to register for user
        city : str
            City to register for user
        state : str
            State to register for user
        zip_ : str
            Postal code to register for user
        country : str
            Country to register for user

        Returns
        -------
        ag_login_id : str
            UUID for new user, or existing user if email already in system
        """
        with TRN:
            clean_email = email.strip().lower()
            ag_login_id = self.check_login_exists(email)
            if not ag_login_id:
                # create the login
                sql = """INSERT INTO ag_login
                         (email, name, address, city, state, zip, country)
                         VALUES (%s, %s, %s, %s, %s, %s, %s)
                         RETURNING ag_login_id"""
                TRN.add(sql, [clean_email, name, address, city, state, zip_,
                              country])
                ag_login_id = TRN.execute_fetchlast()
            return ag_login_id

    def getAGBarcodeDetails(self, barcode):
        """Returns information about the barcode from both AG and standard info

        Parameters
        ----------
        barcode : str
            Barcode to get information for

        Returns
        -------
        dict
            All barcode info, keyed to column name

        Raises
        ------
        ValueError
            Barcode not found in AG information tables
        """
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

        with TRN:
            TRN.add(sql, [barcode])
            row = TRN.execute_fetchindex()
            if not row:
                raise ValueError('Barcode does not exist in AG: %s' % barcode)
            return dict(row[0])

    def getAGKitDetails(self, supplied_kit_id):
        sql = """SELECT cast(ag_kit_id as varchar(100)),
                    supplied_kit_id, kit_password, swabs_per_kit, kit_verified,
                    kit_verification_code, verification_email_sent
                 FROM ag_kit
                 WHERE supplied_kit_id = %s"""

        with TRN:
            TRN.add(sql, [supplied_kit_id])
            row = TRN.execute_fetchindex()
            if not row:
                raise ValueError('Supplied kit id does not exist in AG: %s' %
                                 supplied_kit_id)
            return dict(row[0])

    def registerHandoutKit(self, ag_login_id, supplied_kit_id):
        """Registeres a handout kit to a user

        Parameters
        ----------
        ag_login_id : str
            UUID4 formatted string of login ID to associate with kit
        supplied_kit_id : str
            kit ID for the handout kit

        Returns
        -------
        bool
            True:  success
            False: insert failed due to IntegrityError

        Raises
        ------
        ValueError
            Non-UUID4 value sent as ag_login_id
        """
        with TRN:
            # make sure properly formatted UUID passed in
            UUID(ag_login_id, version=4)

            printresults = self.checkPrintResults(supplied_kit_id)
            # make sure login_id and skid exists
            sql = """SELECT EXISTS(SELECT *
                                   FROM ag.ag_login
                                   WHERE ag_login_id = %s)"""
            TRN.add(sql, [ag_login_id])
            exists = TRN.execute_fetchlast()
            if not exists:
                return False
            sql = """SELECT EXISTS(SELECT *
                                   FROM ag.ag_handout_kits
                                   WHERE kit_id = %s)"""
            TRN.add(sql, [supplied_kit_id])
            if not TRN.execute_fetchlast():
                return False

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
                        SELECT barcode
                        FROM ag_handout_barcodes
                        WHERE kit_id = %s
                    LOOP
                        INSERT  INTO ag_kit_barcodes
                            (ag_kit_id, barcode, sample_barcode_file)
                            VALUES (k_id, bc, bc || '.jpg');
                    END LOOP;
                    DELETE FROM ag_handout_barcodes WHERE kit_id = %s;
                    DELETE FROM ag_handout_kits WHERE kit_id = %s;
                END $do$;
                """.format(ag_login_id, printresults)
            TRN.add(sql, [supplied_kit_id] * 4)
            try:
                TRN.execute()
            except psycopg2.IntegrityError:
                logging.exception('Error on skid %s:' % ag_login_id)
                return False
            return True

    def get_all_handout_kits(self):
        with TRN:
            sql = 'SELECT kit_id FROM ag.ag_handout_kits'
            TRN.add(sql)
            return TRN.execute_fetchflatten()

    def deleteAGParticipantSurvey(self, ag_login_id, participant_name):
        # Remove user from new schema
        with TRN:
            sql = """SELECT survey_id
                     FROM ag_login_surveys
                     WHERE ag_login_id = %s AND participant_name = %s"""
            TRN.add(sql, (ag_login_id, participant_name))
            survey_id = TRN.execute_fetchlast()

            sql = "DELETE FROM survey_answers WHERE survey_id = %s"
            TRN.add(sql, [survey_id])

            sql = "DELETE FROM survey_answers_other WHERE survey_id = %s"
            TRN.add(sql, [survey_id])

            # Reset survey attached to barcode(s)
            sql = """UPDATE ag_kit_barcodes
                     SET survey_id = NULL
                     WHERE survey_id = %s"""
            TRN.add(sql, [survey_id])

            sql = "DELETE FROM promoted_survey_ids WHERE survey_id = %s"
            TRN.add(sql, [survey_id])

            # Delete last due to foreign keys
            sql = "DELETE FROM ag_login_surveys WHERE survey_id = %s"
            TRN.add(sql, [survey_id])

            sql = """DELETE FROM ag_consent
                     WHERE ag_login_id = %s AND participant_name = %s"""
            TRN.add(sql, [ag_login_id, participant_name])

    def getConsent(self, survey_id):
        with TRN:
            TRN.add("""SELECT agc.participant_name,
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
                           FROM ag_consent agc
                           JOIN ag_login_surveys agl
                           USING (ag_login_id, participant_name)
                           WHERE agl.survey_id = %s""", [survey_id])
            result = TRN.execute_fetchindex()
            if not result:
                raise ValueError("Survey ID does not exist in DB: %s" %
                                 survey_id)
            return dict(result[0])

    def logParticipantSample(self, ag_login_id, barcode, sample_site,
                             environment_sampled, sample_date, sample_time,
                             participant_name, notes):
        with TRN:
            if sample_site is not None:
                # Get survey id
                sql = """SELECT survey_id
                         FROM ag_login_surveys
                         WHERE ag_login_id = %s AND participant_name = %s"""

                TRN.add(sql, (ag_login_id, participant_name))
                survey_id = TRN.execute_fetchindex()
                if not survey_id:
                    raise ValueError("No survey ID for ag_login_id %s and "
                                     "participant name %s" %
                                     (ag_login_id, participant_name))
                survey_id = survey_id[0][0]
            else:
                # otherwise, it is an environmental sample
                survey_id = None

            # Add barcode info
            sql = """UPDATE ag_kit_barcodes
                     SET site_sampled = %s, environment_sampled = %s,
                         sample_date = %s, sample_time = %s,
                         participant_name = %s, notes = %s, survey_id = %s
                     WHERE barcode = %s"""
            TRN.add(sql, [sample_site, environment_sampled, sample_date,
                          sample_time, participant_name, notes, survey_id,
                          barcode])

    def deleteSample(self, barcode, ag_login_id):
        """
        Strictly speaking the ag_login_id isn't needed but it makes it really
        hard to hack the function when you would need to know someone else's
        login id (a GUID) to delete something maliciously
        """
        with TRN:
            sql = """UPDATE ag_kit_barcodes
                     SET participant_name = NULL, site_sampled = NULL,
                         sample_time = NULL, sample_date = NULL,
                         environment_sampled = NULL, notes = ''
                    WHERE barcode IN (
                        SELECT  akb.barcode
                        FROM ag_kit_barcodes akb
                        INNER JOIN ag_kit ak USING (ag_kit_id)
                        WHERE ak.ag_login_id = %s and akb.barcode = %s)"""
            TRN.add(sql, [ag_login_id, barcode])
            sql = "UPDATE barcode SET status = NULL WHERE barcode = %s"
            TRN.add(sql, [barcode])

    def getHumanParticipants(self, ag_login_id):
        # get people from new survey setup
        sql = """SELECT participant_name from ag.ag_login_surveys
                 JOIN ag.survey_answers USING (survey_id)
                 JOIN ag.group_questions gq USING (survey_question_id)
                 JOIN ag.surveys ags USING (survey_group)
                 WHERE ag_login_id = %s AND ags.survey_id = %s"""
        with TRN:
            TRN.add(sql, [ag_login_id, 1])
            return TRN.execute_fetchflatten()

    def updateVioscreenStatus(self, survey_id, status):
        with TRN:
            sql = """UPDATE ag_login_surveys
                     SET vioscreen_status = %s
                     WHERE  survey_id = %s"""
            TRN.add(sql, (status, survey_id))

    def get_vioscreen_status(self, survey_id):
        """Retrieves the vioscreen status for a survey_id

        Parameters
        ----------
        survey_id : str
            The survey to get status for

        Returns
        -------
        int
            Vioscreen status

        Raises
        ------
        ValueError
            survey_id passed is not in the database
        """
        with TRN:
            sql = """SELECT vioscreen_status
                     FROM ag.ag_login_surveys
                     WHERE survey_id = %s"""
            TRN.add(sql, [survey_id])
            status = TRN.execute_fetchindex()
            if not status:
                raise ValueError("Survey ID %s not in database" % survey_id)
            return status[0][0]

    def getAnimalParticipants(self, ag_login_id):
        sql = """SELECT participant_name from ag.ag_login_surveys
                 JOIN ag.survey_answers USING (survey_id)
                 JOIN ag.group_questions gq USING (survey_question_id)
                 JOIN ag.surveys ags USING (survey_group)
                 WHERE ag_login_id = %s AND ags.survey_id = %s"""
        with TRN:
            TRN.add(sql, [ag_login_id, 2])
            return TRN.execute_fetchflatten()

    def getParticipantSamples(self, ag_login_id, participant_name):
        sql = """SELECT  barcode, site_sampled, sample_date, sample_time,
                    notes, status
                 FROM ag_kit_barcodes akb
                 INNER JOIN barcode USING (barcode)
                 INNER JOIN ag_kit ak USING (ag_kit_id)
                 WHERE (site_sampled IS NOT NULL AND site_sampled::text <> '')
                 AND ag_login_id = %s AND participant_name = %s"""
        with TRN:
            TRN.add(sql, [ag_login_id, participant_name])
            rows = TRN.execute_fetchindex()
            return [dict(row) for row in rows]

    def getEnvironmentalSamples(self, ag_login_id):
        sql = """SELECT  barcode, site_sampled, sample_date, sample_time,
                    notes, status
                 FROM ag_kit_barcodes
                 INNER JOIN barcode USING (barcode)
                 INNER JOIN ag_kit USING(ag_kit_id)
                 WHERE (environment_sampled IS NOT NULL AND
                    environment_sampled::text <> '')
                    AND ag_login_id = %s"""
        with TRN:
            TRN.add(sql, [ag_login_id])
            rows = TRN.execute_fetchindex()
            return [dict(row) for row in rows]

    def getAvailableBarcodes(self, ag_login_id):
        sql = """SELECT barcode
                 FROM ag_kit_barcodes
                 INNER JOIN ag_kit USING (ag_kit_id)
                 WHERE coalesce(sample_date::text, '') = ''
                 AND kit_verified = 'y' AND ag_login_id = %s"""
        with TRN:
            TRN.add(sql, [ag_login_id])
            return TRN.execute_fetchflatten()

    def verifyKit(self, supplied_kit_id):
        """Set the KIT_VERIFIED for the supplied_kit_id to 'y'"""
        sql = """UPDATE AG_KIT
                 SET kit_verified='y'
                 WHERE supplied_kit_id=%s"""
        with TRN:
            TRN.add(sql, [supplied_kit_id])

    def _get_unverified_kits(self):
        """Gets list of unverified kit IDs, Helper function for tests"""
        sql = """SELECT supplied_kit_id
                 FROM AG_KIT
                 WHERE NOT kit_verified = 'y'"""
        with TRN:
            TRN.add(sql)
            return TRN.execute_fetchflatten()

    def getMapMarkers(self):
        with TRN:
            sql = """SELECT country, count(country)::integer
            FROM ag.ag_login GROUP BY country"""
            TRN.add(sql)
            return dict(TRN.execute_fetchindex())

    def handoutCheck(self, username, password):
        with TRN:
            sql = "SELECT password FROM ag.ag_handout_kits WHERE kit_id = %s"
            TRN.add(sql, [username])
            to_check = TRN.execute_fetchindex()

            if not to_check:
                return False
            else:
                return bcrypt.verify(password, to_check[0][0])

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
        with TRN:
            ag_login_id = self.get_user_for_kit(supplied_kit_id)
            sql = """SELECT EXISTS (
                        SELECT barcode
                        FROM ag.ag_kit
                        JOIN ag.ag_kit_barcodes USING (ag_kit_id)
                      WHERE ag_login_id = %s AND barcode = %s)"""
            TRN.add(sql, [ag_login_id, barcode])
            return TRN.execute_fetchlast()

    def getAGKitIDsByEmail(self, email):
        """Returns a list of kitids based on email

        email is email address of login
        returns a list of kit_id's associated with the email or an empty list
        """
        with TRN:
            sql = """SELECT  supplied_kit_id
                     FROM ag_kit
                     INNER JOIN ag_login USING (ag_login_id)
                     WHERE email = %s"""
            TRN.add(sql, [email.lower()])
            return TRN.execute_fetchflatten()

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
        with TRN:
            TRN.add(sql, [pass_code, kitid, email])

    def ag_update_kit_password(self, kit_id, password):
        """updates ag_kit table with password

        kit_id is supplied_kit_id in the ag_kit table
        password is the new password
        """
        with TRN:
            password = bcrypt.encrypt(password)
            sql = """UPDATE AG_KIT
                     SET kit_password = %s, pass_reset_code = NULL
                     WHERE supplied_kit_id = %s"""
            TRN.add(sql, [password, kit_id])

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
        with TRN:
            TRN.add(sql, [passcode, email, kitid])
            return TRN.execute_fetchlast()

    def getBarcodesByKit(self, kitid):
        """Returns a list of barcodes in a kit

        kitid is the supplied_kit_id from the ag_kit table
        """
        sql = """SELECT barcode
                 FROM ag_kit_barcodes
                 INNER JOIN ag_kit USING (ag_kit_id)
                 WHERE supplied_kit_id = %s"""
        with TRN:
            TRN.add(sql, [kitid])
            return TRN.execute_fetchflatten()

    def checkPrintResults(self, kit_id):
        """Checks whether or not results are available for a given `kit_id`

        Parameters
        ----------
        kit_id : str
            The supplied kit identifier to check for results availability.

        Returns
        -------
        bool
            Whether or not the results are ready for the supplied kit_id.

        Notes
        -----
        If a `kit_id` does not exist this function will return False, as no
        results would be available for a non-existent `kit_id`.
        """
        with TRN:
            sql = "SELECT print_results FROM ag_handout_kits WHERE kit_id = %s"
            TRN.add(sql, [kit_id])
            results = TRN.execute_fetchindex()
            return False if not results else results[0][0]

    def get_user_for_kit(self, supplied_kit_id):
        with TRN:
            sql = """SELECT ag_login_id
                     FROM ag.ag_kit
                     JOIN ag_login USING (ag_login_id)
                     WHERE supplied_kit_id = %s"""
            TRN.add(sql, [supplied_kit_id])
            results = TRN.execute_fetchindex()
            if results:
                return results[0][0]
            else:
                raise ValueError("No user ID for kit %s" % supplied_kit_id)

    def get_menu_items(self, supplied_kit_id):
        """Returns information required to populate the menu of the website"""
        with TRN:
            ag_login_id = self.get_user_for_kit(supplied_kit_id)
            info = self.getAGKitDetails(supplied_kit_id)

            kit_verified = False
            if info['kit_verified'] == 'y':
                kit_verified = True

            human_samples = {hs: self.getParticipantSamples(ag_login_id, hs)
                             for hs in self.getHumanParticipants(ag_login_id)}
            animal_samples = {a: self.getParticipantSamples(ag_login_id, a)
                              for a in self.getAnimalParticipants(ag_login_id)}
            environmental_samples = self.getEnvironmentalSamples(ag_login_id)

            return (human_samples, animal_samples, environmental_samples,
                    kit_verified)

    def check_if_consent_exists(self, ag_login_id, participant_name):
        """Return True if a consent already exists"""
        with TRN:
            sql = """SELECT EXISTS(
                        SELECT 1
                        FROM ag_consent
                        WHERE ag_login_id = %s AND participant_name = %s)"""
            TRN.add(sql, [ag_login_id, participant_name])
            return TRN.execute_fetchlast()

    def get_user_info(self, supplied_kit_id):
        with TRN:
            sql = """SELECT CAST(ag_login_id AS VARCHAR(100)) AS ag_login_id,
                            email, name, address, city, state, zip, country
                     FROM ag_login
                     INNER JOIN ag_kit USING(ag_login_id)
                     WHERE supplied_kit_id = %s"""
            TRN.add(sql, [supplied_kit_id])
            row = TRN.execute_fetchindex()
            if not row:
                raise ValueError('Supplied kit id is not in DB: %s' %
                                 supplied_kit_id)
            user_data = dict(row[0])
            user_data['ag_login_id'] = str(user_data['ag_login_id'])
            return user_data

    def get_barcode_results(self, supplied_kit_id):
        """Get the results associated with the login ID of the kit

        Parameters
        ----------
        supplied_kit_id : str
            The user's supplied kit ID

        Returns
        -------
        list of dict
            A list of the dict of the barcode to participant name associated
            with the login ID where results are ready.
        """
        with TRN:
            ag_login_id = self.get_user_for_kit(supplied_kit_id)
            sql = """SELECT barcode, participant_name
                     FROM ag_kit_barcodes
                     INNER JOIN ag_kit USING (ag_kit_id)
                     WHERE ag_login_id = %s AND results_ready = 'Y'"""

            TRN.add(sql, [ag_login_id])
            return [dict(row) for row in TRN.execute_fetchindex()]

    def get_login_info(self, ag_login_id):
        """Get kit registration information

        Parameters
        ----------
        ag_login_id : str
            A valid login ID, that should be a test as a valid UUID

        Returns
        -------
        list of dict
            A list of registration information associated with a common login
            ID.

        Raises
        ------
        ValueError
            Unknown ag_login_id passed
        """
        with TRN:
            sql = """SELECT ag_login_id, email, name, address, city, state,
                            zip, country
                     FROM ag_login
                     WHERE ag_login_id = %s"""
            TRN.add(sql, [ag_login_id])
            info = TRN.execute_fetchindex()
            if not info:
                raise ValueError('ag_login_id not in database: %s' %
                                 ag_login_id)
            return [dict(row) for row in info]

    def get_survey_id(self, ag_login_id, participant_name):
        """Return the survey ID associated with a participant or None

        Parameters
        ----------
        ag_login_id : str
            A valid login ID, that should be a test as a valid UUID
        participant_name : str
            A participant name

        Returns
        -------
        str or None
            The survey ID, or None if a survey ID cannot be found.

        Raises
        ------
        ValueError
            Unknown ag_login_id or participant_name passed
        """
        with TRN:
            sql = """SELECT survey_id
                     FROM ag_login_surveys
                     WHERE ag_login_id=%s AND participant_name=%s"""
            TRN.add(sql, [ag_login_id, participant_name])
            survey_id = TRN.execute_fetchindex()
            if not survey_id:
                raise ValueError("No survey ID found!")
            return survey_id[0][0]

    def get_countries(self):
        """
        Returns
        -------
        list of str
         All country names in database"""
        with TRN:
            sql = 'SELECT country FROM ag.iso_country_lookup ORDER BY country'
            TRN.add(sql)
            return TRN.execute_fetchflatten()
