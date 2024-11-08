from people import manage_people
from teams import manage_teams
from tasks import manage_tasks

def main():
    actions = {
        '1': manage_people,
        '2': manage_teams,
        '3': manage_tasks
    }
    while True:
        cmd = input('Ingrese que quiere hacer:\n1. Manejar Personas\n2. Manejar Equipos\n3. Manejar Tareas\n')
        while cmd not in ('1', '2', '3'):
            print("Tiene que ingresar un numero entre 1 y 3\n")
            cmd = input()
        actions[cmd]()

main()