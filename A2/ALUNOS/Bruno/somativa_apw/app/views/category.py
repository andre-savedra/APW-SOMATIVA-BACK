from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from ..models import *
from ..serializers import *

class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.DjangoModelPermissions]