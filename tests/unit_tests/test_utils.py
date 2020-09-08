from src.utils import validate_campus_name, validate_course_name, validate_quarter_name, create_time_schedule_url, \
    is_url, get_html

import pytest
import argparse

def test_get_html():
    assert get_html("") is None
    assert get_html("http://www.404simulator.com/") is None
    assert get_html("https://www.washington.edu/students/timeschd/B/AUT2020/css.html") is not None


def test_is_url():
    assert is_url("https://www.google.com")
    assert is_url("http://example.com")
    assert is_url("https://www.washington.edu/students/timeschd/")


def create_time_schedule_url(campus, quarter, department):
    assert create_time_schedule_url("Bothell", "Autumn2020", "CSS") == "https://www.washington.edu/students/timeschd" \
                                                                       "/B/AUT2020/css.html"
    assert create_time_schedule_url("Seattle", "SPR2020", "INFO") == "https://www.washington.edu/students/timeschd" \
                                                                     "/SPR2020/info.html"
    assert create_time_schedule_url("Tacoma", "AUT2020", "TEDNUR") == "https://www.washington.edu/students/timeschd/T" \
                                                                      "/AUT2020/tednur.html "


def test_validate_campus_name():
    with pytest.raises(argparse.ArgumentTypeError):
        validate_campus_name("Test")


def test_validate_quarter_name():
    assert validate_quarter_name('autumn 2019') == 'AUT2019'
    assert validate_quarter_name('SPR2019') == 'SPR2019'
    assert validate_quarter_name('WINTER2020') == 'WIN2020'
    with pytest.raises(argparse.ArgumentTypeError):
        validate_quarter_name("Test")


def test_validate_course_name():
    validate_course_name('INFO200')
    validate_course_name('B PHYS121')
    with pytest.raises(argparse.ArgumentTypeError):
        validate_course_name("Test")
