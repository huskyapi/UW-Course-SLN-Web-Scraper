from scraper import get_courses_by_department

SEASONS = ["AUTUMN", "WINTER", "SPRING", "SUMMER"]
YEARS = ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]
DEPARTMENT = "CSS"
CAMPUS = "Bothell"
OUTPUT_FILE = "courses.json"

for s in SEASONS:
    for y in YEARS:
        get_courses_by_department(CAMPUS, s, y, DEPARTMENT, OUTPUT_FILE)

