import pick

import utils
from src.datos import people
from src.people.people import create_person
from utils import clear_console


def authorization():
    clear_console()
    print("¡Bienvenido al programa de gestión de tareas!")

    actions = {
        'Ingreso': sing_in,
        'Registrarme': create_person,

    }
    session = None
    while session is None:
        input_msg = "Elija que quiere hacer"
        options = list(actions.keys())
        act, act_num = pick.pick(options, input_msg, indicator='=>')
        session = actions[act]()
        if session is not None:
            return session


def sing_in():
    clear_console()
    print("Autenticación")
    login = input("Ingrese su login o -1 para volver al inicio: ")
    logins = [person['login'] for person in people.values()]

    while login not in logins and login != '-1':
        print("No existe un usuario con este login")
        login = input("Ingrese su login o -1 para volver al inicio: ")
    if login == '-1':
        return None
    person_id = None
    for id in people.keys():
        if people[id]['login'] == login:
            person_id = id

    password = input("Ingrese su contraseña:")
    if password != people[person_id]['password']:
        print("Ingresaste una contraseña incorrecta.")
        input("Presiona Enter para continuar...")
        return None

    return {'id': person_id}

def log_out():
    opt, ind = pick.pick(['Si', 'No'], '¿Esta seguro que quiere cerrar session?', indicator='>=')
    if ind == 0:
        close_session()
    else:
        return 0

def close_session():
    utils.save_to_json_file({}, "src/session.json")