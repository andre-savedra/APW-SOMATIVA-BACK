from rest_framework.viewsets import ModelViewSet
from ..models import *
from ..serializers import *
from ..permissions import *

class ItemView(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [Authenticated]