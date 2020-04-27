from selenium.webdriver import Chrome, ChromeOptions
import json
from typing import Dict


def parse_config(path: str) -> Dict[str, str]:
    with open(path) as f:
        config_dict = json.load(f)
        return config_dict


def login(browser, username: str, password: str) -> None:
    username_input = browser.find_element_by_id('username')
    password_input = browser.find_element_by_id('password')
    login_button = browser.find_elements_by_name('_eventId_proceed')[0]

    config = parse_config('config.json')
    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button.click()


def init_browser():
    options = ChromeOptions()
    options.add_argument('headless')
    options.add_argument('log-level=3')

    return Chrome(options=options)


def print_grades(browser) -> None:
    course_table = browser.find_element_by_xpath(
        '/html/body/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/history-academic/div/div[2]/div/div[4]/table/tbody/tr/td/table/tbody')
    for row in course_table.find_elements_by_class_name('courses'):
        cols = row.find_elements_by_tag_name('td')
        print(f'{cols[0].text}: {cols[3].text}')


if __name__ == "__main__":
    browser = init_browser()
    browser.get('https://acorn.utoronto.ca')

    config = parse_config('config.json')
    login(browser, config['username'], config['password'])

    # Printing winter session marks
    browser.get('https://acorn.utoronto.ca/sws/#/history/academic')
    print_grades(browser)

    browser.close()
