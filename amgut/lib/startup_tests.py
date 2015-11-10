from amgut.lib.data_access.sql_connection import TRN
from os import listdir
from os.path import join, dirname, abspath


def startup_tests():
    """Wrapper function for calling all tests needed before startup"""
    patch_number()
    barcodes_correct()


def patch_number():
    # Make sure the system is using the latest patch before starting up.
    with TRN:
        TRN.add('SELECT current_patch FROM ag.settings')
        system = TRN.execute_fetchlast()
        patches_dir = join(dirname(abspath(__file__)), '../db/patches')
        latest = sorted(listdir(patches_dir)).pop()
        if latest != system:
            raise EnvironmentError(("Not running latest patch. System: %s "
                                    "Latest: %s") % (system, latest))


def barcodes_correct():
    # For patch 0011 & 0012
    # Needed because barcodes are added as last barcode in system + 1
    # and system testing was using these larger barcodes. Now use 0-1000 range
    with TRN:
        sql = """SELECT barcode
                 FROM barcodes.barcode
                 WHERE barcode::integer >= 800000000"""
        TRN.add(sql)
        bcs = TRN.execute_fetchindex()
        if bcs:
            joined_bcs = ", ".join([x[0] for x in bcs])
            raise EnvironmentError("Invalid barcodes found: %s" % joined_bcs)
