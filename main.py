from selenium.webdriver import Chrome, ChromeOptions
from typing import List, Dict

import config as cfg
from args import get_parser
from quercus import print_published_courses
from acorn import print_grades

ACORN_URL: str = 'https://acorn.utoronto.ca'

QUERCUS_URL: str = 'https://q.utoronto.ca'


def init_browser() -> Chrome:
    """
    Initializes and returns a headless chrome webDriver 
    """

    print("Initializing WebDriver...")
    options = ChromeOptions()
    options.add_argument('headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    return Chrome(options=options)


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


def login_loop(browser: Chrome, url: str) -> Dict[str, str]:
    browser.get(url)
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

    if args.published:  # Get published courses
        browser = init_browser()
        config = login_loop(browser, QUERCUS_URL)
        if args.fall:
            semester = "Fall"
        elif args.winter:
            semester = "Winter"
        elif args.summer:
            semester = "Summer"
        else:
            fl = config['defaultFlags']['courses']
            if fl == 'None':
                semester = ""
            elif fl == "w":
                semester = "Winter"
            elif fl == "s":
                semester = "Summer"
            elif fl == "f":
                semester = "Fall"
        print_published_courses(browser, semester)

    else:  # Scrape marks
        browser = init_browser()
        # Attempt to login until successful
        config = login_loop(browser, ACORN_URL)

        fl = config['defaultFlags']['marks']
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
            elif fl == "s":
                print_grades(browser, summer=True)
            else:
                print_grades(browser, fall=True, winter=True, summer=True)

        else:
            print_grades(browser, fall=(args.all or args.fall),
                         winter=(args.all or args.winter), summer=(args.all or args.summer))

    browser.quit()
