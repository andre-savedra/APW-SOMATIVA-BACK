from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import MaintenanceHistory
from ..models import Accommodation
from ..serializers import AccommodationSerializer
from ..permissions import HousekeepingPermission, MaintenancePermission

class AccommodationViewSet(viewsets.ModelViewSet):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    permission_classes = [IsAuthenticated, HousekeepingPermission, MaintenancePermission]

    def perform_update(self, serializer):
        # Salva o status antigo antes da atualização
        old_status = serializer.instance.status
        # Atualiza a acomodação com os novos dados
        accommodation = serializer.save()
        
        # Só registra histórico se o status realmente mudou
        if old_status != accommodation.status:
            # Cria registro no MaintenanceHistory
            MaintenanceHistory.objects.create(
                accommodation=accommodation,
                employee=self.request.user.employee,  # funcionário que fez a alteração
                status_before=old_status,
                status_after=accommodation.status
            )