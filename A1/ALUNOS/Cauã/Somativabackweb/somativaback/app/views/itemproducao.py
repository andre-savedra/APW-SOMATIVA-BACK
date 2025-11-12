# app/views/itemproducao.py

from rest_framework import viewsets # Importa o ModelViewSet daqui
from ..models.itemproducao import ItemProducao
from ..serializers.itemproducao import ItemProducaoSerializer
from ..permissions import EngenhariaCanViewOnly # Permissão

class ItemProducaoViewSet(viewsets.ModelViewSet):
    queryset = ItemProducao.objects.all()
    serializer_class = ItemProducaoSerializer
    # Agora a classe EngenhariaCanViewOnly está disponível
    permission_classes = [EngenhariaCanViewOnly]