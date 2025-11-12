from rest_framework.viewsets import ModelViewSet
from ..models import *
from rest_framework import permissions
from ..serializers import *

class ItemView(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.DjangoModelPermissions]