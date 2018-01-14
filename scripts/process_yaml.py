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
        self.aka = []
        self.muscles = {}
        self.info = {}
        self.fixtures = []
        self.rigs = []

        for exercise in data:
            if exercise[0].tag == 'tag:yaml.org,2002:merge':
                for merged_exercise in exercise[1].value:
                    self.setMembers(merged_exercise[0].value, merged_exercise[1].value)
            else:
                self.setMembers(exercise[0].value, exercise[1].value)

    def setMembers(self, key, value):
        if key == 'abbreviation':
            self.abbreviation = value
        elif key == 'aka':
            # Append to merged akas (if any)
            #for aka in value:
            #    self.aka.append(aka.value)

            # overwrite merged akas (if any)
            self.aka = [aka.value for aka in value]
        elif key == 'muscles':
            for muscle in value:
                self.muscles[muscle.value[0][0].value] = float(muscle.value[0][1].value)
        elif key == 'info':
            for info in value:
                self.info[info.value[0][0].value] = info.value[0][1].value
        elif key == 'fixtures':
            self.fixtures = [fixture.value for fixture in value]
        elif key == 'rigs':
            for rigs in value:
                self.rigs.append(rigs.value)
        else:
            print(f"Unknown key: {key}")


    def __str__(self):
        return f"abbreviation: {self.abbreviation}\n" +\
            f"aka: {self.aka}\n" +\
            f"muscles : {self.muscles}\n" +\
            f"info: {self.info}\n" +\
            f"fixtures: {self.fixtures}\n" +\
            f"rigs: {self.rigs}\n"

    @classmethod
    def from_yaml(cls, loader, node):
        return ExerciseYAML(node.value)

class RigYAML(yaml.YAMLObject):
    yaml_tag = u'!rig'
    info = None

    def __init__(self, data):
        pass

    @classmethod
    def from_yaml(cls, loader, node):
        return RigYAML(node.value)

class MuscleYAML(yaml.YAMLObject):
    yaml_tag = u'!muscle'
    group = ""
    info = []
    antagonists = {}

    def __init__(self, data):
        pass

    @classmethod
    def from_yaml(cls, loader, node):
        return MuscleYAML(node.value)

class StretchYAML(yaml.YAMLObject):
    yaml_tag = u'!stretch'
    aka = []
    desc = []
    info = []

    def __init__(self, data):
        pass

    @classmethod
    def from_yaml(cls, loader, node):
        return StretchYAML(node.value)


class FixtureYAML(yaml.YAMLObject):
    yaml_tag = u'!fixture'
    info = []

    def __init__(self, data):
        pass

    @classmethod
    def from_yaml(cls, loader, node):
        return FixtureYAML(node.value)



def process():
    """ Generates the list of exercises and renders the HTML """
    app_args_parser = argparse.ArgumentParser()
    app_args_parser.add_argument('--dbtype', choices=['postgres', 'sqlite3'], default='sqlite3')
    app_args_parser.add_argument('files', nargs=argparse.REMAINDER)
    app_args = app_args_parser.parse_args()

    fixtures = {}
    rigs = {}

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


if __name__ == "__main__":
    process()
