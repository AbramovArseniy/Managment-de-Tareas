from datetime import datetime

from src.people.people import new_person
from src.tasks.tasks import new_task


def test_new_task():
    assert new_task("123", "123", 1) == {
        'name': "123",
        'description': "123",
        'priority': 1,
        'status': 0,
        'team_id': '-1',
        'do_until': datetime.max.strftime("%d/%m/%Y"),
        'done_at': ''
    }


def test_new_person():
    assert new_person("Dani", 19, "dani", "1234") == {
        'name': "Dani",  # Nombre de la persona
        'age': 19,  # Edad de la persona
        'role': 2,  # Rol predeterminado (Desarrollador)
        'login': "dani",  # Login único de la persona
        'password': "1234",  # Contraseña de la persona
    }
