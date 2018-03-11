/*
Copyright (c) 2018 Jesse Pinnell
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
/** 
* @file create.sql
* @brief Creation script for postgres database tables
* This database contains relationships and data for all exercises, muscles, and
* things that are NOT specific to user profiles
* @author Jesse Pinnell
* @date 2018-03-11
*/

CREATE TABLE MuscleGroups
(
   Name TEXT NOT NULL PRIMARY KEY,
   Info TEXT DEFAULT NULL
);

-- Muscles to exercise
CREATE TABLE Muscles
(
   Name TEXT NOT NULL PRIMARY KEY,
   MuscleGroup TEXT NOT NULL,
   Info TEXT DEFAULT NULL
);

CREATE TABLE MuscleAntagonists
(
   Agonist TEXT NOT NULL REFERENCES Muscles(Name),
   Antagonist TEXT NOT NULL REFERENCES Muscles(Name)
);

-- Exercise equipment that is stationary
CREATE TABLE Fixtures
(
   Name TEXT NOT NULL PRIMARY KEY,
   Note TEXT DEFAULT ''
);

-- Exercise equipment that can be moved
-- TODO split differently so note doesn't need to be here
CREATE TABLE Rigs
(
   Name TEXT NOT NULL PRIMARY KEY,
   Note TEXT DEFAULT ''
);

CREATE TABLE Stretches
(
   Name TEXT NOT NULL PRIMARY KEY
);

CREATE TABLE StretchInfo
(
   StretchName TEXT NOT NULL REFERENCES Stretches(Name),
   Key TEXT NOT NULL,
   Value TEXT NOT NULL
);

CREATE TABLE MusclesStretched
(
   StretchName TEXT NOT NULL REFERENCES Stretches(Name), -- can be many per stretch, so not unique
   Muscle TEXT NOT NULL REFERENCES Muscles(Name)
);

-- Individual exercises and the required equipment
CREATE TABLE Exercises
(
   Name TEXT NOT NULL PRIMARY KEY
);

CREATE TABLE ExerciseInfo
(
   ExerciseName TEXT NOT NULL REFERENCES Exercises(Name),
   Key TEXT NOT NULL,
   Value TEXT NOT NULL
);

CREATE TABLE ExerciseFixtures
(
   ExerciseName TEXT NOT NULL REFERENCES Exercises(Name),
   FixtureName TEXT NOT NULL REFERENCES Fixtures(Name)
);

CREATE TABLE ExerciseRigs
(
   ExerciseName TEXT NOT NULL REFERENCES Exercises(Name),
   RigName TEXT NOT NULL REFERENCES Rigs(Name),
   Optional INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE MusclesExercised
(
   ExerciseName TEXT NOT NULL REFERENCES Exercises(Name), -- can be many per exercise, so not unique
   Muscle TEXT NOT NULL REFERENCES Muscles(Name),
   Weighting REAL NOT NULL DEFAULT 1.0 -- how much a particular exercise acts on a muscles compared to others
);
