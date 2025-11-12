from rest_framework import permissions
from .models.customuser import Cargo

# Função auxiliar para obter o cargo, centralizada aqui para as permissões
def get_user_cargo(user):
    if user.is_superuser:
        return Cargo.ADMIN
    try:
        # Acesso direto ao campo 'cargo' no modelo Funcionario
        return user.cargo
    except:
        return None

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        cargo = get_user_cargo(request.user)
        if cargo == Cargo.ADMIN:
            return True
        return request.method in permissions.SAFE_METHODS

class LotePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        cargo = get_user_cargo(user)

        # R. 11: Admin pode tudo
        if cargo == Cargo.ADMIN:
            return True

        # R. 7: Produção pode CRUD
        if cargo == Cargo.PRODUCAO:
            return True

        # R. 6 e R. 5: Engenharia e Inspeção só podem visualizar
        if cargo in [Cargo.ENGENHARIA, Cargo.INSPECAO]:
            return request.method in permissions.SAFE_METHODS
        
        # Manutenção, Líder, etc. só podem visualizar (SAFE_METHODS)
        return request.method in permissions.SAFE_METHODS 
    
class IsLiderProducaoOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
            
        cargo = get_user_cargo(user)
        
        # R. 10: Líder de Produção e Admin podem acessar
        return cargo in [Cargo.ADMIN, Cargo.LIDER_PRODUCAO]

# --- CLASSES ADICIONAIS NECESSÁRIAS (Sem Comentários) ---

class IsProducaoOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        cargo = get_user_cargo(request.user)
        return cargo in [Cargo.PRODUCAO, Cargo.ADMIN]

class IsEngenhariaOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        cargo = get_user_cargo(request.user)
        return cargo in [Cargo.ENGENHARIA, Cargo.ADMIN]

class IsManutencaoOrEngenhariaOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        cargo = get_user_cargo(request.user)
        return cargo in [Cargo.MANUTENCAO, Cargo.ENGENHARIA, Cargo.ADMIN]

class IsManutencaoOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        cargo = get_user_cargo(request.user)
        return cargo in [Cargo.MANUTENCAO, Cargo.ADMIN]
        
class CategoriaPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        cargo = get_user_cargo(request.user)
        if cargo in [Cargo.ADMIN, Cargo.ENGENHARIA]:
            return True
        return request.method in permissions.SAFE_METHODS

class EngenhariaCanViewOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        cargo = get_user_cargo(request.user)
        if cargo in [Cargo.ADMIN, Cargo.PRODUCAO]:
            return True
        if cargo == Cargo.ENGENHARIA:
            return request.method in permissions.SAFE_METHODS
        return False