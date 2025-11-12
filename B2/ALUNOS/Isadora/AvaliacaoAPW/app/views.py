from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from .permissions import IsManutencao
from .serializers import CustomUserSerializer

class ProdutoView(ModelViewSet):    
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer  

class LoteView(ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer

class ItensLoteView(ModelViewSet):    
    queryset = ItensLote.objects.all()
    serializer_class = ItensLoteSerializer

class MaquinaView(ModelViewSet):    
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer 

class ManutencaoView(ModelViewSet):    
    queryset = Manutencao.objects.all()
    serializer_class = ManutencaoSerializer
    
class MaquinaViewSet(ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsManutencao()]
        return super().get_permissions() 
    
class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer