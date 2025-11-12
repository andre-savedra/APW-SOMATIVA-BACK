
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import MaintenanceHistory
from ..serializers import MaintenanceHistorySerializer

class MaintenanceHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MaintenanceHistory.objects.all().order_by('-date')
    serializer_class = MaintenanceHistorySerializer
    permission_classes = [IsAuthenticated]
