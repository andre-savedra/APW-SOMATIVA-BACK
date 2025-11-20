import django_filters
from .models import Reservas

class ReservationFilter(django_filters.FilterSet):
    check_in_min = django_filters.DateFilter(field_name='check_in', lookup_expr='gte')
    check_out_max = django_filters.DateFilter(field_name='check_out', lookup_expr='lte')
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')
    tipo_acomodacao = django_filters.CharFilter(field_name='acomodacao__tipo', lookup_expr='iexact')
    nacionalidade = django_filters.CharFilter(field_name='hospede__nacionalidade', lookup_expr='iexact')

    class Meta:
        model = Reservas
        fields = ['check_in_min','check_out_max','status','tipo_acomodacao','nacionalidade',]
