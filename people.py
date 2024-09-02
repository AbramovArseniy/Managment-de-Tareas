specializations = {
    1: 'Middle programador',
    2: 'Senor programador',
    3: 'Junior programador',
    4: 'Team lid',
}

people = [{
    'name': "Name",
    'surname': "surname",
    'age': "age",
    'specialization': "specialization",  # Baja, Media, Alta
}]


def create_person():
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
    person = {
        'name': name,
        'surname': surname,
        'age': age,
        'specialization': specialization,  # Baja, Media, Alta
    }

    return person


def manage_people():
    print("Ingrase numero de la persona que quieres cambiar ")
    for i, person in enumerate(people):
        print(f"{i + 1}: {person['name']} {person['surname']}")

    id = int(input())
    manage_person(id - 1)


def remove_person(id):
    people.pop(id)
    print("La persona borro")


def change_person_name(id):
    name = input("Ingrese nuevo nombre de persona")
    people[id]['name'] = name
    print(f"El nuevo nombre de persona es {name}")


def change_person_surname(id):
    surname = input("Ingrese nuevo nombre de persona")
    people[id]['surname'] = surname
    print(f"El nuevo apellido de persona es {surname}")


def go_begin():
    return False


def manage_person(id):
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


def print_people(people):
    for s in people.keys():
        print(f"{s}: {people[s]} ")


# person = create_person()
# print_people(people)

manage_people()
manage_people()
