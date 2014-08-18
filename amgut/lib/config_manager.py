# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from functools import partial
from os.path import join, dirname, abspath, exists
from os import environ
from future import standard_library
with standard_library.hooks():
    from configparser import (ConfigParser, NoOptionError,
                              MissingSectionHeaderError)


class ConfigurationManager(object):
    """Holds the configuration information

    Parameters
    ----------
    conf_fp: str, optional
        Filepath to the configuration file. Default: config_test.txt

    Attributes
    ----------
    test_environment : bool
        Whether we are in a test environment or not
    base_data_dir : str
        Path to the base directorys where all data file are stored
    user : str
        The postgres user
    password : str
        The postgres password for the previous user
    database : str
        The postgres database to connect to
    host : str
        The host where the database lives
    port : int
        The port used to connect to the postgres database in the previous host
    """
    def __init__(self):
        conf_fp = join(dirname(abspath(__file__)),
                       '../ag_config.txt')

        # Parse the configuration file
        config = ConfigParser()
        with open(conf_fp, 'U') as conf_file:
            config.readfp(conf_file)

        _expected_sections = {'main', 'postgres'}
        if set(config.sections()) != _expected_sections:
            missing = _expected_sections - set(config.sections())
            raise MissingSectionHeaderError("Missing: %r" % missing)

        self._get_main(config)
        self._get_postgres(config)

    def _get_main(self, config):
        """Get the configuration of the main section"""
        self.test_environment = config.getboolean('main', 'TEST_ENVIRONMENT')
        self.base_data_dir = config.get('main', 'BASE_DATA_DIR')
        if not exists(self.base_data_dir):
            raise IOError("Directory %s does not exist!" % self.base_data_dir)

    def _get_postgres(self, config):
        """Get the configuration of the postgres section"""
        self.user = config.get('postgres', 'USER')
        try:
            self.password = config.get('postgres', 'PASSWORD')
        except NoOptionError as e:
            if self.test_environment:
                self.password = None
            else:
                raise e
        self.database = config.get('postgres', 'DATABASE')
        self.host = config.get('postgres', 'HOST')
        self.port = config.getint('postgres', 'PORT')


AMGUT_CONFIG = ConfigurationManager()
