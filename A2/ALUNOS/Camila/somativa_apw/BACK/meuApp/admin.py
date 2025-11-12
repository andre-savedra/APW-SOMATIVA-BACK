from django.contrib import admin
from .models import *

# ========== CARGO ==========
@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)
    ordering = ('nome',)


# ========== FUNCIONÁRIO ==========
@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'numero_registro', 'cargo', 'email', 'data_contratacao')
    list_filter = ('cargo',)
    search_fields = ('nome', 'email', 'cpf', 'numero_registro')
    fieldsets = (
        ('Informações pessoais', {
            'fields': ('nome', 'cpf', 'email')
        }),
        ('Profissional', {
            'fields': ('numero_registro', 'data_contratacao', 'cargo')
        }),
    )


# ========== MÁQUINA ==========
class ManutencaoInline(admin.TabularInline):
    model = Manutencao
    extra = 0
    readonly_fields = ('data_hora', 'descricao', 'funcionario')

@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo', 'descricao')
    search_fields = ('nome', 'codigo')
    inlines = [ManutencaoInline]


# ========== MANUTENÇÃO ==========
@admin.register(Manutencao)
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ('maquina', 'data_hora', 'funcionario')
    list_filter = ('maquina', 'funcionario')
    search_fields = ('descricao',)
    date_hierarchy = 'data_hora'


# ========== PRODUTO ==========
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nome', 'codigo')


# ========== LOTE ==========
class ItemLoteInline(admin.TabularInline):
    model = ItemLote
    extra = 0
    readonly_fields = ('data_hora', 'maquina')

@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'produto', 'status_inspecao', 'responsavel_inspecao')
    list_filter = ('status_inspecao', 'produto__categoria')
    search_fields = ('codigo', 'produto__nome')
    inlines = [ItemLoteInline]
    fieldsets = (
        ('Informações do lote', {
            'fields': ('codigo', 'produto', 'data_inicio', 'data_fim')
        }),
        ('Inspeção', {
            'fields': ('data_inspecao', 'responsavel_inspecao', 'status_inspecao')
        }),
    )


# ========== ITEM DO LOTE ==========
@admin.register(ItemLote)
class ItemLoteAdmin(admin.ModelAdmin):
    list_display = ('lote', 'maquina', 'data_hora')
    list_filter = ('maquina',)
    date_hierarchy = 'data_hora'
