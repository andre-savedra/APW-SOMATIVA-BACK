from rest_framework.viewsets import ModelViewSet
from ..models import Vehicle
from ..serializers.vehicle import VehicleSerializer

class VehicleView(ModelViewSet):    
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer