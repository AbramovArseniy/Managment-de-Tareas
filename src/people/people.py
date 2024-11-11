from src.datos import *
import src.datos as dt
import utils


specializations = {
    1: 'Middle programador',
    2: 'Senor programador',
    3: 'Junior programador',
    4: 'Team lid',
}


def create_person():
    """
        Crea una nueva persona solicitando al usuario el nombre, apellido, especialización y edad.

        Luego, añade la persona creada a la lista global 'people'.

        Returns:
            dict: La persona creada.
    """

    utils.clear_console()
    try:
        name = input('Ingrese nombre completo de la persona: ')
        for s in specializations.keys():
            print(f"{s}: {specializations[s]}")

        specialization = specializations[int(input(f'Ingrese numero de especialidad de la persona: '))]

        age = int(input(f'Ingrese edad de la persona: '))

        person = new_person(name, age, specialization)
        people[str(people_next_id)] = person
        dt.people_next_id += 1
        print('Persona es guardada\n')
        return person
    except:
        print("Error al agregar la persona")
        input("Presiona Enter para continuar...")


def new_person(name, age, specialization):
    """
        Crea un diccionario con los detalles de una persona.

        Returns:
            dict: Diccionario que contiene los datos de la persona.
    """
    utils.clear_console()
    person = {
        'name': name,
        'age': age,
        'specialization': specialization,
    }
    return person


def manage_people():
    """
       Permite gestionar las personas existentes, ofreciendo opciones para agregar, modificar o volver al inicio.

       Solicita al usuario que elija una acción y llama a la función correspondiente.
    """
    utils.clear_console()
    actions = ["Agregar una persona",
               "Manejar una persona",
               "Ver la lista de personas",
               "Volver a inicio"]

    print("elige accion que quieres hacer:")

    for i, action in enumerate(actions):
        print(f"{i + 1}: {action}")

    act = input()
    while act not in ('1', '2', '3', '4'):
        print("Tiene que ingresar un numero entre 1 y 3\n")
        print("elige accion que quieres hacer: ")

        act = input()

    act = int(act)

    if act == 1:
        create_person()
    elif act == 2:
        id = utils.choose_id(people, "Ingrese numero de persona que desea modificar ")
        manage_person(id)
    elif act == 3:
        utils.print_dict(people)
    elif act == 4:
        go_begin()
    else:
        print("error")
        return 0


def remove_person(person_id):
    """
        Elimina una persona de la lista 'people' basada en su ID.
    """
    utils.clear_console()
    print(teams)
    persons_teams = [person_id in team['person_ids'] for team in teams.values()]
    if True in persons_teams:
        print("Esta persona está en el equipo")
        while True:
            n = input("desea borrarla ?\n"
                      "1. Si\n"
                      "2. No\n")
            if n == "1":
                for team_id, status in enumerate(persons_teams):
                    if status:
                        teams[team_id]['person_ids'].remove(person_id)

                people.pop(person_id)
                print("La persona borro")
                return 0
            if n == "2":
                go_begin()
            else:
                print("Tiene que ingresar 1 o 2")
    else:
        people.pop(person_id)
        print("La persona borro")


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


def show_person(person):
    """
        Imprime la información detallada de una persona.
    """
    print(f"Nombre: {person['name']}\n"
          f"Specializacion: {person['specialization']}\n"
          f"Edad: {person['age']}")
