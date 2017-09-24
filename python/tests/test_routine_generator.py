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

""" Test cases for classes in routine_generator.py """

import unittest
from xrsrv import routine_generator
from xrsrv.type_factories import EquipmentAccessory

EXERCISE_DATABASE_NAME = "exercise.db"

class TestRoutineGenerator(unittest.TestCase):
    """
    Test the routine generator class
    """

    def __init__(self, *args, **kwargs):
        super(TestRoutineGenerator, self).__init__(*args, **kwargs)
        self.generator = routine_generator.RoutineGenerator(EXERCISE_DATABASE_NAME)

        self.build_user()
        self.build_rules()


    def build_user(self):
        """ Builds up test user data """
        self.user_fixtures = [
            "floor",
            "fixed bench",
            "treadmill"
        ]

        self.user_accessories = [
            EquipmentAccessory("olympic barbell", 1),
            EquipmentAccessory("olympic 2.5# plate", 2)
        ]


    def build_rules(self):
        """ Builds up test rules """

        # This example will cause any exercise chosen to be skipped if it
        # exercises the biceps brachii muscle and requires the exercise to
        # exercise either the lats or the triceps
        # Even though this is simplistic, if the user data is constructed properly,
        # then exercise history, muscle targets, etc. can be used
        exclude_muscles = {
            "biceps brachii"
        }

        require_muscles = {
            "triceps brachii",
            "latissimus dorsi"
        }

        exclude_exercises = {
            "overhead front press",
            "decline bench press"
        }

        # No need to handle require_exercises because that should be known external to this method
        # In these rules, x is of type type_factories.Exercise
        # lambdas returning false disqualify the result

        self.rules = [
            lambda x: not set(x.muscles_exercised).intersection(exclude_muscles),
            lambda x: set(x.muscles_exercised).intersection(require_muscles),
            lambda x: not set(x.name).intersection(exclude_exercises)
        ]


    def test_instantiation(self):
        """ Test the creation of the connection to the database """
        self.assertIsInstance(self.generator, routine_generator.RoutineGenerator)


    def test_generate_single_plan(self):
        """ Test the generate_single_plan() method """
        num_exercises_in_plan = 12
        self.generator.set_user_data(self.user_fixtures, self.user_accessories)
        plan = self.generator.generate_single_plan(num_exercises_in_plan, rule_set=self.rules)
        self.assertEqual(len(plan), num_exercises_in_plan)


    # pylint: disable=invalid-name
    def test_generate_single_plan_too_many(self):
        """ Test the generate_single_plan() method but with too many exercises requested
        than could be possibly selected
        """
        num_exercises_in_plan = 342
        self.generator.set_user_data(self.user_fixtures, self.user_accessories)
        plan = self.generator.generate_single_plan(num_exercises_in_plan, rule_set=self.rules)
        self.assertNotEqual(len(plan), num_exercises_in_plan)


if __name__ == '__main__':
    unittest.main()
