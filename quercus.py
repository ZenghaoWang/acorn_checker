from selenium.webdriver import Chrome


COURSES_URL: str = "https://q.utoronto.ca/courses"


def is_published(row, semester: str) -> bool:
    text = row.text
    return semester in text and "This course has been published" in text


def print_published_courses(browser: Chrome, semester: str) -> None:
    browser.get(COURSES_URL)
    table = browser.find_element_by_id("my_courses_table")
    rows: list = table.find_elements_by_class_name("course-list-table-row")
    published: list = list(
        filter(lambda row: is_published(row, semester), rows))

    print("Published courses:")
    for course in published:
        print(course.text.split('\n')[1].split(' ')[0])
