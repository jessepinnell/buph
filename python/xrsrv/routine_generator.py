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


    def has_equipment_in_rig(self, exercise_data, user_fixtures, user_accessories):
        """ check if an excercise can be performed with the equipment """

        if exercise_data.fixture not in user_fixtures:
            return False

        has = frozenset(user_accessories)
        needs = frozenset(self.exercise_database.get_accessories_in_rig(\
            exercise_data.equipment_rig))

        return needs.issubset(has)


    def generate_single_plan(self, n_exercises, user_fixtures, user_accessories, rule_set):
        """ generates single plan

        This is a quick and dirty first pass with limited functionality and a crude
        selection algorithm
        TODO document args in a consistent format
        """

        # get all exercises
        # randomly pick one
        # apply rules
        # if satisfied, remove from list and add to output
        # repeat
        exercises = self.exercise_database.get_list_of_exercise_names()

        selected_exercises = []

        while len(selected_exercises) != n_exercises and len(exercises) != 0:

            exercise = random.choice(exercises)
            exercise_data = self.exercise_database.get_exercise_data(exercise)

            if not self.has_equipment_in_rig(exercise_data, user_fixtures, user_accessories):
                print("Not enough equipment to " + exercise)
                exercises.remove(exercise)
                continue

            for rule in rule_set:
                if rule(exercise):
                    print("Yes: " + exercise)
                    selected_exercises.append(exercise)
                else:
                    print("No: " + exercise)


        print("Selected exercises: {0}".format(selected_exercises))
        return selected_exercises
