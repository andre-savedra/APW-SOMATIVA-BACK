# Obtive ajuda da IA

import django_filters
from ..models import Lot, STATUS

class LotFilter(django_filters.FilterSet):

    # 1. Filtro por Data de Produção 
    # 'Item_lot_FK' (related_name) para acessar os itens do lote
    production_date = django_filters.DateFromToRangeFilter(
        field_name='Item_lot_FK__date',  # Filtra pela data do Item relacionado
    )

    # 2. Filtro por Máquina 
    machine = django_filters.CharFilter(
        field_name='Item_lot_FK__machine_FK__name', # Lot -> Item -> Machine -> name
        lookup_expr='icontains',
    )

    # 3. Filtro por Categoria do Produto
    category = django_filters.CharFilter(
        field_name='product_FK__category_FK__name', # Lot -> Product -> Category -> name
        lookup_expr='icontains',
    )

    status = django_filters.ChoiceFilter(choices=STATUS.choices)

    class Meta:
        model = Lot
        fields = ['production_date', 'machine', 'category', 'status']

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.distinct()