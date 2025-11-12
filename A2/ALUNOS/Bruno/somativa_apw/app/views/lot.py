from rest_framework.viewsets import ModelViewSet
from ..models import *
from rest_framework import permissions
from ..serializers import *

class LotView(ModelViewSet):
    queryset = Lot.objects.all()
    serializer_class = LotSerializer
    permission_classes = [permissions.DjangoModelPermissions]