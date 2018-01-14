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
        self.fixtures = {}
        self.rigs = {}

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
            self.fixtures = {fixture.value for fixture in value}
        elif key == 'rigs':
            self.rigs = {rig.value for rig in value}
        else:
            print(f"Unknown key: {key}")


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
            print(f"Unknown key: {key}")

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
        self.antagonists = {}

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
            print(f"Unknown key: {key}")

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
        self.fixtures = {}
        self.rigs = {}

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
        elif key == 'fixtures':
            self.fixtures = {fixture.value for fixture in value}
        elif key == 'steps':
            self.steps = {fixture.value for fixture in value}
        elif key == 'rigs':
            self.rigs = {rig.value for rig in value}
        else:
            print(f"Unknown key: {key}")


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
            print(f"Unknown key: {key}")

    def __str__(self):
        return f"info: {self.info}\n"

    @classmethod
    def from_yaml(cls, loader, node):
        return FixtureYAML(node.value)


def process():
    """ Generates the list of exercises and renders the HTML """
    app_args_parser = argparse.ArgumentParser()
    app_args_parser.add_argument('--dbtype', choices=['postgres', 'sqlite3'], default='sqlite3')
    app_args_parser.add_argument('files', nargs=argparse.REMAINDER)
    app_args = app_args_parser.parse_args()

    yaml.SafeLoader.add_constructor('!exercise', ExerciseYAML.from_yaml)
    yaml.SafeLoader.add_constructor('!muscle', MuscleYAML.from_yaml)
    yaml.SafeLoader.add_constructor('!rig', RigYAML.from_yaml)
    yaml.SafeLoader.add_constructor('!fixture', FixtureYAML.from_yaml)
    yaml.SafeLoader.add_constructor('!stretch', StretchYAML.from_yaml)

    everything = {}
    exercises = {}
    muscles = {}
    rigs = {}
    fixtures = {}
    stretches = {}

    for yaml_file in app_args.files:
        print(f"Processing {yaml_file}")
        with open(yaml_file) as this_file:
            yaml_objects = yaml.safe_load(this_file)
            everything.update(yaml_objects)
            exercises.update({key: yaml_object for key, yaml_object in yaml_objects.items() if isinstance(yaml_object, ExerciseYAML)})
            muscles.update({key: yaml_object for key, yaml_object in yaml_objects.items() if isinstance(yaml_object, MuscleYAML)})
            rigs.update({key: yaml_object for key, yaml_object in yaml_objects.items() if isinstance(yaml_object, RigYAML)})
            fixtures.update({key: yaml_object for key, yaml_object in yaml_objects.items() if isinstance(yaml_object, FixtureYAML)})
            stretches.update({key: yaml_object for key, yaml_object in yaml_objects.items() if isinstance(yaml_object, StretchYAML)})

    print("Found {} total objects".format(len(everything)))
    print("Found {} exercises".format(len(exercises)))
    print("Found {} muscles".format(len(muscles.keys())))
    print("Found {} rigs".format(len(rigs.keys())))
    print("Found {} fixtures".format(len(fixtures.keys())))
    print("Found {} stretches".format(len(stretches.keys())))

    # Validate keys across objects
    for key, exercise in exercises.items():
        print(f"\033[32m{key}\033[0m:\n{exercise}")

    for key, fixture in fixtures.items():
        print(f"\033[31m{key}\033[0m:\n{fixture}")

    for key, rig in rigs.items():
        print(f"\033[33m{key}\033[0m:\n{rig}")

    for key, muscle in muscles.items():
        print(f"\033[35m{key}\033[0m:\n{muscle}")

    for key, stretch in stretches.items():
        print(f"\033[36m{key}\033[0m:\n{stretch}")

if __name__ == "__main__":
    process()
