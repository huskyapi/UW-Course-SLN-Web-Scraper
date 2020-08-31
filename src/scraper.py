#!/usr/bin/python3

import sys

from bs4 import BeautifulSoup

from course import Course
from utils import create_time_schedule_url, get_html


def get_courses_by_department(campus, quarter, year, department_code, filename=None):
    url = create_time_schedule_url(campus, f"{quarter}{year}", department_code)
    response = get_html(url)
    if response is not None:
        soup = BeautifulSoup(response, "html.parser")

        courses = soup.find_all("table")
        for c in courses:
            course_link = c.select(f"a[name^=\"{department_code.lower()}\"]")
            if course_link:
                course_info = c.find_next_sibling("table")
                while course_info is not None:
                    if not course_info.has_attr("bgcolor") or course_info["bgcolor"] == "#d3d3d3":
                        course_section = Course(c.get_text()[1:], course_info.get_text(), quarter, year)
                        if filename:
                            with open(filename, "a") as f:
                                f.write(f"{course_section.serialize()}\n")
                        else:
                            print(course_section.serialize())
                        course_info = course_info.find_next_sibling("table")
                    else:
                        break
    else:
        print(f"No time schedule available for {campus}, {quarter}", file=sys.syserr)

def scrap_course(table, selector):
    course_link = table.select(selector)
    if course_link:
        course_info = table.find_next_sibling("table")
        while course_info is not None:
            if not course_info.has_attr("bgcolor") or course_info["bgcolor"] == "#d3d3d3":
                course_section = Course(table.get_text()[1:], course_info.get_text())
                return course_section.serialize(), course_section
            else:
                break
    return None, None

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
    else:
        print(f"No time schedule available for {campus}, {quarter}")
