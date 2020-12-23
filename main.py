#!/usr/bin/env python

import logging

logging.getLogger("urllib3").setLevel(logging.WARNING)
from scraper.scraper import get_courses_by_department

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(levelname)-8s '
           '[%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)

log = logging.getLogger(__name__)

SEASONS = ["AUTUMN", "WINTER", "SPRING", "SUMMER"]
YEARS = ["2003", "2004", "2005", "2006", "2007", "2008",
         "2009", "2010", "2011", "2012", "2013", "2014", "2015",
         "2016", "2017", "2018", "2019", "2020"]
DEPARTMENT = "CSS"
CAMPUS = "Bothell"

SLN_ONLY = True

log.info("Starting web scraper...")
for s in SEASONS:
    for y in YEARS:
        if not SLN_ONLY:
            log.info(f"Getting courses for {DEPARTMENT} in {s}{y} at {CAMPUS}...")
            get_courses_by_department(CAMPUS, s, y, DEPARTMENT, "courses.json", False)
        else:
            log.info(f"Getting course SLNs for {DEPARTMENT} in {s}{y} at {CAMPUS}...")
            get_courses_by_department(CAMPUS, s, y, DEPARTMENT, "course_sln.json", True)
