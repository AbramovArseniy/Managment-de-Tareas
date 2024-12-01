import calendar
import time
from datetime import datetime, timedelta

from matplotlib import pyplot as plt

import src.datos as dt
import src.tasks.tasks as tasks_mod
import utils
from src.datos import *
from src.people.people import show_person


def create_team():
    """
        Crea un nuevo equipo solicitando al usuario un nombre y añadiendo personas al equipo.

        Solicita al usuario que seleccione personas de la lista 'people' y las agrega al equipo.
        Una vez completado, añade el nuevo equipo a la lista global 'teams'.
    """
    utils.clear_console()
    name = input('Ingrese nombre de equipo: ')
    while len(name) < 3:
        print("Error. La longitud del nombre debe ser mayor o igual a 3")
        name = input('Ingrese nombre de equipo: ')

    persons = [utils.get_session()['id']]
    while True:
        filtered_people = dict(filter(lambda x: x[0] not in persons, people.items()))
        if len(filtered_people) == 0:
            print("No hay personas disponibles para añadir al equipo ")
            input('Presione Enter para continuar...')
            return 0

        person_id = utils.choose_id(filtered_people, "Elige numero de persona que quiere agregar a su equipo: ")
        if person_id == '-1':
            return 0
        persons.append(person_id)
        print( "\nEsta persona se ha añadido al equipo")
        if len(filtered_people) == 1:
            new_team = {
                "name": name,
                "person_ids": persons
            }
            teams[str(teams_next_id)] = new_team
            dt.teams_next_id += 1
            print("Nuevo equipo ha creado con exito!")
            input('Presione Enter para continuar...')
            return 0
        options = ["  Agregar persona una mas\n",
              "  Continuar\n: "]
        option, ind = utils.choose(options, "Que quieres hacer ?")
        if option == utils.GO_BACK_STR:
            go_begin()
        if ind == 1:
            new_team = {
                "name": name,
                "person_ids": persons
            }
            teams_next_id = 1
            if len(people.keys()) != 0:
                teams_next_id = max(map(int, teams.keys())) + 1
            teams[str(teams_next_id)] = new_team
            print("Nuevo equipo ha creado con exito!")
            return 0


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
    for id in tasks.keys():
        if tasks[id]['team_id'] == team_id:
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
    filtered_people = dict(filter(lambda x: x[0] not in teams[team_id]['person_ids'], people.items()))
    for id in filtered_people.keys():
        print(id, end=".\n")
        show_person(id)
        print("----------------")

    person_id = utils.choose_id(filtered_people, 'Elija la persona que quiere agregar a su equipo: ')
    if person_id == '-1':
        return 0
    print(show_person(person_id), "se ha añadido al equipo")
    input('Presione Enter para continuar...')


def show_team(team_id):
    """
       Muestra la información de un equipo específico, incluyendo su nombre y miembros.
    """
    print("Equipo: ", teams[team_id]['name'])
    print("Miembros del equipo:")
    for person_id in teams[team_id]['person_ids']:
        print(f'\t{people[person_id]["name"]}')
    print("----------------")
    input("Pulse ENTER para continuar")


def manage_team(team_id):
    """
        Administra un equipo seleccionado, ofreciendo opciones para eliminar, cambiar nombre, añadir personas o volver al inicio.
    """
    utils.clear_console()
    actions = {"Borrar equipo": remove_team,
               "Cambiar nombre de equipo": change_team_name,
               "Agregar nueva persona ": add_person_to_team,
               "Eliminar una persona del equipo": remove_from_team,
               "Mostrar estadistica": show_team_stats,}

    input_msg = "Elija que quiere hacer:"
    act, act_num = utils.choose(list(actions.keys()), input_msg)
    if act == utils.GO_BACK_STR:
        go_begin()
    else:
        action = actions[act](team_id)


def remove_from_team(team_id):
    utils.clear_console()
    for i, id in enumerate(teams[team_id]['person_ids']):
        print(i + 1, end=". ")
        show_person(id)
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
    for team_id in teams.keys():
        if team_id != '-1':
            stats[teams[team_id]['name']] = 0
            task_cnt = 0
            for task_id in tasks.keys():
                if tasks[task_id]['team_id'] == id and tasks[task_id]['status'] == tasks_mod.STATUS_DONE:
                    stats[teams[team_id]['name']] += tasks[task_id]['priority'] * min(1, datetime.strptime(tasks[task_id]['done_at'], "%d/%m/%Y") - datetime.strptime(tasks[task_id]['do_until'], "%d/%m/%Y"))/30
                    task_cnt += 1
            try:
                stats[teams[team_id]['name']] /= task_cnt
            except ZeroDivisionError:
                stats[teams[team_id]['name']] = 0
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
    input("Pulse ENTER para continuar")



def manage_teams():
    """
        Gestiona los equipos, permitiendo agregar nuevos equipos, modificar equipos existentes o volver al inicio.

        Muestra los equipos existentes y permite al usuario elegir una acción.
    """
    utils.clear_console()
    input_msg = "Elija accion que quieres hacer"
    actions = ["Ver equipos",
               "Ver equipos mas efectivos"]
    if people[utils.get_session()['id']]['role'] < 2:
        actions = ["Agregar nueva equipo", "Manejar un equipo"] + actions

    act, act_num = utils.choose(actions, input_msg)
    if act == utils.GO_BACK_STR:
        return None
    if act == "Agregar nueva equipo":
        create_team()

    elif act == "Manejar un equipo":
        if len(teams) == 0:
            print("En primer lugar, cree un nuevo equipo ")
            return 0
        user_id = utils.get_session()['id']
        if people[user_id]['role']==1:
            filter_func = lambda item: user_id in item[1].get("person_ids", [])
            id = utils.choose_id(teams, "Elija el id del equipo que desea modificar: ",filter_func=filter_func)
            if id == '-1':
                return 0
            manage_team(id)
        elif people[user_id]['role']==0:
            id = utils.choose_id(teams, "Elija el id del equipo que desea modificar: ",)
            if id == '-1':
                return 0
            manage_team(id)
    elif act == "Ver equipos":
        print(teams)
        id = utils.choose_id(teams, 'Elija un equipo, para ver mas informacion: ')
        if id == '-1':
            return 0
        show_team(id)


    elif act == "Ver equipos mas efectivos":
        print_top_teams()
