from rest_framework.viewsets import ModelViewSet
from ..models import *
from ..serializers import *
from ..permissions import *

class MaquinaView(ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer
    permission_classes = [Authenticated]
