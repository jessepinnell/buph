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

""" Simple application for generating HTML routine """

import sys

from xrsrv import routine_engine
from xrsrv import exercise_rendering
from xrsrv import type_factories

TEST_DATABASE_NAME = "exercise.db"

# pylint: disable=too-few-public-methods
# pylint: disable=no-self-argument

class ExerciseRenderer(object):
    """ Application that generates an HTML rendering based on number of exercises requested """

    def __init__(self):
        pass

    def generate_and_render(database_filename, number_of_routines):
        """ Generates the list of exercises and renders the HTML """
        engine = routine_engine.RoutineEngine(database_filename)

        fixtures = [
            "floor",
            "fixed bench",
            "treadmill"
        ]

        accessories = [
            type_factories.EquipmentAccessory("olympic barbell", 1),
            type_factories.EquipmentAccessory("olympic 2.5# plate", 2)
        ]

        engine.set_user_environment(fixtures, accessories)
        plan = engine.generate_plan("basic_random", n=int(number_of_routines))

        basic_html_renderer = exercise_rendering.BasicHTMLRenderer()

        print(basic_html_renderer.render("exercise_renderer output", plan))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: {0} [exercises database file] [number of routines]".format(sys.argv[0]))
    ExerciseRenderer.generate_and_render(sys.argv[1], sys.argv[2])
