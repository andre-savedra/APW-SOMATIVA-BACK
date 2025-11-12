from rest_framework.viewsets import ModelViewSet
from ..models import *
from ..serializers import *

class MaquinaView(ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer