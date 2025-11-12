# utils.py
from datetime import datetime, timedelta
from models import CustomUser

def is_governance(user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        return user.groups.filter(name='GOVERNANCA').exists()
    except CustomUser.DoesNotExist:
        return False
