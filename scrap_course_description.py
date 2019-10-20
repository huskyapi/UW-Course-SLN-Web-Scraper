#!/usr/bin/python3
from bs4 import BeautifulSoup
from urllib.request import urlopen
from argparse import ArgumentParser

parser = argparse.ArgumentParser()


# args: course name, quarter, campus
# search for specific quarter
# search back multiple quarters


time_schedule_link = f'https://.www.washington.edu/students/timeschd/B/.../~.html'


with urlopen('https://www.washington.edu/students/timeschd/B/AUT2019/stmath.html') as response:
    soup = BeautifulSoup(response, 'html.parser')

    # Find table with a link with the name we want
    for table in soup.find_all('table'):
        for link in table.select('a[name]'):
            if (link['name'] == 'stmath390'):
                course_description = table.find_next_sibling('table')
                while(not course_description.has_attr('bgcolor') or course_description['bgcolor'] == '#d3d3d3'):
                    print(course_description.get_text())
                    course_description = course_description.find_next_sibling('table')