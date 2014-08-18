# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Project Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from amgut.lib.data_access.data_access_connections import data_access_factory
from enums import ServerConfig, DataAccessType
import os
from enums import FieldGrouping
from qiime.parse import parse_mapping_file

portal_type = 'americangut'

# Data Access
DATA_ACCESS = data_access_factory(ServerConfig.data_access_type)
AG_DATA_ACCESS = data_access_factory(ServerConfig.data_access_type,
                                     'american_gut')
