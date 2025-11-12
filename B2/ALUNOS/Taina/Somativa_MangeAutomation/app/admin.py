
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Produto, Lote, Maquina, Manutencao, ItemProduzido

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'role', 'first_name', 'last_name', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_superuser', 'is_active']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Informações Adicionais'), {
            'fields': ('role', 'cpf', 'data_contratacao', 'numero_registro')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name'),
        }),
        (_('Informações Adicionais'), {
            'fields': ('role', 'cpf', 'data_contratacao', 'numero_registro')
        }),
    )

# Registrar TODOS os modelos
admin.site.register(User, CustomUserAdmin)
admin.site.register(Produto)
admin.site.register(Lote)
admin.site.register(Maquina)
admin.site.register(Manutencao)
admin.site.register(ItemProduzido)