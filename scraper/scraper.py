#!/usr/bin/python3
"""
This module defines functions that can be used to scrap courses
from the UW Time Schedule.
"""
import json
import sys
import logging

from bs4 import BeautifulSoup

from scraper.course_sln import CourseSLN
from scraper.course import Course
from scraper.utils import create_time_schedule_url, get_html

log = logging.getLogger(__name__)


def get_courses_by_department(campus, quarter, year, dept_code, filename=None,
                              sln_only=False, url=None):
    """
    Scraps all courses from the given department, campus,
    quarter and year.
    Optional:
        filename: Location of output file.
        url: URL from which to scrap courses.
    """
    if not url:
        log.info(f"Creating time schedule url for {quarter}, {year}, and {dept_code}")
        url = create_time_schedule_url(campus, f"{quarter}{year}", dept_code)
    log.info("Retrieving HTML response..")
    response = get_html(url)
    if response is not None:
        log.info("HTML response successfully queried.")
        soup = BeautifulSoup(response, "html.parser")
        courses = soup.find_all("table")
        log.info(f"Scraping courses for {quarter}, {year}, and {dept_code}")
        for course in courses:
            scrap_course(course, f"a[name^=\"{dept_code.lower()}\"]",
                         quarter, year, filename, sln_only)
    else:
        print(f"No time schedule available for {campus}, {quarter}", file=sys.stderr)


def get_course(campus, quarter, year, department_code,
               course_name, filename=None):
    """
    Scraps the course that corresponds with the given campus,
    quarter, year, and course information.
        department_code: The UW department code. ex: CSE, INFO
        course_name: The full course name. ex: INFO200
    """
    url = create_time_schedule_url(campus, f"{quarter}{year}", department_code)
    response = get_html(url)
    if response is not None:
        soup = BeautifulSoup(response, "html.parser")

        courses = soup.find_all("table")
        for crs in courses:
            scrap_course(crs, f"a[name=\"{course_name}\"]",
                         quarter, year, filename)
    else:
        print(f"No time schedule available for {campus}, {quarter}")


def scrap_course(table, selector, quarter, year, filename=None, sln_only=False):
    """
    Scraps all courses from the given BeautifulSoup HTML table
    string that match the given CSS selector, quarter, and year.
    Optional:
        filename: Location of output file.
    """
    course_link = table.select(selector)
    if course_link:
        course_info = table.find_next_sibling("table")
        while course_info:
            if not course_info.has_attr("bgcolor") or course_info["bgcolor"] == "#d3d3d3":
                if sln_only:
                    log.info("Scraping course SLN from time schedule")
                    tokens = course_info.get_text().partition('\r\n')
                    log.info(f"Tokens: {tokens}")

                    sln_field = tokens[0][7:13].strip()
                    sln = sln_field if ">" not in sln_field else sln_field.replace(">", "")

                    course_sln = CourseSLN(quarter, year, sln)
                    output = json.dumps(course_sln.__dict__)
                else:
                    log.info("Scraping entire course from time schedule ")
                    log.info(f"Header row: \"{table.get_text()[1:]}\"")
                    log.info(f"Main row: \"{course_info.get_text()}\"")
                    course_sec = Course(table.get_text()[1:], course_info.get_text(),
                                        quarter, year)
                    output = course_sec.serialize()
                log.info(output)
                if filename:
                    with open(filename, "a") as file:
                        file.write(f"{output}\n")
                else:
                    print(output)
                course_info = course_info.find_next_sibling("table")
            else:
                break
