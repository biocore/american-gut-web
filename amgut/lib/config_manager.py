# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from os.path import join, dirname, abspath, exists, isfile
from os import environ
from functools import partial
import warnings

from future import standard_library
with standard_library.hooks():
    from configparser import (ConfigParser, NoOptionError,
                              Error as ConfigParser_Error)


class MissingConfigSection(ConfigParser_Error):
    """Exception when the config file is missing a required section"""
    def __init__(self, section):
        super(MissingConfigSection, self).__init__('Missing section(s): %r' %
                                                   (section,))
        self.section = section
        self.args = (section,)


def _warn_on_extra(extra, set_type):
    extra = ', '.join(extra)
    if extra:
        warnings.warn("Extra %s found: %r" % (set_type, extra))


class ConfigurationManager(object):
    """Holds the configuration information

    Parameters
    ----------
    conf_fp: str, optional
        Filepath to the configuration file. Default: ag_config.txt

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
    goodpassword : str
        The correct password for the test account
    badpassword : str
        The password used for testing on the test account
    redis_host : str
        The host on which redis is running
    redis_port : int
        The port that redis is running on
    redis_db_id : int
        The ID of the redis database

    Raises
    ------
    IOError
        If the AG_CONFIG environment variable is set, but does not point to an
        existing file

    Notes
    -----
    - The environment variable AG_CONFIG is checked for a path to the config
      file. If the environment variable is not set, the default config file is
      used.
    """
    def __init__(self):
        conf_fp = environ.get('AG_CONFIG') or join(dirname(abspath(__file__)),
                                                   '../ag_config.txt')

        if not isfile(conf_fp):
            raise IOError("The configuration file '%s' is not an "
                          "existing file" % conf_fp)

        # Parse the configuration file
        config = ConfigParser()
        with open(conf_fp, 'U') as conf_file:
            config.readfp(conf_file)

        _expected_sections = {'main', 'postgres', 'test', 'redis'}

        missing = _expected_sections - set(config.sections())
        if missing:
            raise MissingConfigSection(', '.join(missing))
        extra = set(config.sections()) - _expected_sections
        _warn_on_extra(extra, 'sections')

        self._get_main(config)
        self._get_postgres(config)
        self._get_test(config)
        self._get_redis(config)

    def _get_main(self, config):
        """Get the configuration of the main section"""
        expected_options = {'name', 'shorthand', 'test_environment',
                            'base_data_dir', 'locale'}
        _warn_on_extra(set(config.options('main')) - expected_options,
                       'main section option(s)')

        get = partial(config.get, 'main')
        getboolean = partial(config.getboolean, 'main')

        self.project_name = get('NAME')
        self.project_shorthand = get('SHORTHAND')
        self.test_environment = getboolean('TEST_ENVIRONMENT')
        self.base_data_dir = get('BASE_DATA_DIR')
        self.locale = get('LOCALE')

        if not exists(self.base_data_dir):
            raise IOError("Directory %s does not exist!" % self.base_data_dir)

    def _get_postgres(self, config):
        """Get the configuration of the postgres section"""
        expected_options = {'user', 'password', 'database', 'host', 'port'}
        _warn_on_extra(set(config.options('postgres')) - expected_options,
                       'postgres section option(s)')

        get = partial(config.get, 'postgres')
        getint = partial(config.getint, 'postgres')

        self.user = get('USER')
        try:
            self.password = get('PASSWORD')
        except NoOptionError as e:
            if self.test_environment:
                self.password = None
            else:
                raise e
        self.database = get('DATABASE')
        self.host = get('HOST')
        self.port = getint('PORT')

    def _get_test(self, config):
        """Get the configuration of the test section"""
        expected_options = {'goodpassword', 'badpassword'}
        _warn_on_extra(set(config.options('test')) - expected_options,
                       'test section option(s)')

        get = partial(config.get, 'test')

        self.goodpassword = get('GOODPASSWORD')
        self.badpassword = get('BADPASSWORD')

    def _get_redis(self, config):
        """Get the configuration of the redis section"""
        expected_options = {'host', 'port', 'db_id'}
        _warn_on_extra(set(config.options('redis')) - expected_options,
                       'redis section option(s)')

        get = partial(config.get, 'redis')
        getint = partial(config.getint, 'redis')

        self.redis_host = get('HOST')
        self.redis_port = getint('PORT')
        self.redis_db_id = getint('DB_ID')


AMGUT_CONFIG = ConfigurationManager()
