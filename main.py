task_tmpl = {
    'name':'',
    'description':'',
    'priority':'', # Baja, Media, Alta
    'status':'', # Para Asignar, En Progreso, En Revision, Hecho, Para Eliminar
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

def create_task():
    name = input('Ingrese nombre de la tarea: ')
    desc = input('Ingrese descripcion de la tarea: ')
    priopidad = int(input('Ingrese prioridad de su tarea\n1. Baja\n2. Media\n3. Alta\n'))
    task = new_task(name, desc, priopidad)
    tasks.append(task)
    print('Tarea es guardada\n')



def new_task(name, desc, prio):
    task = {
        'name': name,
        'description': desc,
        'priority': prio,
        'status': 1
    }
    return task


def delete_task(task_ind):
    tasks.pop(task_ind)


def change_task(task, name, desc, prio, status):
    task['name'] = name
    task['description'] = desc
    task['priority'] = prio
    status['status'] = status


def print_task(task):
    print(f'Nombre: {task["name"]}\n'
          f'Descripcion: {task["description"]}\n'
          f'Prioridad: {priorities[task["priority"]]}\n'
          f'Status: {statuses[task["status"]]}\n')

create_task()
create_task()
print_task(tasks[0])
print_task(tasks[1])


