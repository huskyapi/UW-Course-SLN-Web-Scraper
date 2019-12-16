import argparse
import re
from collections import namedtuple

Course = namedtuple('Course', 'code number name')


def campus_name(string):
    if (string != 'Tacoma') and (string != 'Seattle') and (string != 'Bothell'):
        msg = f'\"{string}\" is not a valid UW campus name.'
        raise argparse.ArgumentTypeError(msg)
    if string == 'Tacoma' or string == 'Bothell':
        return f'{string[:1]}/'
    else:
        return ''


def course_name(string):
    code = re.sub(r"[^A-Za-z]+", '', string).lower()
    number = re.sub(r"[^\d+]", '', string)
    name = f'{code}{number}'

    r = re.compile(r'^[a-zA-Z ]{3,6}\d{3}$')
    if not r.match(name):
        msg = f'\"{string}\" is not a valid course name. (i.e, astbio300, INFO200, B PHYS 121)'
        raise argparse.ArgumentTypeError(msg)

    return Course(code, number, name)


def quarter_name(string):
    raw_string = string.replace(" ", "")
    name = f'{raw_string[:3].upper()}{raw_string[-4:]}'

    r = re.compile(r'^(AUT|WIN|SUM|SPR)\d{4}$')
    if not r.match(name):
        msg = f'\"{string}\" is not a valid quarter name. (i.e, autumn 2019, aut2019, spr2000, WIN 2014, SUM2005)'
        raise argparse.ArgumentTypeError(msg)

    return name
