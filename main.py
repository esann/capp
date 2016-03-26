import json

import  os
from os import path
import the_object
from the_object import create_empty_object, set_data, add_link,ID, LINKS, DATA, DATATYPE_NAME, \
                       DATATYPE_OWNER_LINK, create_empty_object_force, set_name, save_obj
from the_objects import get_the_objects
from config.config import get_next_id, load_config
from config.config import ROOT_PATH, ROOT_OBJECT_ID, OWNER_LINK_ID, DATA_TYPE_LINK_ID, DATA_LINK_ID, NAME_LINK_ID



def hello():
    data = {'id': 5, 'name': 'this is name', 'content': 'data content'}
    data_compound = {'id': 6, 'content': data}

    print('--- start ---')

    print('start [{0}] end'.format(data))

    #print(jsonify(data))

    print(data_compound)

    #print(jsonify(data_compound))

    print('--- end ---')


#Загрузка данных по объектам
def check_object_content(object) -> bool:
    if object is None:
        return False

    try:
        if not "id" in object:
            return False

        if not "links" in object:
            return False

        if not "data" in object:
            return False

    except TypeError:
        return False


    return True


def load_objects():

    files_list = [f for f in os.listdir(_config["obj"]) if os.path.isfile(os.path.join(_config["obj"], f))]
    objects = []
    for (file) in files_list:
        content = open(os.path.join(_config["obj"], file))
        object = json.load(content)
        if check_object_content(object):
            objects.append(object)

    return  objects


def check_special_id_in_config(config, special_id_name) -> bool:
    is_need_create_special_object = False
    try:
        if not os.path.exists(os.path.join(config["obj"], config[special_id_name])):
            is_need_create_special_object = True
    except KeyError:
        is_need_create_special_object = True

    if is_need_create_special_object:
        root_object = create_empty_object_force(get_next_id())
        config[special_id_name] = root_object[ID]
        save_obj(_config, root_object)

    return is_need_create_special_object


#Сохранение данных текущей конфигурации
#Инициализация движка
def init_engine():
    if not os.path.exists(_config[ROOT_PATH]):
        os.mkdir(_config[ROOT_PATH])

    #Мета-информация системы
    _config["meta"] = os.path.join(_config[ROOT_PATH], "meta")
    if not os.path.exists(_config["meta"]):
        os.mkdir(_config["meta"])

    #Данные объектов
    _config["data"] = os.path.join(_config[ROOT_PATH], "data")
    if not os.path.exists(_config["data"]):
        os.mkdir(_config["data"])

    #Теги системы
    _config["tags"] = os.path.join(_config["meta"], "tags")
    if not os.path.exists(_config["tags"]):
        os.mkdir(_config["tags"])

    #Данные объектов
    _config["obj"] = os.path.join(_config[ROOT_PATH], "obj")
    if not os.path.exists(_config["obj"]):
        os.mkdir(_config["obj"])


    if not os.path.exists(os.path.join(_config[ROOT_PATH], "id_storage")):
        _config["current_id"] = 1;
        current_id = open(os.path.join(_config[ROOT_PATH], "id_storage"), "w")
        current_id.write(str(_config["current_id"]))
        current_id.close()
    else:
        current_id = open(os.path.join(_config[ROOT_PATH], "id_storage"), "r")
        _config["current_id"] = int(current_id.read())
        current_id.close()

    #Корневой объект
    check_special_id_in_config(_config, ROOT_OBJECT_ID)
    # isNeedCreateRootObject = False
    # try:
    #     if not os.path.exists(os.path.join(_config["obj"], _config[ROOT_OBJECT_ID])):
    #         isNeedCreateRootObject = True
    # except KeyError:
    #     isNeedCreateRootObject = True
    #
    # if isNeedCreateRootObject:
    #     root_object = create_empty_object_force(get_next_id())
    #     _config[ROOT_OBJECT_ID] = root_object[ID]
    #     save_obj(root_object[ID], root_object)

    #Ссылка "тип объекта"
    check_special_id_in_config(_config, DATA_TYPE_LINK_ID)

    #Ссылка "название объекта"
    check_special_id_in_config(_config, NAME_LINK_ID)

    #Ссылка "данные объекта"
    check_special_id_in_config(_config, DATA_LINK_ID)

    #Ссылка "владелец объекта"
    check_special_id_in_config(_config, OWNER_LINK_ID)
    # isNeedCreateOwnerLink = False
    # try:
    #     if not os.path.exists(os.path.join(_config["obj"], _config[OWNER_LINK_ID])):
    #         isNeedCreateOwnerLink = True
    # except KeyError:
    #     isNeedCreateOwnerLink = True
    #
    # if isNeedCreateOwnerLink:
    #     owner_link_id = create_empty_object_force(get_next_id())
    #     _config[OWNER_LINK_ID] = owner_link_id[ID]
    #     save_obj(owner_link_id[ID], owner_link_id)

    # if not os.path.exists(os.path.join(_config["meta"], "root")):
    #     _config["current_id"] = 1;
    #     current_id = open(os.path.join(_config[ROOT_PATH], "id_storage"), "w")
    #     current_id.write(str(_config["current_id"]))
    #     current_id.close()
    # else:
    #     current_id = open(os.path.join(_config[ROOT_PATH], "id_storage"), "r")
    #     _config["current_id"] = int(current_id.read())
    #     current_id.close()

def save_config_data():
    current_id = open(os.path.join(_config[ROOT_PATH], "id_storage"), "w")
    current_id.write(str(_config["current_id"]))
    current_id.close()

    _config_for_save = {}
    _config_for_save[ROOT_PATH] = _config[ROOT_PATH]
    _config_for_save[ROOT_OBJECT_ID] = _config[ROOT_OBJECT_ID]
    _config_for_save[OWNER_LINK_ID] = _config[OWNER_LINK_ID]
    _config_for_save[DATA_TYPE_LINK_ID] = _config[DATA_TYPE_LINK_ID]
    _config_for_save[DATA_LINK_ID] = _config[DATA_LINK_ID]
    with open("config.json", "w") as file:
        json.dump(_config_for_save, file)


def generate_the_objects():
    db_objects = [create_empty_object(get_next_id(), _config, root_object_id), \
                  create_empty_object(get_next_id(), _config, root_object_id), \
                  create_empty_object(get_next_id(), _config, root_object_id), \
                  create_empty_object(get_next_id(), _config, root_object_id)]
    for o in db_objects:
        yield o

    return

_config = {}
root_object_id = None

if __name__ == '__main__':

    _config = load_config()
    init_engine()
    root_object_id = _config[ROOT_OBJECT_ID]

    the_object.test_the_object_module(_config)
    # objects = [o for o in generate_the_objects()]
    #
    # root_folder_link = create_empty_object(get_next_id(), _config)
    # set_data(root_folder_link, DATATYPE_OWNER_LINK)
    #
    # root_folder = create_empty_object(get_next_id(), _config)
    # add_link(root_folder, root_folder_link[ID], None)
    # set_data(root_folder, DATATYPE_NAME, "root")
    #
    # folder = create_empty_object(get_next_id(), _config)
    # add_link(folder, root_folder_link[ID], root_folder[ID])
    # set_data(folder, DATATYPE_NAME, "folder")
    #
    # for o in objects:
    #     save_obj(o[ID], o)
    #

    # folder_main__A = create_empty_object(get_next_id(), _config)
    # set_name(_config, folder_main__A, "Main folder")
    # save_obj(_config, folder_main__A)
    #
    # sub_folder__A_B = create_empty_object(get_next_id(), _config, folder_main__A[ID])
    # set_name(_config, sub_folder__A_B, "Sub folder 1")
    # save_obj(_config, sub_folder__A_B)
    #
    # sub_folder2__A_C = create_empty_object(get_next_id(), _config, folder_main__A[ID])
    # set_name(_config, sub_folder2__A_C, "Sub folder 2")
    # save_obj(_config, sub_folder2__A_C)
    #
    # sub_folder__A_C_D = create_empty_object(get_next_id(), _config, sub_folder2__A_C[ID])
    # set_name(_config, sub_folder__A_C_D, "Sub folder 3")
    # save_obj(_config, sub_folder__A_C_D)

    sub_folder__B_C = get_the_objects(load_objects(), [[_config[OWNER_LINK_ID], "0ac0ad7094fc4911b9feb1c26440cd52"]], [])

    save_config_data()
    exit()

    # load_config()
    # objs = load_objects()
    # print(objs)

    # flask = Flask(__name__)
    # flask.run()



