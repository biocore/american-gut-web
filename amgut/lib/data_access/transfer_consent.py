#!/usr/bin/env python

import binascii
import os

from amgut import db_conn


def iter_old_surveys():
    sql = """select * from ag_human_survey"""

    with db_conn.get_postgres_cursor() as cur:
        cur.execute(sql)
        columns = [x[0] for x in cur.description]

        rows = [dict(zip(columns, row)) for row in cur.fetchall()]

    return iter(rows)


def check_consent_and_survey(ag_login_id, pname):
    consent_sql = """select exists(select * from ag_consent
                     where ag_login_id = %s and participant_name = %s)"""
    survey_sql = """select exists(select * from ag_login_surveys
                    where ag_login_id = %s and participant_name = %s)"""
    
    consent = db_conn.execute_fetchone(consent_sql, (ag_login_id, pname))[0]
    survey = db_conn.execute_fetchone(survey_sql, (ag_login_id, pname))[0]

    if consent:
        raise Exception("%s consent already exists")
    if survey:
        raise Exception("%s already has a survey")


def mod_row_for_consent_table(row):
    juvenile = row.pop('juvenile_age')
    if juvenile is None:
        row['is_juvenile'] = False
    else:
        row['is_juvenile'] = True

    deceased_parent = row.pop('deceased_parent')
    if deceased_parent is None:
        row['deceased_parent'] = False
    else:
        row['deceased_parent'] = True

    return row


if __name__ == '__main__':
    for row in iter_old_surveys():
        check_consent_and_survey(row['ag_login_id'], row['participant_name'])
        # If we get here, then this participant indeed does not yet exist (as
        # expected)

        ag_login_id = row.pop('ag_login_id')
        participant_name = row.pop('participant_name')

        ##################################################################
        # insert row into ag_consent
        ##################################################################
        row = mod_row_for_consent_table(row)
        consent_sql = """insert into ag_consent
                         (ag_login_id, participant_name, participant_email,
                         is_juvenile, parent_1_name, parent_2_name,
                         deceased_parent)
                    VALUES
                        (%s, %s, %s, %s, %s, %s, %s)"""

        consent_args = (ag_login_id, participant_name,
            row['participant_email'], row['is_juvenile'],
            row['parent_1_name'], row['parent_2_name'],
            row['deceased_parent'])

        ##################################################################
        # insert row into ag_login_surveys
        ##################################################################
        new_survey_id = binascii.hexlify(os.urandom(8))
        survey_sql = """insert into ag_login_surveys
                            (ag_login_id, survey_id, participant_name)
                        VALUES
                            (%s, %s, %s)"""

        survey_args = (ag_login_id, new_survey_id, participant_name)
        
        with db_conn.get_postgres_cursor() as cur:
            cur.execute(consent_sql, consent_args)
            cur.execute(survey_sql, survey_args)
