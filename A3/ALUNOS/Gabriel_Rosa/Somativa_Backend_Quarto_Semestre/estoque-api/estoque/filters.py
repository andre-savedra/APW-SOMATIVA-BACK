import django_filters
from django.db.models import Q
from .models import Produto, Escaninho

class ProdutoFilter(django_filters.FilterSet):
    # Filtros básicos
    categoria = django_filters.NumberFilter(field_name='categoria__id')
    categoria_nome = django_filters.CharFilter(field_name='categoria__nome', lookup_expr='icontains')
    marca = django_filters.NumberFilter(field_name='marca__id')
    marca_nome = django_filters.CharFilter(field_name='marca__nome', lookup_expr='icontains')
    em_promocao = django_filters.BooleanFilter(field_name='em_promocao')
    
    # Filtros por valores
    custo_min = django_filters.NumberFilter(field_name='custo', lookup_expr='gte')
    custo_max = django_filters.NumberFilter(field_name='custo', lookup_expr='lte')
    valor_min = django_filters.NumberFilter(field_name='valor_venda', lookup_expr='gte')
    valor_max = django_filters.NumberFilter(field_name='valor_venda', lookup_expr='lte')
    
    # Filtros por datas
    cadastrado_depois = django_filters.DateTimeFilter(field_name='data_cadastro', lookup_expr='gte')
    cadastrado_antes = django_filters.DateTimeFilter(field_name='data_cadastro', lookup_expr='lte')
    
    # Filtros específicos do PDF
    setor = django_filters.CharFilter(method='filter_by_setor')
    escaninho = django_filters.CharFilter(method='filter_by_escaninho')
    codigo_barras_parcial = django_filters.CharFilter(method='filter_codigo_barras_parcial')
    codigo_produto = django_filters.CharFilter(field_name='codigo_registro', lookup_expr='icontains')
    
    class Meta:
        model = Produto
        fields = {
            'nome': ['exact', 'icontains'],
            'codigo_registro': ['exact', 'icontains'],
            'codigo_barras': ['exact', 'icontains'],
        }
    
    def filter_by_setor(self, queryset, name, value):
        """Filtra produtos por setor onde estão armazenados"""
        return queryset.filter(escaninhos__setor__nome__iexact=value).distinct()
    
    def filter_by_escaninho(self, queryset, name, value):
        """Filtra produtos por código do escaninho"""
        return queryset.filter(escaninhos__codigo=value).distinct()
    
    def filter_codigo_barras_parcial(self, queryset, name, value):
        """Permite busca parcial no código de barras"""
        return queryset.filter(codigo_barras__icontains=value)

class EscaninhoFilter(django_filters.FilterSet):
    setor = django_filters.CharFilter(field_name='setor__nome', lookup_expr='iexact')
    setor_id = django_filters.NumberFilter(field_name='setor__id')
    tem_produto = django_filters.BooleanFilter(method='filter_tem_produto')
    produto_promocao = django_filters.BooleanFilter(method='filter_produto_promocao')
    quantidade_min = django_filters.NumberFilter(field_name='quantidade', lookup_expr='gte')
    quantidade_max = django_filters.NumberFilter(field_name='quantidade', lookup_expr='lte')
    
    class Meta:
        model = Escaninho
        fields = {
            'codigo': ['exact', 'icontains'],
            'produto': ['exact'],
            'quantidade': ['exact', 'gte', 'lte'],
        }
    
    def filter_tem_produto(self, queryset, name, value):
        """Filtra escaninhos que têm ou não têm produto"""
        if value:
            return queryset.filter(produto__isnull=False, quantidade__gt=0)
        else:
            return queryset.filter(Q(produto__isnull=True) | Q(quantidade=0))
    
    def filter_produto_promocao(self, queryset, name, value):
        """Filtra escaninhos com produtos em promoção"""
        if value:
            return queryset.filter(produto__em_promocao=True)
        else:
            return queryset.filter(Q(produto__isnull=True) | Q(produto__em_promocao=False))