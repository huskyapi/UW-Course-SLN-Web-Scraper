
'''
Misc utility functions.
'''
from contextlib             import closing
from requests               import get
from requests.utils         import requote_uri
from requests.exceptions    import RequestException

TIME_SCHEDULE_URL = "https://www.washington.edu/students/timeschd"


def get_html(url):
    print(url)
    try:
        with closing(get(url, stream = True)) as response:
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
    return (resp.status_code == 200 and content_type is not None and content_type.find("html") > - 1)

def create_time_schedule_url(campus, quarter, course_code):
    url = f'{TIME_SCHEDULE_URL}/{campus}{quarter}/{course_code}.html'
    return requote_uri(url)
