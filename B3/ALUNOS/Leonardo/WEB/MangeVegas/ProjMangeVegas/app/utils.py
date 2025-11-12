from .models import CustomUser

def check_group(group_name,user_id) -> bool:
    try:
        #select * from CustomUser where id = x
        user = CustomUser.objects.get(id=user_id)
        return user.groups.filter(name=group_name).exists()
    except CustomUser.DoesNotExist:
        return False

def isBasic(user_id) -> bool:
    return check_group('Basic',user_id)

def isPremium(user_id) -> bool:
    return check_group('Premium',user_id)