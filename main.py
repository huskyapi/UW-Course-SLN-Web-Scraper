#!/usr/bin/env python

import sys
import logging
from scraper.scraper import get_courses_by_department

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(levelname)-8s '
           '[%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)

log = logging.getLogger(__name__)

SEASONS = ["AUTUMN"]
YEARS = ["2007"]
DEPARTMENT = "CSS"
CAMPUS = "Bothell"
OUTPUT_FILE = "courses.json"

if "container-mode" in sys.argv:
    log.info("INFO - ENVIRONMENT: Running on a docker container.")

log.info("Starting web scraper...")
for s in SEASONS:
    for y in YEARS:
        log.info(f"Getting courses for {DEPARTMENT} in {s}{y} at {CAMPUS}...")
        get_courses_by_department(CAMPUS, s, y, DEPARTMENT, OUTPUT_FILE)
log.info("Scraping complete! See {OUTPUT_FILE} for results.")
