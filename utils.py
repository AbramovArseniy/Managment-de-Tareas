import os


def clear_console():
    os.system('cls')


import json


def save_to_json_file(obj, file):
    with open(file, 'w+') as file:
        json.dump(obj, file)


def load_from_json(file):
    with open(file, 'r') as file:
        data = json.load(file)
    return data


def choose_id(d, input_msg="Ingrese el Id: "):
    clear_console()
    if len(d) == 0:
        print('No hay elementos adecuados\n')
        return
    page_size = 5
    num_items = len(d)
    i = 0
    cmd = ''
    while cmd not in d.keys():
        for item in list(d.items())[i: min(i + page_size, num_items)]:
            print(f'Id: {item[0]}\n'
                  f'Nombre: {item[1]["name"]}')
            print("---------")

        print(f'Pagina {i // page_size + 1}/{(num_items - 1) // page_size + 1}')
        print('Ingrese:\n'
              'next - Ver proxima pagina\n'
              'prev - Ver pagina previa\n'
              'id - elegir\n')
        cmd = input()

        if cmd == 'next':
            clear_console()
            if i < num_items - page_size:
                i += page_size
            else:
                print('Ya esta en la ultima pagina')
        elif cmd == 'prev':
            clear_console()
            if i >= page_size:
                i -= page_size
            else:
                print('Ya esta en la primera pagina')

        elif cmd in d.keys():
            return cmd
        else:
            clear_console()
            print('Error.\n'
                  'Tiene que ingresar:\n'
                  'next - Ver proxima pagina\n'
                  'prev - Ver pagina previa\n'
                  'id - elegir')


def print_dict(d, filter_func=lambda item: True):
    clear_console()
    filtered_dict = dict(filter(lambda item: int(item[0]) > 0 and filter_func(item), d.items()))
    page_size = 5
    if len(filtered_dict) == 0:
        print('No hay elementos adecuados\n')
        return

    num_items = len(filtered_dict)
    i = 0
    while 0 <= i < num_items:
        for item in list(filtered_dict.items())[i: min(i + page_size, num_items)]:
            print(f'Id: {item[0]}\n'
                  f'Nombre: {item[1]["name"]}')
            print("---------")

        print(f'Pagina {i // page_size + 1}/{(num_items - 1) // page_size + 1}')
        print('Ingrese:\n'
              '1 - Ver proxima pagina\n'
              '2 - Ver pagina previa\n'
              '3 - Continuar')
        cmd = input()
        if cmd not in ('1', '2', '3'):
            clear_console()
            print('Tiene que ingresar un numero entre 1 y 3')
        elif cmd == '1':
            clear_console()
            if i < num_items - page_size:
                i += page_size
            else:
                print('Ya esta en la ultima pagina')
        elif cmd == '2':
            clear_console()
            if i >= page_size:
                i -= page_size
            else:
                print('Ya esta en la primera pagina')
        elif cmd == '3':
            return
