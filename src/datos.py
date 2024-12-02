import utils

# Cargar datos de equipos desde un archivo JSON
teams = utils.load_from_json('src/teams/teams.json')

# Agregar un equipo predeterminado para tareas no asignadas
teams['-1'] = {"name": "No asignada", 'person_ids': []}

# Cargar datos de tareas desde un archivo JSON
tasks = utils.load_from_json('src/tasks/tasks.json')

# Cargar datos de personas desde un archivo JSON
people = utils.load_from_json('src/people/people.json')

# Cargar solicitudes de roles desde un archivo JSON
role_requests = utils.load_from_json('src/people/role_requests.json')
