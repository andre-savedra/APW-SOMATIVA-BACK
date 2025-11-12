from rest_framework.permissions import BasePermission

class IsProducao(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'PRODUCAO'

class IsChefeProducao(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'CHEFE_PRODUCAO'

class IsInspecao(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'INSPECAO'

class IsManutencao(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'MANUTENCAO'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'ADMIN'
