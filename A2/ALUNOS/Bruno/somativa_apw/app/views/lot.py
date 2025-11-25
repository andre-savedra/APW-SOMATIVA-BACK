from rest_framework.viewsets import ModelViewSet
from ..models import Lot, STATUS
from rest_framework import permissions
from ..serializers import LotSerializer
from django_filters.rest_framework import DjangoFilterBackend
from ..filters import LotFilter
from django.db.models import Q  

class LotView(ModelViewSet):
    queryset = Lot.objects.all() 
    serializer_class = LotSerializer
    permission_classes = [permissions.DjangoModelPermissions] 
    
    filter_backends = [DjangoFilterBackend]
    filterset_class = LotFilter             

# IA ajudou a validar essa função
    def get_queryset(self):
        """
        Filtra o que o usuário pode ver com base no seu grupo.
        """
        user = self.request.user

        # Se não estiver logado, não mostra nada.
        if not user.is_authenticated:
            return Lot.objects.none()

        # Verifica se o usuário pertence ao grupo INSPEÇÃO
        is_inspector = user.groups.filter(name='INSPEÇÃO').exists()

        if is_inspector: 
            # (status é Nulo) OU (o inspetor é o usuário atual)
            query_filter = Q(status=None) | Q(inspector_FK=user)
            
            # Retorna apenas os lotes que batem com a regra
            return Lot.objects.filter(query_filter).distinct()
        
        # Para outros usuários (Produção, Admin, etc.), retorna tudo, permitindo que eles filtrem usando o LotFilter
        return Lot.objects.all()