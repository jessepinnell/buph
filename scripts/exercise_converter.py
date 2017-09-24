#!/usr/bin/env python
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

""" script to parse a CSV and generate sqlite queries to populate tables

This makes is much easier to manually add information to tables
"""

import csv
import sys


# XXX This defaults to olympic stuff, need to handle multiple rigs for each exercise
EQUIPMENT_MAP = {
    "B": "balanced olympic barbell",
    "C": "cable",
    "D": "double adjustable dumbbell",
    "E": "balanced olympic e-z bar",
    "N": None,
    "P": None,
    "Q": None,
    "R": None,
    "T": "balanced olympic trap bar"
}

class ExerciseConverter():
    def __init__(self):
        self.exercises = {}
        

    def printExercisesSQL(self, filename):
        with open(filename, "w") as f:
            for exercise, info in self.exercises.items():
                rig = "?" if info[1] is None else "\"{0}\"".format(info[1])
                f.write("INSERT INTO Exercises VALUES (\"{0}\", \"floor\", {1}, ?)\n".format(exercise, rig))

    def printMusclesWorkedSQL(self, filename):
        with open(filename, "w") as f:
            for exercise, info in self.exercises.items():
                for muscle in info[0]:
                    f.write("INSERT INTO MusclesExercised VALUES (\"{0}\", \"{1}\")\n".format(exercise, muscle))

    def addExercise(self, exercise, muscle, equipment_char):
        if exercise not in self.exercises:
            self.exercises[exercise] = (set(), EQUIPMENT_MAP[equipment_char])
        self.exercises[exercise][0].add(muscle)

    def generateSQLFromCSV(self, input_file, exercises_out_file, muscles_worked_out_file):
        """ Generates queries based on CSV """
        with open(input_file, "r") as f:
            reader = csv.reader(f)
            header = next(reader)

            for row in reader:
                if row[0] != "":
                    for i, field in enumerate(row):
                        if field == "⚫":
                            self.addExercise(row[1], header[i], row[2])

        self.printExercisesSQL(exercises_out_file)
        self.printMusclesWorkedSQL(muscles_worked_out_file)

if __name__ == "__main__":
   if len(sys.argv) != 4:
      sys.exit("usage: {0} [input file] [muscles out] [muscles worked out]".format(sys.argv[0]))
   converter = ExerciseConverter()
   converter.generateSQLFromCSV(sys.argv[1], sys.argv[2], sys.argv[3])
