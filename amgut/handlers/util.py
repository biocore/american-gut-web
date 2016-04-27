from functools import wraps

from amgut.lib.data_access.sql_connection import TRN


def as_transaction(f):
    @wraps(f)
    def inner(*args, **kwargs):
        with TRN:
            return f(*args, **kwargs)
    return inner
