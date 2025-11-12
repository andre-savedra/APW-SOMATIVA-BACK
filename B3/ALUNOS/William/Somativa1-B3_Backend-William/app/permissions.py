from rest_framework import permissions

class IsReceptionCreateEditView(permissions.BasePermission):
    """
    Recepção: pode create, update (PUT/PATCH) e view (GET), mas NOT delete.
    We'll allow any authenticated employee with cargo==RECEPCAO, GERENCIA or ADMIN for broader admin tasks.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        # assume you map request.user to Employee via profile in a real app.
        # For now, check Django superuser/staff as override:
        if user.is_superuser:
            return True
        # If you have Employee linked to User, implement the check here.
        # to keep this usable locally, allow authenticated users (dev). Otherwise enforce custom logic.
        if request.method == 'DELETE':
            return False
        return True


class IsGovernanceOnlyCleaning(permissions.BasePermission):
    """
    Governança: somente pode atualizar limpeza (PATCH em endpoint de limpeza) e acessar seu endpoint.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        # for dev simplicity: allow authenticated users (customize to check Employee.cargo == GOVERNANCA)
        return True

    def has_object_permission(self, request, view, obj):
        # Only allow PATCH updates from governance for cleaning update endpoints.
        if request.method in ['PATCH', 'PUT']:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return False


class IsMaintenance(permissions.BasePermission):
    """
    Manutenção: pode atualizar status da acomodação e criar maintenance records.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return True
