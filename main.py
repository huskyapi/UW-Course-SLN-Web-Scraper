from scraper.scraper import get_courses_by_department, get_course

SEASONS = ["AUTUMN", "WINTER", "SPRING", "SUMMER"]
"""
YEARS = ["2003", "2004", "2005", "2006", "2007", "2008",
         "2009", "2010", "2011", "2012", "2013", "2014", "2015",
         "2016", "2017", "2018", "2019", "2020"]
"""
YEARS = ["2018", "2019", "2020"]
DEPARTMENT = "CSS"
CAMPUS = "Bothell"
OUTPUT_FILE = "courses.json"

print("Starting web scraper...")
for s in SEASONS:
    for y in YEARS:
        print(f"\tGetting courses for {DEPARTMENT} in {s}{y} at {CAMPUS}...")
        get_courses_by_department(CAMPUS, s, y, DEPARTMENT, OUTPUT_FILE)
print(f"Scraping complete! See {OUTPUT_FILE} for results.")
