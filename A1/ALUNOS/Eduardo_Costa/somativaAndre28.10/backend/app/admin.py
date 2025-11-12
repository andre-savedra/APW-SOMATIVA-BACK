from django.contrib import admin

from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class AdminFuncionario(UserAdmin):
    model = Funcionario
    search_fields = ('email', 'numero_registro')
    list_display = ['id', 'email', 'numero_registro']
    list_display_links = ('id', 'email', 'numero_registro',)
    fieldsets = (
        (None, {'fields': ('email','password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 
                                    'is_superuser', 'groups', 
                                    'user_permissions',)}),
        ('User data', {'fields': ('numero_registro', 'cpf',)}),
    )
    filter_horizontal = ('groups', 'user_permissions',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','nome','numero_registro','cpf','cargo','dt_contratacao','password1','password2',),
        }),
    )
    ordering = ['email']

admin.site.register(Funcionario, AdminFuncionario)
admin.site.register(Item)
admin.site.register(Lote)
admin.site.register(Maquina)
admin.site.register(Producao)
admin.site.register(Produto)


