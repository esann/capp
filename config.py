config = {"root_path": "c:\\data\\"}

import  uuid

def get_next_id(config = None) -> str:
    return uuid.uuid4().hex