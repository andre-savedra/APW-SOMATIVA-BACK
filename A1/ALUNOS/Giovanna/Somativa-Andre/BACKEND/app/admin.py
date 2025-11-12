from django.contrib import admin
from .models import *

from django.contrib.auth.admin import UserAdmin



class AdminCustomUser(UserAdmin):
    model= CustomUser
    list_display = ['id','email','cpf']
    list_display_links = ('id','email','cpf')
    fieldsets =(
        (None,{'fields':('email','password')}),
        ('Permission',{'fields':('is_active','is_staff','is_superuser', 'groups', 
                                    'user_permissions')}),
        ('User data',{'fields':('cpf','numero_registro','Cargo')})
    )
    filter_horizontal= ('groups','user_permissions')
    add_fieldsets =(
        (None,{
            'classes':('wide',),
            'fields': ('email','nome','cpf','password','password2')
    
        }),
    )
    ordering =['email']

admin.site.register(CustomUser,AdminCustomUser)
admin.site.register(Categoria)
admin.site.register(Lote)
admin.site.register(Maquina)
admin.site.register(Producao)
admin.site.register(Produto)
