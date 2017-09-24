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

# TODO(jessepinnell) This should be a pure virtual persistence object
#    with an sqlite3 implementation; refactor it

import sqlite3
import collections

# TODO(jessepinnell) figure out why lint doesn't like pathlib
# pylint: disable=import-error
from pathlib import Path

from xrsrv import type_factories

class Connection(object):
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


    def get_muscles(self):
        """
        Get set of muscles
        """
        self.cursor.execute("SELECT Name, MuscleGroup, Info FROM Muscles")
        return map(type_factories.Muscle._make, self.cursor.fetchall())


    def get_equipment_rig_resistances(self, name):
        """
        For a given equipment rig name, get all possible resistances based
        on rig definitions and quantity on hand
        """

        #equipment_rig_record = collections.namedtuple(\
        #    "equipment_rig_record", "name, required, paired, max_equippable, equipment_accessory")
        self.cursor.execute("SELECT Name, Required, Paired, MaxEquippable,"\
            "EquipmentAccessory FROM EquipmentRigs WHERE Name = (?)", (name, ))
        #equipment_rigs = map(equipment_rig_record._make, self.cursor.fetchall())

        # TODO calculate all possiblities here
        resistances = [0]
        return resistances


    def get_exercise_data(self, name):
        """
        Get the full set of data for a given exercise
        """
        exercise_record = collections.namedtuple(\
            "ExerciseRecord", "name, fixture, equipment_rig, documentation")
        self.cursor.execute("SELECT Name, Fixture, EquipmentRig, Documentation "\
            "FROM Exercises WHERE Name = ?", (name,))
        this_exercise = exercise_record._make(self.cursor.fetchone())

        # pylint: disable=no-member
        self.cursor.execute(\
            "SELECT Muscle FROM MusclesExercised WHERE ExerciseName = ?", (this_exercise.name, ))

        muscles_exercised = [i[0] for i in self.cursor.fetchall()]

        return type_factories.Exercise(*this_exercise, muscles_exercised)


    # TODO Implement this and remove these when implemented
    # pylint: disable=unused-argument
    # pylint: disable=no-self-use
    def get_accessories_in_rig(self, rig):
        """ get all the accessories in a rig

        This is used to look up whether a particular exercise can be done given a
        set of accessories
        """
        return []


    def __del__(self):
        if self.database_connection is not None:
            self.database_connection.close()
