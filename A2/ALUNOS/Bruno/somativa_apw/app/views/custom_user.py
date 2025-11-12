from rest_framework.viewsets import ModelViewSet
from ..models import *
from rest_framework import permissions
from ..serializers import *

class CustomUserView(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.DjangoModelPermissions]