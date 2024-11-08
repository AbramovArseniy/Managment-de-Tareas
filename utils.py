import os


def clear_console():
    os.system('cls')


import json


def save_to_json_file(object, file):
    with open(file, 'w+') as file:
        json.dump(object, file)


def load_from_json(file):
    with open(file, 'r') as file:
        data = json.load(file)
    return data
