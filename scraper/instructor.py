import requests


class InstructorFallback():
    """
        Created when the Faculty API fails to retrieve
        teacher information.
    """

    def __init__(self, first_name, middle_name, last_name):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name


def retrieve_instructor_object(instructor_name):
    """
    Parse a teacher's name, make a get request
    to the UW Faculty/Staff API, and retrieve an
    extended object of the teacher's information.

    API Info: http://www.uwfaculty-lmao.tk/
    """

    instructor_name.replace(' ', '%20').replace(',', ' ')
    instructor_name_tokens = instructor_name.split(',')
    if len(instructor_name_tokens) > 1:
        first_name = instructor_name_tokens[1].split(' ')
    else:
        return ""
    if len(first_name) > 1:
        first_name = instructor_name_tokens[0]
    last_name = instructor_name_tokens[0]
    if len(first_name) > 1:
        middle_name = first_name[1]
    else:
        middle_name = ""

    instructor = requests.get(f"http://www.uwfaculty-lmao.tk/faculty/api/v1/"
                              f"{first_name} {middle_name}{last_name}")
    if '\"error\":\"Bad request\"' in instructor.text:
        instructor = requests.get(f"http://www.uwfaculty-lmao.tk/faculty/api/v1/"
                                  f"{first_name} {last_name}")
    if instructor.status_code > 200 or '\"error\":\"Bad request\"' in instructor.text:
        instructor = InstructorFallback(first_name, middle_name, last_name).__dict__
    else:
        instructor = instructor.json()

    return instructor
