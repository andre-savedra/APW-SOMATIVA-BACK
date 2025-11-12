from rest_framework import permissions
from .models import Funcionario

def get_user_cargo(user):
    """ Helper para pegar o cargo do usuário logado de forma segura. """
    try:
        return user.funcionario.cargo
    except Funcionario.DoesNotExist:
        return None

class AdminSupervisorFullAccessReadOnlyOthers(permissions.BasePermission):
    """
    Permissão genérica:
    - Admin/Supervisor: Acesso total (CRUD).
    - Outros (Engenheiro, Motorista, Mecânico): Apenas leitura (GET).
    """
    def has_permission(self, request, view):
        if request.user.is_superuser: 
            return True
        
        cargo = get_user_cargo(request.user)
        
        if cargo in [Funcionario.Cargos.ADMIN, Funcionario.Cargos.SUPERVISOR_FROTA]:
            return True 
        
        
        return request.method in permissions.SAFE_METHODS


class ViagemPermission(permissions.BasePermission):
    """
    Regras de Permissão para a ViewSet de Viagens:
    - Admin/Supervisor: Acesso total.
    - Engenheiro/Mecânico: Apenas leitura (GET). <-- MECÂNICO ADICIONADO
    - Motorista: Acesso permitido (lógica de filtro no get_queryset).
    - Outros: Negado.
    """
    def has_permission(self, request, view):
        if request.user.is_superuser: 
            return True
        
        cargo = get_user_cargo(request.user)

        if cargo in [Funcionario.Cargos.ADMIN, Funcionario.Cargos.SUPERVISOR_FROTA]:
            return True

       
       
        if cargo in [Funcionario.Cargos.ENGENHEIRO, Funcionario.Cargos.MECANICO]:
            return request.method in permissions.SAFE_METHODS

        if cargo == Funcionario.Cargos.MOTORISTA:
            return True

        return False


class ManutencaoPermission(permissions.BasePermission):
    """
    Regras de Permissão para Manutenção:
    - Admin/Supervisor/Mecânico: Acesso total (CRUD).
    - Engenheiro: Apenas leitura (GET).
    - Outros: Negado.
    """
    def has_permission(self, request, view):
        if request.user.is_superuser: 
            return True
        
        cargo = get_user_cargo(request.user)

        if cargo in [
            Funcionario.Cargos.ADMIN, 
            Funcionario.Cargos.SUPERVISOR_FROTA, 
            Funcionario.Cargos.MECANICO
        ]:
            return True 

        if cargo == Funcionario.Cargos.ENGENHEIRO:
            return request.method in permissions.SAFE_METHODS 

        return False 

class DashboardAccessPermission(permissions.BasePermission):
    """
    Permite acesso ao Dashboard apenas para cargos de gestão.
    - Admin, Supervisor: Acesso permitido.
    - Outros: Negado.
    """
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        
        cargo = get_user_cargo(request.user)
        
        if cargo in [
            Funcionario.Cargos.ADMIN, 
            Funcionario.Cargos.SUPERVISOR_FROTA
        ]:
            return True
        
        return False

class IsMecanicoOrAdminSupervisor(permissions.BasePermission):
    """
    Permite acesso apenas a Mecânicos, Admins e Supervisores.
    """
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        
        cargo = get_user_cargo(request.user)
        
        return cargo in [
            Funcionario.Cargos.MECANICO,
            Funcionario.Cargos.ADMIN,
            Funcionario.Cargos.SUPERVISOR_FROTA
        ]


class CategoriaVeiculoPermission(permissions.BasePermission):
    """
    Regras de Permissão para a ViewSet de Categorias de Veículo:
    - Admin/Supervisor: Acesso total (CRUD).
    - Engenheiro: Pode ler (GET) e criar (POST).
    - Outros: Apenas leitura (GET).
    """
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        
        cargo = get_user_cargo(request.user)
        
        if cargo in [Funcionario.Cargos.ADMIN, Funcionario.Cargos.SUPERVISOR_FROTA]:
            return True

        if cargo == Funcionario.Cargos.ENGENHEIRO:
            return request.method in (permissions.SAFE_METHODS + ('POST',))

        
        return request.method in permissions.SAFE_METHODS