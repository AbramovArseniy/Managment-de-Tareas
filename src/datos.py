import utils

teams = utils.load_from_json('src/teams/teams.json')
teams['-1'] = {"name": "No assingada",  'person_ids': []}
tasks = utils.load_from_json('src/tasks/tasks.json')
people = utils.load_from_json('src/people/people.json')
session = None