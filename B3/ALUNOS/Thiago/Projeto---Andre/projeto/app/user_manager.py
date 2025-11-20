from rest_framework.permissions import BasePermission, SAFE_METHODS


class RecepcaoPodeModificarReservas(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        cargo = getattr(user, "cargo", None)

        if user.is_staff:
            return True

        if request.method in SAFE_METHODS:
            return True

        if request.method == "DELETE":
            return False

        return cargo in ("Recepçao", "Gerencia", "Admin")


from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsGovernanceForCleaning(BasePermission):
 
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        cargo = getattr(user, "cargo", None)
        
        if user.is_staff or cargo == "Admin":
            return True
    
        if cargo == "Governanca":
            if request.method in SAFE_METHODS:
                return True
            return request.method in ["PUT", "PATCH"]
    
        return request.method in SAFE_METHODS



class IsMaintenanceForAccommodation(BasePermission):
   
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        cargo = getattr(user, "cargo", None)

        if user.is_staff:
            return True

        if request.method in SAFE_METHODS:
            return True

        return cargo == "Manutencao"



class IsRecepcao(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == "Recepçao"


class IsGovernanca(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == "Governanca"


class IsManutencao(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == "Manutencao"
