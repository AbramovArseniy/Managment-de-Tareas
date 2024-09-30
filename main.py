from src.people.people import manage_people
from src.tasks.tasks import manage_tasks
from src.teams.teams import manage_teams
import utils


def main():
    actions = {
        '1': manage_people,
        '2': manage_teams,
        '3': manage_tasks
    }
    while True:
        utils.clear_console()
        cmd = input('Ingrese que quiere hacer:\n1. Manejar Personas\n2. Manejar Equipos\n3. Manejar Tareas\n4. Terminar el programa\n')
        while cmd not in ('1', '2', '3', '4'):
            print("Tiene que ingresar un numero entre 1 y 3\n")
            cmd = input()
        if cmd == '4':
            return
        actions[cmd]()


if __name__ == '__main__':
    main()
