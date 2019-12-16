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

Course = namedtuple('Course', 'sln section credits days time building instructor status description enrolled_students max_students')

def parse_course(course_info):
    course_parts = course_info.strip().partition('\n')
    return ( course_parts[0].split(), " ".join(course_parts[2].split()) )

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
                course_text = course_info.get_text()
                # print(repr(course_text))
                course_parts = course_text.strip().partition('\n')
                course_info_generator = course_info.strings # this gets text in each tag
                attr = re.split('\s\s+', course_parts[0].strip())
                print(attr)
                description = " ".join(course_parts[2].split())
                print(description)
               # print(Course(*attr[0].split(" "), attr[1], attr[2], attr[3], attr[4], " ".join([attr[5], attr[6]]),
                #             attr[7], attr[8], description, 0))
                course_info = course_info.find_next_sibling('table')
            break


