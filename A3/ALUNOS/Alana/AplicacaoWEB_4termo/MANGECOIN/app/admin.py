from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class AdminCustomUser(UserAdmin):
    model = CustomUser
    list_display = ['id', 'email', 'cpf']
    list_display_links = ('id', 'email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions',{'fields': ('is_active','is_staff','is_superuser','groups','user_permissions',)}),
        ('Monitoring', {'fields': ('last_login',)}),
        ('User data', {'fields': ('name', 'cpf', 'rg', 'birth_date','phone','photo',)}),
        ('Address', {'fields': ('address_street', 'address_district', 'address_number',
                       'address_zip_code', 'address_city', 'address_state', 
                       'address_country',)}),        

    )
    filter_horizontal = ('groups', 'user_permissions',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'cpf', 'rg', 'birth_date', 'address_street', 'address_district', 'address_number',
                       'address_zip_code', 'address_city', 'address_state', 
                       'address_country','phone','password1', 'password2'),
        }),
    )
    
                       
    ordering = ['email']

admin.site.register(CustomUser, AdminCustomUser)
admin.site.register(Token)
admin.site.register(Account)
admin.site.register(AccountToken)
admin.site.register(Transactions)
admin.site.register(Bets)
