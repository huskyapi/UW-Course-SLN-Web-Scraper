#!/usr/bin/python3

import sys

from bs4 import BeautifulSoup

from src.course import Course
from src.utils import create_time_schedule_url, get_html


def get_courses_by_department(campus, quarter, year, department_code, filename=None, url=None):
    if not url:
        url = create_time_schedule_url(campus, f"{quarter}{year}", department_code)
    response = get_html(url)
    if response is not None:
        soup = BeautifulSoup(response, "html.parser")

        courses = soup.find_all("table")
        for c in courses:
            scrap_course(c, f"a[name^=\"{department_code.lower()}\"]", quarter, year, filename)

    else:
        print(f"No time schedule available for {campus}, {quarter}", file=sys.syserr)


def get_course(campus, quarter, year, course):
    url = create_time_schedule_url(campus, f"{quarter}{year}", course.code)
    response = get_html(url)
    if response is not None:
        soup = BeautifulSoup(response, "html.parser")

        courses = soup.find_all("table")
        for c in courses:
            scrap_course(c, f"a[name=\"{course.name}\"]", quarter, year, None)
            break
    else:
        print(f"No time schedule available for {campus}, {quarter}")


def scrap_course(table, selector, quarter, year, filename):
    course_link = table.select(selector)
    if course_link:
        course_info = table.find_next_sibling("table")
        while course_info:
            if not course_info.has_attr("bgcolor") or course_info["bgcolor"] == "#d3d3d3":
                course_section = Course(table.get_text()[1:], course_info.get_text(), quarter, year)
                if filename:
                    with open(filename, "a") as f:
                        f.write(f"{course_section.serialize()}\n")
                else:
                    print(course_section.serialize())
                course_info = course_info.find_next_sibling("table")
            else:
                break
