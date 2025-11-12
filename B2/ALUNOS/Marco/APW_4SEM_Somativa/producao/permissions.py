from rest_framework import permissions

class IsChefeProducao(permissions.BasePermission):
    """
    Permissão que permite apenas aos chefes de produção realizar a ação.
    """
    def has_permission(self, request, view):
        return request.user and request.user.cargo == 'CHEFE_PRODUCAO'

class IsManutencao(permissions.BasePermission):
    """
    Permissão que permite apenas aos funcionários de manutenção realizar a ação.
    """
    def has_permission(self, request, view):
        return request.user and request.user.cargo == 'MANUTENCAO'

class IsInspecao(permissions.BasePermission):
    """
    Permissão que permite apenas aos funcionários de inspeção realizar a ação.
    """
    def has_permission(self, request, view):
        return request.user and request.user.cargo == 'INSPECAO'

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissão que permite apenas ao proprietário do objeto editá-lo.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Verifica se o objeto tem um atributo criado_por ou responsavel
        if hasattr(obj, 'criado_por'):
            return obj.criado_por == request.user
        elif hasattr(obj, 'responsavel'):
            return obj.responsavel == request.user
        elif hasattr(obj, 'funcionario'):
            return obj.funcionario == request.user
        
        return False