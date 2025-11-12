# frota/admin.py

from django.contrib import admin
from .models import (
    Funcionario, 
    CategoriaVeiculo, 
    Veiculo, 
    Viagem, 
    Manutencao
)

admin.site.register(Funcionario)
admin.site.register(CategoriaVeiculo)
admin.site.register(Veiculo)
admin.site.register(Viagem)
admin.site.register(Manutencao)