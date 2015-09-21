from os.path import abspath, basename, dirname, join, split, splitext
from glob import glob
from functools import partial
from subprocess import Popen, PIPE
import gzip

from click import echo
from psycopg2 import (connect, OperationalError, ProgrammingError)
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from natsort import natsorted

from amgut.lib.config_manager import AMGUT_CONFIG
from amgut.lib.data_access.sql_connection import SQLConnectionHandler

get_db_file = partial(join, join(dirname(dirname(abspath(__file__))), '..', 'db'))
LAYOUT_FP = get_db_file('ag_unpatched.sql')
INITIALIZE_FP = get_db_file('initialize.sql')
POPULATE_FP = get_db_file('ag_test_patch22.sql.gz')
PATCHES_DIR = get_db_file('patches')


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


def create_database(force=False):
    # Connect to the postgres server
    try:
        conn = connect(dbname='postgres',
                       user=AMGUT_CONFIG.user, password=AMGUT_CONFIG.password,
                       host=AMGUT_CONFIG.host, port=AMGUT_CONFIG.port)
    except OperationalError as e:
        raise OperationalError("Cannot connect to the server, error is %s" %
                               str(e))

    # Set the isolation level to AUTOCOMMIT so we can execute a create database
    # sql query
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # Get the cursor
    cur = conn.cursor()
    db_exists = _check_db_exists(AMGUT_CONFIG.database, cur)

    # Check that the database does not already exist
    if db_exists and force:
        return
    elif db_exists:
        raise ValueError("Database '{}' already present on the system"
                         .format(AMGUT_CONFIG.database))

    # Create the database
    cur.execute('CREATE DATABASE %s' % AMGUT_CONFIG.database)
    cur.close()
    conn.close()

def build(verbose=False):
    conn = connect(user=AMGUT_CONFIG.user, password=AMGUT_CONFIG.password,
                   host=AMGUT_CONFIG.host, port=AMGUT_CONFIG.port,
                   database=AMGUT_CONFIG.database)
    cur = conn.cursor()

    # create the schema and set a search path
    cur.execute('CREATE SCHEMA IF NOT EXISTS ag')
    cur.execute('CREATE SCHEMA IF NOT EXISTS barcodes')
    cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    if verbose:
        echo("Building SQL layout")

    with open(LAYOUT_FP) as f:
        # We have to skip the "create schema" line here
        cur.execute('\n'.join(f.readlines()[1:]))

    cur.execute('SET SEARCH_PATH TO ag, barcodes, public')
    with open(INITIALIZE_FP) as f:
        cur.execute(f.read())
    conn.commit()

def initialize(verbose=False):
    """Initialize the database with permissions and, optionally, a new user

    Parameters
    ----------
    verbose : bool, optional
        Show messages while working, default False
    """
    conn = connect(user=AMGUT_CONFIG.user, password=AMGUT_CONFIG.password,
                   host=AMGUT_CONFIG.host, port=AMGUT_CONFIG.port,
                   database=AMGUT_CONFIG.database)
    cur = conn.cursor()

    if verbose:
        echo('Granting privileges')

    cur.execute('GRANT USAGE ON schema public, ag, barcodes TO %s' % AMGUT_CONFIG.user)
    cur.execute('GRANT CONNECT ON DATABASE %s TO %s' %
                (AMGUT_CONFIG.database, AMGUT_CONFIG.user))
    cur.execute('GRANT INSERT, UPDATE, DELETE, SELECT ON ALL TABLES IN SCHEMA'
                ' public, ag, barcodes TO %s;' % AMGUT_CONFIG.user)
    cur.execute('GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public, ag, barcodes '
                'TO %s;' % AMGUT_CONFIG.user)
    conn.commit()



def make_settings_table():
    conn = SQLConnectionHandler()
    settings = AMGUT_CONFIG.get_settings()

    columns = [' '.join([setting[0], 'varchar']) for setting in settings]
    column_names = [setting[0] for setting in settings]

    num_values = len(settings)
    sql = "INSERT INTO settings ({}) VALUES ({})".format(
        ', '.join(column_names), ', '.join(['%s'] * num_values))
    args = [str(setting[1]) for setting in settings]

    with conn.get_postgres_cursor() as cur:
        create_sql = ("CREATE TABLE ag.settings ({}, current_patch varchar "
                      "NOT NULL DEFAULT 'unpatched')")

        create_sql = create_sql.format(', '.join(columns))

        cur.execute(create_sql)
        cur.execute(sql, args)


def populate_test_db():
    with gzip.open(POPULATE_FP, 'rb') as f:
        test_db = f.read()

    command = ['psql', '-d', AMGUT_CONFIG.database]
    proc = Popen(command, stdin=PIPE, stdout=PIPE)
    proc.communicate(test_db)


def patch_db(patches_dir=PATCHES_DIR, verbose=False):
    """Patches the database schema based on the settings table

    Pulls the current patch from the settings table and applies all subsequent
    patches found in the patches directory.
    """
    conn = SQLConnectionHandler()

    current_patch = conn.execute_fetchone(
        "SELECT current_patch FROM settings")[0]
    current_patch_fp = join(patches_dir, current_patch)

    sql_glob = join(patches_dir, '*.sql')
    patch_files = natsorted(glob(sql_glob))

    if current_patch == 'unpatched':
        next_patch_index = 0
    elif current_patch_fp not in patch_files:
        raise RuntimeError("Cannot find patch file %s" % current_patch)
    else:
        next_patch_index = patch_files.index(current_patch_fp) + 1

    patch_update_sql = "UPDATE settings SET current_patch = %s"

    for patch_fp in patch_files[next_patch_index:]:
        patch_filename = split(patch_fp)[-1]
        with conn.get_postgres_cursor() as cur:
            cur.execute('SET SEARCH_PATH TO ag, barcodes, public')

            with open(patch_fp, 'U') as patch_file:
                if verbose:
                    echo('\tApplying patch %s...' % patch_filename)

                cur.execute(patch_file.read())
                cur.execute(patch_update_sql, [patch_filename])

        conn._connection.commit()

    # Idempotent patches implemented in Python can be run here


def rebuild_test(verbose=False):
    conn = connect(user=AMGUT_CONFIG.user, password=AMGUT_CONFIG.password,
                   host=AMGUT_CONFIG.host, port=AMGUT_CONFIG.port,
                   database=AMGUT_CONFIG.database)
    with conn.cursor() as cur:
        test = cur.execute("SELECT test_environment FROM ag.settings")
        test = cur.fetchone()[0]
        if test != 'true':
            print "ABORTING: Not working on test database"
            return
    conn.close()

    if verbose:
        print "Dropping database %s" % AMGUT_CONFIG.database

    p = Popen(['dropdb', '--if-exists', AMGUT_CONFIG.database])
    retcode = p.wait()

    if retcode != 0:
        raise RuntimeError("Could not delete database %s: retcode %d" %
                           (AMGUT_CONFIG.database, retcode))

    if verbose:
        print "Rebuilding database"
    create_database()
    populate_test_db()
    initialize(verbose)
    if verbose:
        print "Patching database"
    patch_db(verbose=verbose)
