import django_filters
from .models import Produto

class ProdutoFilter(django_filters.FilterSet):
    # Filtro por código de barras (busca parcial)
    codigo_barras = django_filters.CharFilter(field_name='codigo_barras', lookup_expr='icontains')
    
    # Filtro por setor (através dos escaninhos)
    setor = django_filters.CharFilter(field_name='escaninhos__setor__letra', lookup_expr='iexact')
    
    # Filtro por escaninho específico
    escaninho = django_filters.CharFilter(field_name='escaninhos__codigo', lookup_expr='iexact')
    
    # Filtro por marca
    marca_nome = django_filters.CharFilter(field_name='marca__nome', lookup_expr='icontains')
    
    # Filtro por categoria
    categoria_nome = django_filters.CharFilter(field_name='categoria__nome', lookup_expr='icontains')
    
    # Filtro por promoção
    em_promocao = django_filters.BooleanFilter(field_name='em_promocao')
    
    # Filtro por faixa de preço
    preco_min = django_filters.NumberFilter(field_name='valor_venda', lookup_expr='gte')
    preco_max = django_filters.NumberFilter(field_name='valor_venda', lookup_expr='lte')
    
    # Filtro por data de cadastro
    data_cadastro_inicio = django_filters.DateFilter(field_name='data_cadastro', lookup_expr='gte')
    data_cadastro_fim = django_filters.DateFilter(field_name='data_cadastro', lookup_expr='lte')

    class Meta:
        model = Produto
        fields = [
            'codigo_registro', 'codigo_barras', 'categoria', 'marca',
            'em_promocao', 'setor', 'escaninho', 'marca_nome', 'categoria_nome',
            'preco_min', 'preco_max', 'data_cadastro_inicio', 'data_cadastro_fim'
        ]