from rest_framework import permissions


class RecepcaoPodeModificarReservas(permissions.BasePermission):
    def tem_permissao(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        role = getattr(request.user, 'cargo', None) or getattr(request.user, 'cargo', None)
        if request.user.is_staff:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'DELETE':
            return False

        if role == 'RECEPCAO' or role in ('GERENCIA', 'ADMIN'):
            return True

        return False

class IsGovernanceForCleaning(permissions.BasePermission):

    def tem_permissao(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        role = getattr(request.user, 'cargo', None) or getattr(request.user, 'cargo', None)
        if request.user.is_staff:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return role == 'GOVERNANCA'


class IsMaintenanceForAccommodation(permissions.BasePermission):
    
    def tem_permissao(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        role = getattr(request.user, 'cargo', None) or getattr(request.user, 'cargo', None)
        if request.user.is_staff:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return role == 'MANUTENCAO'
    

from rest_framework.permissions import BasePermission

class RecepcaoPermission(BasePermission):
    def has_permission(self, request, view):
        user = getattr(request.user, 'empregado', None)
        if not user:
            return False
        if user.cargo == 'RECEPCAO':
            # Pode criar, editar e visualizar, mas não deletar
            return request.method in ['GET', 'POST', 'PUT', 'PATCH']
        return True
    
from rest_framework.permissions import BasePermission

class IsRecepcao(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'RECEPCAO'

class IsGovernanca(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'GOVERNANCA'

class IsManutencao(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'MANUTENCAO'
