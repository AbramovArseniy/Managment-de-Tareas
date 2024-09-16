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
    person = {
        'name': name,
        'surname': surname,
        'age': age,
        'specialization': specialization,
    }

    return person


def manage_people():
    """
       Permite gestionar las personas existentes, ofreciendo opciones para agregar, modificar o volver al inicio.

       Solicita al usuario que elija una acción y llama a la función correspondiente.
    """
    actions = {"Agregar una persona": create_person,
               "Manejar una persona": manage_person,
               "Volver a inicio": go_begin}

    print("elige accion que quieres hacer:")

    for i, action in enumerate(actions.keys()):
        print(f"{i + 1}: {action}")

    act = int(input())
    if act == 1:
        create_person()
    elif act == 2:
        print("Ingrese numero de persona que desea modificar ")
        for i, person in enumerate(people):
            print(f"{i + 1}: {person['name']} {person['surname']}")
        id = int(input())
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
    people.pop(id)
    print("La persona borro")


def change_person_name(id):
    """
        Cambia el nombre de una persona en la lista 'people'.
    """
    name = input("Ingrese nuevo nombre de persona: ")
    people[id]['name'] = name
    print(f"El nuevo nombre de persona es {name}")


def change_person_surname(id):
    """
        Cambia el apellido de una persona en la lista 'people'.
    """
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
    actions = {"borrar": remove_person,
               "cambiar nombre": change_person_name,
               "cambiar apellido": change_person_surname,
               "volver a inicio": go_begin}

    print("elige accion que quieres hacer:")
    for i, action in enumerate(actions.keys()):
        print(f"{i + 1}: {action}")

    act = int(input())
    action = actions[list(actions.keys())[act - 1]]
    action(id)


def print_person(person):
    """
        Imprime la información detallada de una persona.
    """
    for s in person.keys():
        print(f"{s}: {person[s]} ")


