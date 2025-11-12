from .__init__ import *
from ..models.produtos import Categoria, Produto 
from ..serializers.produtos import CategoriaSerializer, ProdutoSerializer
from ..permissions import CategoriaPermission

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [CategoriaPermission] 


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [permissions.IsAuthenticated]