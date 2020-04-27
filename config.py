import json
import os
from typing import Dict
CONFIG_PATH = 'config.json'


def credentials_not_found(config: Dict[str, str]) -> bool:
    return config.get('username', 'None') == 'None' or config.get('password', 'None') == 'None'


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
