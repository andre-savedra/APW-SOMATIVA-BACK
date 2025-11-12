from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import *
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'name', 'role', 'is_staff', 'is_active', 'nif','cpf', 'hiring_date']
    list_filter = ['role', 'is_staff', 'is_active']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('name', 'nif', 'cpf', 'hiring_date')}),
        ('Cargo', {'fields': ('role',)}),
        ('Permissões', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    
    search_fields = ('email', 'name')
    ordering = ('email',)

# admin.site.register(CustomUser)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Machine)
admin.site.register(Lote)
admin.site.register(Maintence)

