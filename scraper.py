import requests
from bs4 import BeautifulSoup


def get_courses(course_keyword="", prerequisite="", distribution='All', program_area='All', department='All', page='0'):

    URL = "https://utm.calendar.utoronto.ca/course-search?"
    URL += f"course_keyword={course_keyword}&"
    URL += f"field_prerequisite_value={prerequisite}&"
    URL += f"field_distribution_requirements_value={distribution}&"
    URL += f"field_sections_value={program_area}&"
    URL += f"field_department_value={department}&"
    URL += f"page={page}&"

    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('div', class_='view-content')
    courses_raw = s.find_all('div', class_="views-row")
    
    courses = []

    for i in range(0, len(courses_raw), 2):
        course_raw = courses_raw[i]
        info_raw = courses_raw[i+1]

        # extract course code and title
        line = [l.strip() for l in course_raw.find('div', {'aria-label': True}).get_text(strip=True).split("•")]
        code, title = line

        desc = info_raw.find('div', class_="views-field-field-desc").get_text(strip=True)
        
        prereqs = info_raw.find('span', class_="views-field-field-prerequisite")
        if prereqs:
            prereqs = prereqs.get_text(strip=True)
        else:
            prereqs = ''
        
        exclusions = info_raw.find('span', class_="views-field-field-exclusion")
        if exclusions:
            exclusions = exclusions.get_text(strip=True)
        else:
            exclusions = ''        

        preparation = info_raw.find('span', class_="views-field-field-recommended-preparation")
        if preparation:
            preparation = preparation.get_text(strip=True)
        else:
            preparation = 'noneee'

        course = {
            'course_code': code,
            'name': title,
            'description': desc,
            'prerequisites': prereqs,
            'exclusions': exclusions,
            'preparation': preparation,
        }
        courses.append(course)
    
    # recursively call function until reach last page of results
    if len(courses) == 30:
        new_page = str(int(page) + 1)
        courses += get_courses(course_keyword, prerequisite, distribution, program_area, department, new_page)
    return courses


# courses = get_courses(course_keyword="MAT13")
# for c in courses:
#     print(c)
