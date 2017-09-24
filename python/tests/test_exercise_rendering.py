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

""" Test cases for classes in exercise_rendering.py """

import unittest
from xrsrv import routine_generator
from xrsrv import exercise_rendering
from xrsrv import type_factories

EXERCISE_DATABASE_NAME = "exercise.db"

class TestExerciseHTMLRendering(unittest.TestCase):
    """
    Test the exercise HTML rendring classes

    TODO(jessepinnell) refactor or make these more robust tests
    """

    def __init__(self, *args, **kwargs):
        super(TestExerciseHTMLRendering, self).__init__(*args, **kwargs)
        self.generator = routine_generator.RoutineGenerator(EXERCISE_DATABASE_NAME)
        self.basic_html_renderer = exercise_rendering.BasicHTMLRenderer()

        self.build_user()

    def build_user(self):
        """ Builds up test user data """
        self.user_fixtures = [
            "floor",
            "fixed bench",
            "treadmill"
        ]

        self.user_accessories = [
            type_factories.EquipmentAccessory("olympic barbell", 1),
            type_factories.EquipmentAccessory("olympic 2.5# plate", 2)
        ]


    def test_instantiation(self):
        """ Test the creation of the connection to the database """
        self.assertIsInstance(self.basic_html_renderer, exercise_rendering.BasicHTMLRenderer)


    def test_generate_single_plan(self):
        """ Test the generate_single_plan() method """
        num_exercises_in_plan = 12
        self.generator.set_user_data(self.user_fixtures, self.user_accessories)
        plan = self.generator.generate_single_plan(num_exercises_in_plan, rule_set=[])
        self.assertEqual(len(plan), num_exercises_in_plan)

        # TODO perform HTML validation as test
        print(self.basic_html_renderer.render(plan))


if __name__ == '__main__':
    unittest.main()
