import os
import pick


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


def choose_id(d, input_msg="Ingrese el Id: ", filter_func=lambda item: True):
    filtered_dict = dict(filter(lambda item: int(item[0]) > -1 and filter_func(item), d.items()))
    clear_console()

    if len(filtered_dict) == 0:
        print('No hay elementos adecuados\n')
        return
    page_size = 5
    num_items = len(filtered_dict)
    i = 0
    cmd = ''
    while cmd not in filtered_dict.keys():
        options = []
        j = 1
        printed_items = list(filtered_dict.items())[i: min(i + page_size, num_items)]
        for item in list(filtered_dict.items())[i: min(i + page_size, num_items)]:
            options.append(f'{j}.{item[1]["name"]}')
            j += 1
        if i >= page_size:
            options.append('Ver pagina previa')
        if i < num_items - page_size:
            options.append('Ver proxima pagina')
        page_msg = f'Pagina {i // page_size + 1}/{(num_items - 1) // page_size + 1}'
        option, index = choose(options, input_msg + '\n' + page_msg, indicator='=>')

        if option == 'Ver proxima pagina':
            clear_console()
            i += page_size
        elif option == 'Ver pagina previa':
            clear_console()
            i -= page_size
        elif index == len(options):
            return '-1'
        else:
            return printed_items[index][0]


def print_dict(d, filter_func=lambda item: True):
    clear_console()
    filtered_dict = dict(filter(lambda item: int(item[0]) > 0 and filter_func(item), d.items()))
    page_size = 5
    if len(filtered_dict) == 0:
        print('No hay elementos adecuados\n')
        input("Presiona Enter para continuar...")
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
              '3 - Volver al inicio')
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


def choose(options, title, indicator='=>'):
    options.append('Volver al inicio')
    return pick.pick(options, title, indicator)


def get_session():
    return load_from_json("src/session.json")

