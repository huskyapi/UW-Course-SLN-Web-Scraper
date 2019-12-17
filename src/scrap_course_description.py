#!/usr/bin/python3
from bs4 import BeautifulSoup
from urllib.request import urlopen
from requests.utils import requote_uri
from collections import namedtuple

from handle_args import campus_name, course_name, quarter_name

import re
import argparse
import requests
import sys

Course = namedtuple('Course', 'sln section credits days time building_abbr room_number instructor ' 
                    'status enrolled_students max_students description')

parser = argparse.ArgumentParser()
parser.add_argument('course', type=course_name)
parser.add_argument('quarter', type=quarter_name)
parser.add_argument('campus', type=campus_name)

args = parser.parse_args()

time_schedule_link = requote_uri(
    f'https://www.washington.edu/students/timeschd/{args.campus}{args.quarter}/{args.course.code}.html'
)

# make into a function
# have this be called by a separate main.py file

# return json w/ props that format the table data
# each object being one class


response = requests.get(time_schedule_link)
if response.status_code != 200:
    print('Error')
    sys.exit(1)

with urlopen(time_schedule_link) as response:
    soup = BeautifulSoup(response, 'html.parser')
    tables = soup.find_all('table')
    for t in tables:
        course_link = t.select(f'a[name=\"{args.course.name}\"]')
        if course_link:
            course_info = t.find_next_sibling('table')
            while not course_info.has_attr('bgcolor') or course_info['bgcolor'] == '#d3d3d3':
                course_parts = course_info.get_text().strip().partition('\n')
                description = " ".join(course_parts[2].split())
                # Split on multiple space characters
                # (text strings from UW website contain \r, \n and whitespace)
                attributes = re.split('\s\s+', course_parts[0].strip())
                for attr in attributes:
                    if not re.fullmatch(r'[a-zA-Z, ]+', attr) and ' ' in attr:
                        pos = attributes.index(attr)
                        elem1, elem2 = attr.split()
                        attributes[pos:pos + 1] = (elem1, elem2)
                print(Course(*attributes, description))
                course_info = course_info.find_next_sibling('table')
            break




