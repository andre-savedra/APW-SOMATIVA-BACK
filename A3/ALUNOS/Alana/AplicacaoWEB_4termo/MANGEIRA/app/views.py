from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet


class CustomUserView(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class ProdutoView(ModelViewSet):    
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class PedidoView(ModelViewSet):    
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
