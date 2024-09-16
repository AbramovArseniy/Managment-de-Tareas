import teams

task_tmpl = {
    'name':'',
    'description':'',
    'priority':'', # Baja, Media, Alta
    'status':'', # Para Asignar, En Progreso, En Revision, Hecho, Para Eliminar
    'team': None,
}

priorities = {
    1: 'Baja',
    2: 'Media',
    3: 'Alta'
}

statuses = {
    1: 'Para Asignar',
    2: 'En Progreso',
    3: 'En Revision',
    4: 'Hecho',
    5: 'Para Eliminar'
}

tasks = []


def new_task(name, desc, prio):
    task = {
        'name': name,
        'description': desc,
        'priority': prio,
        'status': 1,
        'team':{'name': 'No team assigned'}
    }
    return task


def go_back():
    return 0


def manage_tasks():
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
    name = input('Ingrese nombre de la tarea: ')
    desc = input('Ingrese descripcion de la tarea: ')
    prio = input('Ingrese prioridad de su tarea:\n1. Baja\n2. Media\n3. Alta\n')
    while prio not in ('1', '2', '3'):
        print('Tiene que ingresar un numero entre 1 y 3:')
        prio = input()
    task = new_task(name, desc, int(prio))
    tasks.append(task)
    print('Tarea es guardada\n')


def print_tasks(filter_func=lambda x: True):
    filtered_tasks = list(filter(filter_func, tasks))
    if len(filtered_tasks) == 0:
        print('No hay tareas adecuadas\n')
        return
    for id, task in enumerate(filtered_tasks):
        print(f'Id: {id + 1}\n'
              f'Nombre: {task["name"]}\n'
              f'Prioridad: {priorities[task["priority"]]}\n'
              f'Estado: {statuses[task["status"]]}\n'
              f'Team: {task["team"]["name"]}\n')


def filter_tasks():
    if len(tasks) == 0:
        print('Todavia no hay tareas\n')
        return
    param = input("Por qué quiere filtrar las tareas?\n"
                "1. Prioridad\n"
                "2. Estado\n"
                "3. Equipo\n")
    while param not in ('1', '2', '3'):
        print("Tiene que ingresar un numero entre 1 y 3")
        param = input()
    if param == '1':
        prio = input('Ingrese la nueva prioridad de la tarea:\n1. Baja\n2. Media\n3. Alta\n')
        while prio not in ('1', '2', '3'):
            print("Tiene que ingresar un numero entre 1 y 3")
            prio = input()
        print_tasks(lambda task: task['priority'] == int(prio))
    elif param == '2':
        status = input('Ingrese el estado:\n1. Para Asignar\n2. En Progreso\n3. En Revision\n4. Hecho\n 5. Para Eliminar\n')
        while status not in ('1', '2', '3', '4', '5'):
            print("Tiene que ingresar un numero entre 1 y 5")
            status = input()
        print_tasks(lambda task: task['priority'] == int(prio))
    elif param == '3':
        for i, team in enumerate(teams.teams):
            print(f"{i + 1}: {team['name']}")

        print("Ingrese el número del equipo")
        team_id = input()
        while team_id not in map(str, range(1, len(teams.teams) + 1)):
            print('Id no es valido')
            team_id = input()
        print_tasks(lambda task: task['team'] == teams.teams[int(team_id) - 1])


def choose_task():
    print_tasks()
    id = input("Ingrese el Id de la tarea: ")
    while id not in map(str, range(1, len(tasks) + 1)):
        print("Id no es valido")
        id = input("Ingrese el Id de la tarea: ") - 1
    return int(id) - 1


def delete_task():
    if len(tasks) == 0:
        print('Todavia no hay tareas\n')
        return
    task_id = choose_task()
    tasks.pop(task_id)
    print("Tarea era eliminada con exito")


def change_task():
    if len(tasks) == 0:
        print('Todavia no hay tareas\n')
        return
    task_id = choose_task()
    task = tasks[task_id]
    cmd = input("Elige que quiere cambiar en la tarea: \n"
                "1. Nombre\n"
                "2. Descripcion\n"
                "3. Prioridad\n"
                "4. Estado\n")
    while cmd not in ('1', '2', '3', '4'):
        print("Tiene que ingresar un numero entre 1 y 4")
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
        new_status = input('Ingrese el nuevo estado de la tarea:\n1. Para Asignar\n2. En Progreso\n3. En Revision\n4. Hecho\n 5. Para Eliminar\n')
        while new_status not in ('1', '2', '3', '4', '5'):
            print("Tiene que ingresar un numero entre 1 y 5")
            new_status = input()

        task['status'] = int(new_status)




def print_task_info(task):
    print(f'Nombre: {task["name"]}\n'
          f'Descripcion: {task["description"]}\n'
          f'Prioridad: {priorities[task["priority"]]}\n'
          f'Estado: {statuses[task["status"]]}\n'
          f'Team: {task["team"]["name"]}')


