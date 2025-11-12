from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Producao
from ..serializers import ProducaoSerializer
from ..filters import ProducaoFilter

from ..utils import *

class ProducaoView(ModelViewSet):
    queryset = Producao.objects.all()
    serializer_class = ProducaoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProducaoFilter

def get_queryset(self):
    user = self.request.user

    if user.is_authenticated:
        return Producao.objects.all() if is_Admin(user.id) else \
               Producao.objects.filter(inspector_FK=user.id)
    
    return Producao.objects.none()
