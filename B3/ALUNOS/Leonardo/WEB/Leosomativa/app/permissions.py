from rest_framework import permissions
from .models import Employee


class ReceptionReservationPermission(permissions.BasePermission):
    """
    Permissão para controlar o acesso de funcionários da recepção às reservas.
    """

    def has_permission(self, request, view):
        # Permite leitura para todos usuários autenticados
        if request.method in permissions.SAFE_METHODS:
            return True

        # Usuários autenticados devem ter um Employee vinculado
        try:
            employee = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return False

        # Funcionários da recepção não podem deletar
        if employee.position == 'reception' and request.method == 'DELETE':
            return False

        # Funcionários da recepção podem criar e editar
        if employee.position == 'reception' and request.method in ['POST', 'PUT', 'PATCH']:
            return True

        # Administradores ou outros cargos podem fazer tudo
        if employee.position in ['management', 'admin']:
            return True

        return False


class HousekeepingPermission(permissions.BasePermission):
    """
    Permite que funcionários da governança apenas atualizem
    o status de limpeza e a data da última higienização.
    """

    def has_object_permission(self, request, view, obj):
        # Permite leitura para todos usuários autenticados
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            employee = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return False

        # Funcionário da governança
        if employee.position == 'housekeeping':
            # Permite apenas métodos PATCH ou PUT
            if request.method in ['PATCH', 'PUT']:
                # Verifica se apenas os campos permitidos estão sendo alterados
                allowed_fields = ['status', 'last_cleaning_date', 'last_cleaning_employee']
                if all(field in allowed_fields for field in request.data.keys()):
                    return True
            return False

        # Admins ou gerentes podem fazer tudo
        if employee.position in ['admin', 'management']:
            return True

        return False


class MaintenancePermission(permissions.BasePermission):
    """
    Permite que funcionários da manutenção atualizem o status da acomodação
    e registrem histórico de manutenção.
    """

    def has_object_permission(self, request, view, obj):
        # Permite leitura para todos usuários autenticados
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            employee = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return False

        # Funcionário da manutenção
        if employee.position == 'maintenance':
            if request.method in ['PATCH', 'PUT']:
                # Só permite atualizar o status da acomodação
                allowed_fields = ['status']
                if all(field in allowed_fields for field in request.data.keys()):
                    return True
            return False

        # Admin ou gerência podem fazer tudo
        if employee.position in ['admin', 'management']:
            return True

        return False
