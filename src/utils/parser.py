'''
Handles course data. (More description later)
'''

from collections import namedtuple
import json

TIME_SCHEDULE_URL = "https://www.washington.edu/students/timeschd"
FIELDS=('is_restricted', 'sln', 'section_id', 'credits', 'meeting_times', 'room',
        'instructor', 'status', 'enrollment', 'enrollment_limit', 'is_crnc', 'course_fee', 'special_type')

FIELD_LIMITS=(7, 6, 3, 8, 18, 14, 27, 9, 9, 9, 5, 6)
FIELD_SLICES=[0, 7, 13, 16, 24, 42, 56, 83, 92, 101, 110, 115, 121]

Course = namedtuple('Course', FIELDS, defaults=(None,) * len(FIELDS))
def create_time_schedule_url(campus, quarter, course_code):
    return f'{TIME_SCHEDULE_URL}/{campus}{quarter}/{course_code}.html'

def parse_course(text):
    parts = text.partition('\r\n')
    description = " ".join(parts[2].split())
    unparsed_fields = parts[0]
    fields = [ unparsed_fields[i:j].strip() for i, j in zip(FIELD_SLICES, FIELD_SLICES[1:])]
    return Course(*fields, description)



