from django.contrib import admin

from django.contrib import admin
from .models import Categoria, Marca, Produto, Setor, Escaninho


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'data_registro']
    search_fields = ['nome']
    readonly_fields = ['data_registro']


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cnpj', 'data_inclusao']
    search_fields = ['nome', 'cnpj']
    readonly_fields = ['data_inclusao']


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo_registro', 'codigo_barras', 'categoria', 'marca', 'valor_venda', 'em_promocao']
    list_filter = ['em_promocao', 'categoria', 'marca', 'data_cadastro']
    search_fields = ['nome', 'codigo_registro', 'codigo_barras']
    readonly_fields = ['data_cadastro']
    list_editable = ['em_promocao']


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ['letra', 'descricao', 'data_cadastro']
    search_fields = ['letra', 'descricao']
    readonly_fields = ['data_cadastro']


@admin.register(Escaninho)
class EscaninhoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'setor', 'produto', 'quantidade']
    list_filter = ['setor']
    search_fields = ['codigo', 'produto__nome']
    autocomplete_fields = ['produto']


# Register your models here.
