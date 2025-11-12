import django_filters
from ..models import Producao

class ProducaoFilter(django_filters.FilterSet):
    data_producao = django_filters.DateFromToRangeFilter(field_name='data_producao')
    status = django_filters.CharFilter(lookup_expr='iexact')  # Filtra status da produção
    maquina = django_filters.CharFilter(field_name='maquina_FK__nome', lookup_expr='icontains')
    categoria = django_filters.CharFilter(field_name='lote_FK__categoria_FK__nome', lookup_expr='icontains')

    class Meta:
        model = Producao
        fields = ['data_producao', 'status', 'maquina', 'categoria']
