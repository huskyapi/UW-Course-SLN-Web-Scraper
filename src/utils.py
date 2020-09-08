import argparse
import re
from collections import namedtuple
from contextlib import closing
from requests import get, Response
from requests.utils import requote_uri
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout

TIME_SCHEDULE_URL = "https://www.washington.edu/students/timeschd"
CourseName = namedtuple('CourseName', 'code number name')


def get_html(url):
    """
        Returns an HTML response from the given URL.
    """
    try:
        with closing(get(url, stream=True)) as response:
            if is_html(response):
                return response.content
            else:
                return None
    except HTTPError as http_err:
        print(f"HTTP error while accessing {url} : {str(http_err)}")
    except ConnectionError as connection_err:
        print(f"Error connecting to {url} : {str(connection_err)}")
    except Timeout as timeout_err:
        print(f"Timeout error while accessing {url} : {str(timeout_err)}")
    except RequestException as request_err:
        print(f"There was an unknown error while accessing {url} : {str(request_err)}")


def is_html(resp):
    """
        Returns true if response seems to be HTML, false otherwise.
    """
    if not isinstance(resp, Response):
        return False
    content_type = resp.headers["Content-Type"].lower()
    return resp.status_code == 200 and content_type is not None and content_type.find("html") > - 1


def is_url(url):
    """
        Returns true if the given URL is a valid URL.
        Source: https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None


def create_time_schedule_url(campus, quarter, department):
    """
        Returns a URL for the UW Time Schedule for the given quarter and campus.
    """
    quarter = validate_quarter_name(quarter)
    campus = validate_campus_name(campus)
    department = department.lower()
    url = f'{TIME_SCHEDULE_URL}/{campus}{quarter}/{department}.html'
    if not is_url(url):
        msg = f'Generated URL is an invalid URL. Given arguments are invalid: {campus}, {quarter}, {department}'
        raise ValueError(msg)
    return requote_uri(url)


def validate_campus_name(string):
    """
        Validates that the given string is a valid UW campus name.
        Raises an ArgumentTypeError if it is not.
    """
    campus = string.lower()
    if (campus != 'tacoma') and (campus != 'seattle') and (campus != 'bothell'):
        msg = f'\"{campus}\" is not a valid UW campus name.'
        raise argparse.ArgumentTypeError(msg)
    if campus == 'tacoma' or campus == 'bothell':
        return f'{campus[:1].upper()}/'
    else:
        return ''


def validate_course_name(string):
    """
        Validates that the given string is a valid UW course.
        Raises an ArgumentTypeError if it is not.
    """
    code = re.sub(r"[^A-Za-z]+", '', string).lower()
    number = re.sub(r"[^\d+]", '', string)
    name = f'{code}{number}'

    r = re.compile(r'^[a-zA-Z ]{3,6}\d{3}$')
    if not r.match(name):
        msg = f'\"{string}\" is not a valid course name. (i.e, astbio300, INFO200, B PHYS 121)'
        raise argparse.ArgumentTypeError(msg)

    return CourseName(code, number, name)


def validate_quarter_name(string):
    """
        Validates that the given string is a valida UW quarter.
        Raises an ArgumentTypeError if it is not.
    """
    raw_string = string.replace(" ", "")
    name = f'{raw_string[:3].upper()}{raw_string[-4:]}'

    r = re.compile(r'^(AUT|WIN|SUM|SPR)\d{4}$')
    if not r.match(name):
        msg = f'\"{string}\" is not a valid quarter name. (i.e, autumn 2019, aut2019, spr2000, WIN 2014, SUM2005)'
        raise argparse.ArgumentTypeError(msg)

    return name
