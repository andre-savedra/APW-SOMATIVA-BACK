from django.contrib import admin
from .models import Categoria, Produto, Funcionario, Maquina, Manutencao, Lote, ItemProducao


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'codigo', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nome', 'codigo')


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'registro', 'cargo')
    list_filter = ('cargo',)
    search_fields = ('nome', 'registro', 'cpf')


@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'nome')
    search_fields = ('codigo', 'nome')


@admin.register(Manutencao)
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'maquina', 'data_hora', 'funcionario')
    list_filter = ('data_hora',)


@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'produto', 'inicio', 'fim', 'data_inspecao', 'inspetor', 'status_inspecao')
    list_filter = ('status_inspecao', 'produto__categoria')
    search_fields = ('codigo',)


@admin.register(ItemProducao)
class ItemProducaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'lote', 'data_hora', 'maquina')
    list_filter = ('maquina', 'data_hora')
