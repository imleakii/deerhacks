import requests
from bs4 import BeautifulSoup


def get_html(course_keyword="", prerequisite="", distribution='All', program_area='All', department='All'):

    URL = "https://utm.calendar.utoronto.ca/course-search?"
    URL += f"course_keyword={course_keyword}&"
    URL += f"field_prerequisite_value={prerequisite}&"
    URL += f"field_distribution_requirements_value={distribution}&"
    URL += f"field_sections_value={program_area}&"
    URL += f"field_department_value={department}&"

    r = requests.get(URL)

    return r

r = get_html(course_keyword="EDS100")
soup = BeautifulSoup(r.content, 'html.parser')
print(soup.prettify())