# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Project Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

import sys


class _LazyLoadedConnections(object):
    """
    This class takes the place of the module and handles lazy-loading the
    various connections needed. This simplifies code that relies on amgut
    (like scripts/ag) but that does not need connections to the database since
    it handles them itself.
    """
    def __init__(self):
        self._ag_data_access = None
        self._redis = None

    @property
    def ag_data(self):
        if not self._ag_data_access:
            from amgut.lib.data_access.ag_data_access import AGDataAccess

            print 'Connecting to postgres for ag_data'

            self._ag_data_access = AGDataAccess()

        return self._ag_data_access

    @property
    def redis(self):
        if not self._redis:
            print 'Connecting to redis for redis'

            from amgut.lib.config_manager import AMGUT_CONFIG
            from redis import Redis

            self._redis = Redis(host=AMGUT_CONFIG.redis_host,
                                port=AMGUT_CONFIG.redis_port,
                                db=AMGUT_CONFIG.redis_db_id)

        return self._redis

sys.modules[__name__] = _LazyLoadedConnections()
