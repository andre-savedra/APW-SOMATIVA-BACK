import django_filters
from .models import Viagem

class ViagemFilter(django_filters.FilterSet):
    
    data_inicio__gte = django_filters.DateTimeFilter(field_name='data_inicio', lookup_expr='gte')
    data_termino__lte = django_filters.DateTimeFilter(field_name='data_termino', lookup_expr='lte')
    
  
    veiculo = django_filters.NumberFilter(field_name='veiculo__id')
    
    
    categoria = django_filters.CharFilter(field_name='veiculo__categoria', lookup_expr='iexact')
    
    
    km_min = django_filters.NumberFilter(field_name='km', lookup_expr='gte')

    class Meta:
        model = Viagem
        fields = ['data_inicio__gte', 'data_termino__lte', 'veiculo', 'categoria', 'km_min']
