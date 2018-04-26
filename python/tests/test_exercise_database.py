#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright (c) 2017 Jesse Pinnell
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""" Test cases for classes in exercise_database.py """
# This is the same set of tests in test_exercise_postgres_database

import unittest
import getpass
from xrsrv import exercise_database
from xrsrv import type_factories

TEST_SQLITE_DATABASE_NAME = "exercise.db"
TEST_POSTGRES_DATABASE_NAME = "xrsrv"
TEST_POSTGRES_USER = getpass.getuser()

class TestExerciseDatabase(object):
    """
    Test the exercise database methods

    TODO(jessepinnell) refactor or make these more robust tests
    """
    # This is due to the subclassing
    # pylint: disable=no-member
    def __init__(self):
        super(TestExerciseDatabase, self).setUp()

    def test_instantiation(self):
        """ Test the creation of the connection to the database """
        pass

    def test_get_list_of_exercise_names(self):
        """ Test the get_list_of_exercise_names() method """
        self.assertNotEqual(self.database.get_list_of_exercise_names(), False)

    def test_get_muscle_data(self):
        """ Test the get_muscle_data() method """
        pass

    def test_get_exercise_data(self):
        """ Test the get_muscles_exercised() method """
        exercises = self.database.get_list_of_exercise_names()
        self.assertNotEqual(exercises, False)
        self.assertIsInstance(self.database.get_exercise_data(exercises[0]),\
            type_factories.Exercise)


class TestSQLiteExcerciseDatabase(unittest.TestCase, TestExerciseDatabase):
    """
    Test the exercise database methods

    TODO(jessepinnell) refactor or make these more robust tests
    """

    def __init__(self, *args, **kwargs):
        super(TestSQLiteExcerciseDatabase, self).__init__(*args, **kwargs)
        self.database = exercise_database.SQLiteConnection(TEST_SQLITE_DATABASE_NAME)

    def test_instantiation(self):
        """ Test the creation of the connection to the database """
        self.assertIsInstance(self.database, exercise_database.SQLiteConnection)

class TestPostgresExerciseDatabase(unittest.TestCase, TestExerciseDatabase):
    """
    Test the exercise database methods

    TODO(jessepinnell) refactor or make these more robust tests
    """
    def __init__(self, *args, **kwargs):
        super(TestPostgresExerciseDatabase, self).__init__(*args, **kwargs)
        self.database = exercise_database.PostgresConnection(TEST_POSTGRES_DATABASE_NAME, TEST_POSTGRES_USER)

    def test_instantiation(self):
        """ Test the creation of the connection to the database """
        self.assertIsInstance(self.database, exercise_database.PostgresConnection)


if __name__ == '__main__':
    unittest.main()
