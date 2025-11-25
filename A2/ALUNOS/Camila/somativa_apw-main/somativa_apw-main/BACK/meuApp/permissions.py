from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsProducaoOrReadOnly(BasePermission):
    """PERMITE CRUD APENAS A FUNCIONARIOS DE PRODUCAO"""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        funcionario = getattr(request.user, "funcionario", None)
        return funcionario and funcionario.cargo.nome.upper() == "PRODUÇÃO"
    
    
class IsManutencaoOrReadOnly(BasePermission):
    """PERMITE CRIAR/EDITAR MAQUINAS FUNCIONARIOS DE MANUTENÇÃO"""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        funcionario = getattr(request.user, "funcionario", None)
        return funcionario and funcionario.cargo.nome.upper() == "MANUTENÇÃO"
    
class IsLiderProducao(BasePermission):
    """PERMITE ACESSAR DASHBOARD FUNCIONARIOS LIDERES PRODUTCAO"""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        funcionario = getattr(request.user, "funcionario", None)
        return funcionario and funcionario.cargo.nome.upper() == "LIDER PRODUÇÃO"