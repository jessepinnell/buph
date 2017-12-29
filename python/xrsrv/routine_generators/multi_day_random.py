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

""" Routine generation which applies rules and gives N days of routines """
import random
from xrsrv.routine_generators.generator_exception import GeneratorException

def generate_plan(routine_environment, exercise_data, **kwargs):
    """ generates n random daily plans
    returns a list of lists of exercises
    """

    if len(routine_environment.available_exercises) == 0:
        raise GeneratorException("No available exercises from which to choose")

    if 'n_exercises' not in kwargs:
        raise GeneratorException("Missing argument n_exercises")
    if 'n_days' not in kwargs:
        raise GeneratorException("Missing argument n_days")

    try:
        choose_n = int(kwargs['n_exercises'])
    except Exception as ex:
        raise GeneratorException("Failed to convert choose_n argument: {0}".format(ex))

    try:
        n_days = int(kwargs['n_days'])
    except Exception as ex:
        raise GeneratorException("Failed to convert n_days argument: {0}".format(ex))

    # 1) remove nevers
    # 2) add alwayses

    #print("Available: " + str(routine_environment.available_exercises))

    routines = []
    for i in range(n_days):
        routines.append([exercise_data[name] for name in random.sample(routine_environment.available_exercises,\
            min(choose_n, len(routine_environment.available_exercises)))])

    return routines
