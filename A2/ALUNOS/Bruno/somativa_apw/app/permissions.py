from rest_framework.permissions import BasePermission

class IsMaintenanceUser(BasePermission):
    """
    Permite acesso apenas a usuários do grupo 'MANUTENÇÃO'.
    """
    def has_permission(self, request, view):
        # Verifica se o usuário está logado e se pertence ao grupo
        # Armazena os grupos permitidos em um array
        allowed_groups = ['MANUTENÇÃO', 'ADMIN']
        return request.user.is_authenticated and \
               request.user.groups.filter(name__in=allowed_groups).exists()


class IsLeaderUser(BasePermission):

    def has_permission(self, request, view):
        allowed_groups = ['LIDER_PRODUÇÃO', 'ADMIN']
        return request.user.is_authenticated and \
               request.user.groups.filter(name__in=allowed_groups).exists()