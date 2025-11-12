from django.contrib import admin
from .models import Categoria, Marca, Setor, Produto, Escaninho

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'data_registro', 'total_produtos']
    list_filter = ['data_registro']
    search_fields = ['nome']
    readonly_fields = ['data_registro']

    def total_produtos(self, obj):
        return obj.produtos.count()
    total_produtos.short_description = 'Total de Produtos'

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cnpj', 'data_inclusao', 'total_produtos']
    list_filter = ['data_inclusao']
    search_fields = ['nome', 'cnpj']
    readonly_fields = ['data_inclusao']

    def total_produtos(self, obj):
        return obj.produtos.count()
    total_produtos.short_description = 'Total de Produtos'

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ['letra', 'descricao', 'data_criacao', 'total_escaninhos']
    list_filter = ['data_criacao']
    search_fields = ['letra', 'descricao']
    readonly_fields = ['data_criacao']

    def total_escaninhos(self, obj):
        return obj.escaninhos.count()
    total_escaninhos.short_description = 'Total de Escaninhos'

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = [
        'nome', 'codigo_registro', 'codigo_barras', 'categoria', 
        'marca', 'custo', 'valor_venda', 'em_promocao', 'data_cadastro'
    ]
    list_filter = ['categoria', 'marca', 'em_promocao', 'data_cadastro']
    search_fields = ['nome', 'codigo_registro', 'codigo_barras']
    readonly_fields = ['data_cadastro']
    list_editable = ['em_promocao', 'custo', 'valor_venda']

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'codigo_registro', 'codigo_barras')
        }),
        ('Classificação', {
            'fields': ('categoria', 'marca')
        }),
        ('Valores', {
            'fields': ('custo', 'valor_venda', 'em_promocao')
        }),
        ('Informações Adicionais', {
            'fields': ('informacoes_adicionais', 'data_cadastro'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Escaninho)
class EscaninhoAdmin(admin.ModelAdmin):
    list_display = [
        'localizacao_completa', 'setor', 'codigo', 'produto', 
        'quantidade', 'esta_vazio', 'data_atualizacao'
    ]
    list_filter = ['setor', 'data_criacao']
    search_fields = ['codigo', 'setor__letra', 'produto__nome']
    readonly_fields = ['data_criacao', 'data_atualizacao', 'localizacao_completa', 'esta_vazio']

    def localizacao_completa(self, obj):
        return obj.localizacao_completa
    localizacao_completa.short_description = 'Localização'