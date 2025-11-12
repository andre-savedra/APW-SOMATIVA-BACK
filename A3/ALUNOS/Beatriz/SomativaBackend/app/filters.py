import django_filters
from .models import Produto

class ProdutoFilter(django_filters.FilterSet):
    #filtro por setor:
    setor = django_filters.CharFilter(
        field_name='localizacao_estoque__setor__letra', 
        lookup_expr='iexact', 
        distinct=True
    )

 # filtro por ecaninho:
    escaninho = django_filters.CharFilter(
        field_name='localizacao_estoque__codigo_escaninho', 
        lookup_expr='iexact', 
        distinct=True
    )

    class Meta:
        model = Produto
        # filtros simples:
        fields = ['categoria', 'marca', 'em_promocao']
