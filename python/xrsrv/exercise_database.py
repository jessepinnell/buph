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

""" Abstraction of sqlite3 database """

from pathlib import Path

import sqlite3
import psycopg2
from xrsrv import type_factories

class SQLiteConnection(object):
    """
    Abstraction of a sqllite3 database

    This essentially acts as an object factory for the data structures,
    converting the data into the tables into more easily usable objects.
    """
    database_connection = None

    def __init__(self, database_name):
        # Because this will create a database if it doesn't find one,
        # explicitly check for one
        existing_db_file = Path(database_name)
        if not existing_db_file.exists():
            raise IOError("Database file doesn't exist: " + database_name)

        self.database_connection = sqlite3.connect(database_name)
        self.cursor = self.database_connection.cursor()


    def get_list_of_exercise_names(self):
        """
        Get a list of the exercises in the database
        """
        self.cursor.execute("SELECT Name FROM Exercises")
        exercise_names = [i[0] for i in self.cursor.fetchall()]
        return exercise_names


    def get_muscle_data(self, name):
        """
        Get the full set of data for a given muscle
        """
        return None

    def get_all_fixtures(self):
        """
        Get the full set of fixtures
        """
        return None

    def get_all_rigs(self):
        """
        Get the full set of rigs
        """
        return None

    def get_exercise_data(self, name):
        """
        Get the full set of data for a given exercise
        """
        # pylint: disable=no-member
        self.cursor.execute(\
            "SELECT FixtureName FROM ExerciseFixtures WHERE ExerciseName = ?", (name, ))
        fixtures = {i[0] for i in self.cursor.fetchall()}

        self.cursor.execute(\
            "SELECT RigName, Optional FROM ExerciseRigs WHERE ExerciseName = ?", (name, ))
        rigs = list(map(type_factories.ExerciseRig._make, self.cursor.fetchall()))

        self.cursor.execute(\
            "SELECT Muscle FROM MusclesExercised WHERE ExerciseName = ?", (name, ))
        muscles_exercised = [i[0] for i in self.cursor.fetchall()]

        self.cursor.execute(\
            "SELECT Key, Value FROM ExerciseInfo WHERE ExerciseName = ?", (name, ))
        info = {key: value for (key, value) in self.cursor.fetchall()}

        return type_factories.Exercise(name, fixtures, rigs, muscles_exercised, info)


    def __del__(self):
        if self.database_connection is not None:
            self.database_connection.close()

class PostgresConnection(object):
    """
    Abstraction of a postgres database

    This essentially acts as an object factory for the data structures,
    converting the data into the tables into more easily usable objects.
    """
    database_connection = None

    def __init__(self, database_name, user, host=None, password=None):
        if host is not None and password is not None:
            connection_string = f"dbname='{database_name}' user='{user}' host='{host}' password='{password}'"
        else:
            connection_string = f"dbname='{database_name}' user='{user}'"
        self.database_connection = psycopg2.connect(connection_string)
        self.cursor = self.database_connection.cursor()


    def get_list_of_exercise_names(self):
        """
        Get a list of the exercises in the database
        """
        self.cursor.execute("SELECT Name FROM Exercises")
        exercise_names = [i[0] for i in self.cursor.fetchall()]
        return exercise_names

    def get_all_fixtures(self):
        """
        Get the full set of fixtures
        """
        self.cursor.execute("SELECT Name FROM Fixtures")
        fixture_names = [i[0] for i in self.cursor.fetchall()]
        return fixture_names

    def get_all_rigs(self):
        """
        Get the full set of rigs
        """
        self.cursor.execute("SELECT Name FROM Rigs")
        rig_names = [i[0] for i in self.cursor.fetchall()]
        return rig_names

    def get_muscle_data(self, name):
        """
        Get the full set of data for a given muscle
        """
        # pylint: disable=no-member
        self.cursor.execute(\
            "SELECT MuscleGroup FROM Muscles WHERE Name = %s;", (name, ))
        group = self.cursor.fetchone()[0]

        self.cursor.execute(\
            "SELECT Key, Value FROM MuscleInfo WHERE MuscleName = %s;", (name, ))
        info = {key: value for (key, value) in self.cursor.fetchall()}

        self.cursor.execute(\
            "SELECT Antagonist FROM MuscleAntagonists WHERE Agonist = %s;", (name, ))
        antagonists = list(self.cursor.fetchall())

        return type_factories.Muscle(name, group, antagonists, info)


    def get_exercise_data(self, name):
        """
        Get the full set of data for a given exercise
        """
        # pylint: disable=no-member
        self.cursor.execute(\
            "SELECT FixtureName FROM ExerciseFixtures WHERE ExerciseName = %s;", (name, ))
        fixtures = {i[0] for i in self.cursor.fetchall()}

        self.cursor.execute(\
            "SELECT RigName, Optional FROM ExerciseRigs WHERE ExerciseName = %s;", (name, ))
        rigs = list(map(type_factories.ExerciseRig._make, self.cursor.fetchall()))

        self.cursor.execute(\
            "SELECT Muscle FROM MusclesExercised WHERE ExerciseName = %s;", (name, ))
        muscles_exercised = [i[0] for i in self.cursor.fetchall()]

        self.cursor.execute(\
            "SELECT Key, Value FROM ExerciseInfo WHERE ExerciseName = %s;", (name, ))
        info = {key: value for (key, value) in self.cursor.fetchall()}

        return type_factories.Exercise(name, fixtures, rigs, muscles_exercised, info)


    def __del__(self):
        if self.database_connection is not None:
            self.database_connection.close()
