import argparse
import re
from collections import namedtuple
from contextlib import closing
from requests import get
from requests.utils import requote_uri
from requests.exceptions import RequestException

TIME_SCHEDULE_URL = "https://www.washington.edu/students/timeschd"
CourseName = namedtuple('CourseName', 'code number name')


def get_html(url):
    print(url)
    try:
        with closing(get(url, stream=True)) as response:
            if is_html(response):
                return response.content
            else:
                return None
    except RequestException as re:
        print(f"There was an error while accessing {url} : {str(re)}")


def is_html(resp):
    '''
        Returns true if response seems to be HTML, false otherwise.
    '''
    content_type = resp.headers["Content-Type"].lower()
    return resp.status_code == 200 and content_type is not None and content_type.find("html") > - 1


def create_time_schedule_url(campus, quarter, course_code):
    url = f'{TIME_SCHEDULE_URL}/{campus}{quarter}/{course_code}.html'
    return requote_uri(url)

def validate_campus_name(string):
    campus = string.lower()
    if (campus != 'tacoma') and (campus != 'seattle') and (campus != 'bothell'):
        msg = f'\"{campus}\" is not a valid UW campus name.'
        raise argparse.ArgumentTypeError(msg)
    if campus == 'tacoma' or campus == 'bothell':
        return f'{campus[:1].upper()}/'
    else:
        return ''


def validate_course_name(string):
    code = re.sub(r"[^A-Za-z]+", '', string).lower()
    number = re.sub(r"[^\d+]", '', string)
    name = f'{code}{number}'

    r = re.compile(r'^[a-zA-Z ]{3,6}\d{3}$')
    if not r.match(name):
        msg = f'\"{string}\" is not a valid course name. (i.e, astbio300, INFO200, B PHYS 121)'
        raise argparse.ArgumentTypeError(msg)

    return CourseName(code, number, name)


def validate_quarter_name(string):
    raw_string = string.replace(" ", "")
    name = f'{raw_string[:3].upper()}{raw_string[-4:]}'

    r = re.compile(r'^(AUT|WIN|SUM|SPR)\d{4}$')
    if not r.match(name):
        msg = f'\"{string}\" is not a valid quarter name. (i.e, autumn 2019, aut2019, spr2000, WIN 2014, SUM2005)'
        raise argparse.ArgumentTypeError(msg)

    return name
