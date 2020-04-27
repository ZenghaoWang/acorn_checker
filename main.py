from selenium.webdriver import Chrome, ChromeOptions
from typing import Type
from config import *

ACORN_URL: str = 'https://acorn.utoronto.ca'
MARKS_URL: str = 'https://acorn.utoronto.ca/sws/#/history/academic'


def init_browser() -> Chrome:
    """
    Initializes and returns a headless chrome webDriver.
    """

    print("Initializing WebDriver...")
    options = ChromeOptions()
    options.add_argument('headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    return Chrome(options=options)


def login(browser, username: str, password: str) -> bool:
    print("Logging into acorn...")
    username_input = browser.find_element_by_id('username')
    password_input = browser.find_element_by_id('password')
    login_button = browser.find_elements_by_name('_eventId_proceed')[0]

    config = parse_config('config.json')
    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button.click()

    if len(browser.find_elements_by_class_name('form-element.form-error')) != 0:
        print("Incorrect credentials.")
        return False

    print("Successfully logged in.")
    return True


def print_grades(browser) -> None:
    course_table = browser.find_element_by_xpath(
        '/html/body/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/history-academic/div/div[2]/div/div[4]/table/tbody/tr/td/table/tbody')
    for row in course_table.find_elements_by_class_name('courses'):
        cols = row.find_elements_by_tag_name('td')
        print(
            f'{cols[0].text}: {cols[3].text if cols[3].text else "No mark available" }')


if __name__ == "__main__":

    while True:
        config = parse_config(CONFIG_PATH)
        browser = init_browser()

        browser.get(ACORN_URL)
        successful = login(browser, config['username'], config['password'])

        # Successful login, continue to scrape grades
        if successful:
            break

        # Credentials are incorrect; Prompt user for credentials
        else:
            add_credentials_to_config(CONFIG_PATH)

    # Printing winter session marks
    browser.get(MARKS_URL)
    print_grades(browser)

    browser.close()
