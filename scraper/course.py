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
    def parse_meeting_times(self, meeting_times):
            # Parse meeting times into day arguments, starting time, and ending time
        if "to be arranged" in meeting_times:
            self.meeting_days = ["TBD"]
            self.meeting_time_start = "TBD"
            self.meeting_time_end = "TBD"
        else:
            meeting_times = meeting_times.split(' ')
            self.meeting_days = re.findall(
                "[A-Z][a-z]{0,1}[a-z]{0,1}", meeting_times[0])
            self.meeting_time_start = list(meeting_times[1].split('-')[0])
            self.meeting_time_start.insert(-2, ":")
            self.meeting_time_start = ''.join(self.meeting_time_start)
            self.meeting_time_end = list(meeting_times[1].split('-')[1])
            if ("P" in self.meeting_time_end):  # TODO: Check for morning
                self.meeting_time_end.insert(-3, ":")
                self.meeting_time_end.insert(-1, "M")
            else:
                self.meeting_time_end.insert(-2, ':')
            self.meeting_time_end = ''.join(self.meeting_time_end)

    def parse_enrollment(self, split_enroll):
        enrollment_codes = ['E', 'C']

        # Parse enrollment field to 2 separate JSON numbers
        if len(split_enroll) > 1:
            for code in enrollment_codes:
                split_enroll[1] = split_enroll[1].replace(code, "")
            self.currently_enrolled = int(split_enroll[0])
            self.enrollment_limit = int(split_enroll[1])
        else:
            self.currently_enrolled = 0
            self.enrollment_limit = 0

    def __init__(self, preface, section, quarter, year):
        preface = re.sub("Prerequisites(.*)$", "", preface)
        gen_ed = re.search("\\((.*?)\\)", preface)
        if gen_ed:
            gen_ed = gen_ed.group(0)[1:][:-1]
        else:
            gen_ed = ""

        preface = re.sub("\\((.*)$", "", preface)
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
        self.sln = fields[1] if ">" not in fields[1] else \
            fields[1].replace(">", "")
        self.section_id = fields[2]
        self.credits = fields[3]
        meeting_times = ' '.join(fields[4].split())
        self.room = fields[5]
        pos = 0
        if "Open" in fields[6]:
            pos = fields[6].index("Open")
        elif "Closed" in fields[6]:
            pos = fields[6].index("Closed")
        self.instructor = ' '.join(fields[6][0:pos].split()) \
            if pos != 0 else fields[6]
        if len(self.instructor) == 0:
            self.instructor = 'No instructor assigned.'
        self.status = fields[7]
        split_enroll = fields[8].replace(" ", "").split("/")
        self.is_crnc = fields[9]
        self.course_fee = fields[10]
        self.special_type = fields[11]

        self.parse_meeting_times(meeting_times)
        self.parse_enrollment(split_enroll)

    def serialize(self):
        return json.dumps(self, cls=ComplexEncoder)
