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

    aka = []
    muscles = []
    info = []
    fixtures = []
    rigs = []

    def __init__(self, data):
        pass

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

if __name__ == "__main__":
    process()
