from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

#Nessa página admin.py são inseridas as classes criadas no arquivo models.py. Essas classes se toranam as tabelas do banco de dados.

#Este adminCustomUser é a página que vai mostrar os dados do usuario. Os campos de como devem aparecer
class adminCustomUser(UserAdmin):
    model = CustomUser
    list_display = ['id', 'name', 'email'] #é o que vai aparecer na listagem
    list_display_links = ('id', 'email',) #esse link é o que escolhe para clicar e abrir o usuario
   
   #todos esses dados são os campos que vai aparecer na página do usuario. Ou seja, os dados dele
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

    #este são os campos obrigatorios para poder fazer o cadastro do usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','name', 'cpf', 'rg', 'birth_date', 
                       'address_country', 'address_state', 'address_city',
                       'address_district', 'address_street', 'address_zip_code',
                       'address_number', 'password1', 'password2'),
        }),
    )

    #este organiza a lista de usuarios pelo email
    ordering = ['email']

#Essas são as classes criadas, ou seja, as tabelas feitas no models.py e aqui são chamadas para subir para o banco de dados.
admin.site.register(CustomUser, adminCustomUser)
admin.site.register(Token)
admin.site.register(Account)
admin.site.register(AccountToken)
admin.site.register(Transaction)
admin.site.register(Bet)
