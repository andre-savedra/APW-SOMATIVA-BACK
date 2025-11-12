from rest_framework.permissions import BasePermission

class Admin(BasePermission):
    """Apenas ADMIN tem acesso"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'Admin'


class Inspecao(BasePermission):
    """Apenas INSPEÇÃO tem acesso"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'Inspecao'


class Engenharia(BasePermission):
    """Apenas ENGENHARIA tem acesso"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'Engenharia'


class Producao(BasePermission):
    """Apenas PRODUÇÃO tem acesso"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'Producao'


class Manutencao(BasePermission):
    """Apenas MANUTENÇÃO tem acesso"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'Manutencao'


class LiderProducao(BasePermission):
    """Apenas LÍDER DE PRODUÇÃO tem acesso"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'Lider_producao'


class ManageMaquinas(BasePermission):
    """Apenas MANUTENÇÃO e ENGENHARIA podem gerenciar máquinas"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Admin sempre pode
        if request.user.cargo == 'Admin':
            return True
        
        # Manutenção e Engenharia podem criar/editar
        if request.user.cargo in ['Manutencao', 'Engenharia']:
            return True
        
        # Outros podem apenas visualizar (GET)
        if request.method == 'GET':
            return True
        
        return False


class ManageCategorias(BasePermission):
    """Apenas ENGENHARIA e ADMIN podem criar categorias"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Admin sempre pode
        if request.user.cargo == 'Admin':
            return True
        
        # Engenharia pode criar/editar
        if request.user.cargo == 'Engenharia':
            return True
        
        # Outros podem apenas visualizar (GET)
        if request.method == 'GET':
            return True
        
        return False


class ManageLotes(BasePermission):
    """Apenas PRODUÇÃO e ADMIN podem gerenciar lotes"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Admin sempre pode
        if request.user.cargo == 'Admin':
            return True
        
        # Produção pode fazer CRUD completo
        if request.user.cargo == 'Producao':
            return True
        
        # Engenharia pode apenas visualizar
        if request.user.cargo == 'Engenharia' and request.method == 'GET':
            return True
        
        return False


class Authenticated(BasePermission):
    """Usuário precisa estar autenticado"""
    def has_permission(self, request, view):
        return request.user.is_authenticated