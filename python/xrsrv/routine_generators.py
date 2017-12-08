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

""" HTML rendering classes """

import random

# pylint: disable=too-few-public-methods
# pylint: disable=no-self-use
# pylint: disable=unused-argument
# pylint: disable=no-member

class RoutineGeneratorBase(object):
    """ Abstract base class for routine """

    def __init__(self, exercise_data):
        """ TODO """
        self.routine_environment = None
        self.exercise_data = exercise_data

    def set_routine_environment(self, routine_environment):
        """ set the environment in which to generate the routines

        This consists of information any or all generators may use
        It differs from values that are passed to the generators which are specific to the routines
        """
        self.routine_environment = routine_environment

    def generate_plan(self, **kwargs):
        """ Generate a routine given user_data and arbitrary arguments """
        if self.routine_environment is None:
            raise Exception("Routine environment is not set")


class BasicRandomRoutineGenerator(RoutineGeneratorBase):
    """ TODO """

    def __init__(self, exercise_data):
        """ blah blah """
        super(BasicRandomRoutineGenerator, self).__init__(exercise_data)


    def generate_plan(self, **kwargs):
        """ generates single plan
        This is a quick and dirty first pass with limited functionality and a crude
        selection algorithm
        TODO document args in a consistent format
        """
        super(BasicRandomRoutineGenerator, self).generate_plan(**kwargs)

        if len(self.routine_environment.available_exercises) == 0:
            raise Exception("No available exercises from which to choose")

        choose_n = kwargs['n']
        exercise_names = random.sample(self.routine_environment.available_exercises,\
            min(choose_n, len(self.routine_environment.available_exercises)))
        return [self.exercise_data[name] for name in exercise_names]
