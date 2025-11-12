from rest_framework import permissions

class IsReceptionCreateEdit(permissions.BasePermission):
    
    #Recepção: criar, editar e visualizar reservas, mas NÃO deletar
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.cargo == 'RECEPCAO' or request.user.cargo in ['GERENCIA','ADMIN']

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

class IsGovernanca(permissions.BasePermission):
    
    #Governança: permite atualizar limpeza (data_ultima_limpeza, funcionario_responsavel)
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.cargo == 'GOVERNANCA' or request.user.cargo in ['GERENCIA','ADMIN']

class IsManutencao(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.cargo == 'MANUTENCAO' or request.user.cargo in ['GERENCIA','ADMIN']
