from datetime import datetime

import utils
import src.people.people as people_mod
from src.datos import *

task_tmpl = {
    'name':'',
    'description':'',
    'priority':'', # Baja, Media, Alta
    'status':'', # Para Asignar, En Progreso, En Revision, Hecho
    'team_id': None,
    'do_until': ''
}

PRIORITY_LOW = 0
PRIORITY_MEDIUM = 1
PRIORITY_HIGH = 2

priorities = [
    'Baja',
    'Media',
    'Alta',
]

STATUS_TO_ASSIGN = 0
STATUS_IN_PROGRESS = 1
STATUS_IN_REVIEW = 2
STATUS_DONE = 3

statuses = [
    'Para Asignar',
    'En Progreso',
    'En Revision',
    'Hecho',
]


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
        'team_id': '-1',
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
    user_id = utils.get_session()["id"]

    actions = [
        manage_task,
        filter_tasks,
        go_back,
    ]
    input_msg = "Elija que quiere hacer"
    options = ["Manejar tarea",
               "Ver tareas"]

    if people[user_id]['role'] < 2:
        actions = [create_task] + actions
        options = ["Agregar tarea"] + options
    opt, ind = utils.choose(options, input_msg)
    if opt == utils.GO_BACK_STR:
        return 0
    actions[ind]()


def manage_task():
    utils.clear_console()
    if len(tasks) == 0:
        print('Todavia no hay tareas\n')
        input('Pressiona Enter para volver a menu...')
        return
    actions = [change_task]

    input_msg = "Elija que quiere hacer"
    options = ["Cambiar datos de tarea"]

    user_id = utils.get_session()["id"]
    if people[user_id]['role'] < 2:
        actions = actions + [delete_task, assign_team]
        options = options + ["Borrar tarea", "Assingar tarea a un equipo"]
    opt, ind = utils.choose(options, input_msg)
    if opt == utils.GO_BACK_STR:
        return 0
    actions[ind]()


def assign_team():
    """
       Asigna un equipo a una tarea.

       Permite al usuario elegir una tarea y asignarla a un equipo.
    """
    utils.clear_console()
    if len(teams) == 0:
        print('Primero tiene que crear un equipo')
        return
    task_id = utils.choose_id(tasks, "Elija el Id de la tarea: ")
    if task_id == '-1':
        return 0
    team_id = utils.choose_id(teams, "Elija el Id del equipo: ")
    if team_id == '-1':
        return 0
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
    input_msg = "Elija la prioridad"
    options = ["Baja",
               "Media",
               "Alta"]
    opt, prio = utils.choose(options, input_msg)
    if prio == utils.GO_BACK_STR:
        return 0
    task = new_task(name, desc, prio)


    tasks_next_id = 1
    if len(tasks.keys()) != 0:
        tasks_next_id = max(map(int, tasks.keys())) + 1
    tasks[str(tasks_next_id)] = task
    print('Tarea es guardada\n')
    input("Presiona Enter para continuar...")


def filter_tasks():
    """
        Filtra las tareas por prioridad, estado o equipo.

        Solicita al usuario el criterio de filtrado y llama a la función `utils.print_dict()` para mostrar las tareas filtradas.
    """
    utils.clear_console()
    if len(tasks) == 0:
        print('Todavia no hay tareas\n')
        input('Pressiona Enter para volver a menu...')
        return
    input_msg = "Por qué quiere filtrar las tareas?"
    options = ["Prioridad",
               "Estado",
               "Equipo",
               "Ver Todas"]
    opt, ind = utils.choose(options, input_msg)
    filter_func = lambda x: True
    if opt == "Prioridad":
        input_msg = "Elija la prioridad"
        options = ["Baja",
                   "Media",
                   "Alta"]
        opt, prio = utils.choose(options, input_msg)
        if opt == utils.GO_BACK_STR:
            return None
        filter_func = lambda task: task[1]['priority'] == prio
    elif opt == "Estado":
        input_msg = "Elija el estado"
        options = ["Para Asignar",
                   "En Progreso",
                   "En Revision",
                   "Hecho"]
        opt, status = utils.choose(options, input_msg)
        if opt == utils.GO_BACK_STR:
            return None

        filter_func = lambda task: task[1]['status'] == status
    elif opt == "Equipo":
        team_id = utils.choose_id(teams, "Elija el equipo")
        if team_id == '-1':
            go_back()
        filter_func = lambda task: task[1]['team_id'] == team_id
    elif opt == utils.GO_BACK_STR:
        return 0

    task_id = utils.choose_id(tasks, 'Elija la tarea para ver toda la informacion: ', filter_func)
    if task_id == '-1':
        go_back()
    else:
        print_task_info(tasks[task_id])
        input('Pressiona Enter para volver a menu...')


def delete_task():
    """
        Borra una tarea seleccionada de la lista `tasks`.
    """
    utils.clear_console()
    filter_func = lambda task: True
    user_id = utils.get_session()['id']

    if people[user_id]['role'] == people_mod.USER_ROLE_TEAM_LEAD:
        users_teams = dict(filter(lambda team: user_id in team[1]['person_ids'], teams.items()))
        filtered_tasks = dict(filter(lambda task: task[1]['team_id'] in users_teams.keys(), tasks.items()))
        task_id = utils.choose_id(filtered_tasks, "Elija el Id de la tarea que desea borrar: ")
    else:
        task_id = utils.choose_id(tasks, "Elija el Id de la tarea que desea borrar: ")
    if task_id == '-1':
        return 0
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
    if task_id == '-1':
        return 0
    task = tasks[task_id]
    input_msg = "Elija que quiere cambiar en la tarea:"
    options = ["Estado",
        "Descripcion"]

    if people[utils.get_session()['id']]['role'] < 2:
        options += ["Nombre",
                    "Descripcion",
                    "Prioridad",
                    "Fecha de Deadline"]
    opt, ind = utils.choose(options, input_msg)
    if opt == "Nombre":
        new_name = input('Ingrese el nuevo nombre de la tarea: ')
        task['name'] = new_name
    elif opt == "Descripcion":
        new_desc = input('Ingrese la nueva descripcion de la tarea: ')
        task['description'] = new_desc

    elif opt == "Prioridad":
        input_msg = "Elija la prioridad"
        options = ["Baja",
                   "Media",
                   "Alta"]
        opt, new_prio = utils.choose(options, input_msg)
        if opt == utils.GO_BACK_STR:
            return None
        task['priority'] = new_prio

    elif opt == "Estado":
        input_msg = "Elija el estado"
        options = ["Para Asignar",
                   "En Progreso",
                   "En Revision",
                   "Hecho"]
        opt, new_status = utils.choose(options, input_msg)
        if opt == utils.GO_BACK_STR:
            return None
        task['status'] = new_status
        if new_status == STATUS_DONE:
            task['done_at'] = datetime.now().strftime('%d/%m/%Y')

    elif opt == "Fecha de Deadline":
        is_valid = False
        while not is_valid:
            new_date =  input('Ingrese la fecha en formato DD/MM/YYYY:')

            try:
                datetime.strptime(new_date, '%d/%m/%Y')
                is_valid = True
                task['do_until'] = new_date
            except ValueError:
                print('Formato de fecha es incorecto.')
    else:
        return None


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