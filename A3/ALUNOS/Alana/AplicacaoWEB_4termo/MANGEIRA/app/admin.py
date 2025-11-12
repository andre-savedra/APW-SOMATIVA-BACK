from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['id','email','cpf'] #colocamos o que queremos que aparece de primeira mão
    search_fields = ['email','cpf',]
    ordering = ['email']

class ProdutoAdmin(admin.ModelAdmin): 
    list_display = ('nome','categoria') #colocamos o que queremos que aparece de primeira mão no banco 
    search_fields = ('nome','categoria') # como vamo buscar os filmes 

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Produto)
admin.site.register(Pedido)