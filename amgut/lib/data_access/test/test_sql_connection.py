from unittest import TestCase, main
from os import remove, close
from os.path import exists
from tempfile import mkstemp

from psycopg2._psycopg import connection
from psycopg2 import connect
from psycopg2.extensions import TRANSACTION_STATUS_IDLE

from amgut.lib.data_access.sql_connection import Transaction, TRN
from amgut.lib.config_manager import AMGUT_CONFIG


DB_TEST_TABLE = """CREATE TABLE ag.test_table (
    str_column      varchar DEFAULT 'foo' NOT NULL,
    bool_column     bool DEFAULT True NOT NULL,
    int_column      bigint NOT NULL);"""


class TestBase(TestCase):
    def setUp(self):
        # Add the test table to the database, so we can use it in the tests
        with connect(user=AMGUT_CONFIG.user, password=AMGUT_CONFIG.password,
                     host=AMGUT_CONFIG.host, port=AMGUT_CONFIG.port,
                     database=AMGUT_CONFIG.database) as con:
            with con.cursor() as cur:
                cur.execute(DB_TEST_TABLE)
        self._files_to_remove = []

    def tearDown(self):
        for fp in self._files_to_remove:
            if exists(fp):
                remove(fp)
        with connect(user=AMGUT_CONFIG.user, password=AMGUT_CONFIG.password,
                     host=AMGUT_CONFIG.host, port=AMGUT_CONFIG.port,
                     database=AMGUT_CONFIG.database) as con:
            with con.cursor() as cur:
                cur.execute('DROP TABLE ag.test_table')

    def _populate_test_table(self):
        """Aux function that populates the test table"""
        sql = """INSERT INTO ag.test_table
                    (str_column, bool_column, int_column)
                 VALUES (%s, %s, %s)"""
        sql_args = [('test1', True, 1), ('test2', True, 2),
                    ('test3', False, 3), ('test4', False, 4)]
        with connect(user=AMGUT_CONFIG.user, password=AMGUT_CONFIG.password,
                     host=AMGUT_CONFIG.host, port=AMGUT_CONFIG.port,
                     database=AMGUT_CONFIG.database) as con:
            with con.cursor() as cur:
                cur.executemany(sql, sql_args)
            con.commit()

    def _assert_sql_equal(self, exp):
        """Aux function for testing"""
        with connect(user=AMGUT_CONFIG.user, password=AMGUT_CONFIG.password,
                     host=AMGUT_CONFIG.host, port=AMGUT_CONFIG.port,
                     database=AMGUT_CONFIG.database) as con:
            with con.cursor() as cur:
                cur.execute("SELECT * FROM ag.test_table")
                obs = cur.fetchall()
            con.commit()

        self.assertEqual(obs, exp)


class TestTransaction(TestBase):
    def test_init(self):
        obs = Transaction()
        self.assertEqual(obs._queries, [])
        self.assertEqual(obs._results, [])
        self.assertEqual(obs._connection, None)
        self.assertEqual(obs._contexts_entered, 0)
        with obs:
            pass
        self.assertTrue(isinstance(obs._connection, connection))

    def test_add(self):
        with TRN:
            self.assertEqual(TRN._queries, [])

            sql1 = "INSERT INTO ag.test_table (bool_column) VALUES (%s)"
            args1 = [True]
            TRN.add(sql1, args1)
            sql2 = "INSERT INTO ag.test_table (int_column) VALUES (1)"
            TRN.add(sql2)
            args3 = (False,)
            TRN.add(sql1, args3)
            sql3 = "INSERT INTO ag.test_table (int_column) VALEUS (%(foo)s)"
            args4 = {'foo': 1}
            TRN.add(sql3, args4)

            exp = [(sql1, args1), (sql2, None), (sql1, args3), (sql3, args4)]
            self.assertEqual(TRN._queries, exp)

            # Remove queries so __exit__ doesn't try to execute it
            TRN._queries = []

    def test_add_many(self):
        with TRN:
            self.assertEqual(TRN._queries, [])

            sql = "INSERT INTO ag.test_table (int_column) VALUES (%s)"
            args = [[1], [2], [3]]
            TRN.add(sql, args, many=True)

            exp = [(sql, [1]), (sql, [2]), (sql, [3])]
            self.assertEqual(TRN._queries, exp)

    def test_add_error(self):
        with TRN:
            with self.assertRaises(TypeError):
                TRN.add("SELECT 42", 1)

            with self.assertRaises(TypeError):
                TRN.add("SELECT 42", {'foo': 'bar'}, many=True)

            with self.assertRaises(TypeError):
                TRN.add("SELECT 42", [1, 1], many=True)

    def test_execute(self):
        with TRN:
            sql = """INSERT INTO ag.test_table (str_column, int_column)
                     VALUES (%s, %s)"""
            TRN.add(sql, ["test_insert", 2])
            sql = """UPDATE ag.test_table
                     SET int_column = %s, bool_column = %s
                     WHERE str_column = %s"""
            TRN.add(sql, [20, False, "test_insert"])
            obs = TRN.execute()
            self.assertEqual(obs, [None, None])
            self._assert_sql_equal([])

        self._assert_sql_equal([("test_insert", False, 20)])

    def test_execute_many(self):
        with TRN:
            sql = """INSERT INTO ag.test_table (str_column, int_column)
                     VALUES (%s, %s)"""
            args = [['insert1', 1], ['insert2', 2], ['insert3', 3]]
            TRN.add(sql, args, many=True)
            sql = """UPDATE ag.test_table
                     SET int_column = %s, bool_column = %s
                     WHERE str_column = %s"""
            TRN.add(sql, [20, False, 'insert2'])
            obs = TRN.execute()
            self.assertEqual(obs, [None, None, None, None])

            self._assert_sql_equal([])

        self._assert_sql_equal([('insert1', True, 1),
                                ('insert3', True, 3),
                                ('insert2', False, 20)])

    def test_execute_return(self):
        with TRN:
            sql = """INSERT INTO ag.test_table (str_column, int_column)
                     VALUES (%s, %s) RETURNING str_column, int_column"""
            TRN.add(sql, ['test_insert', 2])
            sql = """UPDATE ag.test_table SET bool_column = %s
                     WHERE str_column = %s RETURNING int_column"""
            TRN.add(sql, [False, 'test_insert'])
            obs = TRN.execute()
            self.assertEqual(obs, [[['test_insert', 2]], [[2]]])

    def test_execute_return_many(self):
        with TRN:
            sql = """INSERT INTO ag.test_table (str_column, int_column)
                     VALUES (%s, %s) RETURNING str_column, int_column"""
            args = [['insert1', 1], ['insert2', 2], ['insert3', 3]]
            TRN.add(sql, args, many=True)
            sql = """UPDATE ag.test_table SET bool_column = %s
                     WHERE str_column = %s"""
            TRN.add(sql, [False, 'insert2'])
            sql = "SELECT * FROM ag.test_table"
            TRN.add(sql)
            obs = TRN.execute()
            exp = [[['insert1', 1]],  # First query of the many query
                   [['insert2', 2]],  # Second query of the many query
                   [['insert3', 3]],  # Third query of the many query
                   None,  # Update query
                   [['insert1', True, 1],  # First result select
                    ['insert3', True, 3],  # Second result select
                    ['insert2', False, 2]]]  # Third result select
            self.assertEqual(obs, exp)

    def test_execute_huge_transaction(self):
        with TRN:
            # Add a lot of inserts to the transaction
            sql = "INSERT INTO ag.test_table (int_column) VALUES (%s)"
            for i in range(1000):
                TRN.add(sql, [i])
            # Add some updates to the transaction
            sql = """UPDATE ag.test_table SET bool_column = %s
                     WHERE int_column = %s"""
            for i in range(500):
                TRN.add(sql, [False, i])
            # Make the transaction fail with the last insert
            sql = """INSERT INTO ag.table_to_make (the_trans_to_fail)
                     VALUES (1)"""
            TRN.add(sql)

            with self.assertRaises(ValueError):
                TRN.execute()

            # make sure rollback correctly
            self._assert_sql_equal([])

    def test_execute_commit_false(self):
        with TRN:
            sql = """INSERT INTO ag.test_table (str_column, int_column)
                     VALUES (%s, %s) RETURNING str_column, int_column"""
            args = [['insert1', 1], ['insert2', 2], ['insert3', 3]]
            TRN.add(sql, args, many=True)

            obs = TRN.execute()
            exp = [[['insert1', 1]], [['insert2', 2]], [['insert3', 3]]]
            self.assertEqual(obs, exp)

            self._assert_sql_equal([])

            TRN.commit()

            self._assert_sql_equal([('insert1', True, 1), ('insert2', True, 2),
                                    ('insert3', True, 3)])

    def test_execute_commit_false_rollback(self):
        with TRN:
            sql = """INSERT INTO ag.test_table (str_column, int_column)
                     VALUES (%s, %s) RETURNING str_column, int_column"""
            args = [['insert1', 1], ['insert2', 2], ['insert3', 3]]
            TRN.add(sql, args, many=True)

            obs = TRN.execute()
            exp = [[['insert1', 1]], [['insert2', 2]], [['insert3', 3]]]
            self.assertEqual(obs, exp)

            self._assert_sql_equal([])

            TRN.rollback()

            self._assert_sql_equal([])

    def test_execute_commit_false_wipe_queries(self):
        with TRN:
            sql = """INSERT INTO ag.test_table (str_column, int_column)
                     VALUES (%s, %s) RETURNING str_column, int_column"""
            args = [['insert1', 1], ['insert2', 2], ['insert3', 3]]
            TRN.add(sql, args, many=True)

            obs = TRN.execute()
            exp = [[['insert1', 1]], [['insert2', 2]], [['insert3', 3]]]
            self.assertEqual(obs, exp)

            self._assert_sql_equal([])

            sql = """UPDATE ag.test_table SET bool_column = %s
                     WHERE str_column = %s"""
            args = [False, 'insert2']
            TRN.add(sql, args)
            self.assertEqual(TRN._queries, [(sql, args)])

            TRN.execute()
            self._assert_sql_equal([])

        self._assert_sql_equal([('insert1', True, 1), ('insert3', True, 3),
                                ('insert2', False, 2)])

    def test_execute_fetchlast(self):
        with TRN:
            sql = """INSERT INTO ag.test_table (str_column, int_column)
                     VALUES (%s, %s) RETURNING str_column, int_column"""
            args = [['insert1', 1], ['insert2', 2], ['insert3', 3]]
            TRN.add(sql, args, many=True)

            sql = """SELECT EXISTS(
                        SELECT * FROM ag.test_table WHERE int_column=%s)"""
            TRN.add(sql, [2])
            self.assertTrue(TRN.execute_fetchlast())

    def test_execute_fetchindex(self):
        with TRN:
            sql = """INSERT INTO ag.test_table (str_column, int_column)
                     VALUES (%s, %s) RETURNING str_column, int_column"""
            args = [['insert1', 1], ['insert2', 2], ['insert3', 3]]
            TRN.add(sql, args, many=True)
            self.assertEqual(TRN.execute_fetchindex(), [['insert3', 3]])

            sql = """INSERT INTO ag.test_table (str_column, int_column)
                     VALUES (%s, %s) RETURNING str_column, int_column"""
            args = [['insert4', 4], ['insert5', 5], ['insert6', 6]]
            TRN.add(sql, args, many=True)
            self.assertEqual(TRN.execute_fetchindex(3), [['insert4', 4]])

    def test_execute_fetchflatten(self):
        with TRN:
            sql = """INSERT INTO ag.test_table (str_column, int_column)
                     VALUES (%s, %s)"""
            args = [['insert1', 1], ['insert2', 2], ['insert3', 3]]
            TRN.add(sql, args, many=True)

            sql = "SELECT str_column, int_column FROM ag.test_table"
            TRN.add(sql)

            sql = "SELECT int_column FROM ag.test_table"
            TRN.add(sql)
            obs = TRN.execute_fetchflatten()
            self.assertEqual(obs, [1, 2, 3])

            sql = "SELECT 42"
            TRN.add(sql)
            obs = TRN.execute_fetchflatten(idx=3)
            self.assertEqual(obs, ['insert1', 1, 'insert2', 2, 'insert3', 3])

    def test_context_manager_rollback(self):
        try:
            with TRN:
                sql = """INSERT INTO ag.test_table (str_column, int_column)
                     VALUES (%s, %s) RETURNING str_column, int_column"""
                args = [['insert1', 1], ['insert2', 2], ['insert3', 3]]
                TRN.add(sql, args, many=True)

                TRN.execute()
                raise ValueError("Force exiting the context manager")
        except ValueError:
            pass
        self._assert_sql_equal([])
        self.assertEqual(
            TRN._connection.get_transaction_status(),
            TRANSACTION_STATUS_IDLE)

    def test_context_manager_execute(self):
        with TRN:
            sql = """INSERT INTO ag.test_table (str_column, int_column)
                 VALUES (%s, %s) RETURNING str_column, int_column"""
            args = [['insert1', 1], ['insert2', 2], ['insert3', 3]]
            TRN.add(sql, args, many=True)
            self._assert_sql_equal([])

        self._assert_sql_equal([('insert1', True, 1), ('insert2', True, 2),
                                ('insert3', True, 3)])
        self.assertEqual(
            TRN._connection.get_transaction_status(),
            TRANSACTION_STATUS_IDLE)

    def test_context_manager_no_commit(self):
        with TRN:
            sql = """INSERT INTO ag.test_table (str_column, int_column)
                 VALUES (%s, %s) RETURNING str_column, int_column"""
            args = [['insert1', 1], ['insert2', 2], ['insert3', 3]]
            TRN.add(sql, args, many=True)

            TRN.execute()
            self._assert_sql_equal([])

        self._assert_sql_equal([('insert1', True, 1), ('insert2', True, 2),
                                ('insert3', True, 3)])
        self.assertEqual(
            TRN._connection.get_transaction_status(),
            TRANSACTION_STATUS_IDLE)

    def test_context_manager_multiple(self):
        self.assertEqual(TRN._contexts_entered, 0)

        with TRN:
            self.assertEqual(TRN._contexts_entered, 1)

            TRN.add("SELECT 42")
            with TRN:
                self.assertEqual(TRN._contexts_entered, 2)
                sql = """INSERT INTO ag.test_table (str_column, int_column)
                         VALUES (%s, %s) RETURNING str_column, int_column"""
                args = [['insert1', 1], ['insert2', 2], ['insert3', 3]]
                TRN.add(sql, args, many=True)

            # We exited the second context, nothing should have been executed
            self.assertEqual(TRN._contexts_entered, 1)
            self.assertEqual(
                TRN._connection.get_transaction_status(),
                TRANSACTION_STATUS_IDLE)
            self._assert_sql_equal([])

        # We have exited the first context, everything should have been
        # executed and committed
        self.assertEqual(TRN._contexts_entered, 0)
        self._assert_sql_equal([('insert1', True, 1), ('insert2', True, 2),
                                ('insert3', True, 3)])
        self.assertEqual(
            TRN._connection.get_transaction_status(),
            TRANSACTION_STATUS_IDLE)

    def test_context_manager_multiple_2(self):
        self.assertEqual(TRN._contexts_entered, 0)

        def tester():
            self.assertEqual(TRN._contexts_entered, 1)
            with TRN:
                self.assertEqual(TRN._contexts_entered, 2)
                sql = """SELECT EXISTS(
                        SELECT * FROM ag.test_table WHERE int_column=%s)"""
                TRN.add(sql, [2])
                self.assertTrue(TRN.execute_fetchlast())
            self.assertEqual(TRN._contexts_entered, 1)

        with TRN:
            self.assertEqual(TRN._contexts_entered, 1)
            sql = """INSERT INTO ag.test_table (str_column, int_column)
                         VALUES (%s, %s) RETURNING str_column, int_column"""
            args = [['insert1', 1], ['insert2', 2], ['insert3', 3]]
            TRN.add(sql, args, many=True)
            tester()
            self.assertEqual(TRN._contexts_entered, 1)
            self._assert_sql_equal([])

        self.assertEqual(TRN._contexts_entered, 0)
        self._assert_sql_equal([('insert1', True, 1), ('insert2', True, 2),
                                ('insert3', True, 3)])
        self.assertEqual(
            TRN._connection.get_transaction_status(),
            TRANSACTION_STATUS_IDLE)

    def test_post_commit_funcs(self):
        fd, fp = mkstemp()
        close(fd)
        self._files_to_remove.append(fp)

        def func(fp):
            with open(fp, 'w') as f:
                f.write('\n')

        with TRN:
            TRN.add("SELECT 42")
            TRN.add_post_commit_func(func, fp)

        self.assertTrue(exists(fp))

    def test_post_commit_funcs_error(self):
        def func():
            raise ValueError()

        with self.assertRaises(RuntimeError):
            with TRN:
                TRN.add("SELECT 42")
                TRN.add_post_commit_func(func)

    def test_post_rollback_funcs(self):
        fd, fp = mkstemp()
        close(fd)
        self._files_to_remove.append(fp)

        def func(fp):
            with open(fp, 'w') as f:
                f.write('\n')

        with TRN:
            TRN.add("SELECT 42")
            TRN.add_post_rollback_func(func, fp)
            TRN.rollback()

        self.assertTrue(exists(fp))

    def test_post_rollback_funcs_error(self):
        def func():
            raise ValueError()

        with self.assertRaises(RuntimeError):
            with TRN:
                TRN.add("SELECT 42")
                TRN.add_post_rollback_func(func)
                TRN.rollback()

    def test_context_manager_checker(self):
        with self.assertRaises(RuntimeError):
            TRN.add("SELECT 42")

        with self.assertRaises(RuntimeError):
            TRN.execute()

        with self.assertRaises(RuntimeError):
            TRN.commit()

        with self.assertRaises(RuntimeError):
            TRN.rollback()

        with TRN:
            TRN.add("SELECT 42")

        with self.assertRaises(RuntimeError):
            TRN.execute()

    def test_index(self):
        with TRN:
            self.assertEqual(TRN.index, 0)

            TRN.add("SELECT 42")
            self.assertEqual(TRN.index, 1)

            sql = "INSERT INTO ag.test_table (int_column) VALUES (%s)"
            args = [[1], [2], [3]]
            TRN.add(sql, args, many=True)
            self.assertEqual(TRN.index, 4)

            TRN.execute()
            self.assertEqual(TRN.index, 4)

            TRN.add(sql, args, many=True)
            self.assertEqual(TRN.index, 7)

        self.assertEqual(TRN.index, 0)


if __name__ == "__main__":
    main()
