from .models import CustomUser

def check_group(group_name,user_id)-> bool:
    try:        
        custom_user = CustomUser.objects.get(id=user_id)
        return custom_user.groups.filter(name=group_name).exists()
    except CustomUser.DoesNotExist:
        return False

def is_Admin(user_id)-> bool:
    return check_group('Admin',user_id)

def is_Premium(user_id)-> bool:
    return check_group('Premium',user_id)

def is_Basic(user_id)-> bool:
    return check_group('Basic',user_id)
