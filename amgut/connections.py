# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Project Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
#
# This module handles lazy-loading the various connections needed. This
# simplifies code that relies on amgut (like scripts/ag) but that does not need
# connections to the database since it handles them itself.


class _LazyAgData(object):
    def __init__(self):
        self._ag_data_access = None

    def __getattr__(self, name):
        if not self._ag_data_access:
            from amgut.lib.data_access.ag_data_access import AGDataAccess

            print 'Connecting to postgres for amgut.connections.ag_data'

            self._ag_data_access = AGDataAccess()

        return getattr(self._ag_data_access, name)


class _LazyRedis(object):
    def __init__(self):
        self._redis = None

    def __getattr__(self, name):
        if not self._redis:
            print 'Connecting to redis for amgut.connections.redis'

            from amgut.lib.config_manager import AMGUT_CONFIG
            from redis import Redis

            self._redis = Redis(host=AMGUT_CONFIG.redis_host,
                                port=AMGUT_CONFIG.redis_port,
                                db=AMGUT_CONFIG.redis_db_id)

        return getattr(self._redis, name)


ag_data = _LazyAgData()
redis = _LazyRedis()

__all__ = ['ag_data', 'redis']
