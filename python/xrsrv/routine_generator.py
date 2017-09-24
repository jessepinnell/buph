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

"""
This module contains the class(es) which process user profile data and generates
exercise routines
"""

import random
from xrsrv import exercise_database

class RoutineGenerator(object):
    """ Routine generation class """
    def __init__(self, exercise_database_name):
        self.exercise_database = exercise_database.Connection(exercise_database_name)
        self.user_fixtures = []
        self.user_accessories = []

    def set_user_data(self, user_fixtures, user_accessories):
        """ set the user data to use for generation functions """
        self.user_fixtures = user_fixtures
        self.user_accessories = user_accessories

    def has_equipment_in_rig(self, exercise_data):
        """ check if an excercise can be performed with the equipment """

        # if the user_fixtures is empty, then provide all
        if self.user_fixtures and exercise_data.fixture not in self.user_fixtures:
            return False

        if not self.user_accessories:
            return True

        has = frozenset(self.user_accessories)
        needs = frozenset(self.exercise_database.get_accessories_in_rig(\
            exercise_data.equipment_rig))

        return needs.issubset(has)


    def generate_single_plan(self, n_exercises, rule_set):
        """ generates single plan

        This is a quick and dirty first pass with limited functionality and a crude
        selection algorithm
        TODO document args in a consistent format
        """

        exercises = self.exercise_database.get_list_of_exercise_names()
        exercise_data = {exercise: self.exercise_database.get_exercise_data(exercise)\
                for exercise in exercises}

        selected_exercises = set()

        # Starting with the full list of exercise choices, remove or use them depending on
        # whether they pass all the rules tests
        while len(selected_exercises) != n_exercises and len(exercises) != len(selected_exercises):
            exercise_name = random.choice(exercises)

            if not self.has_equipment_in_rig(exercise_data[exercise_name]):
                exercises.remove(exercise_name)
                continue

            if all([rule(exercise_data[exercise_name]) for rule in rule_set]):
                selected_exercises.add(exercise_name)
            else:
                exercises.remove(exercise_name)

        #print("Selected {0} exercises (requested {1}): {2}".format(len(selected_exercises),\
        #    n_exercises, ", ".join(selected_exercises)))
        return [exercise_data[exercise] for exercise in selected_exercises]
