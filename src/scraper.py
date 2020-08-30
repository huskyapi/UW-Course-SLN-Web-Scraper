#!/usr/bin/python3

import argparse

from bs4 import BeautifulSoup

from course import Course
from utils import validate_course_name, validate_quarter_name, validate_campus_name, \
                    create_time_schedule_url, get_html

parser = argparse.ArgumentParser()
parser.add_argument('course', type=validate_course_name)
parser.add_argument('quarter', type=validate_quarter_name)
parser.add_argument('campus', type=validate_campus_name)
args = parser.parse_args()

def get_courses_by_department(quarter, department):
    pass

def get_course(campus, quarter, course):
    url = create_time_schedule_url(campus, quarter, course.code)
    response = get_html(url)
    if response is not None:
        soup = BeautifulSoup(response, "html.parser")
        courses = soup.find_all("table")
        for c in courses:
            course_link = c.select(f"a[name=\"{course.name}\"]")
            if course_link:
                course_info = c.find_next_sibling("table")
                while not course_info.has_attr("bgcolor") or course_info["bgcolor"] == "#d3d3d3":
                    course_section = Course(course_info.get_text())
                    print(course_section.serialize())
                    course_info = course_info.find_next_sibling("table")
                break


def main():
    get_course(args.campus, args.quarter, args.course)


if __name__ == '__main__':
    main()
