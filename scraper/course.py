import json
import re
import requests

LIMITS = (7, 6, 3, 8, 18, 14, 27, 9, 9, 9, 5, 6)
LENGTHS = [0, 7, 13, 16, 24, 42, 56, 83, 92, 101, 110, 115, 121]


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Course):
            return obj.__dict__
        return json.JSONEncoder(self, obj)


class InstructorFallback(object):
    """
        Created when the Faculty API fails to retrieve
        teacher information.
    """

    def __init__(self, first_name, middle_name, last_name):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name


class Room(object):
    """
        Organizes room information into following:
        building code, and room number.
        Ex. 'UW1' and '020'
    """

    def __init__(self, building_code, room_number):
        self.building_code = building_code
        self.room_number = room_number


class Course(object):
    def __init__(self, header_row, main_row, quarter, year):
        self.parse_header_row(header_row, quarter, year)
        tokens = main_row.partition('\r\n')
        self.description = " ".join(tokens[2].split())

        fields = [tokens[0]
                  [start:end].strip()
                  for start, end in zip(LENGTHS, LENGTHS[1:])]
        self.parse_main_row(tokens, fields)

    def parse_header_row(self, header_row, quarter, year):
        """
        Parses the header row text of a course section table of
        the UW Time Schedule.
        """
        header_row = re.sub("Prerequisites(.*)$", "", header_row)
        gen_ed = re.search("\\((.*?)\\)", header_row)
        if gen_ed:
            gen_ed = gen_ed.group(0)[1:][:-1]
        else:
            gen_ed = ""

        header_row = re.sub("\\((.*)$", "", header_row)
        code, number, name = header_row.split(maxsplit=2)
        self.name = name
        self.code = code
        self.number = number
        self.quarter = quarter
        self.year = year
        self.gen_ed_marker = gen_ed

    def parse_main_row(self, tokens, fields):
        """
        Parses the main row text of a course section table
        from the UW Time Schedule.
        """
        self.is_restricted = fields[0]
        self.sln = fields[1] if ">" not in fields[1] else \
            fields[1].replace(">", "")
        self.section_id = fields[2]
        self.credits = fields[3]
        meeting_times = ' '.join(fields[4].split())
        self.parse_meeting_times(meeting_times)

        self.room = self.parse_location(fields[5])
        pos = 0
        if "Open" in fields[6]:
            pos = fields[6].index("Open")
        elif "Closed" in fields[6]:
            pos = fields[6].index("Closed")
        self.instructor = ' '.join(fields[6][0:pos].split()) \
            if pos != 0 else fields[6]
        if len(self.instructor) == 0:
            self.instructor = 'No instructor assigned.'
        else:
            self.instructor = self.retrieve_instructor_object(
                self.instructor)
        self.status = fields[7]
        split_enroll = fields[8].replace(" ", "").split("/")
        self.parse_enrollment(split_enroll)
        self.is_crnc = fields[9]
        self.course_fee = fields[10]
        self.special_type = fields[11]

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
            self.meeting_days = re.findall(
                "[A-Z][a-z]{0,1}[a-z]{0,1}", meeting_times[0])
            self.meeting_time_start = list(meeting_times[1].split('-')[0])
            self.meeting_time_start.insert(-2, ":")
            self.meeting_time_start = ''.join(self.meeting_time_start)
            self.meeting_time_end = list(meeting_times[1].split('-')[1])
            if "P" in self.meeting_time_end:  # TODO: Check for morning
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
            self.currently_enrolled = int(split_enroll[0])
            self.enrollment_limit = int(split_enroll[1])
        else:
            self.currently_enrolled = 0
            self.enrollment_limit = 0

    def retrieve_instructor_object(self, instructor_name):
        """
        Parse a teacher's name, make a get request
        to the UW Faculty/Staff API, and retrieve an
        extended object of the teacher's information.

        API Info: http://www.uwfaculty-lmao.tk/
        """

        instructor_name.replace(' ', '%20').replace(',', ' ')
        first_name = instructor_name.split(',')[1].split(' ')[0]
        last_name = instructor_name.split(',')[0]
        if len(instructor_name.split(',')[1].split(' ')) > 1:
            middle_name = instructor_name.split(',')[1].split(' ')[1]
        else:
            middle_name = ""

        # TODO: Enhance performance. Only way to search is by full name ATM.
        instructor = requests.get(
            'http://www.uwfaculty-lmao.tk/faculty/api/v1/'
            + first_name + " " + middle_name + "" + last_name)
        if '"error":"Bad request"' in instructor.text:
            instructor = requests.get(
                'http://www.uwfaculty-lmao.tk/faculty/api/v1/'
                + first_name + " " + last_name)

        if instructor.status_code > 200 or \
                '"error":"Bad request"' in instructor.text:
            instructor = InstructorFallback(
                first_name, middle_name, last_name).__dict__
        else:
            instructor = instructor.json()

        return instructor

    def parse_location(self, location_full):
        """
        Parse a course's room into
        a building code and room number.
        If there is none, "To Be Arranged" is added.
        """

        if "*    *" in location_full or len(location_full) == 0:
            return "To Be Arranged"
        else:
            location_split = re.sub(r'[*]', '', location_full).strip().split(' ')
            if len(location_split)>1:
                while("" in location_split):
                    location_split.remove("")
                return Room(location_split[0].strip(),
                            location_split[1].strip()).__dict__
            else:
                return location_split[0]

    def serialize(self):
        return json.dumps(self, cls=ComplexEncoder)
