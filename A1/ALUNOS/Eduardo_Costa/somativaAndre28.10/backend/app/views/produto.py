from rest_framework.viewsets import ModelViewSet
from ..models import *
from ..serializers import *
from ..permissions import *

class ProdutoView(ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [Authenticated]

def get_queryset(self):
        user = self.request.user
        
        # Admin e Engenharia veem tudo
        if user.cargo in ['Admin', 'Engenharia']:
            return Item.objects.all()
        # Inspeção vê apenas itens dos seus lotes
        if user.cargo == 'Inspecao':
            return Item.objects.filter(__responsavel_inspecao=user)
        
        return Item.objects.none()