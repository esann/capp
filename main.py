import json

import  os
from config import config
from os import path
from the_objects import get_the_objects


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

import  the_object

if __name__ == '__main__':
    the_object.test_the_object_module()
    for o in get_the_objects():
        print(o)

    # load_config()
    # init_engine()
    # objs = load_objects()
    # print(objs)
    # save_config_data()

    # flask = Flask(__name__)
    # flask.run()



