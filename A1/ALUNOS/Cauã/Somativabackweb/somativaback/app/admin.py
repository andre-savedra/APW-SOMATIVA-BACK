from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models.customuser import Funcionario, Cargo
from .models.produtos import Categoria, Produto
from .models.maquinas import Maquina
from .models.lote import Lote
from .models.itemproducao import ItemProducao
from .models.manutencao import Manutencao
from django.utils import timezone


class AdminFuncionario(UserAdmin):
    model = Funcionario
    
    list_display = ['email', 'nome', 'cargo', 'numero_registro', 'is_staff']
    list_display_links = ('email', 'nome',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais/Trabalho', {'fields': (
            'nome', 'cpf', 'numero_registro', 'data_contratacao', 'cargo'
        )}),
        ('Permissões', {'fields': (
            'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',
        )}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'nome', 'cpf', 'numero_registro', 'data_contratacao', 
                'cargo', 'password'
            ),
        }),
    )
    
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'cargo')
    
    ordering = ['email']


class ItemProducaoInline(admin.TabularInline):
    model = ItemProducao
    extra = 0
    fields = ['maquina', 'produto', 'data_hora_item']
    readonly_fields = ['data_hora_item']
    
class ManutencaoInline(admin.TabularInline):
    model = Manutencao
    extra = 0
    fields = ['data_manutencao', 'responsavel', 'descricao']
    readonly_fields = ['data_manutencao']
    
@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'status_inspecao', 'data_hora_inicio', 'responsavel_inspecao']
    list_filter = ['status_inspecao', 'responsavel_inspecao__cargo']
    inlines = [ItemProducaoInline]
    search_fields = ['codigo']
    
@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo_identificador', 'ultima_data_manutencao', 'precisa_manutencao']
    list_filter = ['ultima_data_manutencao']
    inlines = [ManutencaoInline]
    search_fields = ['nome', 'codigo_identificador']
    readonly_fields = ['precisa_manutencao']

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo', 'categoria']
    list_filter = ['categoria']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome']

admin.site.register(Funcionario, AdminFuncionario)
admin.site.register(Manutencao)
admin.site.register(ItemProducao)