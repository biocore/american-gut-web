from amgut.lib.data_access.sql_connection import SQLConnectionHandler
from os import listdir
from os.path import join, dirname, abspath

def startup_tests():
    """Wrapper function for calling all tests needed before startup"""
    patch_number()
    barcodes_correct()

def patch_number():
    # Make sure the system is using the latest patch before starting up.
    conn_handler = SQLConnectionHandler()
    system = conn_handler.execute_fetchone("SELECT current_patch FROM ag.settings")[0]
    patches_dir = join(dirname(abspath(__file__)), '../db/patches')
    latest = sorted(listdir(patches_dir)).pop()
    if latest != system:
        raise EnvironmentError("Not running latest patch! System: %s Latest: %s" %
                               (system, latest))

def barcodes_correct():
    # For patch 0011 & 0012
    # Needed because barcodes are added as last barcode in system + 1
    # and system testing was using these larger barcodes. Now use 0-1000 range
    conn_handler = SQLConnectionHandler()
    sql = "SELECT barcode FROM barcodes.barcode WHERE barcode::integer >= 800000000"
    bcs = conn_handler.execute_fetchall(sql)
    if bcs:
        raise EnvironmentError("Invalid barcodes found: %s" % ", ".join([x[0] for x in bcs]))
