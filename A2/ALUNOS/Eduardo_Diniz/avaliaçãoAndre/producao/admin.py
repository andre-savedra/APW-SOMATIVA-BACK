from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

@admin.register(Funcionario)
class FuncionarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'numero_registro', 'cargo', 'data_contratacao']
    list_filter = ['cargo', 'data_contratacao']
    search_fields = ['username', 'email', 'numero_registro', 'cpf']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('numero_registro', 'cpf', 'data_contratacao', 'cargo')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('numero_registro', 'cpf', 'data_contratacao', 'cargo')}),
    )


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'categoria']
    list_filter = ['categoria']
    search_fields = ['nome', 'codigo']


@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome']
    search_fields = ['nome', 'codigo']


@admin.register(Manutencao)
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ['maquina', 'data_hora', 'funcionario']
    list_filter = ['maquina', 'data_hora']
    search_fields = ['maquina__nome', 'funcionario__username']
    date_hierarchy = 'data_hora'


@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'data_inicio', 'status_inspecao', 'responsavel_inspecao']
    list_filter = ['status_inspecao', 'data_inicio']
    search_fields = ['codigo']
    date_hierarchy = 'data_inicio'


@admin.register(ItemProducao)
class ItemProducaoAdmin(admin.ModelAdmin):
    list_display = ['lote', 'produto', 'maquina', 'data_hora']
    list_filter = ['produto', 'maquina', 'data_hora']
    search_fields = ['lote__codigo', 'produto__nome']
    date_hierarchy = 'data_hora'