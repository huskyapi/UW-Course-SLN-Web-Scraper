'''
Handles course data. (More description later)
'''

from collections import namedtuple
from schema import Schema


import re
import json

fields=('sln',    'section',           'credits',      'days',
        'time', 'building_abbr', 'room_number',      'instructor',   'status',
        'enrolled_students', 'max_students', 'description')

Course = namedtuple('Course', fields, defaults=(None,) * len(fields))

def parse_course(text):
    parts = text.strip().partition('\n')
    description = " ".join(parts[2].split())
    attributes = re.split('\s\s+', parts[0].strip())


    # for attr in attributes:
    #    if not re.fullmatch(r'[a-zA-Z,. ]+', attr) and ' ' in attr:
    #        pos = attributes.index(attr)
    #        elem1, elem2 = attr.split()
    #        attributes[pos:pos + 1] = (elem1, elem2)
    sln = attributes[0] or None
    return Course(*attributes, description)

def get_csv(course):
    # course._fields - gets the fields of a namedtuple
    # zip() - makes a pairwise matched tuple
    for elem, field in zip(course, course._fields):
        print(elem, field)

# https://stackoverflow.com/questions/5906831/serializing-a-python-namedtuple-to-json
def get_json(course):
    # course._asdict() - serializes a namedtuple as dict
    # this only serializes one course
    # what if we want to return a file with many namedtuples at once?
    print(json.dumps(course._asdict()))

