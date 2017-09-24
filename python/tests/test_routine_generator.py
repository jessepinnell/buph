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
        self.rules = [
            lambda x: True
        ]


    def test_instantiation(self):
        """ Test the creation of the connection to the database """
        self.assertIsInstance(self.generator, routine_generator.RoutineGenerator)


    def test_generate_single_plan(self):
        """ Test the generate_single_plan() method """
        plan = self.generator.generate_single_plan(1, self.user_fixtures,\
            self.user_accessories, rule_set=self.rules)
        self.assertEqual(len(plan), 1)


if __name__ == '__main__':
    unittest.main()
