from people import people, print_person

teams = []



def create_team():
    name = input('Ingrese nombre de equipo: ')
    persons = []
    while True:
        filtered_people = list(filter(lambda x: x not in persons, people))
        for i, person in enumerate(filtered_people):
            print(i + 1, end=".\n")
            print_person(person)
            print("----------------")

        person_id = int(input("Elige numero de persona que quiere agregar a su equipo: "))

        if person_id > len(filtered_people) or person_id < 1:
            print("Numero incorrecto")
            continue

        persons.append(filtered_people[person_id - 1])
        print(print_person(filtered_people[person_id - 1]), "\n Esta persona se ha añadido al equipo")

        n = int(input("Que quieres hacer ?\n"
                      "1. Agregar persona una mas\n"
                      "2. Terminar\n: "))

        if n == 2:
            new_team = {
                "name": name,
                "persons": persons
            }
            teams.append(new_team)
            print("Nuevo equipo ha creado con exito!")
            break


def go_begin():
    return 0


def remove_team(team_id):
    teams.pop(team_id)
    print("El equipo borro")


def change_team_name(team_id):
    name = input("Ingrese nuevo nombre de equipo: ")
    teams[team_id]['name'] = name
    print(f"El nuevo nombre de equipo es {name}")


def add_person_to_team(team_id):
    filtered_people = list(filter(lambda x: x not in teams[team_id]['persons'], people))
    for i, person in enumerate(filtered_people):
        print(i + 1, end=".\n")
        print_person(person)
        print("----------------")

    person_id = int(input("Elige numero de person que quiere agregar a su equipo: "))

    if person_id > len(filtered_people) or person_id < 1:
        print("Numero incorrecto")
        return 0

    print(print_person(filtered_people[person_id - 1]), "\n Esta persona se ha añadido al equipo")


def show_team(team_id):
    print("Equipo: ", teams[team_id]['name'])
    print("Miembros del equipo:")
    for person in teams[team_id]['persons']:
        print_person(person)
        print("----------------")


def manage_team(team_id):
    actions = {"borrar equipo": remove_team,
               "cambiar nombre de equipo": change_team_name,
               "agregar nueva persona ": add_person_to_team,
               "volver a inicio": go_begin}

    print("elige accion que quieres hacer:")
    for i, action in enumerate(actions.keys()):
        print(f"{i + 1}: {action}")

    act = int(input())
    if act < 1 or act > len(actions.keys()):
        print('incorrect numero de accion')
        return 0
    action = actions[list(actions.keys())[act - 1]]
    action(team_id)


def manage_teams():
    print("\nEquipos: ")
    for team in teams:
        print("Nombre del equipo:", team['name'])
        print("Miembros del equipo: ", end='')
        for person in team['persons']:
            print(f"{person['name']} {person['surname']}", end=", ")
        print("\n----------------")

    actions = {"Agregar nueva equipo": create_team,
               "Manejar un equipo": manage_team,
               "Volver a inicio": go_begin}

    print("Elige accion que quieres hacer:")

    for i, action in enumerate(actions.keys()):
        print(f"{i + 1}: {action}")

    act = int(input())
    if act == 1:
        create_team()
    elif act == 2:
        if len(teams) == 0:
            print("En primer lugar, cree un nuevo equipo ")
            return 0

        print("ingrese el número del equipo que desea modificar")
        for i, team in enumerate(teams):
            print(f"{i + 1}: {team['name']}")
        id = int(input())
        manage_team(id - 1)
    elif act == 3:
        go_begin()
    else:
        print("error. action incorrect")
        return 0

