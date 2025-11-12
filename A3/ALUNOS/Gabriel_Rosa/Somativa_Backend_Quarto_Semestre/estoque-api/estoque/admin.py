from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Categoria, Marca, Setor, Produto, Escaninho

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'data_registro', 'produtos_count']
    search_fields = ['nome']
    ordering = ['nome']
    readonly_fields = ['data_registro']
    
    def produtos_count(self, obj):
        count = obj.produtos.count()
        return f"{count} produtos"
    produtos_count.short_description = 'Qtd Produtos'

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cnpj', 'data_inclusao', 'produtos_count']
    search_fields = ['nome', 'cnpj']
    ordering = ['nome']
    readonly_fields = ['data_inclusao']
    
    def produtos_count(self, obj):
        count = obj.produtos.count()
        return f"{count} produtos"
    produtos_count.short_description = 'Qtd Produtos'

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'data_criacao', 'escaninhos_count', 'produtos_count']
    search_fields = ['nome', 'descricao']
    ordering = ['nome']
    readonly_fields = ['data_criacao']
    
    def escaninhos_count(self, obj):
        return obj.escaninhos.count()
    escaninhos_count.short_description = 'Qtd Escaninhos'
    
    def produtos_count(self, obj):
        count = obj.escaninhos.filter(produto__isnull=False).count()
        return f"{count} com produtos"
    produtos_count.short_description = 'Escaninhos c/ Produtos'

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = [
        'nome', 'codigo_registro', 'codigo_barras', 
        'categoria', 'marca', 'valor_venda', 'em_promocao', 
        'margem_lucro_percent', 'data_cadastro'
    ]
    list_filter = [
        'em_promocao', 'categoria', 'marca', 'data_cadastro'
    ]
    search_fields = ['nome', 'codigo_registro', 'codigo_barras']
    ordering = ['-data_cadastro']
    readonly_fields = [
        'data_cadastro', 'criado_por', 'promocao_alterada_por', 
        'data_promocao', 'margem_lucro_percent'
    ]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'codigo_registro', 'codigo_barras')
        }),
        ('Categorização', {
            'fields': ('categoria', 'marca')
        }),
        ('Valores', {
            'fields': ('custo', 'valor_venda', 'margem_lucro_percent')
        }),
        ('Promoção', {
            'fields': ('em_promocao',)
        }),
        ('Informações Adicionais', {
            'fields': ('informacoes_adicionais',),
            'classes': ('collapse',)
        }),
        ('Auditoria', {
            'fields': (
                'data_cadastro', 'criado_por', 
                'promocao_alterada_por', 'data_promocao'
            ),
            'classes': ('collapse',)
        })
    )
    
    def margem_lucro_percent(self, obj):
        margem = obj.margem_lucro
        return f"{margem:.1f}%"
    margem_lucro_percent.short_description = 'Margem de Lucro'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Novo objeto
            obj.criado_por = request.user
        
        # Se alterou o status de promoção
        if change and 'em_promocao' in form.changed_data:
            obj.promocao_alterada_por = request.user
            obj.data_promocao = timezone.now()
        
        super().save_model(request, obj, form, change)

@admin.register(Escaninho)
class EscaninhoAdmin(admin.ModelAdmin):
    list_display = [
        'get_localizacao', 'setor', 'produto', 'quantidade', 
        'get_valor_total', 'get_status', 'data_atualizacao'
    ]
    list_filter = ['setor', 'produto__categoria']
    search_fields = ['codigo', 'setor__nome', 'produto__nome']
    ordering = ['setor__nome', 'codigo']
    
    def get_localizacao(self, obj):
        return f"Setor {obj.setor.nome} - {obj.codigo}"
    get_localizacao.short_description = 'Localização'
    
    def get_valor_total(self, obj):
        if obj.produto and obj.quantidade > 0:
            total = float(obj.produto.valor_venda * obj.quantidade)
            return f"R$ {total:.2f}"
        return "-"
    get_valor_total.short_description = 'Valor Total'
    
    def get_status(self, obj):
        if not obj.produto:
            return "VAZIO"
        elif obj.quantidade == 0:
            return "SEM ESTOQUE"
        else:
            return "OCUPADO"
    get_status.short_description = 'Status'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'setor', 'produto__categoria', 'produto__marca'
        )