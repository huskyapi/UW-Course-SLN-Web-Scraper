#!/usr/bin/python3
from bs4 import BeautifulSoup
from urllib.request import urlopen
from requests.utils import requote_uri

from handle_args import campus_name, course_name, quarter_name

import argparse


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
    f'www.washington.edu/students/timeschd/{args.campus}{args.quarter}/{args.course[0]}.html'
)

with urlopen(time_schedule_link) as response:
    soup = BeautifulSoup(response, 'html.parser')

    # Find table with a link with the name we want
    for table in soup.find_all('table'):
        for link in table.select('a[name]'):
            if (link['name'] == args.course[2]):
                course_description = table.find_next_sibling('table')
                while(not course_description.has_attr('bgcolor') or course_description['bgcolor'] == '#d3d3d3'):
                    print(course_description.get_text())
                    course_description = course_description.find_next_sibling('table')