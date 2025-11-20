import django_filters
from .models import Lote, Item


class LoteFilter(django_filters.FilterSet):
    status_inspecao = django_filters.ChoiceFilter(
        choices=[('Aprovado', 'Aprovado'), ('Reprovado', 'Reprovado')]
    )
    dt_inicio_min = django_filters.DateFilter(field_name='dthInicio', lookup_expr='gte')
    dt_inicio_max = django_filters.DateFilter(field_name='dthInicio', lookup_expr='lte')
    maquina = django_filters.NumberFilter(
        field_name='item__identificacaoMaquina__id',
        distinct=True
    )
    categoria = django_filters.NumberFilter(
        field_name='produto__categoria__id'
    )
    
    class Meta:
        model = Lote
        fields = ['status_inspecao', 'dt_inicio_min', 'dt_inicio_max', 'maquina', 'categoria']


class ItemFilter(django_filters.FilterSet):
    maquina = django_filters.NumberFilter(field_name='identificacaoMaquina__id')
    lote = django_filters.NumberFilter(field_name='lote__id')
    
    class Meta:
        model = Item
        fields = ['maquina', 'lote']