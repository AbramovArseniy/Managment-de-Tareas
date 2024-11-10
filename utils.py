import os
import utils


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


def choose_id(d,  input_msg = "Ingrese el Id: "):
    utils.clear_console()
    print_dict(d, lambda task: int(task[0]) > 0)
    id = input(input_msg)
    while id not in d.keys():
        print("Id no es valido")
        id = input("Ingrese el Id: ")
    return id

def print_dict(d, filter_func=lambda item: True):
    utils.clear_console()
    filtered_dict = dict(filter(filter_func, d.items()))
    if len(filtered_dict) == 0:
        print('No hay elementos adecuados\n')
        return

    num_items = len(filtered_dict)
    i = 0
    while i >= 0 and i < num_items:
        for item in list(filtered_dict.items())[i: min(i + 10, num_items)]:
            print(f'Id: {item[0]}\n'
            f'Nombre: {item[1]["name"]}')
            print("---------")
        print(f'Pagina {i // 10 + 1}/{(num_items - 1) // 10 + 1}')
        print('Ingrese:\n'
        '1. Ver proxima pagina\n'
        '2. Ver pagina previa\n'
        '3. Continuar')
        cmd = input()
        if cmd not in ('1', '2', '3'):
            utils.clear_console()
            print('Tiene que ingresar un numero entre 1 y 3')
        elif cmd == '1':
            utils.clear_console()
            if i < num_items - 10:
                i += 10
            else:
                print('Ya esta en la ultima pagina')
        elif cmd == '2':
            utils.clear_console()
            if i >= 10:
                i -= 10
            else:
                print('Ya esta en la primera pagina')
        elif cmd == '3':
            return
