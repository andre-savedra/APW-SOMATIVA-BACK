from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
 
from .models import *

admin.site.register(Funcionario),
admin.site.register(Manutencao),
admin.site.register(Maquina),
admin.site.register(Produto),
admin.site.register(Lote),
admin.site.register(Producao)
