from rest_framework.viewsets import ModelViewSet
from ..models import *
from ..serializers import *

class CategoriaView(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer