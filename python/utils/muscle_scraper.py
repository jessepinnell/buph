#!/usr/bin/env python
# Copyright (c) 2017 Jesse Pinnell
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
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

""" script to scrape a website to pull list of muscles and data

 This script reads a url, scrapes the contents and generates the muscles table data
 The output of this script should satisfy the requirements of the database schema but it will require pruning by hand
 to remove muscles not typically used for fitness exercises.

 To execute, install lxml library and dependencies:
   $ sudo apt-get install libz-dev libxml2-dev libxslt-dev
"""

# pylint: disable=import-error
# pylint: disable=too-many-locals
# pylint: disable=line-too-long
import random
import urllib2
import sys
from lxml import html

# This is a random list of user agents to use during the scraping
USER_AGENTS = [
    "Mozilla/5.0 (Windows; U; ; en-NZ) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.8.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser; Avant Browser; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.8 (KHTML, like Gecko) Beamrise/17.2.0.9 Chrome/17.0.939.0 Safari/535.8",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/28.0.1469.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.0; rv:14.0) Gecko/20100101 Firefox/14.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.2; rv:19.0) Gecko/20121129 Firefox/19.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130401 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0",
    "Mozilla/5.0 (compatible; Konqueror/4.5; Windows) KHTML/4.5.4 (like Gecko)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Maxthon 2.0)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.1 (KHTML, like Gecko) Maxthon/3.0.8.2 Safari/533.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML like Gecko) Maxthon/4.0.0.2000 Chrome/22.0.1229.79 Safari/537.1",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/5.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.2; Trident/5.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.2; WOW64; Trident/5.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; Trident/7.0; .NET4.0E; .NET4.0C)",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.7.62 Version/11.01",
    "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
    "Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.16",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.12 Safari/537.36 OPR/14.0.1116.4",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.29 Safari/537.36 OPR/15.0.1147.24 (Edition Next)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36 OPR/18.0.1284.49",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36 OPR/19.0.1326.56",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows; U; Windows NT 6.2; es-US ) AppleWebKit/540.0 (KHTML like Gecko) Version/6.0 Safari/8900.00",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12",
    "Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1"
]

class MuscleDataScraper():
    """ web scraper for some muscle information """
    def __init__(self, url):
        self.tree_ = None
        self.duplicates_set_ = None
        self.url_ = url

    def generate_sql_from_table(self, group_name, html_table_index,\
        ignore=False, hide_descriptions=True):
        """ Generates queries based on table within HTML

         group_name -- the name of the muscle group to default matching results to
         html_table_index -- The XPATH index of the table in the html
         ignore -- Generate the queries but hide the output in comments
         hide_descriptions -- Generate the muscle motion descriptions but hide it in comments (default to true for now)
        """
        rows_xpath = "count(//html/body/table[{0}]/tr)".format(html_table_index)
        row_elements = self.tree_.xpath(rows_xpath)
        num_rows = int(row_elements)

        if num_rows == 0:
            raise Exception("No rows were found")

        data = {}
        for row in range(1, num_rows+1):
            muscle_xpath = "//html/body/table[{0}]/tr[{1}]/td[1]/text()".format(html_table_index, row)
            element = self.tree_.xpath(muscle_xpath)
            muscle = element

            if not muscle:
                continue

            action_xpath = "//html/body/table[{0}]/tr[{1}]/td[4]/text()".format(html_table_index, row)
            element = self.tree_.xpath(action_xpath)
            action = element
            try:
                # pylint: disable=broad-except
                # clean out extra whitespace
                data[' '.join(muscle[0].split())] = "" if hide_descriptions else ' '.join(action[0].split())
            except Exception as ex:
                print("/* Bad value found: {0} */".format(ex))


        for this_muscle, this_action in data.items():
            if this_muscle not in self.duplicates_set_:
                print("{0} INSERT INTO Muscles VALUES (\"{1}\", \"{2}\", \"{3}\");{4}".format("/*" if ignore else "",\
                    this_muscle, group_name, this_action, "*/" if ignore else ""))
                self.duplicates_set_.add(this_muscle)
            else:
                print("/* Duplicate found: " + this_muscle + "*/")

    def scrape(self):
        """ Retrieve HTML data from URL and extract the data to put into sqlite3 queries """
        user_agent = random.choice(USER_AGENTS)
        req = urllib2.Request(self.url_)
        req.add_header("User-Agent", user_agent)
        page = urllib2.urlopen(req)

        page_html = page.read()

        self.tree_ = html.fromstring(page_html)
        self.duplicates_set_ = set()

        # These are general groupings to have something to start with
        self.generate_sql_from_table("back", 2)
        self.generate_sql_from_table("arms", 3)
        self.generate_sql_from_table("other", 4, True)
        self.generate_sql_from_table("abdomen", 5)
        self.generate_sql_from_table("pelvic", 6)
        self.generate_sql_from_table("pelvic", 7, True) # These are the pelvic muscles
        self.generate_sql_from_table("leg", 8)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: {0} [url]".format(sys.argv[0]))
    SCRAPER = MuscleDataScraper(sys.argv[1])
    SCRAPER.scrape()
