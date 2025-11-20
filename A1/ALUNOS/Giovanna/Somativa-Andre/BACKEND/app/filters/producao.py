import django_filters
from ..models import Producao

class ProducaoFilter(django_filters.FilterSet):
    data_inicio = django_filters.DateFilter(field_name="data_producao", lookup_expr="gte")
    data_fim = django_filters.DateFilter(field_name="data_producao", lookup_expr="lte")
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")
    maquina = django_filters.CharFilter(field_name="maquina__nome", lookup_expr="icontains")
    categoria = django_filters.CharFilter(field_name="produto__categoria__nome", lookup_expr="icontains")

    class Meta:
        model = Producao
        fields = ['data_inicio', 'data_fim', 'status', 'maquina', 'categoria']
