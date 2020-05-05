import json
import os
from typing import Dict, List, Union

CONFIG_PATH: str = os.path.join(os.path.dirname(__file__), './.config/config.json')
DEFAULT_CONFIG: Dict[str, Union[str, dict]] = {
    "username": "None",
    "password": "None",
    "defaultFlags": {
        "marks": "None",
        "courses": "None"
    }
}
FLAGS: List[str] = ['f', 'w', 'a', 's']


def json_to_dict() -> Dict[str, str]:
    """Returns a dict from config.json, or the default config if config.json dne
    """
    with open(CONFIG_PATH, 'r') as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            config = DEFAULT_CONFIG
    return config


def dict_to_json(config: Dict[str, str] = {}) -> None:
    """
    Writes config to config.json, or creates a default config.json if no arg is provided.
    """
    if not config:
        _ = DEFAULT_CONFIG
    else:
        _ = config
    with open(CONFIG_PATH, 'w') as f:
        json.dump(
            _, f)


def reset_credentials() -> None:
    if os.path.isfile(CONFIG_PATH):
        with open(CONFIG_PATH, 'r+') as f:
            config = json.load(f)

        config['username'] = 'None'
        config['password'] = 'None'
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f)

        print("Credentials successfully deleted.")

    else:
        print("No config.json file found.")


def credentials_not_found(config: Dict[str, str]) -> bool:
    return config.get('username', 'None') == 'None' or config.get('password', 'None') == 'None'


def add_credentials_to_config() -> Dict[str, str]:
    """
    Prompts user for username and password, and adds them to config file at path
    Precondition: path to file is valid 
    """
    username = input("Enter UTORID username: ")
    password = input("Enter password: ")

    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)

    config['username'] = username
    config['password'] = password

    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f)

    print("Credentials saved to config.json.")
    return config


def add_flag_pref() -> None:
    """Prompt the user for a default flag to use and store it in config.json.
    """
    marks_flag = ""
    while marks_flag not in FLAGS:
        marks_flag = input(
            """
            What would you like this program to scrape when no flags are passed?
            Options: 
            \tf: Fall semester marks
            \tw: Winter semester marks
            \ts: Summer semester marks 
            \ta: All semesters
            """
        )

    courses_flag = ""
    while courses_flag not in FLAGS:
        courses_flag = input(
            """
            What would you like this program to scrape when the '-p' flag is used? 
            Options:
            \tf: Fall semester published course pages
            \tw: Winter semester published course pages
            \ts: Summer semester published course pages
            \ta: All semesters
            """
        )

    if not os.path.isfile(CONFIG_PATH):
        dict_to_json()

    config = json_to_dict()
    config["defaultFlags"]['marks'] = marks_flag
    config["defaultFlags"]["courses"] = courses_flag
    dict_to_json(config)
    print("Default behavior changed.")


def parse_config() -> Dict[str, str]:
    """
    Reads the JSON file at path, and generates a dictionary containing config settings.
    If JSON does not exist, creates a new one using user input.
    """
    if not os.path.isfile(CONFIG_PATH):
        dict_to_json()

    config = json_to_dict()
    if credentials_not_found(config):
        config = add_credentials_to_config()

    return config
