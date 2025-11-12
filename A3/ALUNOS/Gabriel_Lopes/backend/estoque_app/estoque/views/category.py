from rest_framework import viewsets
from ..models.category import Categoria
from ..serializers.category import CategoriaSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer