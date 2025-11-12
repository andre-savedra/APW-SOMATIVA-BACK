from rest_framework.permissions import BasePermission, SAFE_METHODS


def get_user_role(user):
    if not user.is_authenticated:
        return None
    if user.is_superuser:
        return 'ADMIN'
    try:
        return user.funcionario.cargo
    except Exception:
        return None


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        role = get_user_role(request.user)
        return role == 'ADMIN' or request.user.is_superuser


class IsMaintenanceOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        role = get_user_role(request.user)
        if request.method in SAFE_METHODS:
            return True
        return role in ('MANUTENCAO', 'ADMIN')


class IsProductionOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        role = get_user_role(request.user)
        if request.method in SAFE_METHODS:
            return True
        return role in ('PRODUCAO', 'LIDER_PRODUCAO', 'ADMIN')


class IsLeaderOnly(BasePermission):
    def has_permission(self, request, view):
        role = get_user_role(request.user)
        return role in ('LIDER_PRODUCAO', 'ADMIN')


class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        role = get_user_role(request.user)
        return role == 'ADMIN'

