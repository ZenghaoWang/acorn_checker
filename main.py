from selenium.webdriver import Chrome, ChromeOptions
from typing import List, Dict

import config as cfg
from args import get_parser
from quercus import print_published_courses
from acorn import print_grades

ACORN_URL: str = 'https://acorn.utoronto.ca'
MARKS_URL: str = 'https://acorn.utoronto.ca/sws/#/history/academic'

QUERCUS_URL: str = 'https://q.utoronto.ca'
COURSES_URL: str = "https://q.utoronto.ca/courses"


def init_browser(url: str) -> Chrome:
    """
    Initializes and returns a headless chrome webDriver at <url>.
    """

    print("Initializing WebDriver...")
    options = ChromeOptions()
    options.add_argument('headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    browser = Chrome(options=options)
    browser.get(url)
    return browser


def login(browser: Chrome, username: str, password: str) -> bool:
    print("Logging in...")
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


def login_loop(browser: Chrome) -> Dict[str, str]:
    while True:
        config = cfg.parse_config()

        successful = login(browser, config['username'], config['password'])

        if successful:
            return config

        else:
            cfg.add_credentials_to_config()


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

    if args.published:
        browser = init_browser(QUERCUS_URL)
        config = login_loop(browser)
        browser.get(COURSES_URL)
        print_published_courses(browser)

    else:
        browser = init_browser(ACORN_URL)
        # Attempt to login until successful
        config = login_loop(browser)

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
