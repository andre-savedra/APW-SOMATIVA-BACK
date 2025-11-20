from rest_framework.permissions import BasePermission

class BaseCargoPermission(BasePermission):
    """Base de permissão que dá acesso total ao Admin"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'Admin'


class Admin(BaseCargoPermission):
    """Apenas ADMIN tem acesso"""
    def has_permission(self, request, view):
        # Admin já tem acesso pelo BaseCargoPermission
        if super().has_permission(request, view):
            return True
        return False  # Somente admin


class Inspecao(BaseCargoPermission):
    """Apenas INSPEÇÃO tem acesso"""
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True  # Admin sempre pode
        return request.user.is_authenticated and request.user.cargo == 'Inspecao'


class Engenharia(BaseCargoPermission):
    """Apenas ENGENHARIA tem acesso"""
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True
        return request.user.is_authenticated and request.user.cargo == 'Engenharia'


class Producao(BaseCargoPermission):
    """Apenas PRODUÇÃO tem acesso"""
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True
        return request.user.is_authenticated and request.user.cargo == 'Producao'


class Manutencao(BaseCargoPermission):
    """Apenas MANUTENÇÃO tem acesso"""
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True
        return request.user.is_authenticated and request.user.cargo == 'Manutencao'


class LiderProducao(BaseCargoPermission):
    """Apenas LÍDER DE PRODUÇÃO tem acesso"""
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True
        return request.user.is_authenticated and request.user.cargo == 'Lider_producao'


class ManageMaquinas(BaseCargoPermission):
    """Apenas MANUTENÇÃO e ENGENHARIA podem gerenciar máquinas"""
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True  # Admin sempre pode
        if not request.user.is_authenticated:
            return False
        if request.user.cargo in ['Manutencao', 'Engenharia']:
            return True
        if request.method == 'GET':
            return True
        return False


class ManageCategorias(BaseCargoPermission):
    """Apenas ENGENHARIA e ADMIN podem criar categorias"""
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.cargo == 'Engenharia':
            return True
        if request.method == 'GET':
            return True
        return False


class ManageLotes(BaseCargoPermission):
    """Apenas PRODUÇÃO e ADMIN podem gerenciar lotes"""
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.cargo == 'Producao':
            return True
        if request.user.cargo == 'Engenharia' and request.method == 'GET':
            return True
        return False


class Authenticated(BaseCargoPermission):
    """Usuário precisa estar autenticado"""
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True  # Admin sempre pode
        return request.user.is_authenticated
