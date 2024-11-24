import pick

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
    login = input("ingrese su login: ")
    logins = [person['login'] for person in people.values()]

    if login not in logins:
        print("No existe un usuario con este login")
        input("Presiona Enter para continuar...")
        return None
    person = None
    for person in people.values():
        if person['login'] == login:
            person = person

    password = input("Ingrese su contraseña:")
    if password != person['password']:
        print("Ingresaste una contraseña incorrecta.")
        input("Presiona Enter para continuar...")
        return None

    return person
