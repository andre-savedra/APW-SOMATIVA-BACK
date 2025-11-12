import django_filters
from ..models import Producao, Maquina, Produto

class ProducaoFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr='icontains')==('Reprovado')
    class Meta:
        model = Producao
        fields = ['status']

class MaquinaFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Maquina
        fields = ['nome']

class ProdutoFilter(django_filters.FilterSet):
    categoria = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Produto
        fields = ['categoria']