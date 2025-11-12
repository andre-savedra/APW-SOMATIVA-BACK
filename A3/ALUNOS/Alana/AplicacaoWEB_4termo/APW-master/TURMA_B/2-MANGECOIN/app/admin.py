from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


class AdminCustomUser(UserAdmin):
    model = CustomUser
    list_display = ['id','name','email', 'cpf']
    list_display_links = ('id', 'email', 'cpf',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups','user_permissions',)}),
        ('Monitoring', {'fields': ('last_login',)}),
        ('User Data', {'fields': ('name', 'cpf', 'rg', 'birth_date', 'phone', 'photo',)}),
        ('Address', {'fields': ('address_country','address_state','address_city', 
                                'address_district','address_street','address_number',
                                'address_zip_code',)}),
    )
    filter_horizontal = ('groups', 'user_permissions',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','name', 'cpf', 'rg', 'birth_date', 
                       'address_country', 'address_state', 'address_city',
                       'address_district', 'address_street', 'address_zip_code',
                       'address_number', 'password1', 'password2'),
        }),
    )
    ordering = ['email']

admin.site.register(CustomUser, AdminCustomUser)
admin.site.register(Token)
admin.site.register(Account)
admin.site.register(AccountToken)
admin.site.register(Transaction)
admin.site.register(Bet)
