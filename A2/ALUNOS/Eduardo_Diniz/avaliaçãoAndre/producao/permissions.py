from rest_framework import permissions

class IsProducao(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo in ['PRODUCAO', 'LIDER_PRODUCAO', 'ADMIN']

class IsLiderProducao(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo in ['LIDER_PRODUCAO', 'ADMIN']

class IsInspecao(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo in ['INSPECAO', 'ADMIN']

class IsManutencao(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo in ['MANUTENCAO', 'ADMIN']

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'ADMIN'

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.cargo == 'ADMIN'