from rest_framework import permissions
from .models import *
from datetime import timedelta
from django.utils import timezone

class IsInspector(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == '4'

    def has_object_permission(self, request, view, obj):
        return not obj.inspect_date or obj.inspector == request.user

class IsProduction(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == '1'

class IsMaintenance(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == '2'

class IsProductionLeader(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == '3'
    
    # Permissões funcionando parcialmente :C