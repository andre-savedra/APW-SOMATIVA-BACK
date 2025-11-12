import django_filters
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import *

class LoteFilter(django_filters.FilterSet):
    data_inicio_range = django_filters.DateFromToRangeFilter(field_name='data_inicio')
    status_inspecao = django_filters.ChoiceFilter(choices=[('Aprovado', 'Aprovado'), ('Reprovado', 'Reprovado')])
    maquina = django_filters.CharFilter(method='filter_por_maquina')
    categoria = django_filters.CharFilter(field_name='produto__categoria')

    class Meta:
        model = Lote
        fields = ['status_inspecao']

    def filter_por_maquina(self, queryset, name, value):
        return queryset.filter(itens__maquina__codigo=value).distinct()

class ProducaoReprovadaFilter(django_filters.FilterSet):
    data_inicio_range = django_filters.DateFromToRangeFilter(field_name='data_inicio', label='Período de produção')
    maquina = django_filters.CharFilter(method='filter_por_maquina')
    categoria = django_filters.CharFilter(field_name='produto__categoria')

    class Meta:
        model = Lote
        fields = []

    def filter_por_maquina(self, queryset, name, value):
        return queryset.filter(itens__maquina__codigo=value).distinct()

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(status_inspecao='Reprovado')

class MaquinaFilter(django_filters.FilterSet):
    precisa_manutencao = django_filters.BooleanFilter(method='filter_precisa_manutencao')

    class Meta:
        model = Maquina
        fields = []

    def filter_precisa_manutencao(self, queryset, name, value):
        if value:
            dois_meses_atras = timezone.now() - timedelta(days=60)
            # Máquinas sem manutenção ou com última manutenção há mais de 2 meses
            return queryset.filter(
                Q(manutencoes__isnull=True) | 
                Q(manutencoes__data_hora__lt=dois_meses_atras)
            ).distinct()
        return queryset