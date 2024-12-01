import pick

import utils
from src.authorization import authorization, close_session
from src.people.profile import manage_profile
from src.datos import *
import src.people.people as people_mod
from src.people.people import manage_people
import src.tasks.tasks as tasks_mod
import src.teams.teams as teams_mod
from src.tasks.tasks import manage_tasks
from src.teams.teams import manage_teams


def main():

    actions = {
        'Manejar mi Perfil': manage_profile,
        'Manejar Personas': manage_people,
        'Manejar Equipos': manage_teams,
        'Manejar Tareas': manage_tasks,
        'Terminar el Programa': 0
    }

    close_session()
    try:
        while True:
            utils.clear_console()
            if len(utils.get_session()) == 0:
                utils.save_to_json_file(authorization(), "src/session.json")
            input_msg = "Elija que quiere hacer"
            options = list(actions.keys())
            user_id = utils.get_session()['id']
            if people[user_id]['role'] != people_mod.USER_ROLE_ADMIN:
                options.remove('Manejar Personas')
            act, act_num = pick.pick(options, input_msg, indicator='=>')
            if act_num == len(options) - 1:
                utils.save_to_json_file(tasks, "src/tasks/tasks.json")
                utils.save_to_json_file(teams, "src/teams/teams.json")
                utils.save_to_json_file(people, "src/people/people.json")
                utils.save_to_json_file(role_requests, "src/people/role_requests.json")
                close_session()
                return
            actions[act]()
    except KeyboardInterrupt:
        # Si se mata al termenal, guarda los datos en un archivo.
        utils.save_to_json_file(tasks, "src/tasks/tasks.json")
        utils.save_to_json_file(teams, "src/teams/teams.json")
        utils.save_to_json_file(people, "src/people/people.json")
        utils.save_to_json_file(role_requests, "src/people/role_requests.json")
        close_session()


if __name__ == '__main__':
    main()
