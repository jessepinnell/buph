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

import abc
import textwrap

# pylint: disable=too-few-public-methods
# pylint: disable=no-self-use
# pylint: disable=unused-argument
# pylint: disable=no-member

class BaseRenderer(metaclass=abc.ABCMeta):
    """ Abstract base class for rendering classes """

    def render(self, exercise_data):
        """ Render the exercise data
        TODO this only handles a single set of data; needs to be more powerful (PoC)
        """
        return ""

class BasicHTMLRenderer(object):
    """ Renderer that creates a VERY basic html table of data """

    def render(self, title, exercise_data):
        """ Render the excercise data in HTML

        This is a simple table for printing onto paper (not meant to be pretty)
        """

        RIG_CHAR_MAP = {
            "dumbbell pair" : "DD",
            "dumbbell single" : "D",
            "imbalanced dumbbell pair" : "II",
            "imbalanced dumbbell single" : "I",
            "barbell" : "B",
            "imbalanced barbell" : "iB",
            "trap bar" : "T",
            "ez bar" : "E",
            "plate" : "P",
            "weighted belt" : "W"
        }


        if len(exercise_data) == 1:
            body = "    <table>\n"
            body += "    <tr><th>Exercise</th><th>Muscles</th><th>Fixture(s)</th>"\
                "<th>Rig(s)</th></tr>\n"
            this_exercise_data = exercise_data[0]
            for exercise in this_exercise_data:
                if exercise.rigs is not None:
                    rig_names = ", ".join(["({0})".format(rig.name) \
                       if rig.optional else rig.name for rig in exercise.rigs])
                else:
                    rig_names = ""
                body += "{0}<tr><td>{1}</td><td>{2}</td><td>{3}</td>"\
                    "<td>{4}</td></tr>\n".format(\
                        " " * 16, exercise.name, ", ".join(exercise.muscles_exercised),\
                        ", ".join(exercise.fixtures), rig_names)
            body += "    </table>\n"

            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>{0}</title>
                <style>
                    table {{
                        border-collapse: collapse;
                    }}
                    table, th, td {{
                        border: 1px solid black;
                    }}
                </style>
            </head>
            <body>
            {1}
            </body>
            </html>
            """.format(title, body)
        else:
            body = "    <table>\n    "

            num_sets_per_exercise = 3
            for day_i, day in enumerate(exercise_data):
                body += "<tr>"
                for exercise in day:
                    if exercise.fixtures:
                        fixture_class = list(exercise.fixtures)[0].replace(' ', '_').replace(',', '')
                    rig_string = ",".join([RIG_CHAR_MAP[rig.name] if not rig.optional else "(" + RIG_CHAR_MAP[rig.name] + ")" for rig in exercise.rigs])
                    checkboxes = "<td></td>" * num_sets_per_exercise
                    body += f"<td><span style=\"float: right\"><table class=\"checkly\">{checkboxes}</table>"
                    body += f"<table class=\"checkly\"><td class=\"{fixture_class}\">{rig_string}</td></table></span>"
                    body += f"{exercise.name}</td>\n"
                body += "</tr>\n"

            body += "    </table>"
            body += "<p>(); optional, " + ", ".join([value + ": " + key for key, value in RIG_CHAR_MAP.items()]) + "</p>"
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>{0}</title>
                <style>
                    p {{
                        font-family: "Courier New", sans-serif;
                        font-weight: bold;
                        font-size: 70%;
                    }}
                    table {{
                        border-collapse: collapse;
                        font-family: "Courier New", sans-serif;
                        font-weight: bold;
                        table-layout: fixed;
                        font-size: 60%;
                    }}
                    table.checkly {{
                    }}
                    table.checkly td {{
                        width: 13px;
                        height: 13px;
                        font-size: 200%;
                    }}
                    td {{
                        overflow: hidden;
                        width: 100px;
                    }}
                    td.heady {{
                        background-color: black;
                        color: white;
                    }}
                    td.floor
                    {{
                        background-color: white;
                        color: black;
                    }}
                    td.block_on_floor
                    {{
                        background-color: cyan;
                        color: black;
                    }}
                    td.roman_chair
                    {{
                        background-color: purple;
                        color: white;
                    }}
                    td.horizontal_bench
                    {{
                        background-color: green;
                        color: white;
                    }}
                    td.elevated_horizontal_bench
                    {{
                        background-color: magenta;
                        color: white;
                    }}
                    td.incline_bench
                    {{
                        background-color: yellow;
                        color: black;
                    }}
                    td.decline_bench
                    {{
                        background-color: pink;
                        color: black;
                    }}
                    td.preacher_curl_support
                    {{
                        background-color: #222200;
                        color: white;
                    }}
                    td.pull-up_bar
                    {{
                        background-color: orange;
                        color: black;
                    }}
                    td.cable_system_high_position
                    {{
                        background-color: blue;
                        color: white;
                    }}
                    td.cable_system_middle_position
                    {{
                        background-color: blue;
                        color: white;
                    }}
                    td.cable_system_low_position
                    {{
                        background-color: blue;
                        color: white;
                    }}
                    td.heavy_bag
                    {{
                        background-color: red;
                        color: black;
                    }}
                    td.elliptical
                    {{
                        background-color: red;
                        color: black;
                    }}
                    td.treadmill
                    {{
                        background-color: red;
                        color: black;
                    }}
                    td.bench_press_machine
                    {{
                        background-color: red;
                        color: black;
                    }}
                    td.exercise_ball
                    {{
                        background-color: red;
                        color: black;
                    }}
                    td.leg_extension_machine
                    {{
                        background-color: gray;
                        color: white;
                    }}
                    td.tricep_dip_bars
                    {{
                        background-color: red;
                        color: black;
                    }}
                    td.leg_press_machine
                    {{
                        background-color: red;
                        color: black;
                    }}
                    table, th, td {{
                        border: 1px solid black;
                        text-align: left;
                        vertical-align: top;
                    }}
                </style>
            </head>
            <body>
            {1}
            <table>
                <tr><td class="floor">floor</td>
                    <td class="block_on_floor">block on floor</td>
                    <td class="roman_chair">roman chair</td>
                    <td class="horizontal_bench">horiz. bench</td>
                    <td class="elevated_horizontal_bench">elev. horiz. bench</td>
                    <td class="incline_bench">incl. bench</td>
                    <td class="decline_bench">decl. bench</td>
                    <td class="preacher_curl_support">preach</td>
                    <td class="pull-up_bar">pull-up bar</td>
                    <td class="leg_extension_machine">leg ext.</td>
                    <td class="cable_system_high_position">cable hi</td>
                    <td class="cable_system_middle_position">cable mid</td>
                    <td class="cable_system_low_position">cable lo</td>
                </tr>
                <tr>
                    <!-- XXX put this back
                    <td class="elliptical">ellipt.</td>
                    <td class="treadmill">treadmill</td>
                    <td class="bench_press_machine">b.p. machine</td>
                    <td class="exercise_ball">x-ball</td>
                    <td class="heavy_bag">hvy. bag</td>
                    <td class="tricep_dip_bars">dip bars</td>
                    <td class="leg_press_machine">leg press</td>
                    -->
                </tr>
            <table>
            </body>
            </html>
            """.format(title, body)

        return textwrap.dedent(html)

BaseRenderer.register(BasicHTMLRenderer)
