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

""" The type factories generating the abstractions of data in the database """

import collections

# name: muscle name
# group: muscle grouping
# info: additional information about the muscle
Muscle = collections.namedtuple(\
    "Muscle", "name, group, info")

# name: rig name
# possible_resistances: possible reistances in lbs resistance
EquipmentRig = collections.namedtuple(\
    "EquipmentRig", "name, possible_resistances")

# name: exercise name
# fixture: fixture required
# equipment_rig: equpment_rig required or None if none required
# documentation: additional information about the exercise
# muscles_exercised: list of muscles exercised
Exercise = collections.namedtuple(\
    "Exercise", "name, fixture, equipment_rig, documentation, muscles_exercised")
