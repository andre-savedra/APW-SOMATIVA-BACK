from rest_framework.viewsets import ModelViewSet
from ..models import Escaninhos
from ..serializers import EscaninhosSerializer

class EscaninhosView(ModelViewSet):
    queryset = Escaninhos.objects.all()
    serializer_class = EscaninhosSerializer