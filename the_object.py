# #структура объекта
# {id: UID,
# links: [{link_id: LINK_REF, object_id: OBJECT_REF}],
#  data: {data_type: DATATYPE, content: CONTENT}
# }
#
# UID: String #уникальный строковый идентификатор в виде строки, например, GUID
# LINK_REF: UID #Ссылка на объект-ссылку
# OBJECT_REF: UID #Ссылка на объект
# DATATYPE: String #Тип данных
# CONTENT: String #Данные: ссылка на файл, гиперссылка, текст и т.п. Интерпретация зависит от DATATYPE

from common import UserError
from config.config import ROOT_OBJECT_ID, OWNER_LINK_ID, DATA_TYPE_LINK_ID, DATA_LINK_ID, OBJECTS_PATH, get_next_id, NAME_LINK_ID
import json
import os

ID = "id"
LINKS = "links"
DATA = "data"

DATATYPE_NAME = "name"
DATATYPE_OWNER_LINK = "owner_link"


def create_object(config, uid, owner_id, data_type_id, data_id):
    obj = create_empty_object_force(uid)
    if owner_id is None:
        add_link(obj, config[OWNER_LINK_ID], config[ROOT_OBJECT_ID])
    else:
        add_link(obj, config[OWNER_LINK_ID], owner_id)

    if data_type_id is not None:
        add_link(obj, config[DATA_TYPE_LINK_ID], data_type_id)

    if data_id is not None:
        add_link(obj, config[DATA_LINK_ID], data_id)

    return obj


def create_empty_object_force(uid):
    the_object = {"id": uid, LINKS: [], "data": {}}
    return the_object


def create_empty_object(uid, config, owner_id = None):
    # the_object = {"id": uid, LINKS: [{"abs": "def"}], "data": {"datatype": "text", "content": "hello"}}
    # the_object = {"id": uid, LINKS: [], "data": {"datatype": "text", "content": "hello"}}
    the_object = {"id": uid, LINKS: [], "data": {}}
    if owner_id == None:
        setOwner(config, the_object, config["root_object_id"])
    else:
        setOwner(config, the_object, owner_id)
    return the_object


def set_name(config, the_object, name: str):
    name_obj = create_empty_object(get_next_id(), config, the_object[ID])
    setOwner(config, name_obj, the_object[ID])
    set_data(name_obj, DATATYPE_NAME, name)
    save_obj(config, name_obj, name_obj[ID])
    add_unique_link(the_object, config[NAME_LINK_ID], name_obj[ID])
    pass


def save_obj(config, obj, file_name = None):
    if file_name is None:
        with open(os.path.join(config[OBJECTS_PATH], obj[ID]), 'w') as out_file:
            json.dump(obj, out_file)
    else:
        with open(os.path.join(config[OBJECTS_PATH], file_name), 'w') as out_file:
            json.dump(obj, out_file)


def setOwner(config, object, owner_id):
    add_unique_link(object, config[OWNER_LINK_ID], owner_id)


def add_link(object, link_id, object_id):
    if not ({link_id, object_id} in object[LINKS]):
        object[LINKS].append([link_id, object_id])
    return


def add_unique_link(object, link_id, object_id):
    for l in object[LINKS][:]:
        if l[0] == link_id:
            object[LINKS].remove(l)

    add_link(object, link_id, object_id)
    return


def remove_link(object, link_id, object_id):
    object[LINKS].remove([link_id, object_id])
    return


def link_exists(object, link_id, object_id) -> bool:
    try:
        return [link_id, object_id] in object[LINKS]
    except:
        return False


def links_exists(object, links) -> bool:
    try:
        if links == []:
            if object[LINKS] == links:
                return True
            else:
                return False
        for l in links:
            if not link_exists(object, l[0], l[1]):
                return False;
        return True
    except:
        return False


def set_data(object, datatype, content = None):
    object["data"] = {"data_type": datatype, "content": content}
    return

def test_the_object_module(config):
    # test create_empty_object

    try:
        empty = create_empty_object()
        raise ValueError("Test: No parameter in create_empty_object")
    except TypeError as e:
        pass

    obj = create_empty_object("abc", config, None)
    if not (obj["id"] == "abc"):
        raise ValueError("TEST: Key not equals with create_empty_object argument")

    #ссылки не пустые, т.к. объект ссылается на root_object
    if (obj[LINKS] == []):
        raise ValueError("TEST: Links empty for create_empty_object result")

    if not (obj["data"] == {}):
        raise ValueError("TEST: Data not empty for create_empty_object result")

    # TEST: add_link
    add_link(obj, "abc", "def")

    try:
        if (["abc", "def"] in obj[LINKS]):
            pass
    except:
        raise ValueError("TEST: Link not added with add_link")

    if (["abc", "defg"] in obj[LINKS]):
        raise ValueError("TEST: add_link adds unknown link")

    # TEST: link_exists
    if not link_exists(obj, "abc", "def"):
        raise ValueError("TEST: link_exists fail (link exists)")

    if link_exists(obj, "abc", "defg"):
        raise ValueError("TEST: link_exists fail (link not exists)")

    add_link(obj, "def", "ghi");
    add_link(obj, "jkl", "mno");

    if links_exists(obj, [["jkl", "mnop"]]):
        raise UserError("TEST: links_exists fail (link not exists)")

    if not links_exists(obj, [["jkl", "mno"], ["abc", "def"]]):
        raise UserError("TEST: links_exists fail (link exists)")

    # TEST: remove_link

    try:
        remove_link(obj, "abcd", "def")
        raise UserError("TEST: remove_link removes non-existing link")
    except ValueError:
        pass

    remove_link(obj, "abc", "def")
    if link_exists(obj, "abc", "def"):
        raise ValueError("TEST: remove_link does not removes existing link")

    return
