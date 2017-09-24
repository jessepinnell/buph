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

""" Abstraction of sqlite3 database """

# TODO(jessepinnell) This should be a pure virtual persistence object
#    with an sqlite3 implementation; refactor it

import sqlite3

# TODO(jessepinnell) figure out why lint doesn't like pathlib
# pylint: disable=import-error
from pathlib import Path

from xrsrv import type_factories

class Connection(object):
    """
    Abstraction of a sqllite3 database
    """
    database_connection = None

    def __init__(self, database_name):
        # Because this will create a database if it doesn't find one explicitly check for one
        existing_db_file = Path(database_name)
        if not existing_db_file.exists():
            raise IOError("Database file doesn't exist: " + database_name)

        self.database_connection = sqlite3.connect(database_name)
        self.cursor = self.database_connection.cursor()


    def get_equipment_accessories(self):
        """
        Get set of equipment accessory quantities
        """
        self.cursor.execute("SELECT Name, Quantity FROM EquipmentAccessories")
        return map(type_factories.EquipmentAccessory._make, self.cursor.fetchall())


    def get_fixtures(self):
        """
        Get set of fixture quantities
        """
        self.cursor.execute("SELECT Name, Quantity FROM Fixtures")
        return [i[0] if i[1] > 0 else None for i in self.cursor.fetchall()]


    def __del__(self):
        if self.database_connection is not None:
            self.database_connection.close()
