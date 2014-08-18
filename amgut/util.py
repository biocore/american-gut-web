# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Project Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from amgut.lib.data_access.data_access_connections import data_access_factory
from amgut.lib.enums import ServerConfig, DataAccessType

__all__ = ['DATA_ACCESS', 'AG_DATA_ACCESS']

PORTAL_TYPE = 'americangut'

# Data Access
DATA_ACCESS = data_access_factory(ServerConfig.data_access_type)
AG_DATA_ACCESS = data_access_factory(ServerConfig.data_access_type,
                                     'american_gut')