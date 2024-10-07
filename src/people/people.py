import utils


specializations = {
    1: 'Middle programador',
    2: 'Senor programador',
    3: 'Junior programador',
    4: 'Team lid',
}

people = []


def create_person():
    """
        Crea una nueva persona solicitando al usuario el nombre, apellido, especialización y edad.

        Luego, añade la persona creada a la lista global 'people'.

        Returns:
            dict: La persona creada.
    """
    utils.clear_console()
    name = input('Ingrese nombre de la persona: ')
    surname = input('Ingrese apellido de la persona: ')
    for s in specializations.keys():
        print(f"{s}: {specializations[s]}")

    specialization = specializations[int(input(f'Ingrese numero de especialidad de la persona: '))]

    age = int(input(f'Ingrese edad de la persona: '))

    person = new_person(name, surname, age, specialization)
    people.append(person)
    print('Persona es guardada\n')
    return person


def new_person(name, surname, age, specialization):
    """
        Crea un diccionario con los detalles de una persona.

        Returns:
            dict: Diccionario que contiene los datos de la persona.
    """
    utils.clear_console()
    person = {
        'name': name,
        'surname': surname,
        'age': age,
        'specialization': specialization,  # Baja, Media, Alta
    }

    return person


def manage_people():
    """
       Permite gestionar las personas existentes, ofreciendo opciones para agregar, modificar o volver al inicio.

       Solicita al usuario que elija una acción y llama a la función correspondiente.
    """
    utils.clear_console()
    actions = {"Agregar una persona": create_person,
               "Manejar una persona": manage_person,
               "Volver a inicio": go_begin}

    print("elige accion que quieres hacer:")

    for i, action in enumerate(actions.keys()):
        print(f"{i + 1}: {action}")

    act = input()
    while act not in ('1', '2', '3'):
        print("Tiene que ingresar un numero entre 1 y 3\n")
        print("elige accion que quieres hacer: ")

        act = input()

    act = int(act)

    if act == 1:
        create_person()
    elif act == 2:
        print("Ingrese numero de persona que desea modificar ")
        for i, person in enumerate(people):
            print(f"{i + 1}: {person['name']} {person['surname']}")
        id = input()
        while id not in [str(i) for i in range(1, len(people) + 1)]:
            print(f"Tiene que ingresar un numero entre 1 y {len(people)}\n")
            print("Ingrese numero de persona que desea modificar ")

            id = input()
        id = int(id)
        manage_person(id - 1)
    elif act == 3:
        go_begin()
    else:
        print("error")
        return 0


def remove_person(id):
    """
        Elimina una persona de la lista 'people' basada en su ID.
    """
    utils.clear_console()
    people.pop(id)
    print("La persona borro")


def change_person_name(id):
    """
        Cambia el nombre de una persona en la lista 'people'.
    """
    utils.clear_console()
    name = input("Ingrese nuevo nombre de persona: ")
    people[id]['name'] = name
    print(f"El nuevo nombre de persona es {name}")


def change_person_surname(id):
    """
        Cambia el apellido de una persona en la lista 'people'.
    """
    utils.clear_console()
    surname = input("Ingrese nuevo nombre de persona: ")
    people[id]['surname'] = surname
    print(f"El nuevo apellido de persona es {surname}")


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
               "cambiar apellido": change_person_surname,
               "volver a inicio": go_begin}

    print("elige accion que quieres hacer:")
    for i, action in enumerate(actions.keys()):
        print(f"{i + 1}: {action}")

    act = input()
    while act not in ('1', '2', '3', '4'):
        print("Tiene que ingresar un numero entre 1 y 4\n")
        print("elige accion que quieres hacer:")

        act = input()
    action = actions[list(actions.keys())[int(act) - 1]]
    action(id)


def print_person(person):
    """
        Imprime la información detallada de una persona.
    """
    utils.clear_console()
    for s in person.keys():
        print(f"{s}: {person[s]} ")


