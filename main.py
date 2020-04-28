from selenium.webdriver import Chrome, ChromeOptions
from typing import Type

import config as cfg
from args import get_parser

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


def login(browser: Chrome, username: str, password: str) -> bool:
    print("Logging into acorn...")
    username_input = browser.find_element_by_id('username')
    password_input = browser.find_element_by_id('password')
    login_button = browser.find_elements_by_name('_eventId_proceed')[0]

    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button.click()

    if len(browser.find_elements_by_class_name('form-element.form-error')) != 0:
        print("Incorrect credentials.")
        return False

    print("Successfully logged in.")
    return True


def print_grades(browser: Chrome, fall: bool, winter: bool) -> None:
    course_table_winter = browser.find_element_by_xpath(
        '/html/body/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/history-academic/div/div[2]/div/div[4]/table/tbody/tr/td/table/tbody')
    for row in course_table_winter.find_elements_by_class_name('courses'):
        cols = row.find_elements_by_tag_name('td')
        print(
            f'{cols[0].text}: {cols[3].text if cols[3].text else "No mark available" }')


if __name__ == "__main__":
    # Parse command line args
    parser = get_parser()
    args = parser.parse_args()

    if args.reset:
        cfg.reset_credentials(cfg.CONFIG_PATH)
        exit()

    while True:
        config = cfg.parse_config(cfg.CONFIG_PATH)
        browser = init_browser()

        browser.get(ACORN_URL)
        successful = login(browser, config['username'], config['password'])

        # Successful login, continue to scrape grades
        if successful:
            break

        # Credentials are incorrect; Prompt user for credentials
        else:
            cfg.add_credentials_to_config(cfg.CONFIG_PATH)

    # Printing winter session marks
    browser.get(MARKS_URL)
    print_grades(browser, fall=args.fall, winter=args.winter)

    browser.close()
