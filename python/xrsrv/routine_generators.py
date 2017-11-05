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

    def __init__(self, possible_exercises):
        """ possible_exercies given equipment available """
        self.possible_exercises = possible_exercises

    def generate_plan(self, user_data, **kwargs):
        """ Generate a routine given user_data and arbitrary arguments """
        pass


class BasicRandomRoutineGenerator(RoutineGeneratorBase):
    """ TODO """

    def __init__(self, possible_exercises):
        """ blah blah """
        super(BasicRandomRoutineGenerator, self).__init__(possible_exercises)

    def generate_plan(self, user_data, **kwargs):
        """ generates single plan
        This is a quick and dirty first pass with limited functionality and a crude
        selection algorithm
        TODO document args in a consistent format
        """
        choose_n = kwargs['n']
        return random.sample(self.possible_exercises, min(choose_n, len(self.possible_exercises)))
