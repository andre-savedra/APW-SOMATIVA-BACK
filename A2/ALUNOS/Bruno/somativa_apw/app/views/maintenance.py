# IA ajudou, na validação de tempo e de grupo
from rest_framework import generics, permissions
from ..models import Machine, STATUS # Importe Machine
from ..serializers import MachineReadSerializer # Reutilize seu serializer de leitura
from ..permissions import IsMaintenanceUser # Importe sua nova permissão
from django.db.models import Max, Q
from django.utils import timezone
from dateutil.relativedelta import relativedelta

class MachineNeedingMaintenanceView(generics.ListAPIView):
    """
    Lista máquinas que precisam de manutenção
    (última manutenção há mais de 3 meses ou nunca feita).
    Acessível apenas para o grupo 'MANUTENÇÃO'.
    """
    serializer_class = MachineReadSerializer
    # Verifica se está autenticado e valida a função que verifica se é do grupo de manutenção.
    permission_classes = [permissions.IsAuthenticated, IsMaintenanceUser]

    def get_queryset(self):
        # 1. Define a data limite (3 meses atrás)
        three_months_ago = timezone.now() - relativedelta(months=3)

        # 2. Anota cada máquina com a data da sua última manutenção
        queryset = Machine.objects.annotate(
            latest_maintenance=Max('MachineMaintenance_machine_FK__date')
        )

        # 3. Filtra a lista
        queryset = queryset.filter(
            # Onde a última manutenção foi antes da data limite
            Q(latest_maintenance__lt=three_months_ago) |
            # Ou onde a máquina nunca teve manutenção
            Q(latest_maintenance__isnull=True)
        )
        # .distinct() para evitar que a mesma máquina apareça múltiplas vezes
        return queryset.distinct()