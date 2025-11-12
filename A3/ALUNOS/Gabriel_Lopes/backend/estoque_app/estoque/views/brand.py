from rest_framework import viewsets
from ..models.brand import Marca
from ..serializers.brand import MarcaSerializer

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer