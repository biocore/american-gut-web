# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Project Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from amgut.lib.data_access.ag_data_access import AGDataAccess

__all__ = ['AG_DATA_ACCESS']

PORTAL_TYPE = 'americangut'

# Data Access
AG_DATA_ACCESS = AGDataAccess()