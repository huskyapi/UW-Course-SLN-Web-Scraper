'''
Utility file that validates input arguments.
12/17/2019
'''

import argparse
import re
from collections import namedtuple

Course = namedtuple('Course', 'code number name')


def campus_name(string):
    campus = string.lower()
    if (campus != 'tacoma') and (campus != 'seattle') and (campus != 'bothell'):
        msg = f'\"{campus}\" is not a valid UW campus name.'
        raise argparse.ArgumentTypeError(msg)
    if  campus == 'tacoma' or campus == 'bothell':
        return f'{campus[:1]}/'
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
