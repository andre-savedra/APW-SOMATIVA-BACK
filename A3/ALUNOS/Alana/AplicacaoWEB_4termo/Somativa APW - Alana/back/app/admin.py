from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Produto, Categoria, Setor, Escaninhos, Marca
from .models.custom_user import CustomUser

class AdminCustomUser(UserAdmin):
    model = CustomUser

    list_display = ['id', 'email', 'name', 'is_staff', 'is_active']
    list_display_links = ('id', 'email')

    # Campos exibidos no admin ao editar usuário
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'creation_date')}),
    )

    # Layout ao adicionar novo usuário
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )

    ordering = ['email']
    search_fields = ['email', 'name']


admin.site.register(CustomUser, AdminCustomUser)
admin.site.register(Produto)
admin.site.register(Categoria)
admin.site.register(Setor)
admin.site.register(Escaninhos)
admin.site.register(Marca)

