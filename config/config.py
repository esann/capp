_config = {"root_path": "c:\\data\\"}

import  uuid
from os import path
import json

def get_next_id() -> str:
    return uuid.uuid4().hex

def load_config():
    if path.exists("config.json"):
        with open("config.json", "r") as file:
            return json.load(file)
    else:
        return _config

