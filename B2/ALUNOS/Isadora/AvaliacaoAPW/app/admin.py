from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['id', 'email', 'cpf']
    search_fields = ['email', 'cpf',]
    ordering = ['email']
    fieldsets = (
        ('Campos Obrigatórios', {'fields':('email','password','cpf')}),
        ('Permissões', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions',)}),
        ('Cadastro', {'fields': ('phone_number', 'birth_date',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password1','password2','is_staff','is_active','groups','user_permissions',)
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Produto)
admin.site.register(Maquina)
admin.site.register(Manutencao)
admin.site.register(Lote)
admin.site.register(ItensLote)