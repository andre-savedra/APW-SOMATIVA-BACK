from rest_framework.viewsets import ModelViewSet
from ..models import *
from ..serializers import *
from ..permissions import *

class ProducaoView(ModelViewSet):
    queryset = Producao.objects.all()
    serializer_class = ProducaoSerializer
    def get_queryset(self):
        user = self.request.user
        
        # Admin e Engenharia veem tudo
        if user.cargo in ['Admin', 'Engenharia']:
            return Item.objects.all()
        
        # Produção vê apenas itens dos seus lotes
        if user.cargo == 'Producao':
            return Item.objects.filter(lote__responsavel_inspecao=user)
        
        return Item.objects.none()