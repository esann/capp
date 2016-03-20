import json

import  os
from config import config
from os import path


def hello():
    data = {'id': 5, 'name': 'this is name', 'content': 'data content'}
    data_compound = {'id': 6, 'content': data}

    print('--- start ---')

    print('start [{0}] end'.format(data))

    #print(jsonify(data))

    print(data_compound)

    #print(jsonify(data_compound))

    print('--- end ---')


#Инициализация движка
def init_engine():
    if not os.path.exists(config["root_path"]):
        os.mkdir(config["root_path"])

    #Мета-информация системы
    config["meta"] = os.path.join(config["root_path"], "meta")
    if not os.path.exists(config["meta"]):
        os.mkdir(config["meta"])


    #Данные объектов
    config["obj"] = os.path.join(config["root_path"], "obj")
    if not os.path.exists(config["obj"]):
        os.mkdir(config["obj"])


    if not os.path.exists(os.path.join(config["root_path"], "id_storage")):
        config["current_id"] = 1;
        current_id = open(os.path.join(config["root_path"], "id_storage"), "w")
        current_id.write(str(config["current_id"]))
        current_id.close()
    else:
        current_id = open(os.path.join(config["root_path"], "id_storage"), "r")
        config["current_id"] = int(current_id.read())
        current_id.close()


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

    files_list = [f for f in os.listdir(config["obj"]) if os.path.isfile(os.path.join(config["obj"], f))]
    objects = []
    for (file) in files_list:
        content = open(os.path.join(config["obj"], file))
        object = json.load(content)
        if check_object_content(object):
            objects.append(object)

    return  objects


def save_obj(file_name, content):
    with open(os.path.join(config["obj"], file_name), 'w') as out_file:
        json.dump(content, out_file)


#Сохранение данных текущей конфигурации
def save_config_data():
    current_id = open(os.path.join(config["root_path"], "id_storage"), "w")
    current_id.write(str(config["current_id"]))
    current_id.close()

    config_for_save = {}
    config_for_save["root_path"] = config["root_path"]
    with open("config.json", "w") as file:
        json.dump(config_for_save, file)


def load_config():
    if path.exists("config.json"):
        with open("config.json", "r") as file:
            config = json.load(file)

import the_object
from the_object import create_empty_object, set_data, add_link,ID, LINKS, DATA, DATATYPE_NAME, DATATYPE_OWNER_LINK
from the_objects import get_the_objects
from config import  get_next_id

def generate_the_objects():
    db_objects = [create_empty_object("a"), \
                  create_empty_object("b"), \
                  create_empty_object("c"), \
                  create_empty_object("d")]
    for o in db_objects:
        yield o

    return

if __name__ == '__main__':
    the_object.test_the_object_module()

    load_config()
    init_engine()

    # objects = [o for o in generate_the_objects()]
    #
    # root_folder_link = create_empty_object(get_next_id(config))
    # set_data(root_folder_link, DATATYPE_OWNER_LINK)
    #
    # root_folder = create_empty_object(get_next_id())
    # add_link(root_folder, root_folder_link[ID], None)
    # set_data(root_folder, DATATYPE_NAME, "root")
    #
    # folder = create_empty_object(get_next_id())
    # add_link(folder, root_folder_link[ID], root_folder[ID])
    # set_data(folder, DATATYPE_NAME, "folder")

    objs = load_objects()
    # for o in objs:
    #     save_obj(o[ID], o)

    roots = get_the_objects(objs, [["689a3761b9234b78bbfb3dabe3aa2987", None]], [])
    roots = get_the_objects(objs, [["5f8b873ccba54376b1fa7c6faaf3f96b", None]], [])

    save_config_data()
    exit()

    # load_config()
    # objs = load_objects()
    # print(objs)

    # flask = Flask(__name__)
    # flask.run()



