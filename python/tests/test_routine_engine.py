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
from xrsrv.type_factories import UserRig, UserFixture 

EXERCISE_DATABASE_NAME = "exercise.db"

class TestRoutineEngine(unittest.TestCase):
    """
    Test the routine engine class
    """

    def __init__(self, *args, **kwargs):
        super(TestRoutineEngine, self).__init__(*args, **kwargs)
        self.engine = routine_engine.RoutineEngine(EXERCISE_DATABASE_NAME)
        self.build_user()


    def build_user(self):
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
            UserRig("dumbbell", 55, 55)
        ]


    def test_instantiation(self):
        """ Test the creation of the connection to the database """
        self.assertIsInstance(self.engine, routine_engine.RoutineEngine)


    def test_generate_single_plan(self):
        """ Test the generate_single_plan() method """
        num_exercises_in_plan = 12
        self.engine.set_user_environment(self.user_fixtures, self.user_rigs)
        plan = self.engine.generate_plan("basic_random", n=num_exercises_in_plan)
        self.assertEqual(len(plan), num_exercises_in_plan)


    # pylint: disable=invalid-name
    def test_generate_single_plan_too_many(self):
        """ Test the generate_single_plan() method but with too many exercises requested
        than could be possibly selected
        """
        num_exercises_in_plan = 342
        self.generator.set_user_environment(self.user_fixtures, self.user_rigs)
        plan = self.generator.generate_plan("basic_random", n=num_exercises_in_plan)
        self.assertNotEqual(len(plan), num_exercises_in_plan)


if __name__ == '__main__':
    unittest.main()
