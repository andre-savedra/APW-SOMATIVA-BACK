from rest_framework.viewsets import ModelViewSet
from ..models import Categoria
from ..serializers import CategoriaSerializer
from ..permissions import Engenharia, Admin, Authenticated

class CategoriaView(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [Authenticated]
        else:
            permission_classes = [Engenharia | Admin]
        
        return [permission() for permission in permission_classes]