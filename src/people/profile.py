import utils
import src.people.people as people_mod
import src.tasks.tasks as tasks_mod
from src.datos import *
import src.authorization as auth


def manage_profile():
    cur_user_id = utils.get_session()['id']

    actions = [
        'Ver mi perfil',
        'Cambiar nombre',
        'Ver mis tareas',
        'Cerrar session']
    opt, act = utils.choose(actions, 'Elija que quiere hacer:')
    if opt == utils.GO_BACK_STR:
        return None
    if opt == 'Ver mi perfil':
        people_mod.show_person(cur_user_id)
        input('Presiona Enter para continuar...')
    elif opt == 'Cambiar nombre':
        people_mod.change_person_name(cur_user_id)
    elif opt == 'Ver mis tareas':
        filtered_teams = dict(filter(lambda team: cur_user_id in team[1]['person_ids'], teams.items()))
        filtered_tasks = dict(filter(lambda task: task[1]['team_id'] in filtered_teams.keys(), tasks.items()))
        task_id = utils.choose_id(filtered_tasks, 'Elija la tarea para ver toda la informacion: ')
        if task_id == '-1':
            return None
        else:
            tasks_mod.print_task_info(tasks[task_id])
            input('Pressiona Enter para volver a menu...')
    elif 'Cerrar session':
        auth.log_out()
    else:
        return None



