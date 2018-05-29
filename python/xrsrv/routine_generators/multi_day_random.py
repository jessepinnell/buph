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
# The exclude-if/include-if needs to be redone; remove these after that
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-nested-blocks

""" Routine generation which applies rules and gives N days of routines """
import random
from xrsrv.routine_generators.generator_exception import GeneratorException

def generate_plan(routine_environment, exercise_data, **kwargs):
    """ generates n random daily plans
    example json:
    {
    "n_exercises" : 14,
    "n_days" : 10,
    "exclude" : ["sumo deadlift", "overhead back press"],
    "force" : {"dumbbell wrist curl" : 1, "dumbbell reverse wrist curl" : 2}, # force it every nth day
    "exclusive" : ["leg extension", "cable back kick"] #if one in this sequence is select, remove the rest
    }
    returns a list of lists of exercises
    """


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

    # 1) remove exercises explicitly excluded
    if 'exclude' in kwargs:
        exclude_set = set(kwargs['exclude'])
        for exclude in exclude_set:
            if exclude in routine_environment.available_exercises:
                routine_environment.available_exercises.remove(exclude)

    # remove forces exercises from main pool
    force_set = kwargs['force']


    routine_environment.available_exercises.difference_update(force_set.keys())

    #print("Available: " + str(routine_environment.available_exercises))

    routines = []
    for i in range(n_days):
        this_days_available_names = list(routine_environment.available_exercises)
        forces = []
        # 2) add exercises explicitly added if available
        for force, factor in force_set.items():
            if not random.randrange(factor):
                forces.append(force)

        if len(routine_environment.available_exercises) < choose_n:
            raise GeneratorException("Not enough available exercises from which to choose ({0} < {1})".format(\
                len(routine_environment.available_exercises), choose_n))


        this_days_routine = []
        this_days_routine.extend(forces)

        while len(this_days_routine) < choose_n:
            this_random = random.choice(this_days_available_names)
            this_days_available_names.remove(this_random)

            this_days_routine.append(this_random)


            # TODO excludes removed, use the variation of field for this

        random.shuffle(this_days_routine)
        routines.append([exercise_data[name] for name in this_days_routine])

    return routines
