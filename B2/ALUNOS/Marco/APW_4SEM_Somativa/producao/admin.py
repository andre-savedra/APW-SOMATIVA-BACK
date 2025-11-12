from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    Funcionario, Linha, OrdemProducao, Registro, Alerta, Manutencao,
    Produto, Maquina, ManutencaoMaquina, Lote, ItemProducao
)

@admin.register(Funcionario)
class FuncionarioAdmin(UserAdmin):
    list_display = ('email', 'nome', 'numero_registro', 'cargo', 'data_contratacao')
    list_filter = ('cargo', 'data_contratacao', 'is_active')
    search_fields = ('nome', 'email', 'numero_registro', 'cpf')
    ordering = ('nome',)
    filter_horizontal = ('groups', 'user_permissions')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Informações Pessoais'), {'fields': ('nome', 'numero_registro', 'cpf')}),
        (_('Informações Profissionais'), {'fields': ('cargo', 'data_contratacao')}),
        (_('Permissões'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'nome', 'numero_registro', 'cpf', 'cargo'),
        }),
    )

@admin.register(Linha)
class LinhaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativa', 'data_criacao')
    list_filter = ('ativa',)
    search_fields = ('nome', 'descricao')

@admin.register(OrdemProducao)
class OrdemProducaoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'produto', 'linha', 'responsavel', 'status', 'quantidade_planejada', 'quantidade_produzida')
    list_filter = ('status', 'linha', 'responsavel')
    search_fields = ('numero', 'produto')
    date_hierarchy = 'data_criacao'

@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ('ordem_producao', 'funcionario', 'tipo', 'quantidade', 'data_hora')
    list_filter = ('tipo', 'funcionario', 'data_hora')
    search_fields = ('ordem_producao__numero', 'funcionario__nome', 'descricao')
    date_hierarchy = 'data_hora'

@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'linha', 'prioridade', 'criado_por', 'resolvido', 'data_criacao')
    list_filter = ('prioridade', 'resolvido', 'linha')
    search_fields = ('titulo', 'descricao')
    date_hierarchy = 'data_criacao'

@admin.register(Manutencao)
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ('linha', 'tipo', 'responsavel', 'status', 'data_agendada')
    list_filter = ('tipo', 'status', 'linha', 'responsavel')
    search_fields = ('descricao',)
    date_hierarchy = 'data_agendada'


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo', 'categoria')
    search_fields = ('nome', 'codigo', 'categoria')


@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo', 'data_criacao')
    search_fields = ('nome', 'codigo')


@admin.register(ManutencaoMaquina)
class ManutencaoMaquinaAdmin(admin.ModelAdmin):
    list_display = ('maquina', 'data_hora', 'responsavel')
    search_fields = ('maquina__nome', 'descricao')
    date_hierarchy = 'data_hora'


@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'produto', 'data_hora_inicio', 'data_hora_final', 'status_inspecao')
    search_fields = ('codigo', 'produto__nome')
    readonly_fields = ('qr_code',)


@admin.register(ItemProducao)
class ItemProducaoAdmin(admin.ModelAdmin):
    list_display = ('identificador', 'produto', 'lote', 'maquina', 'data_hora')
    search_fields = ('identificador', 'produto__nome', 'lote__codigo')
