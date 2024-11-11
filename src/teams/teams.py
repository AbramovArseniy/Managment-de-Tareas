from matplotlib import pyplot as plt
from datetime import datetime, timedelta
import src.tasks.tasks as tasks_mod
import utils
import calendar
from src.datos import *
import src.datos as dt
from src.people.people import show_person


def create_team():
    """
        Crea un nuevo equipo solicitando al usuario un nombre y añadiendo personas al equipo.

        Solicita al usuario que seleccione personas de la lista 'people' y las agrega al equipo.
        Una vez completado, añade el nuevo equipo a la lista global 'teams'.
    """
    utils.clear_console()
    name = input('Ingrese nombre de equipo: ')
    persons = []
    while True:
        filtered_people = dict(filter(lambda x: x[0] not in persons, people.items()))
        if len(filtered_people) == 0:
            print("No hay personas disponibles para añadir al equipo ")
            return 0

        person_id = utils.choose_id(filtered_people, "Elige numero de persona que quiere agregar a su equipo: ")

        persons.append(person_id)
        print( "\nEsta persona se ha añadido al equipo")

        print("Que quieres hacer ?\n"
              "1. Agregar persona una mas\n"
              "2. Terminar\n: ")

        n = input()

        while n not in ('1', '2'):
            print("Tiene que ingresar un numero entre 1 y 2\n")
            print("elige accion que quieres hacer:")
            n = input()

        n = int(n)

        if n == 2:
            new_team = {
                "name": name,
                "persons": persons
            }
            teams[str(teams_next_id)] = new_team
            dt.teams_next_id += 1
            print("Nuevo equipo ha creado con exito!")
            break


def go_begin():
    """
        Función de marcador de posición para regresar al menú anterior.
    """
    return 0


def remove_team(team_id):
    """
        Elimina un equipo de la lista 'teams' usando su ID.
    """
    utils.clear_console()
    teams.pop(team_id)
    for id, task in tasks:
        if task['team_id'] == team_id:
            tasks[id]['team_id'] = -1
    print("El equipo borro")


def change_team_name(team_id):
    """
        Cambia el nombre de un equipo.
    """
    utils.clear_console()
    name = input("Ingrese nuevo nombre de equipo: ")
    teams[team_id]['name'] = name
    print(f"El nuevo nombre de equipo es {name}")


def add_person_to_team(team_id):
    """
       Añade una persona al equipo seleccionado.
    """
    utils.clear_console()
    filtered_people = dict(filter(lambda x: x not in teams[team_id]['persons'], people))
    for id, person in filtered_people:
        print(id, end=".\n")
        show_person(person)
        print("----------------")

    person_id = input("Elige numero de person que quiere agregar a su equipo: ")
    while person_id not in range(1, len(filtered_people) + 1):
        print(f"Tiene que ingresar un numero entre 1 y {filtered_people + 1}\n")
        person_id = input()
    person_id = int(person_id)

    if person_id > len(filtered_people) or person_id < 1:
        print("Numero incorrecto")
        return 0

    print(show_person(filtered_people[person_id - 1]), "\n Esta persona se ha añadido al equipo")


def show_team(team_id):
    """
       Muestra la información de un equipo específico, incluyendo su nombre y miembros.
    """
    print("Equipo: ", teams[team_id]['name'])
    print("Miembros del equipo:")
    for person_id in teams[team_id]['person_ids']:
        print(f'\t{people[person_id]["name"]} {people[person_id]["surname"]}')
    print("----------------")


def manage_team(team_id):
    """
        Administra un equipo seleccionado, ofreciendo opciones para eliminar, cambiar nombre, añadir personas o volver al inicio.
    """
    utils.clear_console()
    actions = {"borrar equipo": remove_team,
               "cambiar nombre de equipo": change_team_name,
               "agregar nueva persona ": add_person_to_team,
               "eliminar a una persona del equipo": remove_from_team,
               "ver estadistica": show_team_stats,
               "volver a inicio": go_begin}

    print("elige accion que quieres hacer:")
    for i, action in enumerate(actions.keys()):
        print(f"{i + 1}: {action}")

    act = input()
    while act not in [str(i + 1) for i in range(len(actions.keys()))]:
        print("Tiene que ingresar un numero entre 1 y 6\n")
        print("elige accion que quieres hacer:")
        act = input()

    act = int(act)
    if act < 1 or act > len(actions.keys()):
        print('incorrect numero de accion')
        return 0
    action = actions[list(actions.keys())[act - 1]]
    if act == 6:
        go_begin()
    else:
        action(team_id)


def remove_from_team(team_id):
    utils.clear_console()
    for i, id in enumerate(teams[team_id]['person_ids']):
        print(i + 1, end=". ")
        show_person(people[id])
        print("---------")

    n = input("Ingrese el número de la persona que desea eliminar del equipo.")
    while n not in [str(i + 1) for i in range(len(teams[team_id]['person_ids']))]:
        print("numero incorrecto")
        n = input("Ingrese el número de la persona que desea eliminar del equipo")

    teams[team_id]['person_ids'].pop(int(n) - 1)
    utils.clear_console()
    print("La persona ha sido eliminada del equipo con éxito")
    print("Estado actual del equipo")
    show_team(team_id)


def print_top_teams():
    stats = {}
    for id, team in teams:
        stats[team['name']] = 0
        task_cnt = 0
        for id, task in tasks:
            if task['team_id'] == id and task['status'] == tasks_mod.STATUS_DONE:
                stats[team['name']] += task['priority'] * min(1, datetime.strptime(task['done_at'], "%d/%m/%Y") - datetime.strptime(task['do_until'], "%d/%m/%Y"))/30
                task_cnt += 1
        try:
            stats[team['name']] /= task_cnt
        except ZeroDivisionError:
            stats[team['name']] = 0
    sorted_teams = [k for k, v in sorted(stats.items(), key=lambda item: item[1])][:10]
    for i, team_name in enumerate(sorted_teams):
        print(f"{i+1}. {team_name}")
    input('Presione Enter para continuar...')


def show_team_stats(team_id):
    done_per_month = []
    late_per_month = []
    months = []
    sorted_tasks = sorted(filter(lambda task: task['team_id'] == team_id and task['status'] == tasks_mod.STATUS_DONE  and datetime.today() - datetime.strptime(task['done_at'], "%d/%m/%Y") <= timedelta(days=366), tasks.values()), key=lambda task: datetime.strptime(task['done_at'], "%d/%m/%Y"))
    if len(sorted_tasks) == 0:
        print('Ese equipo todavia no hizo tareas')
        return
    plt.rcParams.update({'font.size': 7})
    cnt_done = 0
    cnt_late = 0
    cur_month = datetime.strptime(sorted_tasks[0]['done_at'], "%d/%m/%Y").month
    cur_year = datetime.strptime(sorted_tasks[0]['done_at'], "%d/%m/%Y").year
    months.append(f'{calendar.month_name[cur_month]},\n{cur_year}')
    for task in sorted_tasks:
        if datetime.strptime(task['done_at'], "%d/%m/%Y").month != cur_month or datetime.strptime(task['done_at'], "%d/%m/%Y").year != cur_year:
            done_per_month.append(cnt_done)
            late_per_month.append(cnt_late)
            cur_year += cur_month // 12
            cur_month = cur_month % 12 + 1
            months.append(f'{calendar.month_name[cur_month]},\n{cur_year}')
            cnt_done = 0
            cnt_late = 0
        cnt_done += 1
        if datetime.strptime(task['done_at'], "%d/%m/%Y") > datetime.strptime(task['do_until'], "%d/%m/%Y"):
            cnt_late += 1

    done_per_month.append(cnt_done)
    late_per_month.append(cnt_late)
    plt.plot(months, done_per_month)
    plt.plot(months, late_per_month)
    plt.title('Tareas Hechas')
    plt.xlabel('Mes')
    plt.ylabel('Cantidad de Tareas')
    plt.legend(['Tareas hechas', 'Hecho con Retraso'])
    plt.show()


def manage_teams():
    """
        Gestiona los equipos, permitiendo agregar nuevos equipos, modificar equipos existentes o volver al inicio.

        Muestra los equipos existentes y permite al usuario elegir una acción.
    """
    utils.clear_console()
    actions = ["Agregar nueva equipo",
               "Manejar un equipo",
               'Ver equipos',
               "Ver equipos mas efectivos",
               "Volver a inicio"]

    print("Elige accion que quieres hacer:")

    for i, action in enumerate(actions):
        print(f"{i + 1}: {action}")
    act = input()
    while act not in ('1', '2', '3', '4', '5'):
        print("Tiene que ingresar un numero entre 1 y 5\n")
        print("elige accion que quieres hacer:")

        act = input()
    act = int(act)
    if act == 1:
        create_team()
    elif act == 2:
        if len(teams) == 0:
            print("En primer lugar, cree un nuevo equipo ")
            return 0

        id = utils.choose_id(teams, "Ingrese el número del equipo que desea modificar: ")
        manage_team(id)

    elif act == 3:
        utils.print_dict(teams, lambda task: int(task[0]) > 0)

    elif act == 4:
        print_top_teams()

    elif act == 5:
        go_begin()
    
    else:
        print("error. action incorrect")
        return 0
