from rest_framework.viewsets import ModelViewSet
from ..models import *
from rest_framework import permissions
from ..serializers import *

class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.DjangoModelPermissions]