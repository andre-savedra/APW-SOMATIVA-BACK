import django_filters
from ..models import Produto

class ProdutoFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains'
    )
    
    setor = django_filters.CharFilter(
        field_name='Escaninhos_produto_FK__setor_FK__name',
        lookup_expr='icontains'
    )

    escaninho = django_filters.CharFilter(
        field_name='Escaninhos_produto_FK__cod',
        lookup_expr='icontains'
    )

    marca_FK = django_filters.CharFilter(
        field_name='marca_FK__name', lookup_expr='icontains'
    )

    codeRegistro = django_filters.CharFilter(lookup_expr='icontains')

    promocao = promocao = django_filters.BooleanFilter(
        field_name='promoção'
    )

    codeBarras = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Produto
        fields = ['name', 'setor', 'escaninho', 'marca_FK', 'codeRegistro', 'promocao', 'codeBarras' ]


#setor, 
#escaninho, 
# marca ou código do produto, 
# promoção;
#também por código de barras (não é necessário digitar o código de barras inteiro);
