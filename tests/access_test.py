# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 19:47:47 2015

@author: Robert Smith
"""

import os
import unittest
from db_utils.access import Access


class Access_Test(unittest.TestCase):

    def setUp(self):
        self.test_db_path = os.path.normpath("C:/test.accdb")
        self.test_sql_query_1 = "SELECT 1;"
        self.test_create_table_1 = "CREATE TABLE TEST_01(ID CHAR(1));"
        self.test_create_table_insert_query = "INSERT INTO TEST_01(ID) VALUES (?);"
        self.test_create_table_count_query = "SELECT COUNT(*) FROM TEST_01;"
        self.test_create_table_value_query = "SELECT ID FROM TEST_01 ORDER BY ID;"
        self.test_create_table_insert_value = ("Z", )
        self.test_create_table_insert_many_values = [("A",), ("B",), ("C",), ("D",), ("E",), ("F",), ("G",)]
        if os.path.isfile(self.test_db_path):
            os.remove(self.test_db_path)
        self.test_db = Access.create_accdb(path=self.test_db_path)
        self.test_db.execute(self.test_create_table_1).commit()

    def tearDown(self):
        self.test_db.close()
        if os.path.isfile(self.test_db_path):
            os.remove(self.test_db_path)
        self.test_db = None

    def test_accdb_create_file_exists(self):
        self.assertTrue(os.path.isfile(self.test_db_path))

    def test_accdb_create_is_instance(self):
        self.assertIsInstance(self.test_db, Access)

    def test_accdb_create_dbq_equal(self):
        self.assertEqual(os.path.normcase(self.test_db.dbq), os.path.normcase(self.test_db_path))

    def test_db_execute_sql_query(self):
        expected_outcome = (1,)
        test_outcome = tuple([val for val in self.test_db.execute(self.test_sql_query_1)][0])
        self.assertEqual(test_outcome, expected_outcome)

    def test_db_execute_sql_create_table(self):
        expected_cnt_qry = 0
        test_cnt_qry = [val for val in self.test_db.execute(self.test_create_table_count_query)][0][0]
        self.assertEqual(expected_cnt_qry, test_cnt_qry)

    def test_db_execute_sql_insert_table_value(self):
        expected_cnt_qry = len(self.test_create_table_insert_value)
        self.test_db.execute(self.test_create_table_insert_query, self.test_create_table_insert_value)
        test_cnt_qry = [val for val in self.test_db.execute(self.test_create_table_count_query)][0][0]
        self.assertEqual(expected_cnt_qry, test_cnt_qry)
        output_values = tuple(tuple(val for val in self.test_db.execute(self.test_create_table_value_query))[0])
        self.assertEqual(self.test_create_table_insert_value, output_values)

    def test_db_execute_sql_insert_many_table_value(self):
        expected_cnt_qry = len(self.test_create_table_insert_many_values)
        self.test_db.executemany(self.test_create_table_insert_query, self.test_create_table_insert_many_values)
        test_cnt_qry = [val for val in self.test_db.execute(self.test_create_table_count_query)][0][0]
        self.assertEqual(expected_cnt_qry, test_cnt_qry)
        output_values = list(tuple(v for v in val) for val in self.test_db.execute(self.test_create_table_value_query))
        self.assertEqual(self.test_create_table_insert_many_values, output_values)


if __name__ == "__main__":
    unittest.main()
