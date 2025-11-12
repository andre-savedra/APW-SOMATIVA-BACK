from rest_framework import viewsets
from ..models.sector import Setor
from ..serializers.sector import SetorSerializer

class SetorViewSet(viewsets.ModelViewSet):
    queryset = Setor.objects.all()
    serializer_class = SetorSerializer