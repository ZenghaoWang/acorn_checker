
from selenium.webdriver import Chrome

from selenium.common.exceptions import NoSuchElementException


MARKS_URL: str = 'https://acorn.utoronto.ca/sws/#/history/academic'

FALL_MARKS_XPATH = '//*[@id="main-content"]/div[2]/div[1]/div/history-academic/div/div[2]/div/div[3]/table/tbody/tr[2]/td/table/tbody'
WINTER_MARKS_XPATH = '//*[@id="main-content"]/div[2]/div[1]/div/history-academic/div/div[2]/div/div[4]/table/tbody/tr[2]/td/table/tbody'
SUMMER_MARKS_XPATH = '//*[@id="main-content"]/div[2]/div[1]/div/history-academic/div/div[2]/div/div[5]/table/tbody/tr/td/table/tbody'


def print_grades_helper(table) -> None:
    courses = table.find_elements_by_class_name('courses')
    for row in courses:
        cols = row.find_elements_by_tag_name('td')
        print(
            f'{cols[0].text}: {cols[3].text if cols[3].text else "No mark available" }'
        )


def print_grades(browser: Chrome, fall: bool = False, winter: bool = False, summer: bool = False) -> None:
    browser.get(MARKS_URL)
    try:
        if fall:
            fall_table = browser.find_element_by_xpath(FALL_MARKS_XPATH)
            print("Fall Semester Marks:")
            print_grades_helper(fall_table)

        if winter:
            winter_table = browser.find_element_by_xpath(WINTER_MARKS_XPATH)
            print("Winter Semester Marks:")
            print_grades_helper(winter_table)

        if summer:
            summer_table = browser.find_element_by_xpath(SUMMER_MARKS_XPATH)
            print("Summer Semester Marks:")
            print_grades_helper(summer_table)

    except NoSuchElementException:
        print("An error occured. Please try again.")
        exit()
