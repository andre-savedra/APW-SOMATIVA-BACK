import django_filters
from ..models import Trip

class TripFilter(django_filters.FilterSet):
    mileage_min = django_filters.NumberFilter(field_name='mileage', lookup_expr='gte')
    mileage_max = django_filters.NumberFilter(field_name='mileage', lookup_expr='lte')
    driver = django_filters.CharFilter(field_name='driver__name', lookup_expr='icontains')
    destination = django_filters.CharFilter(field_name='destination', lookup_expr='iexact')
    start_datetime_after = django_filters.IsoDateTimeFilter(field_name='start_datetime', lookup_expr='gte')
    start_datetime_before = django_filters.IsoDateTimeFilter(field_name='start_datetime', lookup_expr='lte')

    class Meta:
        model = Trip
        fields = ['mileage_min', 'mileage_max', 'driver', 'destination', 'start_datetime_after', 'start_datetime_before']
