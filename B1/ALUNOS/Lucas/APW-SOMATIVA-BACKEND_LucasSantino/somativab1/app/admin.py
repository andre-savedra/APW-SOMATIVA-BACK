from django.contrib import admin
from .models import Categoria, Funcionario, Veiculo, Viagem, Manutencao

admin.site.register(Categoria)
admin.site.register(Funcionario)
admin.site.register(Veiculo)
admin.site.register(Viagem)
admin.site.register(Manutencao)
