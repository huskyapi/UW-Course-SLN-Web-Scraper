import json
import re

from scraper.instructor import retrieve_instructor_object
from scraper.room import parse_location
from scraper.special import parse_special_types

LIMITS = (7, 6, 3, 8, 18, 14, 27, 9, 9, 9, 5, 6)
LENGTHS = [0, 7, 13, 16, 24, 42, 56, 83, 92, 101, 110, 115, 121]


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Course):
            return obj.__dict__
        return json.JSONEncoder(self, obj)


class Course():
    def __init__(self, header_row, main_row, quarter, year):
        self.name = ""
        self.code = ""
        self.number = 0
        self.quarter = ""
        self.year = ""
        self.gen_ed_marker = ""
        self.description = ""
        self.is_restricted = ""
        self.sln = ""
        self.section_id = ""
        self.credits = ""
        self.room = ""
        self.meeting_days = ""
        self.meeting_time_start = ""
        self.meeting_time_end = ""
        self.enrollment_limit = ""
        self.currently_enrolled = ""
        self.instructor = ""
        self.status = ""
        self.is_crnc = False
        self.course_fee = ""
        self.special_type = ""

        self.parse_header_row(header_row, quarter, year)
        tokens = main_row.partition('\r\n')
        self.description = " ".join(tokens[2].split())

        fields = [tokens[0]
                  [start:end].strip()
                  for start, end in zip(LENGTHS, LENGTHS[1:])]
        self.parse_main_row(fields)

    def parse_header_row(self, header_row, quarter, year):
        """
        Parses the header row text of a course section table of
        the UW Time Schedule.
        """
        header_row = re.sub("Prerequisites(.*)$", "", header_row)
        gen_ed = re.search("\\((.*?)\\)", header_row)
        if gen_ed:
            self.gen_ed_marker = gen_ed.group(0)[1:][:-1]
        else:
            self.gen_ed_marker = ""

        header_row = re.sub("\\((.*)$", "", header_row)
        self.code, self.number, self.name = header_row.split(maxsplit=2)
        self.quarter, self.year, = quarter, year

    def parse_main_row(self, fields):
        """
        Parses the main row text of a course section table
        from the UW Time Schedule.
        """
        self.is_restricted = fields[0]
        self.sln = fields[1] if ">" not in fields[1] else fields[1].replace(">", "")
        self.section_id = fields[2]
        self.credits = fields[3]
        meeting_times = ' '.join(fields[4].split())
        self.parse_meeting_times(meeting_times)

        # Checks if there's a 'status' inside the field where it's usually in

        self.room = parse_location(fields[5])

        pos = 0
        if "Open" in fields[6]:
            pos = fields[6].index("Open")
        elif "Closed" in fields[6]:
            pos = fields[6].index("Closed")

        self.instructor = ' '.join(fields[6][0:pos].split()) if pos != 0 else fields[6]
        if len(self.instructor) == 0:
            self.instructor = 'No instructor assigned.'
        else:
            self.instructor = retrieve_instructor_object(self.instructor)

        """
            Splits fields with info in the format: "SHOOPA,M    Closed    1/ 42'
            To: ["SHOOPA, M", Closed, and "1/  42"]
            and appends them in the right order of 'fields'
        """
        if "" in fields[7] or "CR/NC" in fields[7]:
            split_nit_combo = fields.pop(6).split()
            if split_nit_combo[1] == "" and len(split_nit_combo) > 2:
                # Splits names like "LUFFY MONKEY D."
                split_nit_combo[0] = split_nit_combo[0] + split_nit_combo[2]
                split_nit_combo.remove(split_nit_combo[1])
                split_nit_combo.remove(split_nit_combo[1])
            split_nit_combo.reverse()
            for attr in split_nit_combo:
                fields.insert(6, attr)
            fields[8] = fields[8] + fields[9]
            fields.pop(9)
            if not self.status_in_right_field(fields, 7):
                fields.insert(7, "")

        self.status = fields[7]
        split_enroll = fields[8].replace(" ", "").split("/")
        self.split_joined_enroll_crnr(fields)
        self.parse_enrollment(split_enroll)
        self.is_crnc = self.check_for_crnc(fields)
        self.course_fee = fields[10]
        try:
            self.special_type = parse_special_types(fields[11])
        except IndexError:
            self.special_type = ""

    def status_in_right_field(self, fields, num):
        return "Open" in fields[num] or "Closed" in fields[num]

    def split_joined_enroll_crnr(self, fields):
        # Splits fields like " 1/ 42CR/NC"
        if "CR/NC" in fields[8]:
            fields[8] = fields[8].replace("CR/NC", "")
            fields.insert(9, "CR/NC")
            fields.remove(fields[10])

    def check_for_crnc(self, fields):
        if "CR/NC" in fields[9]:
            return True

        # Combines the course fee text in case of no 'CR/NC'.
        if "$" in fields[9]:
            fields.insert(9, False)
            fields[10] = fields[10] + fields[11]
            fields.remove(fields[11])
            return False

    def parse_meeting_times(self, meeting_times):
        """
            Parse meeting times into following:
            day arguments, starting time, and ending time
            Input: meeting_times string fed from __init__
        """
        if "to be arranged" in meeting_times:
            self.meeting_days = ["TBD"]
            self.meeting_time_start = "TBD"
            self.meeting_time_end = "TBD"
        else:
            meeting_times = meeting_times.split(' ')
            self.meeting_days = re.findall("[A-Z][a-z]?[a-z]?", meeting_times[0])
            self.meeting_time_start = list(meeting_times[1].split('-')[0])
            self.meeting_time_start.insert(-2, ":")
            self.meeting_time_start = ''.join(self.meeting_time_start)
            self.meeting_time_end = list(meeting_times[1].split('-')[1])
            if "P" in self.meeting_time_end:
                self.meeting_time_end.insert(-3, ":")
                self.meeting_time_end.append("M")
            else:
                self.meeting_time_end.insert(-2, ':')
            self.meeting_time_end = ''.join(self.meeting_time_end)

    def parse_enrollment(self, split_enroll):
        """
        Parse enrollment field to 2 separate JSON numbers
        Input: split_enroll string array fed from __init__
        Output: currently_enrolled: 15, enrollment_limit: 30
        """
        enrollment_codes = ['E', 'C']

        if len(split_enroll) > 1:
            for code in enrollment_codes:
                split_enroll[1] = split_enroll[1].replace(code, "")
            try:
                self.currently_enrolled = int(split_enroll[0])
                self.enrollment_limit = int(split_enroll[1])
            except ValueError:
                return
        else:
            self.currently_enrolled = 0
            self.enrollment_limit = 0

    def serialize(self):
        return json.dumps(self, cls=ComplexEncoder)
