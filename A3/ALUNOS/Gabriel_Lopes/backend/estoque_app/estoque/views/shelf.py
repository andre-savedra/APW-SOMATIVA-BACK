from rest_framework import viewsets
from ..models.shelf import Escaninho
from ..serializers.shelf import EscaninhoSerializer

class EscaninhoViewSet(viewsets.ModelViewSet):
    queryset = Escaninho.objects.all()
    serializer_class = EscaninhoSerializer