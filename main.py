import json

import  os
from os import path
import the_object
from the_object import create_empty_object, set_data, add_link,ID, LINKS, DATA, DATATYPE_NAME, DATATYPE_OWNER_LINK, create_empty_object_force
from the_objects import get_the_objects
from config.config import get_next_id, load_config




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


def save_obj(file_name, content):
    with open(os.path.join(_config["obj"], file_name), 'w') as out_file:
        json.dump(content, out_file)


#Сохранение данных текущей конфигурации
#Инициализация движка
def init_engine():
    if not os.path.exists(_config["root_path"]):
        os.mkdir(_config["root_path"])

    #Мета-информация системы
    _config["meta"] = os.path.join(_config["root_path"], "meta")
    if not os.path.exists(_config["meta"]):
        os.mkdir(_config["meta"])

    #Теги системы
    _config["tags"] = os.path.join(_config["meta"], "tags")
    if not os.path.exists(_config["tags"]):
        os.mkdir(_config["tags"])

    #Данные объектов
    _config["obj"] = os.path.join(_config["root_path"], "obj")
    if not os.path.exists(_config["obj"]):
        os.mkdir(_config["obj"])


    if not os.path.exists(os.path.join(_config["root_path"], "id_storage")):
        _config["current_id"] = 1;
        current_id = open(os.path.join(_config["root_path"], "id_storage"), "w")
        current_id.write(str(_config["current_id"]))
        current_id.close()
    else:
        current_id = open(os.path.join(_config["root_path"], "id_storage"), "r")
        _config["current_id"] = int(current_id.read())
        current_id.close()

    #Корневой объект
    isNeedCreateRootObject = False
    try:
        if not os.path.exists(os.path.join(_config["obj"], _config["root_object_id"])):
            isNeedCreateRootObject = True
    except KeyError:
        isNeedCreateRootObject = True

    if isNeedCreateRootObject:
        root_object = create_empty_object_force(get_next_id())
        _config["root_object_id"] = root_object[ID]
        save_obj(root_object[ID], root_object)


    #Ссылка "владелец объекта"
    isNeedCreateOwnerLink = False
    try:
        if not os.path.exists(os.path.join(_config["obj"], _config["owner_link_id"])):
            isNeedCreateOwnerLink = True
    except KeyError:
        isNeedCreateOwnerLink = True

    if isNeedCreateOwnerLink:
        owner_link_id = create_empty_object_force(get_next_id())
        _config["owner_link_id"] = owner_link_id[ID]
        save_obj(owner_link_id[ID], owner_link_id)

    if not os.path.exists(os.path.join(_config["meta"], "root")):
        _config["current_id"] = 1;
        current_id = open(os.path.join(_config["root_path"], "id_storage"), "w")
        current_id.write(str(_config["current_id"]))
        current_id.close()
    else:
        current_id = open(os.path.join(_config["root_path"], "id_storage"), "r")
        _config["current_id"] = int(current_id.read())
        current_id.close()

def save_config_data():
    current_id = open(os.path.join(_config["root_path"], "id_storage"), "w")
    current_id.write(str(_config["current_id"]))
    current_id.close()

    _config_for_save = {}
    _config_for_save["root_path"] = _config["root_path"]
    _config_for_save["root_object_id"] = _config["root_object_id"]
    _config_for_save["owner_link_id"] = _config["owner_link_id"]
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
    root_object_id = _config["root_object_id"]

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
    objs = load_objects()

    roots = get_the_objects(objs, [], [])
    roots = get_the_objects(objs, [], [["ab436a1d56ee4d9b8e0168c04d065e74", None]])

    save_config_data()
    exit()

    # load_config()
    # objs = load_objects()
    # print(objs)

    # flask = Flask(__name__)
    # flask.run()



