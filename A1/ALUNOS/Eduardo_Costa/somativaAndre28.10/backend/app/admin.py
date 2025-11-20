from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class AdminFuncionario(UserAdmin):
    model = Funcionario
    search_fields = ('email', 'numero_registro', 'nome', 'cpf')
    list_display = ['id', 'nome', 'email', 'numero_registro', 'cargo', 'dt_contratacao']
    list_display_links = ('id', 'email', 'nome')
    list_filter = ('cargo', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nome', 'numero_registro', 'cpf', 'cargo', 'dt_contratacao')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    filter_horizontal = ('groups', 'user_permissions',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'numero_registro', 'cpf', 'cargo', 'dt_contratacao', 'password1', 'password2'),
        }),
    )
    ordering = ['email']
    list_per_page = 25


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    list_display_links = ['id', 'nome']
    search_fields = ['nome']
    list_per_page = 20


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'codigo', 'categoria', 'descricao_curta']
    list_display_links = ['id', 'nome', 'codigo']
    search_fields = ['nome', 'codigo', 'descricao']
    list_filter = ['categoria']
    list_per_page = 25
    
    def descricao_curta(self, obj):
        """Mostra apenas os primeiros 50 caracteres da descrição"""
        if len(obj.descricao) > 50:
            return obj.descricao[:50] + '...'
        return obj.descricao
    descricao_curta.short_description = 'Descrição'


class MaquinaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'code', 'ultima_manutencao', 'responsavel', 'precisa_manutencao']
    list_display_links = ['id', 'nome', 'code']
    search_fields = ['nome', 'code', 'descricao']
    list_filter = ['ultima_manutencao']
    date_hierarchy = 'ultima_manutencao'
    list_per_page = 25
    
    def precisa_manutencao(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        # tres_meses_atras = timezone.now().date() - timedelta(days=90)
        # if obj.ultima_manutencao and obj.ultima_manutencao < tres_meses_atras:
            # return '⚠️ SIM'
        return '✅ Não'
    precisa_manutencao.short_description = 'Precisa Manutenção'


class LoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'status_inspecao', 'responsavel', 'dthInicio', 'dthFim', 'dtInspecao', 'itens']
    list_display_links = ['id', 'code']
    search_fields = ['code', 'responsavel__nome']
    list_filter = ['status_inspecao', 'dthInicio', 'dthFim']
    date_hierarchy = 'dthInicio'
    list_per_page = 25
    raw_id_fields = ['responsavel', 'itens']


class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'identificacaoMaquina', 'dthItem']
    list_display_links = ['id', 'nome']
    search_fields = ['nome', 'identificacaoMaquina__nome']
    list_filter = ['identificacaoMaquina', 'dthItem']
    date_hierarchy = 'dthItem'
    list_per_page = 25
    raw_id_fields = ['identificacaoMaquina']

# Registrar todos os models com suas classes personalizadas
admin.site.register(Funcionario, AdminFuncionario)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Maquina, MaquinaAdmin)
admin.site.register(Lote, LoteAdmin)
admin.site.register(Item, ItemAdmin)


# Customizar o cabeçalho do admin
admin.site.site_header = 'Administração - Sistema de Produção'
admin.site.site_title = 'Admin Produção'
admin.site.index_title = 'Gestão de Produção Industrial'