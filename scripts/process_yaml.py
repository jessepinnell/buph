#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright (c) 2018 Jesse Pinnell
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

""" Utility to process YAML into various flavors of SQL """

import sys
import argparse
import yaml

# pylint: disable=too-few-public-methods
# pylint: disable=no-self-argument

class ExerciseYAML(yaml.YAMLObject):
    yaml_tag = u'!exercise'

    def __init__(self, data):
        self.abbreviation = ""
        self.variation_of = ""
        self.aka = []
        self.muscles = {}
        self.steps = []
        self.info = {}
        self.fixtures = set()
        self.rigs = set()
        self.optional_rigs = set()

        for exercise in data:
            if exercise[0].tag == 'tag:yaml.org,2002:merge':
                for merged_exercise in exercise[1].value:
                    self.setMembers(merged_exercise[0].value, merged_exercise[1].value)
            else:
                self.setMembers(exercise[0].value, exercise[1].value)

    def setMembers(self, key, value):
        if key == 'abbreviation':
            self.abbreviation = value
        elif key == 'variation of':
            self.variation_of = value
        elif key == 'aka':
            # overwrite merged akas (if any)
            self.aka = {aka.value for aka in value}
        elif key == 'muscles':
            for muscle in value:
                self.muscles[muscle.value[0][0].value] = float(muscle.value[0][1].value)
        elif key == 'info':
            for info in value:
                self.info[info.value[0][0].value] = info.value[0][1].value
        elif key == 'steps':
            self.steps = [step.value for step in value]
        elif key == 'fixtures':
            self.fixtures = {fixture[0].value for fixture in value}
        elif key == 'rigs':
            self.rigs = {rig[0].value for rig in value}
        elif key == 'optional rigs':
            self.optional_rigs = {rig[0].value for rig in value}
        else:
            raise SystemExit(f"ERROR: unknown exercise key: {key}")


    def __str__(self):
        return f"abbreviation: {self.abbreviation}\n" +\
            f"variation of: {self.variation_of}\n" +\
            f"aka: {self.aka}\n" +\
            f"muscles : {self.muscles}\n" +\
            f"info: {self.info}\n" +\
            f"steps: {self.steps}\n" +\
            f"fixtures: {self.fixtures}\n" +\
            f"rigs: {self.rigs}\n" +\
            f"optional rigs: {self.optional_rigs}\n"

    @classmethod
    def from_yaml(cls, loader, node):
        return ExerciseYAML(node.value)

class RigYAML(yaml.YAMLObject):
    yaml_tag = u'!rig'

    def __init__(self, data):
        self.info = ""

        for rig in data:
            if rig[0].tag == 'tag:yaml.org,2002:merge':
                for merged_rigs in rig[1].value:
                    self.setMembers(merged_rigs[0].value, merged_rigs[1].value)
            else:
                self.setMembers(rig[0].value, rig[1].value)

    def setMembers(self, key, value):
        if key == 'info':
            self.info = value
        else:
            raise SystemExit(f"ERROR: unknown rig key: {key}")

    def __str__(self):
        return f"info: {self.info}\n"

    @classmethod
    def from_yaml(cls, loader, node):
        return RigYAML(node.value)

class MuscleYAML(yaml.YAMLObject):
    yaml_tag = u'!muscle'

    def __init__(self, data):
        self.group = ""
        self.fma = None
        self.info = {}
        self.antagonists = set()

        for muscle  in data:
            if muscle[0].tag == 'tag:yaml.org,2002:merge':
                for merged_muscles in muscles[1].value:
                    self.setMembers(merged_muscles[0].value, merged_muscles[1].value)
            else:
                self.setMembers(muscle[0].value, muscle[1].value)

    def setMembers(self, key, value):
        if key == 'group':
            self.group = value
        elif key == 'fma':
            self.fma = int(value)
        elif key == 'info':
            if isinstance(value, list):
                for info in value:
                    self.info[info.value[0][0].value] = info.value[0][1].value
        elif key == 'antagonists':
            if isinstance(value, list):
                self.antagonists = {antagonist[0].value for antagonist in value}
        else:
            raise SystemExit(f"ERROR: unknown muscle key: {key}")

    def __str__(self):
        return f"group: {self.group}\n" +\
           f"FMA: {self.fma}\n" +\
           f"info: {self.info}\n" +\
           f"antagonists: {self.antagonists}"

    @classmethod
    def from_yaml(cls, loader, node):
        return MuscleYAML(node.value)

class StretchYAML(yaml.YAMLObject):
    yaml_tag = u'!stretch'

    def __init__(self, data):
        self.abbreviation = ""
        self.variation_of = ""
        self.aka = {}
        self.muscles = {}
        self.info = {}
        self.steps = []
        self.fixtures = set()
        self.rigs = set()

        for exercise in data:
            if exercise[0].tag == 'tag:yaml.org,2002:merge':
                for merged_exercise in exercise[1].value:
                    self.setMembers(merged_exercise[0].value, merged_exercise[1].value)
            else:
                self.setMembers(exercise[0].value, exercise[1].value)

    def setMembers(self, key, value):
        if key == 'abbreviation':
            self.abbreviation = value
        elif key == 'variation of':
            self.variation_of = value
        elif key == 'aka':
            # overwrite merged akas (if any)
            self.aka = {aka.value for aka in value}
        elif key == 'muscles':
            for muscle in value:
                self.muscles[muscle.value[0][0].value] = float(muscle.value[0][1].value)
        elif key == 'info':
            for info in value:
                self.info[info.value[0][0].value] = info.value[0][1].value
        elif key == 'steps':
            self.steps = {step.value for step in value}
        elif key == 'fixtures':
            self.fixtures = {fixture[0].value for fixture in value}
        elif key == 'rigs':
            self.rigs = {rig[0].value for rig in value}
        else:
            raise SystemExit(f"ERROR: unknown stretch key: {key}")


    def __str__(self):
        return f"abbreviation: {self.abbreviation}\n" +\
            f"variation of: {self.variation_of}\n" +\
            f"aka: {self.aka}\n" +\
            f"muscles : {self.muscles}\n" +\
            f"info: {self.info}\n" +\
            f"steps: {self.steps}\n" +\
            f"fixtures: {self.fixtures}\n" +\
            f"rigs: {self.rigs}\n"


    @classmethod
    def from_yaml(cls, loader, node):
        return StretchYAML(node.value)


class FixtureYAML(yaml.YAMLObject):
    yaml_tag = u'!fixture'

    def __init__(self, data):
        self.info = ""

        for fixture in data:
            if fixture[0].tag == 'tag:yaml.org,2002:merge':
                for merged_fixtures in fixture[1].value:
                    self.setMembers(merged_fixtures[0].value, merged_fixtures[1].value)
            else:
                self.setMembers(fixture[0].value, fixture[1].value)

    def setMembers(self, key, value):
        if key == 'info':
            self.info = value
        else:
            raise SystemExit(f"ERROR: unknown fixture key: {key}")

    def __str__(self):
        return f"info: {self.info}\n"

    @classmethod
    def from_yaml(cls, loader, node):
        return FixtureYAML(node.value)


class YAMLProcessor():
    def __init__(self):
        """ Generates the list of exercises and renders the HTML """
        app_args_parser = argparse.ArgumentParser()
        app_args_parser.add_argument('--format', choices=['dump', 'postgres', 'sqlite3'], default='dump')
        app_args_parser.add_argument('files', nargs=argparse.REMAINDER)
        app_args = app_args_parser.parse_args()

        yaml.SafeLoader.add_constructor('!exercise', ExerciseYAML.from_yaml)
        yaml.SafeLoader.add_constructor('!muscle', MuscleYAML.from_yaml)
        yaml.SafeLoader.add_constructor('!rig', RigYAML.from_yaml)
        yaml.SafeLoader.add_constructor('!fixture', FixtureYAML.from_yaml)
        yaml.SafeLoader.add_constructor('!stretch', StretchYAML.from_yaml)

        self.everything = {}
        self.exercises = {}
        self.muscles = {}
        self.rigs = {}
        self.fixtures = {}
        self.stretches = {}
        

        self.load_files(app_args.files)
        self.validate()

        if app_args.format == 'postgres':
           self.write_postgres() 
        elif app_args.format == 'sqlite3':
           self.write_sqlite3() 
        else:
           self.dump() 
            

    def load_files(self, input_files):
        for yaml_file in input_files:
            with open(yaml_file) as this_file:
                yaml_objects = yaml.safe_load(this_file)
                self.everything.update(yaml_objects)
                self.exercises.update({key: yaml_object for key, yaml_object in yaml_objects.items() if isinstance(yaml_object, ExerciseYAML)})
                self.muscles.update({key: yaml_object for key, yaml_object in yaml_objects.items() if isinstance(yaml_object, MuscleYAML)})
                self.rigs.update({key: yaml_object for key, yaml_object in yaml_objects.items() if isinstance(yaml_object, RigYAML)})
                self.fixtures.update({key: yaml_object for key, yaml_object in yaml_objects.items() if isinstance(yaml_object, FixtureYAML)})
                self.stretches.update({key: yaml_object for key, yaml_object in yaml_objects.items() if isinstance(yaml_object, StretchYAML)})

    def validate(self):
        abbreviations = [exercise.abbreviation for key, exercise in self.exercises.items()] 
        for abbreviation in abbreviations:
            if abbreviations.count(abbreviation) > 1:
                raise SystemExit(f"ERROR: duplicate abbreviation: {abbreviation}")


        for key, exercise in self.exercises.items():
            if exercise.variation_of and exercise.variation_of not in self.exercises.keys():
                raise SystemExit(f"ERROR: exercise {key} is a variation of invalid exercise: {exercise.variation_of}")

            muscles = set(exercise.muscles.keys())
            if not muscles.issubset(self.muscles.keys()):
                invalid_muscles = ", ".join(exercise.muscles.keys() - self.muscles.keys())
                raise SystemExit(f"ERROR: exercise {key} has invalid muscle(s): {invalid_muscles}")

            if not exercise.fixtures.issubset(self.fixtures.keys()):
                invalid_fixtures = ", ".join(exercise.fixtures - self.fixtures.keys())
                raise SystemExit(f"ERROR: exercise {key} has invalid fixture(s): {invalid_fixtures}")

            if not exercise.rigs.issubset(self.rigs.keys()):
                invalid_rigs = ", ".join(exercise.rigs - self.rigs.keys())
                raise SystemExit(f"ERROR: exercise {key} has invalid rig(s): {invalid_rigs}")

        for key, muscle in self.muscles.items():
            antagonists = set(muscle.antagonists)
            if not antagonists.issubset(self.muscles.keys()):
                invalid_antagonists = ", ".join(muscle.antagonists - self.muscles.keys())
                raise SystemExit(f"ERROR: muscle {key} has invalid antagonist(s): {invalid_antagonists}")

        for key, stretch in self.stretches.items():
            muscles = set(stretch.muscles.keys())
            if not muscles.issubset(self.muscles.keys()):
                invalid_muscles = ", ".join(stretch.muscles.keys() - self.muscles.keys())
                raise SystemExit(f"ERROR: stretch {key} has invalid muscle(s): {invalid_muscles}")

            if not stretch.fixtures.issubset(self.fixtures.keys()):
                invalid_fixtures = ", ".join(stretch.fixtures - self.fixtures.keys())
                raise SystemExit(f"ERROR: stretch {key} has invalid fixture(s): {invalid_fixtures}")

            if not stretch.rigs.issubset(self.rigs.keys()):
                invalid_rigs = ", ".join(stretch.rigs - self.rigs.keys())
                raise SystemExit(f"ERROR: stretch {key} has invalid rig(s): {invalid_rigs}")




    def write_sqlite3(self):
        pass

    def write_postgre(self):
        pass

    def dump(self):
        # Validate keys across objects
        for key, exercise in self.exercises.items():
            print(f"\033[32m{key}\033[0m:\n{exercise}")

        for key, fixture in self.fixtures.items():
            print(f"\033[31m{key}\033[0m:\n{fixture}")

        for key, rig in self.rigs.items():
            print(f"\033[33m{key}\033[0m:\n{rig}")

        for key, muscle in self.muscles.items():
            print(f"\033[35m{key}\033[0m:\n{muscle}")

        for key, stretch in self.stretches.items():
            print(f"\033[36m{key}\033[0m:\n{stretch}")


if __name__ == "__main__":
    processor = YAMLProcessor()
