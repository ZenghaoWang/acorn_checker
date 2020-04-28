from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import NoSuchElementException
from typing import List

import config as cfg
from args import get_parser

ACORN_URL: str = 'https://acorn.utoronto.ca'
MARKS_URL: str = 'https://acorn.utoronto.ca/sws/#/history/academic'

FALL_MARKS_XPATH = '//*[@id="main-content"]/div[2]/div[1]/div/history-academic/div/div[2]/div/div[3]/table/tbody/tr[2]/td/table/tbody'
WINTER_MARKS_XPATH = '/html/body/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/history-academic/div/div[2]/div/div[4]/table/tbody/tr/td/table/tbody'


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


def print_grades(browser: Chrome, fall: bool = False, winter: bool = False) -> None:
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


if __name__ == "__main__":
    # Parse command line args
    parser = get_parser()
    args = parser.parse_args()

    if args.config:
        cfg.add_flag_pref()
        exit()

    if args.reset:
        cfg.reset_credentials()
        exit()

    while True:
        config = cfg.parse_config()
        browser = init_browser()

        browser.get(ACORN_URL)
        successful = login(browser, config['username'], config['password'])

        # Successful login, continue to scrape grades
        if successful:
            break

        # Credentials are incorrect; Prompt user for credentials
        else:
            cfg.add_credentials_to_config()

    browser.get(MARKS_URL)

    fl = config['flag']
    # No flags
    # If default flag stored in config, use that.
    # Otherwise, print all
    if not any(vars(args).values()):
        if fl == "f":
            print_grades(browser, fall=True)
        elif fl == "w":
            print_grades(browser, winter=True)
        elif fl == "a":
            print_grades(browser, fall=True, winter=True)
        else:
            print_grades(browser, fall=True, winter=True)

    else:
        print_grades(browser, fall=(args.all or args.fall),
                     winter=(args.all or args.winter))

    browser.close()
