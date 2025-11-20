from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Item
from ..serializers import ItemSerializer
from ..permissions import Producao, Admin, Authenticated
from app.filter import ItemFilter


class ItemView(ModelViewSet):
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ItemFilter
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [Authenticated]
        else:
            permission_classes = [Producao | Admin]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.cargo in ['Admin', 'Engenharia', 'Producao']:
            return Item.objects.all()
        
        return Item.objects.none()