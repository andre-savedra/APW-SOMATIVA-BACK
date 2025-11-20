from.models import CustomUser

def check_group(group_name: str, user) -> bool:
    if not user or not user.is_authenticated:
        return False
    if hasattr(user, 'cargo') and user.cargo.upper() == group_name.upper():
        return True
    if hasattr(user, 'groups'):
        return user.groups.filter(name=group_name.upper()).exists()
    return False
def is_Admin(user_id) -> bool:
    return check_group('ADMIN', user_id)

def is_Inspecao(user_id) -> bool:
    return check_group('INSPECAO', user_id)

def is_Engenharia(user_id) -> bool:
    return check_group('ENGENHARIA', user_id)

def is_Producao(user_id) -> bool:
    return check_group('PRODUCAO', user_id)

def is_Manutencao(user_id) -> bool:
    return check_group('MANUTENCAO', user_id)

def is_LiderProducao(user_id) -> bool:
    return check_group('LIDER_PRODUCAO', user_id)

