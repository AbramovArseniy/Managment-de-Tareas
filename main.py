import utils
from src.people.people import manage_people, people
from src.tasks.tasks import manage_tasks, tasks
from src.teams.teams import manage_teams, teams


def main():
    actions = {
        '1': manage_people,
        '2': manage_teams,
        '3': manage_tasks
    }
    try:
        while True:
            utils.clear_console()
            cmd = input(
                'Ingrese que quiere hacer:\n1. Manejar Personas\n2. Manejar Equipos\n3. Manejar Tareas\n4. Terminar el programa\n')
            while cmd not in ('1', '2', '3', '4'):
                print("Tiene que ingresar un numero entre 1 y 3\n")
                cmd = input()

            if cmd == '4':
                utils.save_to_json_file(tasks, "src/tasks/tasks.json")
                utils.save_to_json_file(teams, "src/teams/teams.json")
                utils.save_to_json_file(people, "src/people/people.json")
                return

            actions[cmd]()

    except KeyboardInterrupt:
        # Si se mata al termenal, guarda los datos en un archivo.
        utils.save_to_json_file(tasks, "src/tasks/tasks.json")
        utils.save_to_json_file(teams, "src/teams/teams.json")
        utils.save_to_json_file(people, "src/people/people.json")


if __name__ == '__main__':
    main()
