#!/usr/bin/env python

# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from os import listdir
from os.path import abspath, join, dirname

from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import click

from amgut.lib.config_manager import AMGUT_CONFIG
from amgut.lib.util import LAYOUT_FP, INITIALIZE_FP, POPULATE_FP


def _check_db_exists(db, cursor):
    r"""Check if the database db exists on the postgres server

    Parameters
    ----------
    db : str
        The database name
    cursor : psycopg2.cursor
        The cursor connected to the server
    """
    cursor.execute('SELECT datname FROM pg_database')
    # It's a list of tuple, so just create the tuple to check if exists
    return (db,) in cursor.fetchall()


@click.command()
def create_test_db():
    r"""Creates the american gut test database"""
    if not AMGUT_CONFIG.test_environment:
        raise ValueError("The configuration file in use is not set up for a "
                         "test environment")

    # Connect to the postgres server
    conn = connect(user=AMGUT_CONFIG.user, password=AMGUT_CONFIG.password,
                   host=AMGUT_CONFIG.host, port=AMGUT_CONFIG.port)
    # Set the isolation level to AUTOCOMMIT so we can execute a create database
    # sql query
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    # Get the cursor
    cur = conn.cursor()
    # Check that the database does not already exists
    if _check_db_exists(AMGUT_CONFIG.database, cur):
        raise ValueError("Database '%s' already present on the system"
                         % AMGUT_CONFIG.database)
    # Create the database
    print("Creating database")
    cur.execute('CREATE DATABASE %s' % AMGUT_CONFIG.database)
    cur.close()
    conn.close()

    # Connect to the postgres server, but this time to the just created db
    conn = connect(user=AMGUT_CONFIG.user, password=AMGUT_CONFIG.password,
                   host=AMGUT_CONFIG.host, port=AMGUT_CONFIG.port,
                   database=AMGUT_CONFIG.database)
    cur = conn.cursor()

    print("Inserting procedures")
    procedures_dirpath = join(dirname(dirname(abspath(__file__))), "lib",
                              "data_access", "procedures")
    for procedure_f in listdir(procedures_dirpath):
        with open(join(procedures_dirpath, procedure_f)) as f:
            cur.execute(f.read())

    print("Building SQL layout")
    with open(LAYOUT_FP) as f:
        cur.execute(f.read())

    # The following lines are commented out because the initialize.sql and
    # populate_test.sql files are empty, so psycopg2 fails. Once this files
    # have data, those lines should be executed
    print("Initializing the test database")
    # with open(INITIALIZE_FP) as f:
    #     cur.execute(f.read)

    print("Initializing the test database")
    # with open(POPULATE_FP) as f:
    #     cur.execute(f.read)

    conn.commit()
    cur.close()
    conn.close()

    print("Test environment successfully created")

if __name__ == '__main__':
    create_test_db()
