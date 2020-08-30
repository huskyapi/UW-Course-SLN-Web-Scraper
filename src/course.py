import json

LIMITS = (7, 6, 3, 8, 18, 14, 27, 9, 9, 9, 5, 6)
LENGTHS = [0, 7, 13, 16, 24, 42, 56, 83, 92, 101, 110, 115, 121]


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Course):
            return obj.__dict__
        return json.JSONEncoder(self, obj)

class Course(object):
    def __init__(self, text):
        tokens = text.partition('\r\n')
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
        self.enrollment_limit = fields[9]
        self.is_crnc = fields[10]
        self.course_fee = fields[11]
        if len(fields) > 12:
            self.special_type = fields[12]

    def serialize(self):
        return json.dumps(self, cls=ComplexEncoder)
