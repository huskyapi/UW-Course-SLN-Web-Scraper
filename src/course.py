import json
import re

LIMITS = (7, 6, 3, 8, 18, 14, 27, 9, 9, 9, 5, 6)
LENGTHS = [0, 7, 13, 16, 24, 42, 56, 83, 92, 101, 110, 115, 121]


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Course):
            return obj.__dict__
        return json.JSONEncoder(self, obj)

class Course(object):
    def __init__(self, preface, section, quarter, year):
        preface = re.sub("Prerequisites(.*)$", "", preface)
        gen_ed = re.search("\((.*?)\)", preface)
        if gen_ed:
            gen_ed = gen_ed.group(0)[1:][:-1]
        else:
            gen_ed = ""
        preface = re.sub("\((.*)$", "", preface)
        code, number, name = preface.split(maxsplit=2)

        self.name = name
        self.code = code
        self.number = number
        self.quarter = quarter
        self.year = year
        self.gen_ed_marker = gen_ed

        tokens = section.partition('\r\n')
        fields = [tokens[0]
                  [start:end].strip()
                  for start, end in zip(LENGTHS, LENGTHS[1:])]

        self.description = " ".join(tokens[2].split())
        self.is_restricted = fields[0]
        self.sln = fields[1]
        self.section_id = fields[2]
        self.credits = fields[3]
        self.meeting_times = fields[4]
        self.room = fields[5]
        self.instructor = fields[6]
        self.status = fields[7]
        self.enrollment = fields[8]
        self.is_crnc = fields[9]
        self.course_fee = fields[10]
        self.special_type = fields[11]

    def serialize(self):
        return json.dumps(self, cls=ComplexEncoder)
