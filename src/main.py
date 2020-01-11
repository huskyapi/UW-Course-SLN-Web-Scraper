#!/usr/bin/python3

import bs4
from bs4 import BeautifulSoup
from urllib.request import urlopen
from requests.utils import requote_uri

from utils.validation import campus_name, course_name, quarter_name
from utils.parser import parse_course

import argparse
import requests
import sys

parser = argparse.ArgumentParser()
parser.add_argument('course', type=course_name)
parser.add_argument('quarter', type=quarter_name)
parser.add_argument('campus', type=campus_name)

args = parser.parse_args()


time_schedule_link = requote_uri(
    f'https://www.washington.edu/students/timeschd/{args.campus}{args.quarter}/{args.course.code}.html'
)

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
                course = parse_course(course_info.get_text())
                print(course)
                course_info = course_info.find_next_sibling('table')
            break




