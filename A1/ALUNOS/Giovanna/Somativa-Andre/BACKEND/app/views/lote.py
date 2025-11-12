from rest_framework.viewsets import ModelViewSet
from ..models import *
from ..serializers import *

class LoteView(ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer