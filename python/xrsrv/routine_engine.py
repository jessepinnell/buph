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

1) determine what exercises are available based on equipment
2) set user history
3) callers select generation routine and feed it that information
4) the routine generators generate lists of exercises meeting requirements
"""

# TODO Add logging
# pylint: disable=too-many-branches

from xrsrv import exercise_database
from xrsrv import routine_generators

class RoutineEngine(object):
    """ Routine engine """
    def __init__(self, exercise_database_name, verbose=True):
        self.exercise_database = exercise_database.Connection(exercise_database_name)
        self.generators = {}
        self.user_fixtures = []
        self.user_rigs = []
        self.user_routine_history = []
        self.possible_exercises = []
        self.verbose = verbose


    def add_generator(self, generator_name, generator):
        """ TODO """
        self.generators[generator_name] = generator


    def set_user_environment(self, user_fixtures, user_rigs, verbose=False):
        """ set the user environment to use for generation functions

        if len(user_fixtures) = 0, give all exercises possible
        """
        print_verbose = print if verbose else lambda *a, **k: None
        self.user_fixtures = user_fixtures
        self.user_rigs = user_rigs

        exercise_names = self.exercise_database.get_list_of_exercise_names()
        print_verbose("Number of exercises: {0}".format(len(exercise_names)))
        exercise_data = {exercise: self.exercise_database.get_exercise_data(exercise)\
                for exercise in exercise_names}

        selected_exercises = set()

        # Starting with the full list of exercise choices, remove or use them depending on
        # whether they pass all the rules tests
        for exercise_name, exercise in exercise_data.items():
            # *** Fixture checks ***
            if not self.user_fixtures:
                print_verbose("Y: No user fixtures supplied, adding by default: " + exercise_name)
                selected_exercises.add(exercise_name)
                continue

            #Check if the user has any fixture satisfying this exercise
            #if count(exercise_fixtures) > 1 then any single fixture can be used
            if self.user_fixtures and exercise.fixtures.intersection({uf.name for uf in self.user_fixtures}):
                # User had the fixture, check rigs

                if exercise.rigs:
                    exercise_rig_names = {rig.name for rig in exercise.rigs}
                    user_rig_names = {rig.name for rig in self.user_rigs}
                    #print("Exercise {0} has rigs: {1}".format(exercise.name, str(exercise.rigs)))
                    #print("user rigs: " + str(user_rig_names))
                    #print("exer rigs: " + str(exercise_rig_names))

                    # If count(exercise_rigs) > 0 and all are optional, then any single one or none can be used
                    optional_values = [rig.optional for rig in exercise.rigs]
                    if optional_values and all(optional_values):
                        print_verbose("Y: All rigs are optional ({0}), adding {1}".format(exercise.rigs, exercise_name))
                        selected_exercises.add(exercise_name)
                        continue

                    # If count(exercise_rigs) > 1 and all are not optional, then any single one can be used
                    if len(exercise_rig_names) == 1:
                        if exercise_rig_names.issubset(user_rig_names):
                            print_verbose("Y: Has the single required rig ({0}), adding {1}".format(\
                                    *exercise_rig_names, exercise_name))
                            selected_exercises.add(exercise_name)
                            continue
                        else:
                            print_verbose("N: User doesn't have the fixture, skipping " + exercise_name)
                            continue

                    else: # assume > 1
                        required_rig_names = {rig.name for rig in exercise.rigs if not rig.optional}
                        if user_rig_names.intersection(required_rig_names):
                            print_verbose("Y: Has more than one that work as the required rig ({0}), adding {1}"\
                                .format(user_rig_names.intersection(required_rig_names), exercise_name))
                            selected_exercises.add(exercise_name)
                            continue
                        else:
                            print_verbose("N: User doesn't have any that work for " + exercise_name)
                            continue

                else:
                    print_verbose("Y: User has fixture and exercise requires no rigs, adding " + exercise_name)
                    selected_exercises.add(exercise_name)
                    continue

                raise Exception("failed to classify exercise: " + exercise_name)

            else:
                print_verbose("N: User doesn't have the fixture, skipping " + exercise_name)

        self.possible_exercises = [exercise_data[exercise] for exercise in selected_exercises]

        self.generators["basic_random"] =\
            routine_generators.BasicRandomRoutineGenerator(self.possible_exercises)

    def set_user_routine_history(self, user_routine_history):
        """ set the user exercise history
        This should be a sequence of outputs from generate_single_plan()
        """
        self.user_routine_history = user_routine_history


    def generate_plan(self, generator, **kwargs):
        """ generates single plan by generator referred to by name with arbitrary args
        TODO document args in a consistent format
        """
        if generator in self.generators:
            return self.generators[generator].generate_plan(self.user_routine_history, **kwargs)
        else:
            raise Exception("Invalid generator: " + str(generator))
