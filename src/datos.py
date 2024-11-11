import utils

teams = utils.load_from_json('src/teams/teams.json')
teams['-1'] = {"name": "No assingada",  'person_ids': []}
tasks = utils.load_from_json('src/tasks/tasks.json')
people = utils.load_from_json('src/people/people.json')
people_next_id = max(map(int, people.keys())) + 1
teams_next_id = max(map(int, teams.keys())) + 1
tasks_next_id = max(map(int, tasks.keys())) + 1

