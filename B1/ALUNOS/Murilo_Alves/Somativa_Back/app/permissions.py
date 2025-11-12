# app/permissions.py
from rest_framework import permissions
from .models import Manutencao

class CargoPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if hasattr(request.user, 'funcionario'):
            print(request.user.funcionario.cargo)
            view.cargo_user = request.user.funcionario.cargo
            return True
        return False

    def has_object_permission(self, request, view, obj):
        cargo = getattr(view, 'cargo_user', None)

        if cargo == 'ADMIN':
            return True
        elif cargo == 'MOTORISTA':
            if hasattr(obj, 'motorista'):
                return obj.motorista.usuario == request.user
        elif cargo == 'ENGENHEIRO':
            return True  # só leitura
        elif cargo == 'MECANICO':
            if isinstance(obj, Manutencao):
                return True
        elif cargo == 'SUPERVISOR_FROTA':
            return True
        return False
