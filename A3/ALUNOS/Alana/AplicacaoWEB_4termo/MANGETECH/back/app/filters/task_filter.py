import django_filters
from ..models import Task

class TaskFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains') #Faz um filtro chamado nome, do tipo conter (icontains), ou seja, não precisa ser exato
    description = django_filters.CharFilter(lookup_expr='icontains')
    creation_date = django_filters.DateFromToRangeFilter(lookup_expr='iexact')
    suggested_date = django_filters.DateFromToRangeFilter(lookup_expr='iexact')
    urgency_level = django_filters.CharFilter(lookup_expr='iexact')
    creator_FK = django_filters.CharFilter(
        field_name='creator_FK__email', lookup_expr='icontains' #Quando colocamos dois __ é como se entrássemos no consterUser 
    )
    
    class Meta:
        model = Task
        fields = ['name', 'description', 'creation_date', 'suggested_date',
                  'urgency_level', 'creator_FK']