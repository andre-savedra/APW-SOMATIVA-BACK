import django_filters
from django_filters import rest_framework as filters
from ..models.lote import Lote


class LoteFilter(filters.FilterSet):
    data_inicio = filters.DateTimeFilter(field_name="data_hora_inicio", lookup_expr='gte')
    data_fim = filters.DateTimeFilter(field_name="data_hora_inicio", lookup_expr='lte')

    maquina_id = filters.NumberFilter(
        field_name='itens_produzidos__maquina__id',
        distinct=True
    )
    
    categoria_id = filters.NumberFilter(
        field_name='itens_produzidos__produto__categoria__id',
        distinct=True
    )

    class Meta:
        model = Lote
        fields = ['data_inicio', 'data_fim', 'maquina_id', 'categoria_id']