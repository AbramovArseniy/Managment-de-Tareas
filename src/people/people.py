import time
import utils
from src.datos import *  # Importamos todos los objetos de datos.py

# Constantes para definir roles de usuario
USER_ROLE_ADMIN = 0
USER_ROLE_TEAM_LEAD = 1
USER_ROLE_DEV = 2

roles = ['Administrador',  # Rol de administrador
         'Team lead',      # Rol de líder del equipo
         'Desarrollador']  # Rol de desarrollador


def create_person():
    """
        Crea una nueva persona solicitando al usuario el nombre, apellido, rol y edad.

        Luego, añade la persona creada a la lista global 'people'.

        Returns:
            dict: La persona creada.
    """
    utils.clear_console()
    try:
        # Solicitar el nombre completo
        name = input('Ingrese su nombre completo o -1 para volver al inicio: ')
        while len(name) < 3 and name != '-1':
            print("Error. La longitud del nombre debe ser mayor o igual a 3")
            name = input('Ingrese su nombre completo o -1 para volver al inicio: ')
        if name == '-1':
            return None

        # Seleccionar un rol para la persona
        opt, role = utils.choose(roles, 'Elija su rol')
        if opt == utils.GO_BACK_STR:
            return None
        ok = False
        age = 0

        # Validar la edad
        while not ok:
            try:
                age = int(input('Ingrese su edad o -1 para volver al inicio: '))
                if age == -1:
                    return None
                if age < 18 or age > 80:
                    print("La edad debe ser entre 18 y 80")
                else:
                    ok = True
            except ValueError:
                print("La edad debe ser un número")

        # Validar y solicitar login único
        logins = [person['login'] for person in people.values()]
        login = input('Ingrese su login o -1 para volver al inicio: ')
        while (len(login) < 3 and login != '-1') or login in logins:
            if len(login) < 3:
                print("Error. La longitud del login debe ser mayor o igual a 3")
            else:
                print("Error. Este login ya está en uso. Por favor, ingrese otro.")
            login = input('Ingrese su login o -1 para volver al inicio: ')
        if login == '-1':
            return None

        # Solicitar contraseña
        password = input("Ingrese su contraseña o -1 para volver al inicio:")
        if password == '-1':
            return None

        # Calcular el próximo ID disponible para la nueva persona
        people_next_id = 1
        if len(people.keys()) != 0:
            people_next_id = max(map(int, people.keys())) + 1

        # Crear el objeto de la persona
        person = new_person(name, age, login, password)
        people[str(people_next_id)] = person

        # Manejar solicitudes de roles si el rol no es desarrollador
        if role != USER_ROLE_DEV:
            role_req_next_id = 1
            if len(role_requests.keys()) != 0:
                role_req_next_id = max(map(int, role_requests.keys())) + 1
            role_requests[role_req_next_id] = {
                "role": role,
                "person_id": str(people_next_id),
                "name": f'{name}. Rol: {roles[role]}',
            }

        print('Persona es guardada\n')
        input("Presiona Enter para continuar...")
        return {'id': str(people_next_id)}
    except Exception as e:
        print(e)
        print("Error al agregar la persona")
        input("Presiona Enter para continuar...")


def new_person(name, age, login, password):
    """
        Crea un diccionario con los detalles de una persona.

        Returns:
            dict: Diccionario que contiene los datos de la persona.
    """
    utils.clear_console()
    person = {
        'name': name,       # Nombre de la persona
        'age': age,         # Edad de la persona
        'role': USER_ROLE_DEV,  # Rol predeterminado (Desarrollador)
        'login': login,     # Login único de la persona
        'password': password,  # Contraseña de la persona
    }
    return person


def manage_people():
    """
       Permite gestionar las personas existentes, ofreciendo opciones para agregar, modificar o volver al inicio.

       Solicita al usuario que elija una acción y llama a la función correspondiente.
    """
    utils.clear_console()
    actions = ["Borrar una persona del sistema",
               "Manejar solicitudes de roles"]

    print("elige accion que quieres hacer:")

    opt, ind = utils.choose(actions, 'Elija que quiere hacer:')
    if opt == utils.GO_BACK_STR:
        return None
    if ind == 0:
        person_id = utils.choose_id(people, 'Elija la persona que quire borrar')
        if person_id == '-1':
            return None
        remove_person(person_id)
    elif ind == 1:
        manage_role_requests()


def remove_person(person_id):
    """
        Elimina una persona de la lista 'people' basada en su ID.
    """
    utils.clear_console()
    for team_id in teams.keys():
        if person_id in teams[team_id]['person_ids']:
            teams[team_id]['person_ids'].remove(person_id)
    people.pop(person_id)


def change_person_name(id):
    """
        Cambia el nombre de una persona en la lista 'people'.
    """
    utils.clear_console()
    name = input("Ingrese nuevo nombre de persona: ")
    people[id]['name'] = name
    print(f"El nuevo nombre de persona es {name}")


def go_begin(*args):
    """
        Función para volver al menú inicial.
    """
    return 0


def manage_person(id):
    """
        Permite gestionar una persona específica, ofreciendo opciones para borrar, cambiar nombre, cambiar apellido o volver al inicio.
    """
    utils.clear_console()
    actions = {"borrar": remove_person,
               "cambiar nombre": change_person_name,
               "volver a inicio": go_begin}

    print("elige accion que quieres hacer:")
    for i, action in enumerate(actions.keys()):
        print(f"{i + 1}: {action}")

    act = input()
    while act not in ('1', '2', '3'):
        print("Tiene que ingresar un numero entre 1 y 3\n")
        print("elige accion que quieres hacer:")

        act = input()
    action = actions[list(actions.keys())[int(act) - 1]]
    action(id)


def show_person(id):
    utils.clear_console()
    """
        Imprime la información detallada de una persona.
    """
    person_teams = []
    for team in teams.items():
        if id in team[1]['person_ids']:
            person_teams.append(team[1]['name'])
    print(f"Nombre: {people[id]['name']}\n"
          f"Role: {roles[people[id]['role']]}\n"
          f"Edad: {people[id]['age']}\n"
          f"Equipos: {person_teams}")


def manage_role_requests():
    id = utils.choose_id(role_requests, 'Elija la solicitud de rol')
    while id != '-1':
        person_id = role_requests[id]['person_id']
        role = role_requests[id]['role']
        title = f'{people[person_id]} quiere ser un {roles[role]}'
        options = ['Aprobar', 'Rechazar']
        opt, ind = utils.choose(options, title)
        if opt == utils.GO_BACK_STR:
            return None
        if ind == 0:
            people[person_id]['role'] = role
            role_requests.pop(id)
        if ind == 1:
            role_requests.pop(id)
        id = utils.choose_id(role_requests, 'Elija la solicitud de rol')
    return None
