from rest_framework.viewsets import ModelViewSet
from ..models import Maintenance
from ..serializers.maintenance import MaintenanceSerializer

class MaintenanceView(ModelViewSet):    
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer