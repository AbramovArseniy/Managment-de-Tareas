import utils
import src.people.people as people_mod
import src.tasks.tasks as tasks_mod
from src.datos import *
import src.authorization as auth


def manage_profile():
    """
        Permite gestionar el perfil del usuario actual.

        Ofrece opciones para ver el perfil, cambiar el nombre, ver tareas asignadas o cerrar sesión.
    """
    # Obtener el ID del usuario actual desde la sesión
    cur_user_id = utils.get_session()['id']

    # Opciones disponibles para la gestión del perfil
    actions = [
        'Ver mi perfil',    # Mostrar la información del perfil
        'Cambiar nombre',   # Cambiar el nombre del usuario
        'Ver mis tareas',   # Ver las tareas asignadas al usuario
        'Cerrar sesión']    # Cerrar la sesión actual

    # Elegir una acción
    opt, act = utils.choose(actions, 'Elija qué quiere hacer:')
    if opt == utils.GO_BACK_STR:
        return None
    if opt == 'Ver mi perfil':
        # Mostrar la información del usuario actual
        people_mod.show_person(cur_user_id)
        input('Presiona Enter para continuar...')
    elif opt == 'Cambiar nombre':
        # Cambiar el nombre del usuario actual
        people_mod.change_person_name(cur_user_id)
    elif opt == 'Ver mis tareas':
        # Filtrar los equipos en los que está el usuario
        filtered_teams = dict(filter(lambda team: cur_user_id in team[1]['person_ids'], teams.items()))
        # Filtrar las tareas asignadas a esos equipos
        filtered_tasks = dict(filter(lambda task: task[1]['team_id'] in filtered_teams.keys(), tasks.items()))
        # Permitir al usuario elegir una tarea para ver más detalles
        task_id = utils.choose_id(filtered_tasks, 'Elija la tarea para ver toda la información: ')
        if task_id == '-1':
            return None
        else:
            # Mostrar la información de la tarea seleccionada
            tasks_mod.print_task_info(tasks[task_id])
            input('Presiona Enter para volver al menú...')
    elif 'Cerrar sesión':
        # Cerrar la sesión del usuario actual
        auth.log_out()
    else:
        return None
