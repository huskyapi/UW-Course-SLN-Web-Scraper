#!/usr/bin/python3
from bs4 import BeautifulSoup
from urllib.request import urlopen
from requests.utils import requote_uri

from handle_args import campus_name, course_name, quarter_name

import argparse
import requests
import sys


parser = argparse.ArgumentParser()
parser.add_argument('course', type=course_name)
parser.add_argument('quarter', type=quarter_name)
parser.add_argument('campus', type=campus_name)

args = parser.parse_args()

# args: course name, quarter, campus
# search for specific quarter
# search back multiple quarters
# search for classes from past quarters


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
    for table in tables:
        course_link = table.select(f'a[name=\"{args.course.name}\"]')
        if course_link:
            course_desc = table.find_next_sibling('table')
            while not course_desc.has_attr('bgcolor') or course_desc['bgcolor'] == '#d3d3d3':
                print(course_desc.get_text())
                course_desc = course_desc.find_next_sibling('table')
            break