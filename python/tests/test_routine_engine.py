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

""" Test cases for classes in routine_engine.py """

import unittest
from xrsrv import routine_engine
from xrsrv import exercise_database
from xrsrv.type_factories import UserRig, UserFixture

# The test function names are quite long
# pylint: disable=invalid-name
EXERCISE_DATABASE_NAME = "exercise.db"

class TestRoutineEngine(unittest.TestCase):
    """
    Test the routine engine class
    """

    def __init__(self, *args, **kwargs):
        super(TestRoutineEngine, self).__init__(*args, **kwargs)
        exercise_db = exercise_database.SQLiteConnection(EXERCISE_DATABASE_NAME)
        self.engine = routine_engine.RoutineEngine(exercise_db)
        self.build_user_all()


    def build_user_all(self):
        """ Builds up test user data """
        self.user_fixtures = [
            UserFixture("floor", 0, 0),
            UserFixture("block on floor", 0, 0),
            UserFixture("horizontal bench", 0, 0)
        ]

        self.user_rigs = [
            UserRig("barbell", 25, 25),
            UserRig("barbell", 35, 35),
            UserRig("barbell", 45, 45),
            UserRig("barbell", 55, 55),
            UserRig("dumbbell pair", 55, 55),
            UserRig("dumbbell single", 55, 55),
            UserRig("imbalanced dumbbell single", 55, 55),
        ]


    def test_instantiation(self):
        """ Test the creation of the connection to the database """
        self.assertIsInstance(self.engine, routine_engine.RoutineEngine)

    def test_exercise_one_fixture(self):
        """ Simple test for a single fixture exercise """
        user_fixtures = [
            UserFixture("test fixture 1", 0, 0)
        ]
        user_rigs = []
        self.engine.set_user_exercise_environment(user_fixtures, user_rigs)
        self.assertEqual(len(self.engine.available_exercises), 1)
        self.assertIn("test exercise 1", self.engine.available_exercises)


    def test_exercise_two_fixtures(self):
        """ Test exercise having two acceptable fixtures """
        user_fixtures = [
            UserFixture("test fixture 2a", 0, 0),
        ]
        user_rigs = []
        self.engine.set_user_exercise_environment(user_fixtures, user_rigs)
        self.assertEqual(len(self.engine.available_exercises), 1)
        self.assertIn("test exercise 2", self.engine.available_exercises)

        user_fixtures = [
            UserFixture("test fixture 2b", 0, 0),
        ]
        self.engine.set_user_exercise_environment(user_fixtures, user_rigs)
        self.assertEqual(len(self.engine.available_exercises), 1)
        self.assertIn("test exercise 2", self.engine.available_exercises)


    def test_exercise_multiple_optional_rigs(self):
        """ Test exercise having one or more optional rigs

        Examples:
        *  holding a plate when doing sit-ups
        *  holding barbells when doing calf raises
        """
        user_fixtures = [
            UserFixture("test fixture 3", 0, 0)
        ]
        user_rigs = [
            UserRig("test rig 1", 0, 0)
        ]
        self.engine.set_user_exercise_environment(user_fixtures, user_rigs)
        self.assertIn("test exercise 3", self.engine.available_exercises)

        user_rigs = [
            UserRig("test rig 2", 0, 0)
        ]
        self.engine.set_user_exercise_environment(user_fixtures, user_rigs)
        self.assertIn("test exercise 3", self.engine.available_exercises)

        user_rigs = []
        self.engine.set_user_exercise_environment(user_fixtures, user_rigs)
        self.assertIn("test exercise 3", self.engine.available_exercises)


    def test_exercise_multiple_required_rigs(self):
        """ Test exercise having more than one possible rig

        Example:
        *  front dumbbell raise using either balanced dumbbell or an imbalanced dumbbell

        This wouldn't apply to things such as overhead presses with barbells versus dumbbells.
        They would be considered different exercises due to range of motion, angle, etc.
        """
        user_fixtures = [
            UserFixture("test fixture 4", 0, 0)
        ]
        user_rigs = [
            UserRig("test rig 1", 0, 0)
        ]
        self.engine.set_user_exercise_environment(user_fixtures, user_rigs)
        self.assertIn("test exercise 4", self.engine.available_exercises)

        user_rigs = [
            UserRig("test rig 2", 0, 0)
        ]
        self.engine.set_user_exercise_environment(user_fixtures, user_rigs)
        self.assertIn("test exercise 4", self.engine.available_exercises)

        user_rigs = []
        self.engine.set_user_exercise_environment(user_fixtures, user_rigs)
        self.assertNotIn("test exercise 4", self.engine.available_exercises)


    def test_generate_single_plan(self):
        """ Test the generate_single_plan() method """
        num_exercises_in_plan = 12
        self.engine.set_user_exercise_environment(self.user_fixtures, self.user_rigs)
        plan = self.engine.generate_plan("basic_random", n=num_exercises_in_plan)
        self.assertEqual(len(plan), 1)
        self.assertEqual(len(plan[0]), num_exercises_in_plan)


    def test_generate_single_plan_too_many(self):
        """ Test the generate_single_plan() method but with too many exercises requested
        than could be possibly selected
        """
        num_exercises_in_plan = 342
        self.engine.set_user_exercise_environment(self.user_fixtures, self.user_rigs)
        plan = self.engine.generate_plan("basic_random", n=num_exercises_in_plan)
        self.assertEqual(len(plan), 1)
        self.assertNotEqual(len(plan[0]), num_exercises_in_plan)


if __name__ == '__main__':
    unittest.main()
