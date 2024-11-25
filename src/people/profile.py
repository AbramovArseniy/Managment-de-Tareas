import utils
import src.people.people as people
import src.authorization as auth


def manage_profile():
    session = utils.get_session()

    actions = [
        '   Ver mi perfil',
        '   Cambiar nombre',
        '   Cerrar session']
    opt, act = utils.choose(actions, 'Elija que quiere hacer:')
    if act == 0:
        people.show_person(session['id'])
        input('Presiona Enter para continuar...')
    elif act == 1:
        people.change_person_name(session['id'])
    elif act == 2:
        auth.log_out()
    else:
        return 0



