_config = {"root_path": "c:\\data\\"}

import  uuid
from os import path
import json

ROOT_PATH = "root_path"
OBJECTS_PATH = "obj"

ROOT_OBJECT_ID = "root_object_id"
OWNER_LINK_ID = "owner_link_id"
DATA_TYPE_LINK_ID = "data_type_link_id"
DATA_LINK_ID = "data_link_id"
NAME_LINK_ID = "name_link_id"

#from config import ROOT_PATH, ROOT_OBJECT_ID, OWNER_LINK_ID, DATA_TYPE_LINK_ID, DATA_LINK_ID, NAME_LINK_ID, OBJECTS_PATH


def get_next_id() -> str:
    return uuid.uuid4().hex

def load_config():
    if path.exists("config.json"):
        with open("config.json", "r") as file:
            return json.load(file)
    else:
        return _config

