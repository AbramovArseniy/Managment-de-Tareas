import json

import utils
from datetime import datetime
from src.datos import *
import src.datos as dt

task_tmpl = {
    'name':'',
    'description':'',
    'priority':'', # Baja, Media, Alta
    'status':'', # Para Asignar, En Progreso, En Revision, Hecho
    'team': None,
    'do_until': ''
}

PRIORITY_LOW = 1
PRIORITY_MEDIUM = 2
PRIORITY_HIGH = 3

priorities = {
    1: 'Baja',
    2: 'Media',
    3: 'Alta'
}

STATUS_TO_ASSIGN = 1
STATUS_IN_PROGRESS = 2
STATUS_IN_REVIEW = 3
STATUS_DONE = 4

statuses = {
    1: 'Para Asignar',
    2: 'En Progreso',
    3: 'En Revision',
    4: 'Hecho',
}

def new_task(name, desc, prio):
    """
    Crea una nueva tarea y la devuelve como un diccionario.

    Returns:
        dict: Nueva tarea con el estado 'Para Asignar' y equipo estándar 'No team assigned'.
    """
    utils.clear_console()

    task = {
        'name': name,
        'description': desc,
        'priority': prio,
        'status': STATUS_TO_ASSIGN,
        'team': '-1',
        'do_until': datetime.max.strftime("%d/%m/%Y"),
        'done_at': ''
    }
    return task


def go_back():
    """
        Función de marcador de posición para volver al menú anterior.

    """
    return 0


def manage_tasks():
    """
      Administra las tareas, permitiendo agregar, modificar o filtrar tareas.

      Solicita al usuario la acción que quiere realizar y llama a la función correspondiente.
    """
    utils.clear_console()
    actions = {
        '1': create_task,
        '2': manage_task,
        '3': filter_tasks,
        '4': go_back
    }
    cmd = input('Ingrese que quiere hacer:\n1. Agregar tarea\n2. Manejar tarea\n3. Ver tareas filtradas\n4. Volver al inicio\n')
    while cmd not in ('1', '2', '3', '4'):
        print("Tiene que ingresar un numero entre 1 y 4")
        cmd = input()
    actions[cmd]()

def manage_task():
    utils.clear_console()
    if len(tasks) == 0:
        print('Todavia no hay tareas\n')
        return
    actions = {
        '1': change_task,
        '2': delete_task,
        '3': assign_team
    }
    cmd = input('Ingrese que quiere hacer:\n1. Cambiar datos de tarea\n2. Borrar tarea\n3. Assingar tarea a un equipo\n')
    while cmd not in ('1', '2', '3'):
        print("Tiene que ingresar un numero entre 1 y 3")
        cmd = input()
    actions[cmd]()


def assign_team():
    """
       Asigna un equipo a una tarea.

       Permite al usuario elegir una tarea y asignarla a un equipo.
    """
    utils.clear_console()
    if len(teams) == 0:
        print('Primero tiene que crear un equipo')
        return
    task_id = utils.choose_id(tasks, "Ingrese el Id de la tarea: ")
    team_id = utils.choose_id(teams, "Ingrese el Id del equipo: ")
    tasks[task_id]['team_id'] = team_id
    tasks[task_id]['status'] = max(STATUS_IN_PROGRESS, tasks[task_id]['status'])




def create_task():
    """
        Crea una nueva tarea solicitando al usuario el nombre, descripción y prioridad.

        Agrega la tarea creada a la lista `tasks`.
    """
    utils.clear_console()
    name = input('Ingrese nombre de la tarea: ')
    while name == '':
        print("El nombre no puede ser vacio")
        name = input('Ingrese nombre de la tarea: ')
    desc = input('Ingrese descripcion de la tarea: ')
    prio = input('Ingrese prioridad de su tarea:\n1. Baja\n2. Media\n3. Alta\n')
    while prio not in ('1', '2', '3'):
        print('Tiene que ingresar un numero entre 1 y 3:')
        prio = input()
    task = new_task(name, desc, int(prio))
    tasks[str(tasks_next_id)] = task
    dt.tasks_next_id += 1
    print('Tarea es guardada\n')


def filter_tasks():
    """
        Filtra las tareas por prioridad, estado o equipo.

        Solicita al usuario el criterio de filtrado y llama a la función `utils.print_dict()` para mostrar las tareas filtradas.
    """
    utils.clear_console()
    if len(tasks) == 0:
        print('Todavia no hay tareas\n')
        return
    param = input("Por qué quiere filtrar las tareas?\n"
                "1. Prioridad\n"
                "2. Estado\n"
                "3. Equipo\n"
                "4. Ver Todas\n")
    while param not in ('1', '2', '3', '4'):
        print("Tiene que ingresar un numero entre 1 y 4")
        param = input()
    if param == '1':
        prio = input('Ingrese la nueva prioridad de la tarea:\n1. Baja\n2. Media\n3. Alta\n')
        while prio not in ('1', '2', '3'):
            print("Tiene que ingresar un numero entre 1 y 3")
            prio = input()
        utils.print_dict(tasks, lambda task: task[1]['priority'] == int(prio))
    elif param == '2':
        status = input('Ingrese el estado:\n1. Para Asignar\n2. En Progreso\n3. En Revision\n4. Hecho\n')
        while status not in ('1', '2', '3', '4'):
            print("Tiene que ingresar un numero entre 1 y 4")
            status = input()
        utils.print_dict(tasks, lambda task: task[1]['status'] == int(status))
    elif param == '3':
        for id, team in teams:
            print(f"{id}: {team['name']}")
        team_id = utils.choose_id(teams, "Ingrese el número del equipo")
        utils.print_dict(tasks, lambda task: task[1]['team_id'] == team_id)
    elif param == '4':
        utils.print_dict(tasks)


    id = input('Ingrese Id de tarea para ver mas informacion o -1 para volver al inicio: ')
    while id not in tasks.keys() and id != '-1':
        id = input('Id no es valido. Ingrese otra: ')
    if id == '-1':
        go_back()
    else:
        print_task_info(tasks[id])
        input('Pressiona Enter para volver a menu...')


def delete_task():
    """
        Borra una tarea seleccionada de la lista `tasks`.
    """
    utils.clear_console()
    if len(tasks) == 0:
        print('Todavia no hay tareas\n')
        return
    task_id = utils.choose_id(tasks, "Ingrese el Id de la tarea que desea borrar: ")
    tasks.pop(task_id)
    print("Tarea era borrada con exito")


def change_task():
    """
        Modifica las propiedades de una tarea seleccionada (nombre, descripción, prioridad o estado).
    """
    utils.clear_console()
    if len(tasks) == 0:
        print('Todavia no hay tareas\n')
        return
    task_id = utils.choose_id(tasks, "Ingrese el Id de la tarea: ")
    task = tasks[task_id]
    cmd = input("Elige que quiere cambiar en la tarea: \n"
                "1. Nombre\n"
                "2. Descripcion\n"
                "3. Prioridad\n"
                "4. Estado\n"
                "5. Hacer Antes de (Fecha)\n")
    while cmd not in ('1', '2', '3', '4', '5'):
        print("Tiene que ingresar un numero entre 1 y 5")
        cmd = input()
    if cmd == '1':
        new_name = input('Ingrese el nuevo nombre de la tarea: ')
        task['name'] = new_name
    elif cmd == '2':
        new_desc = input('Ingrese la nueva descripcion de la tarea: ')
        task['description'] = new_desc

    elif cmd =='3':
        new_prio = input('Ingrese la nueva prioridad de la tarea:\n1. Baja\n2. Media\n3. Alta\n')
        while new_prio not in ('1', '2', '3'):
            print("Tiene que ingresar un numero entre 1 y 3")
            new_prio = input()

        task['priority'] = int(new_prio)

    elif cmd == '4':
        new_status = input('Ingrese el nuevo estado de la tarea:\n1. Para Asignar\n2. En Progreso\n3. En Revision\n4. Hecho\n')
        while new_status not in ('1', '2', '3', '4'):
            print("Tiene que ingresar un numero entre 1 y 4")
            new_status = input()
        new_status = int(new_status)
        task['status'] = int(new_status)
        if new_status == STATUS_DONE:
            task['done_at'] = datetime.now().strftime('%d/%m/%Y')

    elif cmd == '5':
        is_valid = False
        while not is_valid:
            new_date =  input('Ingrese la fecha en formato DD/MM/YYYY:')

            try:
                datetime.strptime(new_date, '%d/%m/%Y')
                is_valid = True
                task['do_until'] = new_date
            except ValueError:
                print('Formato de fecha es incorecto.')



def print_task_info(task):
    """
       Imprime la información detallada de una tarea específica.
    """
    utils.clear_console()
    print(f'Nombre: {task["name"]}\n'
          f'Descripcion: {task["description"]}\n'
          f'Prioridad: {priorities[task["priority"]]}\n'
          f'Estado: {statuses[task["status"]]}\n'
          f'Team: {teams[task["team_id"]]["name"]}\n')