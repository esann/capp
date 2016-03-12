from flask import jsonify, Flask
import  os
import json
from config import config

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
def load_objects():

    files_list = [f for f in os.listdir(config["obj"]) if os.path.isfile(os.path.join(config["obj"], f))]
    objects = []
    for (file) in files_list:
        content = open(os.path.join(config["obj"], file))
        objects.append(json.load(content))

    return  objects


def save_obj(file_name, content):
    with open(os.path.join(config["obj"], file_name), 'w') as out_file:
        json.dump(content, out_file)


#Сохранение данных текущей конфигурации
def save_config_data():
    current_id = open(os.path.join(config["root_path"], "id_storage"), "w")
    current_id.write(str(config["current_id"]))
    current_id.close()


if __name__ == '__main__':
    init_engine()

    objs = load_objects()

    #
    # data = {'id': 5, 'name': 'this is name', 'content': 'data content'}
    # save_obj("2", data)


    print(objs)

    # hello()
    # flask = Flask(__name__)
    # flask.run()


    save_config_data()