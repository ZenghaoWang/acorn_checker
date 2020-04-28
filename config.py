import json
import os
from typing import Dict

CONFIG_PATH: str = 'config.json'
DEFAULT_CONFIG: Dict[str, str] = {
    "username": "None", "password": "None", "flag": "None"}


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
        _ = {"username": "None", "password": "None", "flag": "None"}
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
    flag = ""
    while flag not in ['f', 'w', 'a']:
        flag = input(
            """What would you like this program to scrape when no flags are passed?
            Options: 
            \tf: Fall semester marks
            \tw: Winter semester marks
            \ta: Both semesters
        """)

    if not os.path.isfile(CONFIG_PATH):
        dict_to_json()

    config = json_to_dict()
    config["flag"] = flag
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
