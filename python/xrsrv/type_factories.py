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

# **** Exercise types ****
# name: muscle name
# group: muscle grouping
# antagonists: muscle antagonists
# info: dictionary of additional information about the muscle
Muscle = collections.namedtuple("Muscle", "name, group, antagonist, info")

# name: exercise name
# fixtures: fixtures required
# rigs: rigs to be used with this exercise
# muscles_exercised: list of muscles exercised
# info: dictionary of additional information about the exercise
Exercise = collections.namedtuple(\
    "Exercise", "name, fixtures, rigs, muscles_exercised, info")

# name: rig name
# optional: optional in exercise
ExerciseRig = collections.namedtuple("ExerciseRig", "name, optional")

# **** User types ****
# name: fixture name
# min_setting: either minimum speed, weight, or resistance
# max_setting: either maximum speed, weight, or resistance
UserFixture = collections.namedtuple("UserFixture", "name, min_setting, max_setting")

# name: rig name
# min_setting: either minimum speed, weight, or resistance
# max_setting: either maximum speed, weight, or resistance
UserRig = collections.namedtuple("UserRig", "name, min_setting, max_setting")

# name: equipment accessory name (must match expected names in exercise_db)
# quantity: equipment accessory quantity available
EquipmentAccessory = collections.namedtuple("EquipmentAccessory", "name, quantity")
