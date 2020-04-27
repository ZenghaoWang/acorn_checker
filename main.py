from selenium.webdriver import Chrome, ChromeOptions
import json
import os
from typing import Dict

CONFIG_PATH = 'config.json'


def credentials_not_found(config: Dict[str, str]) -> bool:
    return config.get('username', 'None') == 'None' or config.get('password', 'None') == 'None'


def init_browser():
    """
    Initializes and returns a headless chrome webDriver.
    """
    print("Initializing WebDriver...")
    options = ChromeOptions()
    options.add_argument('headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    return Chrome(options=options)


def add_credentials_to_config(path: str) -> Dict[str, str]:
    """
    Prompts user for username and password, and adds them to config file at path
    Precondition: path to file is valid 
    """
    username = input("Enter UTORID username: ")
    password = input("Enter password: ")

    with open(path, 'r+') as f:
        config = json.load(f)

    config['username'] = username
    config['password'] = password

    with open(path, 'w') as f:
        json.dump(config, f)

    print("Credentials saved to config.json.")
    return config


def parse_config(path: str) -> Dict[str, str]:
    """
    Reads the JSON file at path, and generates a dictionary containing config settings.
    If JSON does not exist, creates a new one using user input.
    """
    if not os.path.isfile(path):
        with open(path, 'x') as f:
            json.dump({"username": "None", "password": "None"}, f)

    with open(path, 'r+') as f:
        config = json.load(f)
        if credentials_not_found(config):
            config = add_credentials_to_config(path)

    return config


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
        print(f'{cols[0].text}: {cols[3].text}')


if __name__ == "__main__":

    while True:
        config = parse_config(CONFIG_PATH)
        browser = init_browser()

        browser.get('https://acorn.utoronto.ca')
        successful = login(browser, config['username'], config['password'])

        # Successful login, continue to scrape grades
        if successful:
            break

        # Credentials are incorrect; Prompt user for credentials
        else:
            add_credentials_to_config(CONFIG_PATH)

    # Printing winter session marks
    browser.get('https://acorn.utoronto.ca/sws/#/history/academic')
    print_grades(browser)

    browser.close()
