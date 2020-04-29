from selenium.webdriver import Chrome


def is_published(row) -> bool:
    text = row.text
    return "Summer" in text and "This course has been published" in text


def print_published_courses(browser: Chrome) -> None:
    table = browser.find_element_by_id("my_courses_table")
    rows: list = table.find_elements_by_class_name("course-list-table-row")
    published: list = list(filter(is_published, rows))

    print("Published courses:")
    for course in published:
        print(course.text.split('\n')[1].split(' ')[0])
