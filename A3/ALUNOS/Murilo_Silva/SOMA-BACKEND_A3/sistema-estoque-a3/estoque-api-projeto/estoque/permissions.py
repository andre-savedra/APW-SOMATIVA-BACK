from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Permissão customizada que permite:
    - Leitura para usuários autenticados
    - Escrita apenas para administradores (is_staff=True)
    """
    
    def has_permission(self, request, view):
        # Permite leitura para usuários autenticados
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Permite escrita apenas para administradores
        return request.user and request.user.is_authenticated and request.user.is_staff

class IsOwnerOrAdmin(BasePermission):
    """
    Permissão customizada que permite acesso ao objeto apenas para:
    - O proprietário do objeto
    - Administradores
    """
    
    def has_object_permission(self, request, view, obj):
        # Administradores têm acesso total
        if request.user.is_staff:
            return True
        
        # Verifica se o objeto tem um campo 'user' ou similar
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False