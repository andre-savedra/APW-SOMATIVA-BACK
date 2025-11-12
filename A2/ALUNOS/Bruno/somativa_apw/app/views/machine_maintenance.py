from rest_framework import viewsets
from ..models.machine import MachineMaintenance
from rest_framework import permissions
from ..serializers.machine import MachineMaintenanceSerializer

class MachineMaintenanceView(viewsets.ModelViewSet):
    queryset = MachineMaintenance.objects.all()
    serializer_class = MachineMaintenanceSerializer
    permission_classes = [permissions.DjangoModelPermissions]
  