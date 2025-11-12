from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permissão customizada que permite apenas leitura para usuários não-admin
    e acesso completo para admins
    """
    
    def has_permission(self, request, view):
        # Permissões de leitura são permitidas para qualquer usuário autenticado
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Permissões de escrita apenas para admins
        return request.user and request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser
        )

class IsAdminForPromotion(permissions.BasePermission):
    """
    Permissão específica para alterar status de promoção - apenas admins
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser
        )
    
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser
        )

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permissão que permite ao dono do objeto ou admin acessar/modificar
    """
    
    def has_object_permission(self, request, view, obj):
        # Admin tem acesso total
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # Verifica se o objeto tem um campo 'criado_por' e se é o dono
        if hasattr(obj, 'criado_por') and obj.criado_por == request.user:
            return True
        
        # Apenas leitura para outros usuários autenticados
        return request.method in permissions.SAFE_METHODS