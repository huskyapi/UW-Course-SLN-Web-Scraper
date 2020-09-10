import argparse
import pytest

from scraper.utils import validate_campus_name, validate_quarter_name, \
    validate_course_name, create_time_schedule_url, is_url, get_html

test_data = {
    'quarters': [('autumn2019', 'AUT2019'),
                 ('SPR2019', 'SPR2019'),
                 ('WINTER2020', 'WIN2020')],
    'courses': ['INFO200', 'B PHYS121'],
    'campuses': ['Bothell', 'Tacoma', 'Seattle'],
    'urls': [
        "https://www.google.com",
        "http://example.com",
        "https://www.washington.edu/students/timeschd/"
    ]
}


def test_get_html():
    assert get_html("") is None
    assert get_html("http://www.404simulator.com/") is None
    assert get_html(
        "https://www.washington.edu/students/timeschd/B/AUT2020/css.html"
    ) is not None


@pytest.mark.parametrize("url", test_data['urls'])
def test_is_url(url):
    assert is_url(url)


def test_create_time_schedule_url():
    assert create_time_schedule_url(
        "Bothell", "Autumn2020", "CSS"
    ) == "https://www.washington.edu/students/timeschd/B/AUT2020/css.html"
    assert create_time_schedule_url(
        "Seattle", "SPR2020", "INFO"
    ) == "https://www.washington.edu/students/timeschd/SPR2020/info.html"
    assert create_time_schedule_url(
        "Tacoma", "AUT2020", "TEDNUR"
    ) == "https://www.washington.edu/students/timeschd/T/AUT2020/tednur.html"


@pytest.mark.parametrize("campus", test_data['campuses'])
def test_validate_campus_name(campus):
    validate_campus_name(campus)
    with pytest.raises(argparse.ArgumentTypeError):
        validate_campus_name("Test")


@pytest.mark.parametrize("quarter, expected", test_data['quarters'])
def test_validate_quarter_name(quarter, expected):
    assert validate_quarter_name(quarter) == expected
    with pytest.raises(argparse.ArgumentTypeError):
        validate_quarter_name("Test")


@pytest.mark.parametrize("course", test_data['courses'])
def test_validate_course_name(course):
    validate_course_name(course)
    with pytest.raises(argparse.ArgumentTypeError):
        validate_course_name("Test")
