import django_filters
from .models import Viagem, Veiculo, CategoriaVeiculo

class ViagemFilter(django_filters.FilterSet):
    """
    FilterSet para o modelo Viagem, permitindo filtros avançados.
    """
    data_inicio = django_filters.DateTimeFilter(
        field_name="data_hora_inicio", 
        lookup_expr='gte'  
    )
    data_fim = django_filters.DateTimeFilter(
        field_name="data_hora_inicio", 
        lookup_expr='lte' 
    )

    categoria = django_filters.ModelChoiceFilter(
        field_name='veiculo__categoria',
        queryset=CategoriaVeiculo.objects.all(),
        label='Categoria (ID)'
    )
    
    km_minima = django_filters.NumberFilter(
        field_name="quilometragem", 
        lookup_expr='gte' 
    )

    class Meta:
        model = Viagem
        fields = [
            'veiculo', 
            'data_inicio', 
            'data_fim',
            'categoria',
            'km_minima'
        ]

        #teste git