import src.teams.teams as teams
import utils
from datetime import datetime

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

tasks = []


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
        'team': {'name': 'No assignada'},
        'do_until': datetime.max(),
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
    if len(teams.teams) == 0:
        print('Primero tiene que crear un equipo')
        return
    task_id = choose_task()
    for i, team in enumerate(teams.teams):
        print(f"{i + 1}: {team['name']}")

    print("Ingrese el número del equipo a que desea assingar la tarea")
    team_id = input()
    while team_id not in map(str, range(1, len(teams.teams) + 1)):
        print('Id no es valido')
        team_id = input()
    tasks[task_id]['team'] = teams.teams[int(team_id) - 1]
    tasks[task_id]['status'] = 2




def create_task():
    """
        Crea una nueva tarea solicitando al usuario el nombre, descripción y prioridad.

        Agrega la tarea creada a la lista `tasks`.
    """
    utils.clear_console()
    name = input('Ingrese nombre de la tarea: ')
    desc = input('Ingrese descripcion de la tarea: ')
    prio = input('Ingrese prioridad de su tarea:\n1. Baja\n2. Media\n3. Alta\n')
    while prio not in ('1', '2', '3'):
        print('Tiene que ingresar un numero entre 1 y 3:')
        prio = input()
    task = new_task(name, desc, int(prio))
    tasks.append(task)
    print('Tarea es guardada\n')


def print_tasks(filter_func=lambda task: True):
    """
        Muestra una lista de tareas filtradas por una función específica.

        Args:
            filter_func (function, optional): Función de filtrado que toma una tarea y devuelve True o False.
                                              Por defecto, muestra todas las tareas.
    """
    utils.clear_console()
    filtered_tasks = list(filter(filter_func, tasks))
    if len(filtered_tasks) == 0:
        print('No hay tareas adecuadas\n')
        return
    num_tasks = len(filtered_tasks)
    i = 0
    while i >= 0 and i < num_tasks:
        for id, task in enumerate(filtered_tasks[i:min(i + 10, num_tasks)]):
            print(f'Id: {tasks.index(task) + 1}\n'
                  f'Nombre: {task["name"]}\n')
        print(f'Pagina {i//10 + 1}/{(num_tasks - 1)//10 + 1}')
        print('Ingrese:\n'
              '1. Ver proxima pagina\n'
              '2. Ver pagina previa\n'
              '3. Continuar')
        cmd = input()
        if cmd not in ('1', '2', '3'):
            utils.clear_console()
            print('Tiene que ingresar un numero entre 1 y 3')
        elif cmd == '1':
            utils.clear_console()
            if i < num_tasks - 10:
                i += 10
            else:
                print('Ya esta en la ultima pagina')
        elif cmd == '2':
            utils.clear_console()
            if i >= 10:
                i -= 10
            else:
                print('Ya esta en la primepa pagina')
        elif cmd == '3':
            return



def filter_tasks():
    """
        Filtra las tareas por prioridad, estado o equipo.

        Solicita al usuario el criterio de filtrado y llama a la función `print_tasks()` para mostrar las tareas filtradas.
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
        print_tasks(lambda task: task['priority'] == int(prio))
    elif param == '2':
        status = input('Ingrese el estado:\n1. Para Asignar\n2. En Progreso\n3. En Revision\n4. Hecho\n')
        while status not in ('1', '2', '3', '4'):
            print("Tiene que ingresar un numero entre 1 y 4")
            status = input()
        print_tasks(lambda task: task['status'] == int(status))
    elif param == '3':
        for i, team in enumerate(teams.teams):
            print(f"{i + 1}: {team['name']}")

        print("Ingrese el número del equipo")
        team_id = input()
        while team_id not in map(str, range(1, len(teams.teams) + 1)):
            print('Id no es valido')
            team_id = input()
        print_tasks(lambda task: task['team'] == teams.teams[int(team_id) - 1])
    elif param == '4':
        print_tasks()


    id = input('Ingrese Id de tarea para ver mas informacion o -1 para volver al inicio: ')
    while id not in map(str, range(1, len(tasks) + 1)) and id != '-1':
        id = input('Id no es valido. Ingrese otra: ')
    if id == '-1':
        go_back()
    else:
        task = tasks[int(id) - 1]
        print_task_info(task)
        input('Pressiona Enter para volver a menu')


def choose_task():
    """
        Muestra una lista de tareas y solicita al usuario el ID de la tarea a seleccionar.

        Returns:
            int: Índice de la tarea seleccionada en la lista `tasks`.
    """
    utils.clear_console()
    print_tasks()
    id = input("Ingrese el Id de la tarea: ")
    while id not in map(str, range(1, len(tasks) + 1)):
        print("Id no es valido")
        id = input("Ingrese el Id de la tarea: ") - 1
    return int(id) - 1


def delete_task():
    """
        Elimina una tarea seleccionada de la lista `tasks`.
    """
    utils.clear_console()
    if len(tasks) == 0:
        print('Todavia no hay tareas\n')
        return
    task_id = choose_task()
    tasks.pop(task_id)
    print("Tarea era eliminada con exito")


def change_task():
    """
        Modifica las propiedades de una tarea seleccionada (nombre, descripción, prioridad o estado).
    """
    utils.clear_console()
    if len(tasks) == 0:
        print('Todavia no hay tareas\n')
        return
    task_id = choose_task()
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
            task['done_at'] = datetime.now()

    elif cmd == '5':
        is_valid = False
        while not is_valid:
            new_date =  input('Ingrese la fecha en formato DD/MM/YYYY:')

            try:
                parsed_date = datetime.strptime(new_date, '%d/%m/%Y')
                is_valid = True
                task['do_until'] = parsed_date
            except ValueError:
                print('Formato de fecha es incorecto. Ingrese la fecha en formato DD/MM/YYYY:')



def print_task_info(task):
    """
       Imprime la información detallada de una tarea específica.
    """
    utils.clear_console()
    print(f'Nombre: {task["name"]}\n'
          f'Descripcion: {task["description"]}\n'
          f'Prioridad: {priorities[task["priority"]]}\n'
          f'Estado: {statuses[task["status"]]}\n'
          f'Team: {task["team"]["name"]}\n')