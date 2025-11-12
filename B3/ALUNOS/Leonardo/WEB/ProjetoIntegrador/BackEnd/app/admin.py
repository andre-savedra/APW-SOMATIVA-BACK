from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Campos que aparecem na listagem
    list_display = ['id', 'registro', 'email', 'cpf', 'name', 'is_active', 'is_staff']
    search_fields = ['registro', 'email', 'cpf', 'name']
    ordering = ['name']  # Ordenação principal

    readonly_fields = ('creation_date',)

    # Campos exibidos no formulário de edição
    fieldsets = (
        (None, {'fields': ('registro', 'email', 'password')}),
        ('Informações Pessoais', {'fields': ('name', 'cpf', 'birth_date', 'phone', 'photo')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas importantes', {'fields': ('last_login',)}),
    )

    # Campos usados ao criar um novo usuário no admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('registro', 'email', 'cpf', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Ambiente)
admin.site.register(Category)
admin.site.register(Ativo)
admin.site.register(Tarefas)
admin.site.register(HistoricoStatus)
admin.site.register(TarefaStatusImage)
admin.site.register(Notification)

