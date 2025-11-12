import django_filters
from models import reservation

class ReservationFilters(django_filters.FilterSet):
    # Filtrar por período
    check_in = django_filters.DateFromToRangeFilter()
    check_out = django_filters.DateFromToRangeFilter()

    # Filtrar por status
    status = django_filters.ChoiceFilter(
        choices=reservation.STATUS_CHOICES  # assumindo que você definiu STATUS_CHOICES no model
    )

    # Filtrar por tipo de acomodação (campo relacionado)
    accommodation_type = django_filters.CharFilter(
        field_name='accommodation__type',  # FK para Accommodation
        lookup_expr='iexact'
    )

    # Filtrar por nacionalidade do hóspede (campo relacionado)
    guest_nationality = django_filters.CharFilter(
        field_name='guest__user__nationality',  # Guest → CustomUser → nationality
        lookup_expr='iexact'
    )

    class Meta:
        model = reservation
        fields = ['check_in', 'check_out', 'status', 'accommodation_type', 'guest_nationality']