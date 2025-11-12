from rest_framework.viewsets import ModelViewSet
from ..models import Marca
from ..serializers import MarcaSerializer

class MarcaView(ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer