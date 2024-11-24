import pick

import utils
from src.authorization import authorization
from src.people.people import manage_people, people
from src.tasks.tasks import manage_tasks, tasks
from src.teams.teams import manage_teams, teams


def main():
    utils.save_to_json_file(authorization(), "src/session.json")

    actions = {
        'Manejar Personas': manage_people,
        'Manejar Equipos': manage_teams,
        'Manejar Tareas': manage_tasks,
        'Terminar el programa': 0
    }

    try:
        while True:
            utils.clear_console()

            input_msg = "Elija que quiere hacer"
            options = list(actions.keys())
            act, act_num = pick.pick(options, input_msg, indicator='=>')
            if act_num == 3:
                utils.save_to_json_file(tasks, "src/tasks/tasks.json")
                utils.save_to_json_file(teams, "src/teams/teams.json")
                utils.save_to_json_file(people, "src/people/people.json")
                return
            actions[act]()

    except KeyboardInterrupt:
        # Si se mata al termenal, guarda los datos en un archivo.
        utils.save_to_json_file(tasks, "src/tasks/tasks.json")
        utils.save_to_json_file(teams, "src/teams/teams.json")
        utils.save_to_json_file(people, "src/people/people.json")


if __name__ == '__main__':
    main()
