from rest_framework.viewsets import ModelViewSet
from ..models import *
from ..serializers import *

class ProducaoView(ModelViewSet):
    queryset = Producao.objects.all()
    serializer_class = ProducaoSerializer