from src.people.people import new_person
from src.tasks.tasks import new_task


def new_task_test():
    assert new_task("123", "123", 1) == {
        'name': "123",
        'description': "123",
        'priority': 1,
        'status': 1,
        'team': {'name': 'No assignada'}
    }


def new_person_test():
    assert new_person("Dani", "Igoshev", 19, 1) == {
        'name': "Dani",
        'surname': "Igoshev",
        'age': 19,
        'specialization': 1,
    }


new_task_test()
new_person_test()