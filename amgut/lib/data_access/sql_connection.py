# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import division
from contextlib import contextmanager
from itertools import chain
from tempfile import mktemp

from psycopg2 import connect, ProgrammingError, Error as PostgresError
from psycopg2.extras import DictCursor
from psycopg2.extensions import (
    ISOLATION_LEVEL_AUTOCOMMIT, ISOLATION_LEVEL_READ_COMMITTED)

from amgut.lib.config_manager import AMGUT_CONFIG


def flatten(listOfLists):
    # https://docs.python.org/2/library/itertools.html
    return chain.from_iterable(listOfLists)


class SQLConnectionHandler(object):
    """Encapsulates the DB connection with the Postgres DB

    Parameters
    ----------
    admin : {'no_admin', 'no_database', 'database'}, optional
        Whether or not to connect as the admin user. Options other than
        `no_admin` depend on admin credentials in the qiita configuration. If
        'admin_without_database', the connection will be made to the server
        specified in the qiita configuration, but not to a specific database.
        If 'admin_with_database', then a connection will be made to the server
        and database specified in the qiita config.
    """
    def __init__(self, con=None, admin='no_admin'):
        if admin not in ('no_admin', 'admin_with_database',
                         'admin_without_database'):
            raise RuntimeError("admin takes only {'no_admin', "
                               "'admin_with_database', or "
                               "'admin_without_database'}")

        self.admin = admin
        if not con:
            self._open_connection()
        else:
            self._connection = con
        # queues for transaction blocks. Format is {str: list} where the str
        # is the queue name and the list is the queue of SQL commands
        self.queues = {}

    def __del__(self):
        # make sure if connection close fails it doesn't raise error
        # should only error if connection already closed
        try:
            self._connection.close()
        except:
            pass

    def _open_connection(self):
        # connection string arguments for a normal user
        args = {
            'user': AMGUT_CONFIG.user,
            'password': AMGUT_CONFIG.password,
            'database': AMGUT_CONFIG.database,
            'host': AMGUT_CONFIG.host,
            'port': AMGUT_CONFIG.port}

        # if this is an admin user, use the admin credentials
        if self.admin != 'no_admin':
            args['user'] = AMGUT_CONFIG.admin_user
            args['password'] = AMGUT_CONFIG.admin_password

        # Do not connect to a particular database unless requested
        if self.admin == 'admin_without_database':
            del args['database']

        try:
            self._connection = connect(**args)
            self.execute('set search_path to ag, public')
        except Exception as e:
            # catch any exception and raise as runtime error
            raise RuntimeError("Cannot connect to database: %s" % str(e))

    @contextmanager
    def get_postgres_cursor(self):
        """ Returns a Postgres cursor

        Returns
        -------
        pgcursor : psycopg2.cursor

        Raises a RuntimeError if the cursor cannot be created
        """
        if self._connection.closed:
            # Currently defaults to non-admin connection
            self._open_connection()

        try:
            with self._connection.cursor(cursor_factory=DictCursor) as cur:
                yield cur
        except PostgresError as e:
            raise RuntimeError("Cannot get postgres cursor! %s" % e)

    def set_autocommit(self, on_or_off):
        """Sets the isolation level to autocommit or default (read committed)

        Parameters
        ----------
        on_or_off : {'on', 'off'}
            If 'on', isolation level will be set to autocommit. Otherwise,
            it will be set to read committed.
        """
        if on_or_off not in {'on', 'off'}:
            raise ValueError("set_autocommit takes only 'on' or 'off'")

        if on_or_off == 'on':
            level = ISOLATION_LEVEL_AUTOCOMMIT
        else:
            level = ISOLATION_LEVEL_READ_COMMITTED

        self._connection.set_isolation_level(level)

    def _check_sql_args(self, sql_args):
        """ Checks that sql_args have the correct type

        Inputs:
            sql_args : SQL arguments

        Raises a TypeError if sql_args does not have the correct type,
            otherwise it just returns the execution to the caller
        """
        # Check that sql arguments have the correct type
        if sql_args and type(sql_args) not in [tuple, list, dict]:
            raise TypeError("sql_args should be tuple, list or dict. Found %s "
                            % type(sql_args))

    @contextmanager
    def _sql_executor(self, sql, sql_args=None, many=False):
        """Executes an SQL query

        Parameters
        ----------
        sql : str
            The SQL query
        sql_args : tuple or list, optional
            The arguments for the SQL query
        many : bool, optional
            If true, performs an execute many call

        Returns
        -------
        pgcursor : psycopg2.cursor
            The cursor in which the SQL query was executed

        Raises
        ------
        ValueError
            If there is some error executing the SQL query
        """
        # Check that sql arguments have the correct type
        if many:
            for args in sql_args:
                self._check_sql_args(args)
        else:
            self._check_sql_args(sql_args)

        # Execute the query
        with self.get_postgres_cursor() as cur:
            try:
                if many:
                    cur.executemany(sql, sql_args)
                else:
                    cur.execute(sql, sql_args)
                yield cur
                self._connection.commit()
            except PostgresError as e:
                self._connection.rollback()
                raise ValueError(("\nError running SQL query: %s"
                                             "\nARGS: %s"
                                             "\nError: %s" %
                                             (sql, str(sql_args), e)))

    def _rollback_raise_error(self, queue, sql, sql_args, e):
        self._connection.rollback()
        # wipe out queue since it has an error in it
        del self.queues[queue]
        raise ValueError(
            ("\nError running SQL query in queue %s: %s"
             "\nARGS: %s\nError: %s" % (queue, sql,
                                        str(sql_args), e)))

    def execute_queue(self, queue):
        """Executes all sql in a queue in a single transaction block

        Parameters
        ----------
        queue : str
            Name of queue to execute

        Notes
        -----
        Does not support executemany command. Instead, enter the multiple
        SQL commands as multiple entries in the queue.

        Queues are executed in FIFO order
        """
        with self.get_postgres_cursor() as cur:
            results = []
            clear_res = False
            for sql, sql_args in self.queues[queue]:
                if sql_args is not None:
                    for pos, arg in enumerate(sql_args):
                        # check if previous results needed and replace
                        if isinstance(arg, str) and \
                                arg[0] == "{" and arg[-1] == "}":
                            result_pos = int(arg[1:-1])
                            sql_args[pos] = results[result_pos]
                            clear_res = True
                # wipe out results if needed and reset clear_res
                if clear_res:
                    results = []
                    clear_res = False
                # Fire off the SQL command
                try:
                    cur.execute(sql, sql_args)
                except Exception as e:
                    self._rollback_raise_error(queue, sql, sql_args, e)

                # fetch results if available and append to results list
                try:
                    res = cur.fetchall()
                except ProgrammingError as e:
                    # ignore error if nothing to fetch
                    pass
                except Exception as e:
                    self._rollback_raise_error(queue, sql, sql_args, e)
                else:
                    # append all results linearly
                    results.extend(flatten(res))
        self._connection.commit()
        # wipe out queue since finished
        del self.queues[queue]
        return results

    def list_queues(self):
        """Returns list of all queue names currently in handler

        Returns
        -------
        list
            names of queues in handler
        """
        return self.queues.keys()

    def create_queue(self, queue_name):
        """Add a new queue to the connection

        Parameters
        ----------
        queue_name : str
            Name of the new queue

        Raises
        ------
        KeyError
            Queue name already exists
        """
        if queue_name in self.queues:
            raise KeyError("Queue already contains %s" % queue_name)

        self.queues[queue_name] = []

    def add_to_queue(self, queue, sql, sql_args=None, many=False):
        """Add an sql command to the end of a queue

        Parameters
        ----------
        queue : str
            name of queue adding to
        sql : str
            sql command to run
        sql_args : list or tuple, optional
            the arguments to fill sql command with
        many : bool, optional
            Whether or not this should be treated as an executemany command.
            Default False

        Raises
        ------
        KeyError
            queue does not exist

        Notes
        -----
        Queues are executed in FIFO order
        """
        if many:
            for args in sql_args:
                self._check_sql_args(args)
                self.queues[queue].append((sql, args))
        else:
            self._check_sql_args(sql_args)
            self.queues[queue].append((sql, sql_args))

    def execute_fetchall(self, sql, sql_args=None):
        """ Executes a fetchall SQL query

        Parameters
        ----------
        sql : str
            The SQL query
        sql_args : tuple or list, optional
            The arguments for the SQL query

        Returns
        ------
        list of tuples
            The results of the fetchall query

        Raises
        ------
        ValueError
            If there is some error executing the SQL query

        Note: from psycopg2 documentation, only variable values should be bound
            via sql_args, it shouldn't be used to set table or field names. For
            those elements, ordinary string formatting should be used before
            running execute.
        """
        with self._sql_executor(sql, sql_args) as pgcursor:
            result = pgcursor.fetchall()
        return result

    def execute_fetchone(self, sql, sql_args=None):
        """ Executes a fetchone SQL query

        Parameters
        ----------
        sql : str
            The SQL query
        sql_args : tuple or list, optional
            The arguments for the SQL query

        Returns
        -------
        Tuple
            The results of the fetchone query

        Raises
        ------
        ValueError
            if there is some error executing the SQL query

        Note: from psycopg2 documentation, only variable values should be bound
            via sql_args, it shouldn't be used to set table or field names. For
            those elements, ordinary string formatting should be used before
            running execute.
        """
        with self._sql_executor(sql, sql_args) as pgcursor:
            result = pgcursor.fetchone()
        return result

    def execute(self, sql, sql_args=None):
        """ Executes an SQL query with no results

        Parameters
        ----------
        sql : str
            The SQL query
        sql_args : tuple or list, optional
            The arguments for the SQL query

        Raises
        ------
        ValueError
            if there is some error executing the SQL query

        Note: from psycopg2 documentation, only variable values should be bound
            via sql_args, it shouldn't be used to set table or field names. For
            those elements, ordinary string formatting should be used before
            running execute.
        """
        with self._sql_executor(sql, sql_args):
            pass

    def executemany(self, sql, sql_args_list):
        """ Executes an executemany SQL query with no results

        Parameters
        ----------
        sql : str
            The SQL query
        sql_args : list of tuples
            The arguments for the SQL query

        Raises
        ------
        ValueError
            If there is some error executing the SQL query

        Note: from psycopg2 documentation, only variable values should be bound
            via sql_args, it shouldn't be used to set table or field names. For
            those elements, ordinary string formatting should be used before
            running execute.
        """
        with self._sql_executor(sql, sql_args_list, True):
            pass

    def get_temp_queue(self):
        """Get a queue name that did not exist when this function was called

        Returns
        -------
        str
            The name of the queue
        """
        temp_queue_name = mktemp()
        while temp_queue_name in self.queues:
            temp_queue_name = mktemp()

        self.create_queue(temp_queue_name)

        return temp_queue_name

    def execute_proc_return_cursor(self, procname, proc_args):
        """Executes a stored procedure and returns a cursor

        Parameters
        ----------
        procname: str
            the name of the stored procedure
        proc_args: list
            arguments sent to the stored procedure
        """
        proc_args.append('cur2')
        if self._connection.closed:
            self._open_connection()
        cur = self._connection.cursor()

        try:
            cur.callproc(procname, proc_args)
        except Exception as e:
            # catch any error from the database and raise for site to catch
            self._connection.rollback()
            raise RuntimeError("Failed to execute stored procedure !\n%s" %
                               str(e))
        else:
            return self._connection.cursor('cur2')
        finally:
            cur.close()
