
from selenium.webdriver import Chrome

from selenium.common.exceptions import NoSuchElementException


MARKS_URL: str = 'https://acorn.utoronto.ca/sws/#/history/academic'

FALL_MARKS_XPATH = '//*[@id="main-content"]/div[2]/div[1]/div/history-academic/div/div[2]/div/div[3]/table/tbody/tr[2]/td/table/tbody'
WINTER_MARKS_XPATH = '/html/body/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/history-academic/div/div[2]/div/div[4]/table/tbody/tr/td/table/tbody'


def print_grades(browser: Chrome, fall: bool = False, winter: bool = False) -> None:
    browser.get(MARKS_URL)
    try:
        if fall:
            fall_table = browser.find_element_by_xpath(
                FALL_MARKS_XPATH)

            print("Fall Semester:")
            for row in fall_table.find_elements_by_class_name('courses'):
                cols = row.find_elements_by_tag_name('td')
                print(
                    f'{cols[0].text}: {cols[3].text if cols[3].text else "No mark available" }')

        if winter:
            winter_table = browser.find_element_by_xpath(
                WINTER_MARKS_XPATH)
            print("Winter Semester:")
            for row in winter_table.find_elements_by_class_name('courses'):
                cols = row.find_elements_by_tag_name('td')
                print(
                    f'{cols[0].text}: {cols[3].text if cols[3].text else "No mark available" }')

    except NoSuchElementException:
        print("An error occured. Please try again.")
        exit()
