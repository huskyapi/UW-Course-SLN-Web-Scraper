'''
Handles course data. (More description later)
'''

from collections import namedtuple

import re

Course = namedtuple('Course', 'sln section credits days time building_abbr room_number instructor ' 
                    'status enrolled_students max_students description')

def parse_course(text):
    parts = text.strip().partition('\n')
    description = " ".join(parts[2].split())
    attributes = re.split('\s\s+', parts[0].strip())
    for attr in attributes:
        if not re.fullmatch(r'[a-zA-Z, ]+', attr) and ' ' in attr:
            pos = attributes.index(attr)
            elem1, elem2 = attr.split()
            attributes[pos:pos + 1] = (elem1, elem2)
    return Course(*attributes, description)

def get_csv(course):
    pass

def get_json(course):
    pass

