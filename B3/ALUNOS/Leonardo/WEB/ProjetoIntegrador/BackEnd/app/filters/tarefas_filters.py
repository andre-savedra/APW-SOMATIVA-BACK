import django_filters
from  ..models import Tarefas

class TarefasFilters(django_filters.FilterSet):
    urgency_level = django_filters.CharFilter(lookup_expr='exact')
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    start_date_status = django_filters.DateFromToRangeFilter(lookup_expr='iexact')

    class Meta:
        model = Tarefas
        fields = ['name','description','start_date_status','urgency_level']