from.models import CustomUser

def check_group(group_name, user_id) -> bool:
    try:
        custom_user = CustomUser.objects.get(id=user_id)
        return custom_user.groups.filter(name=group_name).exists()
    except CustomUser.DoesNotExist:
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

